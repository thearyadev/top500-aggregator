import type { Metadata } from "next";
import '@mantine/core/styles.css';
import { Inter } from "next/font/google";
import "./globals.scss";
import { Footer, Header } from "@/app/components";
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/next"
const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "T500 Aggregator",
    description: "T500 Aggregator",
};

// export const dynamic = "force-dynamic";
export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body>
                <Analytics /> 
                <SpeedInsights />
                <Header />
                {children}
                <Footer />
            </body>
        </html>
    );
}
