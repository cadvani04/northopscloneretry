import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Site",
};

/** Required root layout; HTML routes bypass this via Route Handlers. */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  );
}
