import type { AnalyzeResponse, AnalyzeOptions } from "../types/index"

const BASE_URL = (import.meta as any).env?.VITE_API_URL || "http://localhost:8000"

async function request<T>(path: string, init: RequestInit = {}, timeout = 30000): Promise<T> {
  const controller = new AbortController()
  const id = setTimeout(() => controller.abort(), timeout)
  try {
    const res = await fetch(`${BASE_URL}${path}`, { ...init, signal: controller.signal })
    clearTimeout(id)
    if (!res.ok) {
      const text = await res.text()
      throw new Error(`${res.status} ${res.statusText}: ${text}`)
    }
    return await res.json()
  } finally {
    clearTimeout(id)
  }
}

export async function analyzeText(content: string, inputType: string, options: AnalyzeOptions): Promise<AnalyzeResponse> {
  return request<AnalyzeResponse>('/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input_type: inputType, content, options }),
  })
}

export async function analyzeFile(file: File, options: AnalyzeOptions): Promise<AnalyzeResponse> {
  const fd = new FormData()
  fd.append('file', file)
  fd.append('options', JSON.stringify(options))
  return request<AnalyzeResponse>('/analyze', { method: 'POST', body: fd })
}

export async function checkHealth(): Promise<{ status: string; version: string }> {
  return request('/health')
}

