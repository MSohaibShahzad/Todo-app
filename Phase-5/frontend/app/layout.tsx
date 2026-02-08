import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ToastProvider } from "@/components/providers/ToastProvider";
import Script from "next/script";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Nexus tasks - Your Intelligent Task Management System",
  description: "Manage your tasks beautifully with Nexus tasks. Stay organized, focused, and productive with our modern task management application.",
};

/**
 * T112: Root layout with viewport meta tag and responsive container
 * Added ToastProvider for global error/success notifications
 * Updated for custom page backgrounds
 */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0" />
        {/* Polyfill for crypto.randomUUID() - required for ChatKit */}
        <Script id="crypto-polyfill" strategy="beforeInteractive">
          {`
            if (typeof crypto !== 'undefined' && !crypto.randomUUID) {
              crypto.randomUUID = function() {
                return '10000000-1000-4000-8000-100000000000'.replace(/[018]/g, function(c) {
                  return (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16);
                });
              };
            }
          `}
        </Script>
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* Load ChatKit web component from CDN */}
        <Script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          strategy="afterInteractive"
        />
        <ToastProvider>
          {children}
        </ToastProvider>
      </body>
    </html>
  );
}
