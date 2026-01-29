'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GitCompare, Loader2, Video } from 'lucide-react';
import { API_BASE } from '@/lib/api';

export default function ComparePage() {
    const [file1, setFile1] = useState<File | null>(null);
    const [file2, setFile2] = useState<File | null>(null);
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const handleCompare = async () => {
        if (!file1 || !file2) return;
        setLoading(true);
        setResult(null);

        const formData = new FormData();
        formData.append('video1', file1);
        formData.append('video2', file2);

        try {
            const response = await fetch(`${API_BASE}/api/compare`, {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Comparison failed:', error);
        } finally {
            setLoading(false);
        }
    };

    const FileUploadBox = ({ file, setFile, label, number }: { file: File | null; setFile: (f: File | null) => void; label: string; number: string }) => (
        <div style={{ position: 'relative' }}>
            <input
                type="file"
                accept="video/*"
                onChange={(e) => e.target.files?.[0] && setFile(e.target.files[0])}
                style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0, cursor: 'pointer', zIndex: 10 }}
            />
            <div style={{
                border: '2px dashed rgba(255,255,255,0.2)',
                borderRadius: 16,
                padding: 48,
                textAlign: 'center',
                position: 'relative'
            }}>
                <div style={{
                    position: 'absolute',
                    top: 16,
                    left: 16,
                    width: 32,
                    height: 32,
                    borderRadius: '50%',
                    border: '1px solid rgba(255,255,255,0.2)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'rgba(255,255,255,0.4)',
                    fontSize: 14,
                    fontWeight: 500
                }}>
                    {number}
                </div>
                <Video style={{ width: 40, height: 40, margin: '0 auto 16px', color: 'rgba(255,255,255,0.4)' }} />
                <p style={{ color: '#fff', fontWeight: 500, marginBottom: 4 }}>
                    {file ? file.name : label}
                </p>
                <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: 14 }}>
                    {file ? `${(file.size / 1024 / 1024).toFixed(1)} MB` : 'Click to select'}
                </p>
            </div>
        </div>
    );

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
                        Video Comparison
                    </h1>
                    <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: 18 }}>
                        Compare two videos side by side
                    </p>
                </div>

                {/* Upload Boxes */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24, marginBottom: 32 }}>
                    <FileUploadBox file={file1} setFile={setFile1} label="Original Video" number="1" />
                    <FileUploadBox file={file2} setFile={setFile2} label="Suspect Video" number="2" />
                </div>

                {/* Compare Button */}
                {file1 && file2 && !result && (
                    <button
                        onClick={handleCompare}
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
                                <Loader2 style={{ width: 20, height: 20 }} />
                                Comparing...
                            </>
                        ) : (
                            <>
                                <GitCompare style={{ width: 20, height: 20 }} />
                                Compare Videos
                            </>
                        )}
                    </button>
                )}

                {/* Results */}
                <AnimatePresence>
                    {result && !result.error && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            style={{ marginTop: 32 }}
                        >
                            {/* Verdict */}
                            <div style={{
                                padding: 32,
                                borderRadius: 16,
                                border: '1px solid rgba(255,255,255,0.1)',
                                backgroundColor: 'rgba(255,255,255,0.02)',
                                textAlign: 'center',
                                marginBottom: 24
                            }}>
                                <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>
                                    Verdict
                                </div>
                                <div style={{
                                    fontSize: 32,
                                    fontWeight: 700,
                                    color: result.comparison?.verdict === 'Similar' ? '#22c55e' : '#ef4444',
                                    marginBottom: 8
                                }}>
                                    {result.comparison?.verdict || 'Analysis Complete'}
                                </div>
                                <p style={{ color: 'rgba(255,255,255,0.5)' }}>
                                    Score Difference: {((result.comparison?.trust_score_diff || 0) * 100).toFixed(1)}%
                                </p>
                            </div>

                            {/* Side by Side */}
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24, marginBottom: 24 }}>
                                {['video1', 'video2'].map((key, index) => {
                                    const video = result[key];
                                    if (!video) return null;

                                    return (
                                        <div key={key} style={{
                                            padding: 24,
                                            borderRadius: 16,
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            backgroundColor: 'rgba(255,255,255,0.02)'
                                        }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                                                <div style={{
                                                    width: 24,
                                                    height: 24,
                                                    borderRadius: '50%',
                                                    border: '1px solid rgba(255,255,255,0.2)',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'center',
                                                    color: 'rgba(255,255,255,0.4)',
                                                    fontSize: 12
                                                }}>
                                                    {index + 1}
                                                </div>
                                                <span style={{ color: 'rgba(255,255,255,0.6)', fontSize: 14, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                                    {video.filename}
                                                </span>
                                            </div>

                                            <div style={{ textAlign: 'center', marginBottom: 16 }}>
                                                <div style={{ fontSize: 36, fontWeight: 700, color: getScoreColor(video.trust_score) }}>
                                                    {(video.trust_score * 100).toFixed(0)}%
                                                </div>
                                                <div style={{
                                                    fontSize: 14,
                                                    color: video.decision?.includes('Real') ? '#22c55e' :
                                                        video.decision?.includes('Fake') ? '#ef4444' : '#eab308'
                                                }}>
                                                    {video.decision}
                                                </div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>

                            {/* Reset */}
                            <button
                                onClick={() => { setFile1(null); setFile2(null); setResult(null); }}
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
                                Compare Different Videos
                            </button>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
