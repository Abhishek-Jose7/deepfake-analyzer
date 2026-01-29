'use client';

import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Loader2, CheckCircle, FileVideo, Zap } from 'lucide-react';
import { API_BASE } from '@/lib/api';

interface BatchJob {
    id: string;
    status: string;
    total: number;
    completed: number;
    progress: number;
    results: any[];
}

export default function BatchPage() {
    const [files, setFiles] = useState<File[]>([]);
    const [job, setJob] = useState<BatchJob | null>(null);
    const [loading, setLoading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const pollingRef = useRef<NodeJS.Timeout | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFiles(Array.from(e.target.files));
            setJob(null);
        }
    };

    const startBatch = async () => {
        if (files.length === 0) return;
        setLoading(true);

        const formData = new FormData();
        files.forEach((file) => formData.append('videos', file));

        try {
            const response = await fetch(`${API_BASE}/api/batch/create`, {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();

            if (data.job_id) {
                setJob({ id: data.job_id, status: 'pending', total: data.total_files, completed: 0, progress: 0, results: [] });
                startPolling(data.job_id);
            }
        } catch (error) {
            console.error('Batch creation failed:', error);
        } finally {
            setLoading(false);
        }
    };

    const startPolling = (jobId: string) => {
        if (pollingRef.current) clearInterval(pollingRef.current);

        pollingRef.current = setInterval(async () => {
            try {
                const response = await fetch(`${API_BASE}/api/batch/status/${jobId}`);
                const data = await response.json();
                setJob({ ...data, id: jobId });

                if (data.status === 'completed' || data.status === 'failed') {
                    if (pollingRef.current) clearInterval(pollingRef.current);
                }
            } catch (error) {
                console.error('Polling failed:', error);
            }
        }, 1000);
    };

    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#000', paddingTop: 96, paddingBottom: 64 }}>
            <div style={{ maxWidth: 800, margin: '0 auto', padding: '0 24px' }}>

                {/* Header */}
                <div style={{ textAlign: 'center', marginBottom: 48 }}>
                    <h1 style={{ fontSize: 40, fontWeight: 700, color: '#fff', marginBottom: 16 }}>
                        Batch Processing
                    </h1>
                    <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: 18 }}>
                        Analyze multiple videos concurrently
                    </p>
                </div>

                {/* Upload Area */}
                <div
                    onClick={() => fileInputRef.current?.click()}
                    style={{
                        border: '2px dashed rgba(255,255,255,0.2)',
                        borderRadius: 16,
                        padding: 64,
                        textAlign: 'center',
                        cursor: 'pointer',
                        marginBottom: 32,
                        transition: 'border-color 0.2s ease'
                    }}
                >
                    <input
                        type="file"
                        ref={fileInputRef}
                        multiple
                        accept="video/*"
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                    />
                    <Upload style={{ width: 48, height: 48, margin: '0 auto 16px', color: 'rgba(255,255,255,0.4)' }} />
                    <p style={{ color: '#fff', fontWeight: 500, fontSize: 18, marginBottom: 8 }}>
                        {files.length > 0 ? `${files.length} videos selected` : 'Select multiple videos'}
                    </p>
                    <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: 14 }}>
                        Click to select or drag and drop
                    </p>
                </div>

                {/* File List */}
                {files.length > 0 && !job && (
                    <div style={{ marginBottom: 32 }}>
                        {files.map((file, index) => (
                            <div key={index} style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: 12,
                                padding: 16,
                                borderRadius: 12,
                                border: '1px solid rgba(255,255,255,0.1)',
                                backgroundColor: 'rgba(255,255,255,0.02)',
                                marginBottom: 8
                            }}>
                                <FileVideo style={{ width: 20, height: 20, color: 'rgba(255,255,255,0.4)' }} />
                                <span style={{ color: 'rgba(255,255,255,0.6)', fontSize: 14, flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                    {file.name}
                                </span>
                                <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: 12 }}>
                                    {(file.size / 1024 / 1024).toFixed(1)} MB
                                </span>
                            </div>
                        ))}
                    </div>
                )}

                {/* Start Button */}
                {files.length > 0 && !job && (
                    <button
                        onClick={startBatch}
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
                                Starting...
                            </>
                        ) : (
                            <>
                                <Zap style={{ width: 20, height: 20 }} />
                                Start Batch Processing
                            </>
                        )}
                    </button>
                )}

                {/* Job Progress */}
                <AnimatePresence>
                    {job && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            {/* Progress */}
                            <div style={{
                                padding: 24,
                                borderRadius: 16,
                                border: '1px solid rgba(255,255,255,0.1)',
                                backgroundColor: 'rgba(255,255,255,0.02)',
                                marginBottom: 24
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
                                    <span style={{ color: '#fff', fontWeight: 500, textTransform: 'capitalize' }}>
                                        Status: {job.status}
                                    </span>
                                    <span style={{ color: 'rgba(255,255,255,0.6)' }}>
                                        {job.completed} / {job.total}
                                    </span>
                                </div>
                                <div style={{ height: 8, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 4, overflow: 'hidden' }}>
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${job.progress}%` }}
                                        style={{ height: '100%', backgroundColor: '#fff' }}
                                    />
                                </div>
                            </div>

                            {/* Results */}
                            {job.results.length > 0 && (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                                    {job.results.map((item: any, index: number) => (
                                        <motion.div
                                            key={index}
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            style={{
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: 16,
                                                padding: 16,
                                                borderRadius: 12,
                                                border: '1px solid rgba(255,255,255,0.1)',
                                                backgroundColor: 'rgba(255,255,255,0.02)'
                                            }}
                                        >
                                            <CheckCircle style={{ width: 20, height: 20, color: '#22c55e' }} />
                                            <div style={{ flex: 1, minWidth: 0 }}>
                                                <p style={{ color: '#fff', fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                                    {item.filename}
                                                </p>
                                            </div>
                                            <div style={{ textAlign: 'right' }}>
                                                <div style={{ color: '#fff', fontWeight: 500 }}>
                                                    {(item.result.trust_score * 100).toFixed(0)}%
                                                </div>
                                                <div style={{
                                                    fontSize: 12,
                                                    color: item.result.decision?.includes('Real') ? '#22c55e' :
                                                        item.result.decision?.includes('Fake') ? '#ef4444' : '#eab308'
                                                }}>
                                                    {item.result.decision}
                                                </div>
                                            </div>
                                        </motion.div>
                                    ))}
                                </div>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
