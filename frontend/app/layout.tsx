
import '@mantine/core/styles.css';

import { ColorSchemeScript, createTheme, MantineProvider } from "@mantine/core";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.scss";
import { Footer, Header, ScrollToTop } from "@/app/components";
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/next"
import Head from "next/head";
const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "Overwatch 2: Top 500 Aggregator",
    description: "A data aggregation for the Overwatch 2 Top 500 Leaderboards.",
};

const theme = createTheme({})


export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <Head>
                <ColorSchemeScript />
            </Head>
            <body>
                <Analytics />
                <SpeedInsights />
                <MantineProvider theme={theme}>
                    <Header />
                    {children}
                    <Footer />
                    <ScrollToTop />
                </MantineProvider>
            </body>
        </html>
    );
}
