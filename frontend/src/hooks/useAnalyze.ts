import { useState } from 'react'
import type { AnalyzeResponse, AnalyzeOptions } from '../types'
import * as api from '../services/api'

export function useAnalyze() {
  const [result, setResult] = useState<AnalyzeResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function analyze(content: string, inputType: string, options: AnalyzeOptions) {
    setLoading(true)
    setError(null)
    try {
      const res = await api.analyzeText(content, inputType, options)
      setResult(res)
      return res
    } catch (e: any) {
      setError(e?.message || 'Unknown error')
      throw e
    } finally {
      setLoading(false)
    }
  }

  async function analyzeFile(file: File, options: AnalyzeOptions) {
    setLoading(true)
    setError(null)
    try {
      const res = await api.analyzeFile(file, options)
      setResult(res)
      return res
    } catch (e: any) {
      setError(e?.message || 'Unknown error')
      throw e
    } finally {
      setLoading(false)
    }
  }

  function reset() {
    setResult(null)
    setError(null)
  }

  return { result, loading, error, analyze, analyzeFile, reset }
}
