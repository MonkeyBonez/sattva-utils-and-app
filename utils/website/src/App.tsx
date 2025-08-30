import { useEffect, useMemo, useRef, useState } from 'react'
import './index.css'

// Types
export type UnitSpan = { chapter: number; start: number; end: number }
export type Candidate = {
  lesson_id?: string
  old_cluster_id?: number
  text: string
  units?: UnitSpan[]
  source_ids?: string[]
  [key: string]: any
}
export type Cluster = {
  cluster_id: number
  candidates: Candidate[]
  [key: string]: any
}

// Utilities
function download(filename: string, content: string, mime = 'text/plain;charset=utf-8') {
  const blob = new Blob([content], { type: mime })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

function parseJSONL(text: string): Cluster[] {
  const lines = text.split(/\r?\n/).filter(Boolean)
  const out: Cluster[] = []
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    let obj: any
    try {
      obj = JSON.parse(line)
    } catch (e) {
      throw new Error(`Line ${i + 1}: invalid JSON`)
    }

    // Format A: { cluster_id, candidates: [{lesson_id|old_cluster_id,text,...}] }
    if (typeof obj.cluster_id === 'number' && Array.isArray(obj.candidates)) {
      for (let j = 0; j < obj.candidates.length; j++) {
        const c = obj.candidates[j]
        if (typeof c !== 'object' || c === null) {
          throw new Error(`Line ${i + 1}: candidate ${j + 1} is not an object`)
        }
        if (typeof c.text !== 'string') {
          throw new Error(`Line ${i + 1}: candidate ${j + 1} missing text`)
        }
        // allow either lesson_id or old_cluster_id
        if (typeof c.lesson_id !== 'string' && typeof c.old_cluster_id !== 'number') {
          throw new Error(`Line ${i + 1}: candidate ${j + 1} missing lesson_id/old_cluster_id`)
        }
      }
      out.push(obj as Cluster)
      continue
    }

    // Format B: human-pass reps per line: { cluster_id, lesson_id, text, ... }
    if (
      (typeof obj.cluster_id === 'number' || typeof obj.cluster_id === 'string') &&
      (typeof obj.lesson_id === 'string' || typeof obj.old_cluster_id === 'number') &&
      typeof obj.text === 'string'
    ) {
      const cid = Number(obj.cluster_id)
      if (!Number.isFinite(cid)) {
        throw new Error(`Line ${i + 1}: cluster_id is not numeric`)
      }
      const candidate: Candidate = {
        ...(typeof obj.lesson_id === 'string' ? { lesson_id: obj.lesson_id } : {}),
        ...(typeof obj.old_cluster_id === 'number' ? { old_cluster_id: obj.old_cluster_id } : {}),
        text: obj.text,
        ...(Array.isArray(obj.units) ? { units: obj.units } : {}),
        ...(Array.isArray(obj.source_ids) ? { source_ids: obj.source_ids } : {}),
      }
      out.push({ cluster_id: cid, candidates: [candidate] })
      continue
    }

    throw new Error(
      `Line ${i + 1}: unsupported row shape. Expected {cluster_id,candidates:[...]} or {cluster_id,lesson_id|old_cluster_id,text}`,
    )
  }
  return out
}

function stringifyJSONL(objects: any[]): string {
  return objects.map((o) => JSON.stringify(o)).join('\n') + '\n'
}

// Normalize text for duplicate detection
function normalizeText(input: string): string {
  return input.replace(/\s+/g, ' ').trim().toLowerCase()
}

function dedupeClustersByText(input: Cluster[]): Cluster[] {
  return input.map((cl) => {
    const seen = new Set<string>()
    const deduped: Candidate[] = []
    for (const cand of cl.candidates) {
      const key = normalizeText(cand.text)
      if (seen.has(key)) continue
      seen.add(key)
      deduped.push(cand)
    }
    return { ...cl, candidates: deduped }
  })
}

