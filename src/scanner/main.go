// Package main is the entry point for the DeFi lending rate scanner.
//
// The scanner connects to multiple EVM chains via JSON-RPC, queries
// lending protocol contracts for current rates, and outputs aggregated
// rate data for the Python engine to consume.
package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/nasrulniroi/defi-lending-aggregator/scanner/cmd"
	"go.uber.org/zap"
)

// Version is set at build time via ldflags.
var Version = "dev"

func main() {
	logger, err := zap.NewProduction()
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to initialize logger: %v\n", err)
		os.Exit(1)
	}
	defer logger.Sync()

	ctx, cancel := signal.NotifyContext(
		context.Background(),
		syscall.SIGINT,
		syscall.SIGTERM,
	)
	defer cancel()

	logger.Info("starting DeFi lending rate scanner",
		zap.String("version", Version),
	)

	if err := cmd.Execute(ctx, logger); err != nil {
		logger.Error("scanner exited with error", zap.Error(err))
		os.Exit(1)
	}

	logger.Info("scanner stopped gracefully")
}
