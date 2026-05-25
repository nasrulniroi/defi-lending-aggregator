"""Configuration loading and validation utilities.

Provides functions for loading YAML configuration files with
environment variable interpolation and validation.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Optional

import yaml

logger = logging.getLogger(__name__)

_ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)(?::([^}]*))?\}")


def load_config(path: str, interpolate_env: bool = True) -> dict[str, Any]:
    """Load a YAML configuration file with optional env var interpolation.

    Args:
        path: Path to the YAML configuration file.
        interpolate_env: Whether to replace ${VAR} patterns with env values.

    Returns:
        Parsed configuration dictionary.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        yaml.YAMLError: If the file contains invalid YAML.
    """
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(config_path, "r") as f:
        raw_content = f.read()

    if interpolate_env:
        raw_content = _interpolate_env_vars(raw_content)

    config = yaml.safe_load(raw_content)
    logger.debug("Loaded config from %s (%d keys)", path, len(config or {}))
    return config or {}


def _interpolate_env_vars(content: str) -> str:
    """Replace ${VAR} and ${VAR:default} patterns with environment values.

    Args:
        content: Raw string content with potential env var references.

    Returns:
        Content with env vars replaced.
    """
    def replace(match: re.Match) -> str:
        var_name = match.group(1)
        default = match.group(2)
        value = os.environ.get(var_name)
        if value is not None:
            return value
        if default is not None:
            return default
        logger.warning("Environment variable %s not set, no default", var_name)
        return match.group(0)

    return _ENV_VAR_PATTERN.sub(replace, content)


def get_nested(config: dict, key_path: str, default: Any = None) -> Any:
    """Get a nested config value using dot notation.

    Args:
        config: Configuration dictionary.
        key_path: Dot-separated key path (e.g., 'server.port').
        default: Default value if key not found.

    Returns:
        Configuration value or default.

    Examples:
        >>> cfg = {"server": {"port": 8080}}
        >>> get_nested(cfg, "server.port")
        8080
    """
    keys = key_path.split(".")
    current = config

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current


def validate_required(config: dict, required_keys: list[str]) -> list[str]:
    """Validate that required configuration keys are present.

    Args:
        config: Configuration dictionary.
        required_keys: List of dot-separated key paths that must exist.

    Returns:
        List of missing key paths.
    """
    missing = []
    for key in required_keys:
        if get_nested(config, key) is None:
            missing.append(key)
    return missing


def merge_configs(base: dict, override: dict) -> dict:
    """Deep-merge two configuration dictionaries.

    Args:
        base: Base configuration.
        override: Override values (take precedence).

    Returns:
        Merged configuration dictionary.
    """
    result = dict(base)

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result
