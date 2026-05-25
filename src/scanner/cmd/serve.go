package cmd

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/chain"
	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/protocol"
	"go.uber.org/zap"
	"github.com/spf13/cobra"
)

func newServeCmd(logger *zap.Logger) *cobra.Command {
	var (
		port     int
		chains   []string
		interval time.Duration
	)

	cmd := &cobra.Command{
		Use:   "serve",
		Short: "Run scanner as a long-lived HTTP service",
		RunE: func(cmd *cobra.Command, args []string) error {
			return runServe(cmd.Context(), logger, port, chains, interval)
		},
	}

	cmd.Flags().IntVar(&port, "port", 8080, "HTTP server port")
	cmd.Flags().StringSliceVar(&chains, "chains", []string{"ethereum", "arbitrum", "polygon", "base", "avalanche"}, "chains to scan")
	cmd.Flags().DurationVar(&interval, "interval", 60*time.Second, "scan interval")

	return cmd
}

func runServe(ctx context.Context, logger *zap.Logger, port int, chains []string, interval time.Duration) error {
	agg := protocol.NewAggregator(logger)

	// Start background scanner
	go func() {
		ticker := time.NewTicker(interval)
		defer ticker.Stop()

		// Initial scan
		scanAllChains(ctx, logger, agg, chains)

		for {
			select {
			case <-ctx.Done():
				return
			case <-ticker.C:
				scanAllChains(ctx, logger, agg, chains)
			}
		}
	}()

	// HTTP server
	mux := http.NewServeMux()

	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	mux.HandleFunc("/rates", func(w http.ResponseWriter, r *http.Request) {
		rates := agg.GetAllRates()
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"data":      rates,
			"error":     nil,
			"timestamp": time.Now().UTC().Format(time.RFC3339),
		})
	})

	mux.HandleFunc("/rates/protocol/{protocol}", func(w http.ResponseWriter, r *http.Request) {
		proto := r.PathValue("protocol")
		rates := agg.GetRatesByProtocol(proto)
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"data":      rates,
			"error":     nil,
			"timestamp": time.Now().UTC().Format(time.RFC3339),
		})
	})

	addr := fmt.Sprintf(":%d", port)
	srv := &http.Server{
		Addr:         addr,
		Handler:      mux,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	go func() {
		<-ctx.Done()
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		srv.Shutdown(shutdownCtx)
	}()

	logger.Info("HTTP server starting", zap.String("addr", addr))
	if err := srv.ListenAndServe(); err != http.ErrServerClosed {
		return fmt.Errorf("HTTP server error: %w", err)
	}

	return nil
}

func scanAllChains(ctx context.Context, logger *zap.Logger, agg *protocol.Aggregator, chains []string) {
	for _, chainName := range chains {
		scanner, err := chain.NewScanner(chainName, logger)
		if err != nil {
			logger.Error("scanner creation failed", zap.String("chain", chainName), zap.Error(err))
			continue
		}

		rates, err := scanner.ScanRates(ctx)
		if err != nil {
			logger.Error("scan failed", zap.String("chain", chainName), zap.Error(err))
			continue
		}

		agg.ReplaceRates(chainName, rates...)
		logger.Info("scan complete", zap.String("chain", chainName), zap.Int("rates", len(rates)))
	}
}
