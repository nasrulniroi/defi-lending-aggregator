import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../styles/globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "DeFi Lending Aggregator",
  description: "Real-time lending and borrowing rate aggregation across DeFi protocols",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          <nav className="border-b border-gray-200 bg-white">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <div className="flex h-16 items-center justify-between">
                <div className="flex items-center space-x-8">
                  <h1 className="text-xl font-bold text-indigo-600">DeFi Lending</h1>
                  <a href="/" className="text-sm font-medium text-gray-700 hover:text-indigo-600">Dashboard</a>
                  <a href="/rates" className="text-sm font-medium text-gray-700 hover:text-indigo-600">Rates</a>
                  <a href="/protocols" className="text-sm font-medium text-gray-700 hover:text-indigo-600">Protocols</a>
                  <a href="/optimizer" className="text-sm font-medium text-gray-700 hover:text-indigo-600">Optimizer</a>
                  <a href="/alerts" className="text-sm font-medium text-gray-700 hover:text-indigo-600">Alerts</a>
                </div>
              </div>
            </div>
          </nav>
          <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">{children}</main>
        </div>
      </body>
    </html>
  );
}
