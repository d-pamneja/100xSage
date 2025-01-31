import type { Metadata } from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "100xSage",
  description: "100xSage is AI powered TA for online cohort students",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
