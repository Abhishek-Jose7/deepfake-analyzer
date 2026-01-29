'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Loader2, CheckCircle, AlertCircle, Eye, Shield, Zap, BookOpen } from 'lucide-react';
import { API_BASE } from '@/lib/api';

const modes = [
    { id: 'standard', label: 'Standard', icon: <CheckCircle style={{ width: 16, height: 16 }} />, endpoint: '/api/analyze' },
    { id: 'heatmap', label: 'Heatmaps', icon: <Eye style={{ width: 16, height: 16 }} />, endpoint: '/api/analyze/heatmap' },
    { id: 'adversarial', label: 'Robustness', icon: <Shield style={{ width: 16, height: 16 }} />, endpoint: '/api/analyze/adversarial' },
    { id: 'educational', label: 'Educational', icon: <BookOpen style={{ width: 16, height: 16 }} />, endpoint: '/api/analyze/educational' },
];

function AnalyzeContent() {
    const searchParams = useSearchParams();
    const initialMode = searchParams.get('mode') || 'standard';

    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [activeMode, setActiveMode] = useState(initialMode);
    const [dragOver, setDragOver] = useState(false);

    useEffect(() => {
        const mode = searchParams.get('mode');
        if (mode && modes.find(m => m.id === mode)) {
            setActiveMode(mode);
        }
    }, [searchParams]);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0]) {
            setFile(e.target.files[0]);
            setResult(null);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setDragOver(false);
        if (e.dataTransfer.files?.[0]) {
            setFile(e.dataTransfer.files[0]);
            setResult(null);
        }
    };

    const handleAnalyze = async () => {
        if (!file) return;
        setLoading(true);
        setResult(null);

        const formData = new FormData();
        formData.append('video', file);

        try {
            const mode = modes.find(m => m.id === activeMode);
            const response = await fetch(`${API_BASE}${mode?.endpoint}`, {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Analysis failed:', error);
            setResult({ error: 'Analysis failed. Is the backend running?' });
        } finally {
            setLoading(false);
        }
    };

    const getScoreColor = (score: number) => {
        if (score >= 0.7) return '#22c55e';
        if (score >= 0.4) return '#eab308';
        return '#ef4444';
    };

    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#000', paddingTop: 96, paddingBottom: 64 }}>
            <div style={{ maxWidth: 800, margin: '0 auto', padding: '0 24px' }}>

                {/* Header */}
                <div style={{ textAlign: 'center', marginBottom: 48 }}>
                    <h1 style={{ fontSize: 40, fontWeight: 700, color: '#fff', marginBottom: 16 }}>
                        Video Analysis
                    </h1>
                    <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: 18 }}>
                        Upload a video to analyze with multi-signal intelligence
                    </p>
                </div>

                {/* Mode Selector */}
                <div style={{ marginBottom: 32 }}>
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(4, 1fr)',
                        gap: 12
                    }}>
                        {modes.map((mode) => (
                            <button
                                key={mode.id}
                                onClick={() => setActiveMode(mode.id)}
                                style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    gap: 8,
                                    padding: 16,
                                    borderRadius: 12,
                                    border: activeMode === mode.id ? 'none' : '1px solid rgba(255,255,255,0.1)',
                                    backgroundColor: activeMode === mode.id ? '#fff' : 'transparent',
                                    color: activeMode === mode.id ? '#000' : 'rgba(255,255,255,0.6)',
                                    fontWeight: 500,
                                    cursor: 'pointer',
                                    transition: 'all 0.2s ease'
                                }}
                            >
                                {mode.icon}
                                <span>{mode.label}</span>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Upload Area */}
                <div
                    onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                    onDragLeave={() => setDragOver(false)}
                    onDrop={handleDrop}
                    style={{
                        position: 'relative',
                        border: `2px dashed ${dragOver ? '#fff' : 'rgba(255,255,255,0.2)'}`,
                        borderRadius: 16,
                        padding: 64,
                        textAlign: 'center',
                        marginBottom: 32,
                        backgroundColor: dragOver ? 'rgba(255,255,255,0.05)' : 'transparent',
                        transition: 'all 0.2s ease'
                    }}
                >
                    <input
                        type="file"
                        accept="video/*"
                        onChange={handleFileChange}
                        style={{
                            position: 'absolute',
                            inset: 0,
                            width: '100%',
                            height: '100%',
                            opacity: 0,
                            cursor: 'pointer'
                        }}
                    />
                    <Upload style={{ width: 48, height: 48, margin: '0 auto 16px', color: dragOver ? '#fff' : 'rgba(255,255,255,0.4)' }} />
                    <p style={{ color: '#fff', fontWeight: 500, fontSize: 18, marginBottom: 8 }}>
                        {file ? file.name : 'Drop video here or click to upload'}
                    </p>
                    <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: 14 }}>
                        MP4, AVI, MOV, MKV, WEBM • Max 100MB
                    </p>
                </div>

                {/* Analyze Button */}
                {file && !result && (
                    <motion.button
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        onClick={handleAnalyze}
                        disabled={loading}
                        style={{
                            width: '100%',
                            padding: 16,
                            backgroundColor: '#fff',
                            color: '#000',
                            fontWeight: 600,
                            borderRadius: 12,
                            border: 'none',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            opacity: loading ? 0.5 : 1,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: 12,
                            fontSize: 15
                        }}
                    >
                        {loading ? (
                            <>
                                <Loader2 style={{ width: 20, height: 20, animation: 'spin 1s linear infinite' }} />
                                Analyzing...
                            </>
                        ) : (
                            <>
                                <Zap style={{ width: 20, height: 20 }} />
                                Analyze Video
                            </>
                        )}
                    </motion.button>
                )}

                {/* Results */}
                <AnimatePresence>
                    {result && !result.error && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            style={{ marginTop: 32 }}
                        >
                            {/* Trust Score */}
                            {activeMode === 'standard' && result.trust_score !== undefined && (
                                <div style={{
                                    padding: 32,
                                    borderRadius: 16,
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    backgroundColor: 'rgba(255,255,255,0.02)',
                                    textAlign: 'center',
                                    marginBottom: 24
                                }}>
                                    <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>
                                        Trust Score
                                    </div>
                                    <div style={{ fontSize: 64, fontWeight: 700, color: getScoreColor(result.trust_score), marginBottom: 16 }}>
                                        {(result.trust_score * 100).toFixed(0)}%
                                    </div>
                                    <div style={{
                                        display: 'inline-block',
                                        padding: '8px 16px',
                                        borderRadius: 50,
                                        fontSize: 14,
                                        fontWeight: 500,
                                        backgroundColor: result.decision?.includes('Real') ? 'rgba(34,197,94,0.2)' :
                                            result.decision?.includes('Fake') ? 'rgba(239,68,68,0.2)' : 'rgba(234,179,8,0.2)',
                                        color: result.decision?.includes('Real') ? '#22c55e' :
                                            result.decision?.includes('Fake') ? '#ef4444' : '#eab308',
                                        border: `1px solid ${result.decision?.includes('Real') ? 'rgba(34,197,94,0.3)' :
                                            result.decision?.includes('Fake') ? 'rgba(239,68,68,0.3)' : 'rgba(234,179,8,0.3)'}`
                                    }}>
                                        {result.decision}
                                    </div>
                                    {result.reason && (
                                        <p style={{ marginTop: 16, color: 'rgba(255,255,255,0.5)' }}>{result.reason}</p>
                                    )}
                                </div>
                            )}

                            {/* Signal Breakdown */}
                            {result.signals && (
                                <div style={{
                                    padding: 32,
                                    borderRadius: 16,
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    backgroundColor: 'rgba(255,255,255,0.02)',
                                    marginBottom: 24
                                }}>
                                    <h3 style={{ fontSize: 18, fontWeight: 600, color: '#fff', marginBottom: 24 }}>Signal Analysis</h3>
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                                        {Object.entries(result.signals).map(([key, value]: [string, any]) => (
                                            <div key={key}>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                                                    <span style={{ color: 'rgba(255,255,255,0.6)', textTransform: 'capitalize' }}>{key}</span>
                                                    <span style={{ color: '#fff', fontWeight: 500 }}>{(value.score * 100).toFixed(0)}%</span>
                                                </div>
                                                <div style={{ height: 8, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 4, overflow: 'hidden' }}>
                                                    <div style={{ height: '100%', width: `${value.score * 100}%`, backgroundColor: '#fff', transition: 'width 0.5s ease' }} />
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* LLM Analysis */}
                            {result.llm_analysis && result.llm_analysis.enabled && (
                                <div style={{
                                    padding: 32,
                                    borderRadius: 16,
                                    border: '1px solid rgba(139,92,246,0.3)',
                                    backgroundColor: 'rgba(139,92,246,0.1)',
                                    marginBottom: 24
                                }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                                        <div style={{
                                            padding: '4px 12px',
                                            borderRadius: 50,
                                            backgroundColor: 'rgba(139,92,246,0.2)',
                                            border: '1px solid rgba(139,92,246,0.3)',
                                            fontSize: 12,
                                            color: '#a78bfa'
                                        }}>
                                            🦙 Llama 3.2 Vision
                                        </div>
                                        <span style={{ fontSize: 12, color: 'rgba(255,255,255,0.4)' }}>AI-Powered Analysis</span>
                                    </div>

                                    {result.llm_analysis.parsed && (
                                        <div style={{ marginBottom: 16 }}>
                                            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 12 }}>
                                                <span style={{
                                                    padding: '4px 12px',
                                                    borderRadius: 4,
                                                    fontSize: 12,
                                                    backgroundColor: result.llm_analysis.parsed.verdict === 'authentic' ? 'rgba(34,197,94,0.2)' :
                                                        result.llm_analysis.parsed.verdict === 'manipulated' ? 'rgba(239,68,68,0.2)' : 'rgba(234,179,8,0.2)',
                                                    color: result.llm_analysis.parsed.verdict === 'authentic' ? '#22c55e' :
                                                        result.llm_analysis.parsed.verdict === 'manipulated' ? '#ef4444' : '#eab308'
                                                }}>
                                                    LLM Verdict: {result.llm_analysis.parsed.verdict?.toUpperCase()}
                                                </span>
                                                <span style={{
                                                    padding: '4px 12px',
                                                    borderRadius: 4,
                                                    fontSize: 12,
                                                    backgroundColor: 'rgba(255,255,255,0.1)',
                                                    color: 'rgba(255,255,255,0.6)'
                                                }}>
                                                    Confidence: {result.llm_analysis.parsed.confidence?.toUpperCase()}
                                                </span>
                                            </div>

                                            {result.llm_analysis.parsed.artifacts_detected?.length > 0 && (
                                                <div style={{ marginBottom: 12 }}>
                                                    <span style={{ fontSize: 12, color: 'rgba(255,255,255,0.4)' }}>Artifacts Detected: </span>
                                                    <span style={{ fontSize: 14, color: 'rgba(255,255,255,0.7)' }}>
                                                        {result.llm_analysis.parsed.artifacts_detected.join(', ')}
                                                    </span>
                                                </div>
                                            )}
                                        </div>
                                    )}

                                    {result.llm_analysis.analysis && (
                                        <div style={{
                                            padding: 16,
                                            borderRadius: 12,
                                            backgroundColor: 'rgba(0,0,0,0.3)',
                                            border: '1px solid rgba(255,255,255,0.1)'
                                        }}>
                                            <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: 14, lineHeight: 1.6, margin: 0, whiteSpace: 'pre-wrap' }}>
                                                {result.llm_analysis.analysis}
                                            </p>
                                        </div>
                                    )}

                                    <p style={{ marginTop: 12, fontSize: 12, color: 'rgba(255,255,255,0.3)' }}>
                                        {result.llm_analysis.frames_analyzed} frames analyzed by {result.llm_analysis.model}
                                    </p>
                                </div>
                            )}

                            {/* LLM Explanation (Educational Mode) */}
                            {result.llm_explanation && (
                                <div style={{
                                    padding: 24,
                                    borderRadius: 16,
                                    border: '1px solid rgba(59,130,246,0.3)',
                                    backgroundColor: 'rgba(59,130,246,0.1)',
                                    marginBottom: 24
                                }}>
                                    <h4 style={{ fontSize: 14, fontWeight: 600, color: '#60a5fa', marginBottom: 12 }}>
                                        🎓 AI Explanation
                                    </h4>
                                    <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: 15, lineHeight: 1.7, margin: 0 }}>
                                        {result.llm_explanation}
                                    </p>
                                </div>
                            )}

                            {/* Reset Button */}
                            <button
                                onClick={() => { setFile(null); setResult(null); }}
                                style={{
                                    width: '100%',
                                    padding: 16,
                                    border: '1px solid rgba(255,255,255,0.2)',
                                    backgroundColor: 'transparent',
                                    color: '#fff',
                                    fontWeight: 500,
                                    borderRadius: 12,
                                    cursor: 'pointer'
                                }}
                            >
                                Analyze Another Video
                            </button>
                        </motion.div>
                    )}

                    {/* Error */}
                    {result?.error && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            style={{
                                marginTop: 32,
                                padding: 24,
                                borderRadius: 16,
                                border: '1px solid rgba(239,68,68,0.3)',
                                backgroundColor: 'rgba(239,68,68,0.1)'
                            }}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: 12, color: '#ef4444' }}>
                                <AlertCircle style={{ width: 20, height: 20 }} />
                                <span style={{ fontWeight: 500 }}>{result.error}</span>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            <style jsx global>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
        </div>
    );
}

export default function AnalyzePage() {
    return (
        <Suspense fallback={
            <div style={{ minHeight: '100vh', backgroundColor: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Loader2 style={{ width: 32, height: 32, color: '#fff', animation: 'spin 1s linear infinite' }} />
            </div>
        }>
            <AnalyzeContent />
        </Suspense>
    );
}
