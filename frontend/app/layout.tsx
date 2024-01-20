import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.scss";
import { Footer, Header } from "@/app/components";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "T500 Aggregator",
  description: "T500 Aggregator",
};

export const dynamic = "force-dynamic";
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}
