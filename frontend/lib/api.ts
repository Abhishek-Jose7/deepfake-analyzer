/**
 * API Configuration for DeepTrust Frontend
 * 
 * This module provides centralized API URL management.
 * For production deployment:
 * 1. Set NEXT_PUBLIC_API_URL in Vercel environment variables
 * 2. Point it to your Hugging Face Spaces URL
 */

// API Base URL - defaults to localhost for development
export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:7860';

// API Endpoints
export const API_ENDPOINTS = {
    // Analysis
    analyze: `${API_BASE}/api/analyze`,
    analyzeHeatmap: `${API_BASE}/api/analyze/heatmap`,
    analyzeAdversarial: `${API_BASE}/api/analyze/adversarial`,
    analyzeEducational: `${API_BASE}/api/analyze/educational`,

    // Batch Processing
    batchCreate: `${API_BASE}/api/batch/create`,
    batchStatus: (jobId: string) => `${API_BASE}/api/batch/status/${jobId}`,

    // Comparison
    compare: `${API_BASE}/api/compare`,

    // Reports
    reportGenerate: `${API_BASE}/api/report/generate`,
    reportDownload: (reportId: string) => `${API_BASE}/api/report/download/${reportId}`,

    // Verification
    verifyHash: `${API_BASE}/api/verify/hash`,
};

// Helper function for API calls
export async function apiCall(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(endpoint, {
        ...options,
        headers: {
            ...options.headers,
        },
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'API request failed' }));
        throw new Error(error.detail || 'API request failed');
    }

    return response.json();
}

// Helper for file uploads
export async function uploadFile(endpoint: string, file: File, fieldName = 'video') {
    const formData = new FormData();
    formData.append(fieldName, file);

    return apiCall(endpoint, {
        method: 'POST',
        body: formData,
    });
}

// Helper for multiple file uploads
export async function uploadMultipleFiles(endpoint: string, files: File[], fieldName = 'videos') {
    const formData = new FormData();
    files.forEach((file) => formData.append(fieldName, file));

    return apiCall(endpoint, {
        method: 'POST',
        body: formData,
    });
}
