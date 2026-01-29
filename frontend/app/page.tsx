'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import {
    Shield,
    Eye,
    Zap,
    FileText,
    GitCompare,
    Layers,
    ArrowRight,
    Play
} from 'lucide-react';

export default function HomePage() {
    const features = [
        {
            icon: <Eye style={{ width: 20, height: 20 }} />,
            title: 'Visual Heatmaps',
            description: 'See exactly where deepfake artifacts are located with interactive overlays.'
        },
        {
            icon: <Shield style={{ width: 20, height: 20 }} />,
            title: 'Adversarial Testing',
            description: 'Test detection robustness under 21 different attack scenarios.'
        },
        {
            icon: <Zap style={{ width: 20, height: 20 }} />,
            title: 'Multi-Signal Analysis',
            description: 'Vision, audio, and temporal signals combined for accurate detection.'
        },
        {
            icon: <FileText style={{ width: 20, height: 20 }} />,
            title: 'Evidence Reports',
            description: 'Generate professional reports with blockchain verification.'
        },
        {
            icon: <GitCompare style={{ width: 20, height: 20 }} />,
            title: 'Video Comparison',
            description: 'Compare original and suspect videos side by side.'
        },
        {
            icon: <Layers style={{ width: 20, height: 20 }} />,
            title: 'Batch Processing',
            description: 'Analyze multiple videos concurrently with progress tracking.'
        }
    ];

    const stats = [
        { value: '12+', label: 'API Endpoints' },
        { value: '21', label: 'Test Scenarios' },
        { value: '3', label: 'Signal Types' },
        { value: '100%', label: 'Explainable' }
    ];

    const steps = [
        { num: '01', title: 'Upload', desc: 'Drop your video file or paste a URL' },
        { num: '02', title: 'Analyze', desc: 'Our AI examines vision, audio, and temporal signals' },
        { num: '03', title: 'Report', desc: 'Get detailed results with visual explanations' }
    ];

    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#000' }}>

            {/* ===== HERO SECTION ===== */}
            <section style={{
                position: 'relative',
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                paddingTop: 80
            }}>
                {/* Grid Background */}
                <div style={{
                    position: 'absolute',
                    inset: 0,
                    opacity: 0.2,
                    backgroundImage: 'linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)',
                    backgroundSize: '60px 60px'
                }} />

                <div style={{
                    width: '100%',
                    maxWidth: 1200,
                    margin: '0 auto',
                    padding: '0 24px',
                    position: 'relative',
                    zIndex: 10
                }}>
                    <div style={{ maxWidth: 800, margin: '0 auto', textAlign: 'center' }}>

                        {/* Badge */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5 }}
                            style={{ marginBottom: 24 }}
                        >
                            <span style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: 8,
                                padding: '8px 16px',
                                borderRadius: 50,
                                border: '1px solid rgba(255,255,255,0.2)',
                                fontSize: 14,
                                color: 'rgba(255,255,255,0.7)'
                            }}>
                                <span style={{
                                    width: 8,
                                    height: 8,
                                    backgroundColor: '#22c55e',
                                    borderRadius: '50%'
                                }} />
                                v2.0 — Now with adversarial testing
                            </span>
                        </motion.div>

                        {/* Headline */}
                        <motion.h1
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.1 }}
                            style={{
                                fontSize: 'clamp(40px, 8vw, 72px)',
                                fontWeight: 700,
                                color: '#fff',
                                marginBottom: 24,
                                lineHeight: 1.1,
                                letterSpacing: '-0.02em'
                            }}
                        >
                            Truth in the age
                            <br />
                            <span style={{ color: 'rgba(255,255,255,0.4)' }}>of deepfakes</span>
                        </motion.h1>

                        {/* Subheadline */}
                        <motion.p
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            style={{
                                fontSize: 'clamp(16px, 2vw, 20px)',
                                color: 'rgba(255,255,255,0.5)',
                                marginBottom: 40,
                                maxWidth: 600,
                                margin: '0 auto 40px',
                                lineHeight: 1.6
                            }}
                        >
                            Multi-signal intelligence platform that degrades confidence
                            instead of hallucinating certainty. Powered by explainable AI.
                        </motion.p>

                        {/* CTA Buttons */}
                        <motion.div
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            style={{
                                display: 'flex',
                                flexWrap: 'wrap',
                                gap: 16,
                                justifyContent: 'center'
                            }}
                        >
                            <Link
                                href="/analyze"
                                style={{
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: 8,
                                    padding: '16px 32px',
                                    backgroundColor: '#fff',
                                    color: '#000',
                                    fontWeight: 600,
                                    borderRadius: 12,
                                    fontSize: 15
                                }}
                            >
                                Start Analysis
                                <ArrowRight style={{ width: 16, height: 16 }} />
                            </Link>
                            <Link
                                href="/docs"
                                style={{
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: 8,
                                    padding: '16px 32px',
                                    border: '1px solid rgba(255,255,255,0.2)',
                                    color: '#fff',
                                    fontWeight: 500,
                                    borderRadius: 12,
                                    fontSize: 15
                                }}
                            >
                                <Play style={{ width: 16, height: 16 }} />
                                View Docs
                            </Link>
                        </motion.div>
                    </div>
                </div>

                {/* Scroll Indicator */}
                <div style={{
                    position: 'absolute',
                    bottom: 40,
                    left: '50%',
                    transform: 'translateX(-50%)'
                }}>
                    <motion.div
                        animate={{ y: [0, 8, 0] }}
                        transition={{ duration: 1.5, repeat: Infinity }}
                        style={{
                            width: 24,
                            height: 40,
                            border: '2px solid rgba(255,255,255,0.2)',
                            borderRadius: 12,
                            display: 'flex',
                            justifyContent: 'center',
                            paddingTop: 8
                        }}
                    >
                        <div style={{
                            width: 4,
                            height: 8,
                            backgroundColor: 'rgba(255,255,255,0.4)',
                            borderRadius: 2
                        }} />
                    </motion.div>
                </div>
            </section>

            {/* ===== STATS SECTION ===== */}
            <section style={{
                padding: '80px 0',
                borderTop: '1px solid rgba(255,255,255,0.1)',
                borderBottom: '1px solid rgba(255,255,255,0.1)'
            }}>
                <div style={{ maxWidth: 1200, margin: '0 auto', padding: '0 24px' }}>
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                        gap: 32
                    }}>
                        {stats.map((stat, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: index * 0.1 }}
                                style={{ textAlign: 'center' }}
                            >
                                <div style={{
                                    fontSize: 'clamp(36px, 5vw, 48px)',
                                    fontWeight: 700,
                                    color: '#fff',
                                    marginBottom: 8
                                }}>
                                    {stat.value}
                                </div>
                                <div style={{
                                    color: 'rgba(255,255,255,0.4)',
                                    fontSize: 12,
                                    textTransform: 'uppercase',
                                    letterSpacing: 1
                                }}>
                                    {stat.label}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ===== FEATURES SECTION ===== */}
            <section style={{ padding: '100px 0' }}>
                <div style={{ maxWidth: 1200, margin: '0 auto', padding: '0 24px' }}>

                    {/* Section Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        style={{ textAlign: 'center', marginBottom: 64 }}
                    >
                        <h2 style={{
                            fontSize: 'clamp(28px, 4vw, 40px)',
                            fontWeight: 700,
                            color: '#fff',
                            marginBottom: 16
                        }}>
                            Everything you need
                        </h2>
                        <p style={{
                            color: 'rgba(255,255,255,0.5)',
                            fontSize: 18,
                            maxWidth: 500,
                            margin: '0 auto'
                        }}>
                            A complete platform for deepfake detection, analysis, and reporting.
                        </p>
                    </motion.div>

                    {/* Features Grid */}
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                        gap: 24
                    }}>
                        {features.map((feature, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: index * 0.1 }}
                                style={{
                                    padding: 32,
                                    borderRadius: 16,
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    backgroundColor: 'rgba(255,255,255,0.02)',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s ease'
                                }}
                            >
                                <div style={{
                                    width: 48,
                                    height: 48,
                                    borderRadius: 12,
                                    backgroundColor: 'rgba(255,255,255,0.05)',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    marginBottom: 24,
                                    color: '#fff'
                                }}>
                                    {feature.icon}
                                </div>
                                <h3 style={{
                                    fontSize: 20,
                                    fontWeight: 600,
                                    color: '#fff',
                                    marginBottom: 12
                                }}>
                                    {feature.title}
                                </h3>
                                <p style={{
                                    color: 'rgba(255,255,255,0.5)',
                                    lineHeight: 1.6
                                }}>
                                    {feature.description}
                                </p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ===== HOW IT WORKS SECTION ===== */}
            <section style={{
                padding: '100px 0',
                borderTop: '1px solid rgba(255,255,255,0.1)'
            }}>
                <div style={{ maxWidth: 1200, margin: '0 auto', padding: '0 24px' }}>

                    {/* Section Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        style={{ textAlign: 'center', marginBottom: 64 }}
                    >
                        <h2 style={{
                            fontSize: 'clamp(28px, 4vw, 40px)',
                            fontWeight: 700,
                            color: '#fff',
                            marginBottom: 16
                        }}>
                            How it works
                        </h2>
                        <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: 18 }}>
                            Three simple steps to verify any video
                        </p>
                    </motion.div>

                    {/* Steps */}
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                        gap: 48
                    }}>
                        {steps.map((step, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: index * 0.15 }}
                            >
                                <div style={{
                                    fontSize: 64,
                                    fontWeight: 700,
                                    color: 'rgba(255,255,255,0.05)',
                                    marginBottom: 16,
                                    lineHeight: 1
                                }}>
                                    {step.num}
                                </div>
                                <h3 style={{
                                    fontSize: 22,
                                    fontWeight: 600,
                                    color: '#fff',
                                    marginBottom: 8
                                }}>
                                    {step.title}
                                </h3>
                                <p style={{ color: 'rgba(255,255,255,0.5)' }}>
                                    {step.desc}
                                </p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ===== PHILOSOPHY SECTION ===== */}
            <section style={{ padding: '100px 0' }}>
                <div style={{ maxWidth: 800, margin: '0 auto', padding: '0 24px', textAlign: 'center' }}>
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                    >
                        <div style={{
                            width: 64,
                            height: 64,
                            borderRadius: 16,
                            border: '1px solid rgba(255,255,255,0.1)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            margin: '0 auto 32px',
                            color: 'rgba(255,255,255,0.6)'
                        }}>
                            <Shield style={{ width: 32, height: 32 }} />
                        </div>
                        <h2 style={{
                            fontSize: 'clamp(22px, 3vw, 32px)',
                            fontWeight: 500,
                            color: '#fff',
                            marginBottom: 24,
                            lineHeight: 1.4
                        }}>
                            "We degrade confidence instead of{' '}
                            <span style={{ color: 'rgba(255,255,255,0.4)' }}>
                                hallucinating certainty
                            </span>."
                        </h2>
                        <p style={{
                            color: 'rgba(255,255,255,0.4)',
                            fontSize: 18
                        }}>
                            Our core philosophy: when input quality is poor, we tell you honestly
                            rather than making false accusations.
                        </p>
                    </motion.div>
                </div>
            </section>

            {/* ===== CTA SECTION ===== */}
            <section style={{
                padding: '100px 0',
                borderTop: '1px solid rgba(255,255,255,0.1)'
            }}>
                <div style={{ maxWidth: 600, margin: '0 auto', padding: '0 24px', textAlign: 'center' }}>
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                    >
                        <h2 style={{
                            fontSize: 'clamp(28px, 4vw, 40px)',
                            fontWeight: 700,
                            color: '#fff',
                            marginBottom: 24
                        }}>
                            Ready to get started?
                        </h2>
                        <p style={{
                            color: 'rgba(255,255,255,0.5)',
                            fontSize: 18,
                            marginBottom: 32
                        }}>
                            Upload your first video and see the difference.
                        </p>
                        <Link
                            href="/analyze"
                            style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: 8,
                                padding: '16px 32px',
                                backgroundColor: '#fff',
                                color: '#000',
                                fontWeight: 600,
                                borderRadius: 12,
                                fontSize: 15
                            }}
                        >
                            Start Free Analysis
                            <ArrowRight style={{ width: 16, height: 16 }} />
                        </Link>
                    </motion.div>
                </div>
            </section>

        </div>
    );
}
