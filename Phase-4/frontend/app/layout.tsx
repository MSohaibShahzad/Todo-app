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