// Store (simple local state + autosave)
const LS_KEY = 'pickA_state_v1'

type PicksMap = Record<number, Candidate>

function useAutosave<T>(value: T, key: string) {
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch {}
  }, [value, key])
}

function useAutoload<T>(key: string, fallback: T): T {
  const [state] = useState<T>(() => {
    try {
      const s = localStorage.getItem(key)
      return s ? (JSON.parse(s) as T) : fallback
    } catch {
      return fallback
    }
  })
  return state
}

export default function App() {
  const [clusters, setClusters] = useState<Cluster[]>([])
  const [picks, setPicks] = useState<PicksMap>({})
  const [selectedClusterId, setSelectedClusterId] = useState<number | null>(null)
  const [filter, setFilter] = useState('')
  const [showOnlyUnpicked, setShowOnlyUnpicked] = useState(false)
  const [isDragging, setIsDragging] = useState(false)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const [selectedCandidateIds, setSelectedCandidateIds] = useState<Set<string>>(new Set())
  const [moveTargetId, setMoveTargetId] = useState<string>('')
  const fileInputRef = useRef<HTMLInputElement | null>(null)

  function candKey(c: Candidate | undefined): string {
    if (!c) return ''
    return typeof c.lesson_id === 'string' ? c.lesson_id : `old:${c.old_cluster_id ?? -1}`
  }

  // autoload picks on first render
  const loaded = useAutoload<{ picks: PicksMap } | null>(LS_KEY, null)
  useEffect(() => {
    if (loaded && loaded.picks) setPicks(loaded.picks)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useAutosave({ picks }, LS_KEY)

  const summary = useMemo(() => {
    const totalClusters = clusters.length
    const totalCandidates = clusters.reduce((acc, c) => acc + c.candidates.length, 0)
    const pickedCount = Object.keys(picks).length
    return { totalClusters, totalCandidates, pickedCount }
  }, [clusters, picks])

  const filteredClusters = useMemo(() => {
    const f = filter.trim().toLowerCase()
    let list = clusters
    if (f) {
      list = list.filter((c) =>
        c.candidates.some((cand) => cand.text.toLowerCase().includes(f)),
      )
    }
    if (showOnlyUnpicked) {
      list = list.filter((c) => !picks[c.cluster_id])
    }
    return list
  }, [clusters, filter, showOnlyUnpicked, picks])

  // Ensure we always have a selected cluster if any are visible
  useEffect(() => {
    if (filteredClusters.length === 0) {
      if (selectedClusterId !== null) setSelectedClusterId(null)
      return
    }
    const stillVisible = selectedClusterId !== null && filteredClusters.some(c => c.cluster_id === selectedClusterId)
    if (!stillVisible) {
      setSelectedClusterId(filteredClusters[0].cluster_id)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filteredClusters])

  function onUploadFile(text: string) {
    let parsed: Cluster[] = []
    try {
      parsed = parseJSONL(text)
    } catch (e: any) {
      console.error('Failed to parse JSONL:', e)
      setErrorMsg(String(e?.message || 'Failed to parse JSONL'))
      return
    }
    setErrorMsg(null)
    // Dedupe identical candidate texts within each cluster
    const deduped = dedupeClustersByText(parsed)
    setClusters(deduped)
    // reset picks on new upload, then auto-pick singletons
    const autoPicks: PicksMap = {}
    for (const cl of deduped) {
      if (Array.isArray(cl.candidates) && cl.candidates.length === 1) {
        autoPicks[cl.cluster_id] = cl.candidates[0]
      }
    }
    setPicks(autoPicks)
    // default selection to first cluster if available
    setSelectedClusterId(deduped.length > 0 ? deduped[0].cluster_id : null)
    setSelectedCandidateIds(new Set())
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => onUploadFile(String(reader.result || ''))
    reader.readAsText(file)
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault()
    setIsDragging(true)
  }

  function handleDragLeave(e: React.DragEvent) {
    e.preventDefault()
    setIsDragging(false)
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer?.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => onUploadFile(String(reader.result || ''))
    reader.readAsText(file)
  }

  function exportJSONL() {
    const lines = clusters.map((cluster) => {
      const rep = picks[cluster.cluster_id]
      const memberIds = Array.from(
        new Set(
          cluster.candidates.map((c) =>
            typeof c.lesson_id === 'string' ? c.lesson_id : `old:${c.old_cluster_id}`,
          ),
        ),
      )
      return {
        cluster_id: cluster.cluster_id,
        // Prefer lesson_id when available; else keep old_cluster_id to preserve backtracking
        lesson_id: rep ? (rep.lesson_id ?? null) : null,
        old_cluster_id: rep && rep.lesson_id ? null : rep?.old_cluster_id ?? null,
        text: rep ? rep.text : null,
        member_ids: memberIds,
        members_count: cluster.candidates.length,
      }
    })
    download('A_reps.jsonl', stringifyJSONL(lines), 'application/jsonl')
  }

  function exportCSV() {
    const header = ['cluster_id', 'lesson_id', 'old_cluster_id', 'text', 'members_count', 'member_ids']
    const rows = clusters.map((cluster) => {
      const rep = picks[cluster.cluster_id]
      const memberIds = Array.from(
        new Set(
          cluster.candidates.map((c) =>
            typeof c.lesson_id === 'string' ? c.lesson_id : `old:${c.old_cluster_id}`,
          ),
        ),
      )
      return [
        String(cluster.cluster_id),
        rep?.lesson_id || '',
        rep?.old_cluster_id != null ? String(rep.old_cluster_id) : '',
        rep?.text?.replace(/\n/g, ' ') || '',
        String(cluster.candidates.length),
        memberIds.join(';'),
      ]
    })
    const csv = [header, ...rows]
      .map((r) => r.map((c) => '"' + c.replace(/"/g, '""') + '"').join(','))
      .join('\n')
    download('A_reps.csv', csv, 'text/csv')
  }

  return (
    <div
      className="flex min-h-screen w-full flex-col"
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      {errorMsg && (
        <div className="sticky top-0 z-20 border-b border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          <div className="flex items-center justify-between">
      <div>
              <b>Failed to load file:</b> {errorMsg}
            </div>
            <button className="rounded border px-2 py-0.5 text-xs" onClick={() => setErrorMsg(null)}>Dismiss</button>
          </div>
        </div>
      )}
      {/* File bar */}
      <div className="sticky top-0 z-10 border-b bg-white/80 p-3 backdrop-blur">
        <div className="flex flex-wrap items-center gap-2">
          <input
            ref={fileInputRef}
            type="file"
            accept=".jsonl"
            className="hidden"
            onChange={handleFileChange}
          />
          <button
            className="rounded bg-blue-600 px-3 py-1 text-sm font-medium text-white hover:bg-blue-700"
            onClick={() => fileInputRef.current?.click()}
          >
            Upload .jsonl
          </button>
          <div className="text-sm text-gray-600">
            clusters: <b>{summary.totalClusters}</b> · candidates: <b>{summary.totalCandidates}</b> · picked: <b>{summary.pickedCount}</b>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <button className="rounded border px-3 py-1 text-sm" onClick={exportJSONL}>
              Export JSONL
            </button>
            <button className="rounded border px-3 py-1 text-sm" onClick={exportCSV}>
              Export CSV
            </button>
          </div>
        </div>
        <div className="mt-2 flex items-center gap-2">
          <input
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Filter by text..."
            className="w-72 rounded border px-2 py-1 text-sm"
          />
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={showOnlyUnpicked}
              onChange={(e) => setShowOnlyUnpicked(e.target.checked)}
            />
            show only unpicked
          </label>
        </div>
      </div>

      {/* Two-pane layout */}
      <div className="grid flex-1 grid-cols-12">
        {/* Cluster list */}
        <div className="col-span-3 border-r">
          <div className="h-full overflow-auto">
            {filteredClusters.map((c) => {
              const picked = !!picks[c.cluster_id]
              const isSelected = selectedClusterId === c.cluster_id
              return (
                <button
                  key={c.cluster_id}
                  onClick={() => setSelectedClusterId(c.cluster_id)}
                  className={
                    'flex w-full items-center justify-between border-b p-2 text-left text-sm hover:bg-gray-50 ' +
                    (isSelected ? 'bg-gray-100' : '')
                  }
                >
                  <div>
                    <div className="font-medium">Cluster {c.cluster_id}</div>
                    <div className="text-xs text-gray-500">members: {c.candidates.length}</div>
                  </div>
                  <div className={picked ? 'text-green-700' : 'text-gray-400'}>{picked ? 'picked' : '—'}</div>
                </button>
              )
            })}
          </div>
        </div>

        {/* Cluster detail (first in filtered for now) */}
        <div className="col-span-9">
          <div className="h-full overflow-auto p-3">
            {filteredClusters.length === 0 ? (
              <div
                className={
                  'mt-4 flex h-48 cursor-pointer items-center justify-center rounded border-2 border-dashed ' +
                  (isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300')
                }
                onClick={() => fileInputRef.current?.click()}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <div className="text-center">
                  <div className="text-base font-medium text-gray-700">Drop .jsonl here or click to upload</div>
                  <div className="mt-1 text-xs text-gray-500">One JSON object per line: {`{"cluster_id": ..., "candidates": [...]}`}</div>
                </div>
              </div>
            ) : (
              <>
                {(() => {
                  const cluster = filteredClusters.find(c => c.cluster_id === selectedClusterId) || filteredClusters[0]
                  return (
                    <div key={cluster.cluster_id} className="space-y-3">
                      <div className="text-lg font-semibold">Cluster {cluster.cluster_id}</div>
                      {/* Move controls */}
                      <div className="flex flex-wrap items-center gap-2 rounded border bg-gray-50 p-2">
                        <div className="text-xs text-gray-600">Selected: {selectedCandidateIds.size}</div>
                        <button
                          className="rounded border px-2 py-1 text-xs"
                          onClick={() => {
                            // Move to new cluster: assign a new id (max+1)
                            if (selectedCandidateIds.size === 0) return
                            setClusters((prev) => {
                              const next: Cluster[] = []
                              const maxId = prev.reduce((m, c) => Math.max(m, c.cluster_id), -1)
                              const newId = maxId + 1
                              for (const cl of prev) {
                                if (cl.cluster_id !== cluster.cluster_id) {
                                  next.push(cl)
                                  continue
                                }
                                const keep: Candidate[] = []
                                const move: Candidate[] = []
                                for (const cand of cl.candidates) {
                                  if (selectedCandidateIds.has(candKey(cand))) move.push(cand)
                                  else keep.push(cand)
                                }
                                next.push({ ...cl, candidates: keep })
                                if (move.length > 0) next.push({ cluster_id: newId, candidates: move })
                              }
                              return dedupeClustersByText(next)
                            })
                            // reconcile picks
                            setPicks((prev) => {
                              const newPicks: PicksMap = { ...prev }
                              // unpick moved from source
                              if (newPicks[cluster.cluster_id] && selectedCandidateIds.has(candKey(newPicks[cluster.cluster_id]))) {
                                delete newPicks[cluster.cluster_id]
                              }
                              return newPicks
                            })
                            setSelectedCandidateIds(new Set())
                          }}
                          disabled={selectedCandidateIds.size === 0}
                        >
                          Move to new cluster
                        </button>
                        <div className="flex items-center gap-1 text-xs">
                          <span>Move to cluster</span>
                          <input
                            value={moveTargetId}
                            onChange={(e) => setMoveTargetId(e.target.value)}
                            placeholder="ID"
                            className="w-16 rounded border px-2 py-1"
                          />
                          <button
                            className="rounded border px-2 py-1"
                            onClick={() => {
                              if (selectedCandidateIds.size === 0) return
                              const target = parseInt(moveTargetId, 10)
                              if (!Number.isFinite(target)) return
                              setClusters((prev) => {
                                // First pass: remove selected from source, collect toMove
                                const intermediate: Cluster[] = []
                                let toMove: Candidate[] = []
                                for (const cl of prev) {
                                  if (cl.cluster_id === cluster.cluster_id) {
                                    const keep: Candidate[] = []
                                    const move: Candidate[] = []
                                    for (const cand of cl.candidates) {
                                      if (selectedCandidateIds.has(candKey(cand))) move.push(cand)
                                      else keep.push(cand)
                                    }
                                    toMove = move
                                    intermediate.push({ ...cl, candidates: keep })
                                  } else {
                                    intermediate.push(cl)
                                  }
                                }

                                // Second pass: attach to target (even if it appears before source)
                                let attached = false
                                const next = intermediate.map((cl) => {
                                  if (!attached && cl.cluster_id === target && toMove.length > 0) {
                                    attached = true
                                    return { ...cl, candidates: [...cl.candidates, ...toMove] }
                                  }
                                  return cl
                                })
                                if (!attached && toMove.length > 0) {
                                  next.push({ cluster_id: target, candidates: toMove })
                                }
                                return dedupeClustersByText(next)
                              })
                              setPicks((prev) => {
                                const newPicks: PicksMap = { ...prev }
                                if (newPicks[cluster.cluster_id] && selectedCandidateIds.has(candKey(newPicks[cluster.cluster_id]))) {
                                  delete newPicks[cluster.cluster_id]
                                }
                                return newPicks
                              })
                              setSelectedCandidateIds(new Set())
                            }}
                            disabled={selectedCandidateIds.size === 0 || moveTargetId.trim().length === 0}
                          >
                            Move
        </button>
                        </div>
                      </div>
                      <div className="space-y-2">
                        {cluster.candidates.map((cand, idx) => {
                          const isPicked = candKey(picks[cluster.cluster_id]) === candKey(cand)
                          const keyStr = candKey(cand)
                          const isChecked = selectedCandidateIds.has(keyStr)
                          return (
                            <div key={cand.lesson_id} className="rounded border p-2">
                              <div className="flex items-start gap-2">
                                <input
                                  type="checkbox"
                                  checked={isChecked}
                                  onChange={(e) => {
                                    setSelectedCandidateIds((prev) => {
                                      const copy = new Set(prev)
                                      if (e.target.checked) copy.add(keyStr)
                                      else copy.delete(keyStr)
                                      return copy
                                    })
                                  }}
                                  className="mt-1"
                                />
                                <input
                                  type="radio"
                                  name={`pick-${cluster.cluster_id}`}
                                  checked={isPicked}
                                  onChange={() =>
                                    setPicks((prev) => ({ ...prev, [cluster.cluster_id]: cand }))
                                  }
                                  className="mt-1"
                                />
                                <div>
                                  <div className="font-medium">{cand.text}</div>
                                  <div className="mt-1 text-xs text-gray-500">
                                    {cand.units && cand.units.length > 0 && (
                                      <span className="mr-2">
                                        units:{' '}
                                        {cand.units
                                          .map((u) => `${u.chapter}.${u.start}\u2013${u.end}`)
                                          .join('; ')}
                                      </span>
                                    )}
                                    {cand.source_ids && cand.source_ids.length > 0 && (
                                      <span>sources: {cand.source_ids.join(', ')}</span>
                                    )}
                                  </div>
                                </div>
                                <div className="ml-auto text-xs text-gray-400">{idx + 1}</div>
                              </div>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  )
                })()}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
