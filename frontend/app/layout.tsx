import type { Metadata } from "next";
import "./globals.css";
import Navigation from "@/components/Navigation";

export const metadata: Metadata = {
    title: "DeepTrust - AI-Powered Deepfake Detection",
    description: "Multi-signal intelligence platform for detecting deepfakes with visual heatmaps, adversarial testing, and blockchain verification.",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body style={{
                backgroundColor: '#000',
                color: '#fff',
                margin: 0,
                padding: 0,
                minHeight: '100vh'
            }}>
                <Navigation />
                <main>{children}</main>

                {/* Footer */}
                <footer style={{
                    borderTop: '1px solid rgba(255,255,255,0.1)',
                    padding: '48px 0'
                }}>
                    <div style={{
                        maxWidth: 1200,
                        margin: '0 auto',
                        padding: '0 24px'
                    }}>
                        <div style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            gap: 16
                        }}>
                            <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: 14 }}>
                                © 2026 DeepTrust. Built for truth.
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 24, fontSize: 14, color: 'rgba(255,255,255,0.4)' }}>
                                <a href="/docs" style={{ color: 'inherit', transition: 'color 0.2s' }}>Documentation</a>
                                <a href="/analyze" style={{ color: 'inherit', transition: 'color 0.2s' }}>Get Started</a>
                            </div>
                        </div>
                    </div>
                </footer>
            </body>
        </html>
    );
}
