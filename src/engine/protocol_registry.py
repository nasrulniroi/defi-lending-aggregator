"""Protocol registry for managing DeFi protocol configurations.

Loads protocol definitions from YAML configuration and provides
lookup, filtering, and validation methods.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from engine.models.protocol import Protocol, ProtocolStatus
from engine.utils.config import load_config

logger = logging.getLogger(__name__)


class ProtocolNotFoundError(Exception):
    """Raised when a requested protocol is not in the registry."""

    def __init__(self, protocol_id: str) -> None:
        self.protocol_id = protocol_id
        super().__init__(f"Protocol not found: {protocol_id}")


class ProtocolRegistry:
    """Registry of all configured DeFi lending protocols.

    Loads protocol definitions from YAML config files and provides
    methods to query, filter, and validate protocol configurations.

    Attributes:
        config_path: Path to the protocols configuration file.
        protocols: Dictionary of registered protocols by ID.
    """

    def __init__(self, config_path: Optional[str] = None) -> None:
        """Initialize the protocol registry.

        Args:
            config_path: Path to protocols.yaml. Defaults to config/protocols.yaml.
        """
        self.config_path = config_path or str(
            Path(__file__).parent.parent.parent / "config" / "protocols.yaml"
        )
        self.protocols: dict[str, Protocol] = {}
        self._loaded = False

    def load(self) -> None:
        """Load protocols from configuration file.

        Raises:
            FileNotFoundError: If the config file doesn't exist.
            yaml.YAMLError: If the config file is invalid YAML.
        """
        config = load_config(self.config_path)
        protocols_config = config.get("protocols", {})

        for proto_id, proto_data in protocols_config.items():
            try:
                launch_date = datetime.fromisoformat(
                    proto_data.get("launch_date", "2023-01-01")
                )
                protocol = Protocol(
                    id=proto_id,
                    name=proto_data["name"],
                    version=proto_data.get("version", "v1"),
                    chains=proto_data.get("chains", []),
                    risk_score=proto_data.get("risk_score", 5.0),
                    audit_count=proto_data.get("audit_count", 0),
                    launch_date=launch_date,
                    website=proto_data.get("website", ""),
                    contracts=proto_data.get("contracts", {}),
                )
                self.protocols[proto_id] = protocol
                logger.info("Registered protocol: %s (%s)", protocol.name, proto_id)
            except (KeyError, ValueError) as exc:
                logger.error("Failed to load protocol %s: %s", proto_id, exc)

        self._loaded = True
        logger.info("Loaded %d protocols from registry", len(self.protocols))

    def ensure_loaded(self) -> None:
        """Ensure protocols are loaded, loading if necessary."""
        if not self._loaded:
            self.load()

    def get_protocol(self, protocol_id: str) -> Optional[Protocol]:
        """Get a protocol by ID.

        Args:
            protocol_id: Protocol identifier.

        Returns:
            Protocol object, or None if not found.
        """
        self.ensure_loaded()
        return self.protocols.get(protocol_id)

    def get_all_protocols(self) -> list[Protocol]:
        """Get all registered protocols.

        Returns:
            List of all Protocol objects.
        """
        self.ensure_loaded()
        return list(self.protocols.values())

    def get_protocols_for_chain(self, chain: str) -> list[Protocol]:
        """Get all protocols deployed on a specific chain.

        Args:
            chain: Chain identifier.

        Returns:
            List of protocols supporting the given chain.
        """
        self.ensure_loaded()
        return [p for p in self.protocols.values() if p.supports_chain(chain)]

    def get_chains_for_protocol(self, protocol_id: str) -> list[str]:
        """Get all chains supported by a protocol.

        Args:
            protocol_id: Protocol identifier.

        Returns:
            List of chain identifiers.

        Raises:
            ProtocolNotFoundError: If the protocol is not registered.
        """
        protocol = self.get_protocol(protocol_id)
        if protocol is None:
            raise ProtocolNotFoundError(protocol_id)
        return protocol.chains

    def get_all_chains(self) -> list[str]:
        """Get the union of all chains across all protocols.

        Returns:
            Sorted list of unique chain identifiers.
        """
        self.ensure_loaded()
        chains: set[str] = set()
        for protocol in self.protocols.values():
            chains.update(protocol.chains)
        return sorted(chains)

    def get_contracts(
        self, protocol_id: str, chain: str
    ) -> dict[str, str]:
        """Get contract addresses for a protocol on a chain.

        Args:
            protocol_id: Protocol identifier.
            chain: Chain identifier.

        Returns:
            Dictionary mapping contract name to address.
        """
        protocol = self.get_protocol(protocol_id)
        if protocol is None:
            raise ProtocolNotFoundError(protocol_id)
        return protocol.contracts.get(chain, {})

    def validate(self) -> list[str]:
        """Validate all registered protocols for consistency.

        Returns:
            List of validation warning/error messages.
        """
        self.ensure_loaded()
        issues: list[str] = []

        for proto_id, protocol in self.protocols.items():
            if not protocol.chains:
                issues.append(f"{proto_id}: no chains configured")

            if protocol.risk_score < 1.0 or protocol.risk_score > 10.0:
                issues.append(
                    f"{proto_id}: risk_score {protocol.risk_score} "
                    f"outside valid range [1.0, 10.0]"
                )

            for chain in protocol.chains:
                if chain not in protocol.contracts:
                    issues.append(
                        f"{proto_id}: no contracts configured for chain {chain}"
                    )

        return issues

    def to_dict(self) -> dict:
        """Serialize registry to dictionary.

        Returns:
            Dictionary of all protocols keyed by ID.
        """
        self.ensure_loaded()
        return {
            pid: p.to_dict() for pid, p in self.protocols.items()
        }
