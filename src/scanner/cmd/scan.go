// Package cmd implements CLI commands for the scanner.
package cmd

import (
	"context"
	"fmt"
	"time"

	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/chain"
	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/protocol"
	"github.com/spf13/cobra"
	"go.uber.org/zap"
)

var rootCmd *cobra.Command

// Execute runs the root command.
func Execute(ctx context.Context, logger *zap.Logger) error {
	rootCmd = &cobra.Command{
		Use:   "scanner",
		Short: "DeFi lending rate scanner",
		Long:  "High-performance on-chain data scanner for DeFi lending rates.",
	}

	rootCmd.AddCommand(newScanCmd(logger))
	rootCmd.AddCommand(newServeCmd(logger))

	return rootCmd.ExecuteContext(ctx)
}

func newScanCmd(logger *zap.Logger) *cobra.Command {
	var (
		chains   []string
		interval time.Duration
	)

	cmd := &cobra.Command{
		Use:   "scan",
		Short: "Run a one-shot scan of all chains",
		RunE: func(cmd *cobra.Command, args []string) error {
			return runScan(cmd.Context(), logger, chains, interval)
		},
	}

	cmd.Flags().StringSliceVar(&chains, "chains", []string{"ethereum", "arbitrum", "polygon", "base", "avalanche"}, "chains to scan")
	cmd.Flags().DurationVar(&interval, "interval", 60*time.Second, "scan interval")

	return cmd
}

func runScan(ctx context.Context, logger *zap.Logger, chains []string, interval time.Duration) error {
	logger.Info("starting scan",
		zap.Strings("chains", chains),
		zap.Duration("interval", interval),
	)

	agg := protocol.NewAggregator(logger)

	for _, chainName := range chains {
		scanner, err := chain.NewScanner(chainName, logger)
		if err != nil {
			logger.Error("failed to create scanner",
				zap.String("chain", chainName),
				zap.Error(err),
			)
			continue
		}

		rates, err := scanner.ScanRates(ctx)
		if err != nil {
			logger.Error("scan failed",
				zap.String("chain", chainName),
				zap.Error(err),
			)
			continue
		}

		agg.AddRates(rates...)
		logger.Info("chain scan complete",
			zap.String("chain", chainName),
			zap.Int("rates", len(rates)),
		)
	}

	allRates := agg.GetAllRates()
	fmt.Printf("Total rates collected: %d\n", len(allRates))

	for _, rate := range allRates {
		fmt.Printf("  %s/%s %s: supply=%.2f%% borrow=%.2f%%\n",
			rate.Protocol, rate.Chain, rate.Asset,
			rate.SupplyAPY, rate.BorrowAPY,
		)
	}

	return nil
}
