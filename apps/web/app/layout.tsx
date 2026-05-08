import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "We Are Not Building Another AI",
  description: "Cognitive workflow infrastructure for the AI era.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
