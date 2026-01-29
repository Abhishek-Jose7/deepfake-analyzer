'use client';

import { motion } from 'framer-motion';
import { Shield, Zap, Eye, Code, Terminal, FileText } from 'lucide-react';

export default function DocsPage() {
    const endpoints = [
        { method: 'POST', path: '/api/analyze', desc: 'Standard analysis' },
        { method: 'POST', path: '/api/analyze/heatmap', desc: 'Visual heatmaps' },
        { method: 'POST', path: '/api/analyze/adversarial', desc: 'Robustness testing' },
        { method: 'POST', path: '/api/analyze/educational', desc: 'Educational content' },
        { method: 'POST', path: '/api/batch/create', desc: 'Batch processing' },
        { method: 'GET', path: '/api/batch/status/:id', desc: 'Batch status' },
        { method: 'POST', path: '/api/compare', desc: 'Video comparison' },
        { method: 'POST', path: '/api/report/generate', desc: 'Generate report' },
        { method: 'GET', path: '/api/report/download/:id', desc: 'Download report' },
        { method: 'POST', path: '/api/verify/hash', desc: 'Get verification hash' },
    ];

    const signals = [
        { icon: <Eye style={{ width: 20, height: 20 }} />, title: 'Vision', desc: 'Analyzes pixel-level artifacts using Laplacian variance and edge consistency.' },
        { icon: <Zap style={{ width: 20, height: 20 }} />, title: 'Audio', desc: 'Examines spectral features to identify synthetic text-to-speech signatures.' },
        { icon: <FileText style={{ width: 20, height: 20 }} />, title: 'Temporal', desc: 'Tracks frame-to-frame consistency and optical flow for temporal jitter.' }
    ];

    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#000', paddingTop: 96, paddingBottom: 64 }}>
            <div style={{ maxWidth: 800, margin: '0 auto', padding: '0 24px' }}>

                {/* Header */}
                <div style={{ textAlign: 'center', marginBottom: 64 }}>
                    <h1 style={{ fontSize: 40, fontWeight: 700, color: '#fff', marginBottom: 16 }}>
                        Documentation
                    </h1>
                    <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: 18 }}>
                        Architecture, API reference, and philosophy
                    </p>
                </div>

                {/* Philosophy */}
                <motion.section
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    style={{
                        padding: 32,
                        borderRadius: 16,
                        border: '1px solid rgba(255,255,255,0.1)',
                        backgroundColor: 'rgba(255,255,255,0.02)',
                        marginBottom: 32
                    }}
                >
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
                        <Shield style={{ width: 24, height: 24, color: 'rgba(255,255,255,0.6)' }} />
                        <h2 style={{ fontSize: 20, fontWeight: 600, color: '#fff' }}>Core Philosophy</h2>
                    </div>
                    <div style={{ color: 'rgba(255,255,255,0.6)', lineHeight: 1.7 }}>
                        <p style={{ marginBottom: 16 }}>
                            Most deepfake detectors attempt to give a binary "Real/Fake" answer even when
                            they are uncertain. Our system follows a different principle.
                        </p>
                        <div style={{
                            padding: 24,
                            borderRadius: 12,
                            backgroundColor: 'rgba(255,255,255,0.05)',
                            borderLeft: '2px solid rgba(255,255,255,0.2)',
                            marginBottom: 16
                        }}>
                            <p style={{ fontSize: 20, fontWeight: 500, color: '#fff', fontStyle: 'italic' }}>
                                "We degrade confidence instead of hallucinating certainty."
                            </p>
                        </div>
                        <p>
                            If an input video is heavily compressed, dark, or low-resolution, we explicitly
                            lower our confidence and flag it as "Ambiguous" rather than making a false accusation.
                        </p>
                    </div>
                </motion.section>

                {/* Signal Pipeline */}
                <motion.section
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    style={{
                        padding: 32,
                        borderRadius: 16,
                        border: '1px solid rgba(255,255,255,0.1)',
                        backgroundColor: 'rgba(255,255,255,0.02)',
                        marginBottom: 32
                    }}
                >
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
                        <Zap style={{ width: 24, height: 24, color: 'rgba(255,255,255,0.6)' }} />
                        <h2 style={{ fontSize: 20, fontWeight: 600, color: '#fff' }}>Signal Pipeline</h2>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
                        {signals.map((signal, index) => (
                            <div key={index} style={{
                                padding: 24,
                                borderRadius: 12,
                                backgroundColor: 'rgba(255,255,255,0.05)',
                                border: '1px solid rgba(255,255,255,0.1)'
                            }}>
                                <div style={{
                                    width: 40,
                                    height: 40,
                                    borderRadius: 8,
                                    backgroundColor: 'rgba(255,255,255,0.05)',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    marginBottom: 16,
                                    color: '#fff'
                                }}>
                                    {signal.icon}
                                </div>
                                <h3 style={{ color: '#fff', fontWeight: 500, marginBottom: 8 }}>{signal.title}</h3>
                                <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: 14 }}>{signal.desc}</p>
                            </div>
                        ))}
                    </div>
                </motion.section>

                {/* API Reference */}
                <motion.section
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    style={{
                        padding: 32,
                        borderRadius: 16,
                        border: '1px solid rgba(255,255,255,0.1)',
                        backgroundColor: 'rgba(255,255,255,0.02)',
                        marginBottom: 32
                    }}
                >
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
                        <Code style={{ width: 24, height: 24, color: 'rgba(255,255,255,0.6)' }} />
                        <h2 style={{ fontSize: 20, fontWeight: 600, color: '#fff' }}>API Reference</h2>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        {endpoints.map((endpoint, index) => (
                            <div key={index} style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: 16,
                                padding: 16,
                                borderRadius: 12,
                                backgroundColor: 'rgba(255,255,255,0.05)',
                                border: '1px solid rgba(255,255,255,0.1)'
                            }}>
                                <span style={{
                                    fontSize: 12,
                                    fontFamily: 'monospace',
                                    padding: '4px 8px',
                                    borderRadius: 4,
                                    backgroundColor: endpoint.method === 'GET' ? 'rgba(34,197,94,0.2)' : 'rgba(59,130,246,0.2)',
                                    color: endpoint.method === 'GET' ? '#22c55e' : '#3b82f6'
                                }}>
                                    {endpoint.method}
                                </span>
                                <code style={{ color: 'rgba(255,255,255,0.8)', fontSize: 14, fontFamily: 'monospace', flex: 1 }}>
                                    {endpoint.path}
                                </code>
                                <span style={{ color: 'rgba(255,255,255,0.4)', fontSize: 14 }}>{endpoint.desc}</span>
                            </div>
                        ))}
                    </div>
                </motion.section>

                {/* Quick Start */}
                <motion.section
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    style={{
                        padding: 32,
                        borderRadius: 16,
                        border: '1px solid rgba(255,255,255,0.1)',
                        backgroundColor: 'rgba(255,255,255,0.02)'
                    }}
                >
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
                        <Terminal style={{ width: 24, height: 24, color: 'rgba(255,255,255,0.6)' }} />
                        <h2 style={{ fontSize: 20, fontWeight: 600, color: '#fff' }}>Quick Start</h2>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                        <div style={{
                            padding: 16,
                            borderRadius: 12,
                            backgroundColor: 'rgba(0,0,0,0.5)',
                            border: '1px solid rgba(255,255,255,0.1)'
                        }}>
                            <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>
                                Terminal 1 - Backend
                            </p>
                            <code style={{ color: 'rgba(255,255,255,0.8)', fontSize: 14, fontFamily: 'monospace' }}>
                                cd c:\deepfak && python app.py
                            </code>
                        </div>
                        <div style={{
                            padding: 16,
                            borderRadius: 12,
                            backgroundColor: 'rgba(0,0,0,0.5)',
                            border: '1px solid rgba(255,255,255,0.1)'
                        }}>
                            <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>
                                Terminal 2 - Frontend
                            </p>
                            <code style={{ color: 'rgba(255,255,255,0.8)', fontSize: 14, fontFamily: 'monospace' }}>
                                cd c:\deepfak\frontend && npm run dev
                            </code>
                        </div>
                        <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: 14 }}>
                            Open{' '}
                            <code style={{ color: 'rgba(255,255,255,0.8)', backgroundColor: 'rgba(255,255,255,0.1)', padding: '2px 8px', borderRadius: 4 }}>
                                http://localhost:3000
                            </code>
                            {' '}in your browser.
                        </p>
                    </div>
                </motion.section>
            </div>
        </div>
    );
}
