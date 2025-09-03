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

function parseJSONL(text: string): { clusters: Cluster[]; warnings: string | null } {
  const lines = text.split(/\r?\n/).filter(Boolean)
  const out: Cluster[] = []
  let droppedLines = 0
  let prunedCandidates = 0

  const normNum = (v: any): number | null => {
    if (typeof v === 'number' && Number.isFinite(v)) return v
    if (typeof v === 'string' && v.trim().length > 0) {
      const n = Number(v)
      return Number.isFinite(n) ? n : null
    }
    return null
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    let obj: any
    try {
      obj = JSON.parse(line)
    } catch (e) {
      droppedLines++
      continue
    }

    // Format A: { cluster_id, candidates: [{lesson_id|old_cluster_id,text,...}] }
    if ((typeof obj.cluster_id === 'number' || typeof obj.cluster_id === 'string') && Array.isArray(obj.candidates)) {
      const cid = normNum(obj.cluster_id)
      if (cid == null) { droppedLines++; continue }
      const filtered: Candidate[] = []
      for (let j = 0; j < obj.candidates.length; j++) {
        const c = obj.candidates[j]
        if (typeof c !== 'object' || c === null) { prunedCandidates++; continue }
        const text = typeof c.text === 'string' ? c.text.trim() : ''
        if (!text) { prunedCandidates++; continue }
        let lessonId: string | undefined
        if (typeof c.lesson_id === 'string' && c.lesson_id.trim().length > 0) lessonId = c.lesson_id
        const oldId = normNum(c.old_cluster_id)
        if (!lessonId && oldId == null) { prunedCandidates++; continue }
        const cand: Candidate = {
          ...(lessonId ? { lesson_id: lessonId } : {}),
          ...(oldId != null ? { old_cluster_id: oldId } : {}),
          text,
          ...(Array.isArray(c.units) ? { units: c.units } : {}),
          ...(Array.isArray(c.source_ids) ? { source_ids: c.source_ids } : {}),
        }
        filtered.push(cand)
      }
      if (filtered.length === 0) { droppedLines++; continue }
      out.push({ cluster_id: cid, candidates: filtered })
      continue
    }

    // Format B: { cluster_id, lesson_id|old_cluster_id, text, ... }
    if (typeof obj === 'object' && obj !== null) {
      const cid = normNum(obj.cluster_id)
      const text = typeof obj.text === 'string' ? obj.text.trim() : ''
      const lid = (typeof obj.lesson_id === 'string' && obj.lesson_id.trim().length > 0) ? obj.lesson_id : undefined
      const oldId = normNum(obj.old_cluster_id)
      if (cid != null && text && (lid || oldId != null)) {
        const candidate: Candidate = {
          ...(lid ? { lesson_id: lid } : {}),
          ...(oldId != null ? { old_cluster_id: oldId } : {}),
          text,
          ...(Array.isArray(obj.units) ? { units: obj.units } : {}),
          ...(Array.isArray(obj.source_ids) ? { source_ids: obj.source_ids } : {}),
        }
        out.push({ cluster_id: cid, candidates: [candidate] })
        continue
      }
    }

    droppedLines++
  }

  const warnings: string[] = []
  if (droppedLines > 0) warnings.push(`skipped ${droppedLines} invalid line(s)`) 
  if (prunedCandidates > 0) warnings.push(`pruned ${prunedCandidates} invalid candidate(s)`) 
  return { clusters: out, warnings: warnings.length ? warnings.join('; ') : null }
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

// Merge clusters that share the same cluster_id (useful for Format B input)
function mergeClustersById(input: Cluster[]): Cluster[] {
  const map = new Map<number, Candidate[]>()
  for (const cl of input) {
    const cur = map.get(cl.cluster_id) || []
    map.set(cl.cluster_id, cur.concat(cl.candidates))
  }
  const merged: Cluster[] = []
  for (const [cid, candidates] of map.entries()) {
    merged.push({ cluster_id: cid, candidates })
  }
  // Deduplicate candidate texts within each merged cluster
  return dedupeClustersByText(merged)
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
  const [activeTab, setActiveTab] = useState<'reps' | 'ops'>('reps')
  const [unitEdit, setUnitEdit] = useState<{ chapter: string; start: string; end: string }>({ chapter: '', start: '', end: '' })
  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const versesFileInputRef = useRef<HTMLInputElement | null>(null)
  const [versesIndex, setVersesIndex] = useState<Record<number, Record<number, string>>>({})

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
    const { clusters: parsed, warnings } = parseJSONL(text)
    if (warnings) {
      setErrorMsg(warnings)
    } else {
      setErrorMsg(null)
    }
    // Merge same-id clusters (Format B lines) then dedupe texts within clusters
    const merged = mergeClustersById(parsed)
    const deduped = merged
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

  // Export current state as Units JSONL (site_units_view shape)
  function exportUnitsJSONL() {
    const lines = clusters.map((cl) => {
      const rep = cl.candidates[0]
      const text = rep?.text || ''
      const aggUnits: UnitSpan[] = []
      for (const c of cl.candidates) {
        if (Array.isArray(c.units)) aggUnits.push(...c.units)
      }
      const seen = new Set<string>()
      const units: UnitSpan[] = []
      for (const u of aggUnits) {
        const k = `${u.chapter}:${u.start}-${u.end}`
        if (seen.has(k)) continue
        seen.add(k)
        units.push(u)
      }
      return { cluster_id: cl.cluster_id, candidates: [{ text, units }] }
    })
    download('site_units_view.edited.jsonl', stringifyJSONL(lines), 'application/jsonl')
  }

  function updateLessonText(clusterId: number, newText: string) {
    setClusters((prev) => prev.map((cl) => {
      if (cl.cluster_id !== clusterId) return cl
      if (cl.candidates.length === 0) return cl
      const next = [...cl.candidates]
      next[0] = { ...next[0], text: newText }
      return { ...cl, candidates: next }
    }))
  }

  function onUploadVersesJSON(text: string) {
    try {
      const arr = JSON.parse(text) as Array<{ text: string; chapterNumber: number; verseNumber: number }>
      const idx: Record<number, Record<number, string>> = {}
      for (const v of arr) {
        if (!idx[v.chapterNumber]) idx[v.chapterNumber] = {}
        idx[v.chapterNumber][v.verseNumber] = v.text
      }
      setVersesIndex(idx)
      setErrorMsg(null)
    } catch (e: any) {
      setErrorMsg('Failed to parse verses JSON')
    }
  }

  function handleVersesFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => onUploadVersesJSON(String(reader.result || ''))
    reader.readAsText(file)
  }

  function getUnitText(u: UnitSpan): string {
    const chap = versesIndex[u.chapter]
    if (!chap) return ''
    const parts: string[] = []
    for (let v = u.start; v <= u.end; v++) {
      const t = chap[v]
      if (t) parts.push(t)
    }
    return parts.join(' ')
  }

  function moveUnitToCluster(sourceClusterId: number, candKeyStr: string, unitIdx: number, targetClusterId: number) {
    if (!Number.isFinite(targetClusterId)) return
    setClusters((prev) => {
      let moved: UnitSpan | null = null
      const intermediate: Cluster[] = prev.map((cl) => {
        if (cl.cluster_id !== sourceClusterId) return cl
        const nextCandidates = cl.candidates.map((c) => {
          const k = typeof c.lesson_id === 'string' ? c.lesson_id : `old:${c.old_cluster_id ?? -1}`
          if (k !== candKeyStr) return c
          const u = c.units ? [...c.units] : []
          if (unitIdx >= 0 && unitIdx < u.length) {
            moved = u[unitIdx]
            u.splice(unitIdx, 1)
          }
          return { ...c, units: u }
        })
        return { ...cl, candidates: nextCandidates }
      })
      if (!moved) return intermediate
      let attached = false
      const next = intermediate.map((cl) => {
        if (!attached && cl.cluster_id === targetClusterId) {
          attached = true
          if (cl.candidates.length === 0) {
            return { cluster_id: cl.cluster_id, candidates: [{ text: '', units: [moved!] }] }
          }
          const first = cl.candidates[0]
          const mergedUnits = dedupeUnitSpans([...(first.units || []), moved!])
          const newCandidates = [...cl.candidates]
          newCandidates[0] = { ...first, units: mergedUnits }
          return { ...cl, candidates: newCandidates }
        }
        return cl
      })
      if (!attached) next.push({ cluster_id: targetClusterId, candidates: [{ text: '', units: [moved] }] })
      return next.filter((cl) => cl.candidates.some((c) => (c.units?.length || 0) > 0))
    })
  }

  // Export clusters_humanpass1.jsonl (cluster_id -> member_lesson_ids[])
  function exportClustersJSONL() {
    const lines = clusters.map((cluster) => {
      const memberLessonIds = Array.from(
        new Set(
          cluster.candidates
            .map((c) => c.lesson_id)
            .filter((v): v is string => typeof v === 'string')
        )
      )
      return {
        cluster_id: cluster.cluster_id,
        member_lesson_ids: memberLessonIds,
        members_count: cluster.candidates.length,
      }
    })
    download('clusters_humanpass1.jsonl', stringifyJSONL(lines), 'application/jsonl')
  }

  

  // Helpers for unit operations
  function dedupeUnitSpans(units: UnitSpan[]): UnitSpan[] {
    const seen = new Set<string>()
    const out: UnitSpan[] = []
    for (const u of units) {
      const key = `${u.chapter}:${u.start}-${u.end}`
      if (seen.has(key)) continue
      seen.add(key)
      out.push(u)
    }
    return out
  }

  function addUnitToCandidate(clusterId: number, candKeyStr: string) {
    const chapter = parseInt(unitEdit.chapter, 10)
    const start = parseInt(unitEdit.start, 10)
    const end = parseInt(unitEdit.end, 10)
    if (!Number.isFinite(chapter) || !Number.isFinite(start) || !Number.isFinite(end)) return
    setClusters((prev) => {
      return prev.map((cl) => {
        if (cl.cluster_id !== clusterId) return cl
        const nextCandidates = cl.candidates.map((c) => {
          const k = typeof c.lesson_id === 'string' ? c.lesson_id : `old:${c.old_cluster_id ?? -1}`
          if (k !== candKeyStr) return c
          const nextUnits = dedupeUnitSpans([...(c.units || []), { chapter, start, end }])
          return { ...c, units: nextUnits }
        })
        return { ...cl, candidates: nextCandidates }
      })
    })
    setUnitEdit({ chapter: '', start: '', end: '' })
  }

  function deleteUnitFromCandidate(clusterId: number, candKeyStr: string, idx: number) {
    setClusters((prev) => {
      const next = prev.map((cl) => {
        if (cl.cluster_id !== clusterId) return cl
        const nextCandidates = cl.candidates.map((c) => {
          const k = typeof c.lesson_id === 'string' ? c.lesson_id : `old:${c.old_cluster_id ?? -1}`
          if (k !== candKeyStr) return c
          const u = c.units ? [...c.units] : []
          if (idx >= 0 && idx < u.length) u.splice(idx, 1)
          return { ...c, units: u }
        })
        return { ...cl, candidates: nextCandidates }
      })
      // prune empty clusters
      return next.filter((cl) => cl.candidates.length > 0)
    })
  }

  function moveUnitsBetweenCandidates(clusterId: number, fromKey: string, toKey: string, unitIdxs: number[]) {
    if (fromKey === toKey || unitIdxs.length === 0) return
    setClusters((prev) => {
      const mapped = prev.map((cl) => {
        if (cl.cluster_id !== clusterId) return cl
        let moved: UnitSpan[] = []
        const nextCandidates = cl.candidates.map((c) => {
          const k = typeof c.lesson_id === 'string' ? c.lesson_id : `old:${c.old_cluster_id ?? -1}`
          if (k === fromKey) {
            const sourceUnits = c.units ? [...c.units] : []
            // collect and remove specified indices
            const keep: UnitSpan[] = []
            for (let i = 0; i < sourceUnits.length; i++) {
              if (unitIdxs.includes(i)) moved.push(sourceUnits[i])
              else keep.push(sourceUnits[i])
            }
            return { ...c, units: keep }
          }
          return c
        }).map((c) => {
          const k = typeof c.lesson_id === 'string' ? c.lesson_id : `old:${c.old_cluster_id ?? -1}`
          if (k === toKey && moved.length > 0) {
            const merged = dedupeUnitSpans([...(c.units || []), ...moved])
            return { ...c, units: merged }
          }
          return c
        })
        return { ...cl, candidates: nextCandidates }
      })
      // prune empty clusters
      return mapped.filter((cl) => cl.candidates.length > 0)
    })
  }

  function mergeClusterIntoTarget(sourceId: number, targetId: number) {
    if (sourceId === targetId) return
    setClusters((prev) => {
      // First: move all candidates from source to target
      const intermediate: Cluster[] = []
      let moved: Candidate[] = []
      for (const cl of prev) {
        if (cl.cluster_id === sourceId) {
          moved = cl.candidates
          continue
        }
        intermediate.push(cl)
      }
      // Second: attach to target or create if missing
      let attached = false
      const next = intermediate.map((cl) => {
        if (!attached && cl.cluster_id === targetId) {
          attached = true
          // dedupe by text at candidate level
          const combined = [...cl.candidates, ...moved]
          const seen = new Set<string>()
          const deduped: Candidate[] = []
          for (const cand of combined) {
            const key = normalizeText(cand.text)
            if (seen.has(key)) continue
            seen.add(key)
            deduped.push(cand)
          }
          return { ...cl, candidates: deduped }
        }
        return cl
      })
      if (!attached && moved.length > 0) next.push({ cluster_id: targetId, candidates: moved })
      const pruned = next.filter((cl) => cl.candidates.length > 0)
      return dedupeClustersByText(pruned)
    })
    // Clear selection if we merged the currently selected
    if (selectedClusterId === sourceId) setSelectedClusterId(targetId)
  }

  function deleteCluster(clusterId: number) {
    setClusters((prev) => prev.filter((cl) => cl.cluster_id !== clusterId))
    setPicks((prev) => {
      const copy = { ...prev }
      delete copy[clusterId]
      return copy
    })
    if (selectedClusterId === clusterId) setSelectedClusterId(null)
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
      {/* File bar + Tabs */}
      <div className="sticky top-0 z-10 border-b bg-white/80 p-3 backdrop-blur">
        <div className="flex flex-wrap items-center gap-2">
          <input
            ref={fileInputRef}
            type="file"
            accept=".jsonl"
            className="hidden"
            onChange={handleFileChange}
          />
          <input
            ref={versesFileInputRef}
            type="file"
            accept=".json"
            className="hidden"
            onChange={handleVersesFileChange}
          />
          <button
            className="rounded bg-blue-600 px-3 py-1 text-sm font-medium text-white hover:bg-blue-700"
            onClick={() => fileInputRef.current?.click()}
          >
            Upload .jsonl
          </button>
          <button
            className="rounded border px-3 py-1 text-sm"
            onClick={() => versesFileInputRef.current?.click()}
            title="Optional: upload verses-formatted.json to see the exact unit text"
          >
            Upload Units Text (optional)
          </button>
          <div className="text-sm text-gray-600">
            clusters: <b>{summary.totalClusters}</b> · candidates: <b>{summary.totalCandidates}</b> · picked: <b>{summary.pickedCount}</b>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <div className="flex items-center gap-1 text-sm">
              <button
                className={
                  'rounded px-3 py-1 ' + (activeTab === 'reps' ? 'bg-gray-800 text-white' : 'border')
                }
                onClick={() => setActiveTab('reps')}
              >
                Reps
              </button>
              <button
                className={
                  'rounded px-3 py-1 ' + (activeTab === 'ops' ? 'bg-gray-800 text-white' : 'border')
                }
                onClick={() => setActiveTab('ops')}
              >
                Cluster Ops
              </button>
            </div>
            {activeTab === 'reps' ? (
              <>
                <button className="rounded border px-3 py-1 text-sm" onClick={exportJSONL}>
                  Export JSONL
                </button>
                <button className="rounded border px-3 py-1 text-sm" onClick={exportCSV}>
                  Export CSV
                </button>
              </>
            ) : (
              <>
                <button className="rounded border px-3 py-1 text-sm" onClick={exportClustersJSONL}>
                  Export clusters_humanpass1.jsonl
                </button>
                <button className="rounded border px-3 py-1 text-sm" onClick={exportUnitsJSONL}>
                  Export Units JSONL
                </button>
              </>
            )}
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
                    <div className="text-xs text-gray-500">units: {c.candidates.reduce((acc, cc) => acc + (cc.units?.length || 0), 0)}</div>
                  </div>
                  {activeTab === 'reps' ? (
                    <div className={picked ? 'text-green-700' : 'text-gray-400'}>{picked ? 'picked' : '—'}</div>
                  ) : (
                    <div className="text-gray-400">&nbsp;</div>
                  )}
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
                      {activeTab === 'ops' && (
                        <div className="flex items-center gap-2">
                          <input
                            defaultValue={cluster.candidates[0]?.text || ''}
                            onBlur={(e) => updateLessonText(cluster.cluster_id, e.target.value)}
                            placeholder="Lesson text"
                            className="w-full rounded border px-2 py-1 text-sm"
                          />
                        </div>
                      )}

                      {activeTab === 'reps' ? (
                        <div className="flex flex-wrap items-center gap-2 rounded border bg-gray-50 p-2">
                          <div className="text-xs text-gray-600">Selected: {selectedCandidateIds.size}</div>
                          <button
                            className="rounded border px-2 py-1 text-xs"
                            onClick={() => {
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
                              setPicks((prev) => {
                                const newPicks: PicksMap = { ...prev }
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
                      ) : (
                        <div className="space-y-2 rounded border bg-gray-50 p-2">
                          <div className="flex flex-wrap items-center gap-2 text-xs text-gray-700">
                            <span className="font-medium">Cluster Ops</span>
                            <div className="flex items-center gap-1">
                              <span>Merge into</span>
                              <input
                                value={moveTargetId}
                                onChange={(e) => setMoveTargetId(e.target.value)}
                                placeholder="Target ID"
                                className="w-20 rounded border px-2 py-1"
                              />
                              <button
                                className="rounded border px-2 py-1"
                                onClick={() => {
                                  const target = parseInt(moveTargetId, 10)
                                  if (!Number.isFinite(target)) return
                                  mergeClusterIntoTarget(cluster.cluster_id, target)
                                  setMoveTargetId('')
                                }}
                              >
                                Merge
                              </button>
                            </div>
                            <button
                              className="rounded border px-2 py-1 text-red-700"
                              onClick={() => deleteCluster(cluster.cluster_id)}
                            >
                              Delete cluster
                            </button>
                            <button
                              className="rounded border px-2 py-1"
                              onClick={exportClustersJSONL}
                            >
                              Export clusters jsonl
                            </button>
                            <button
                              className="rounded border px-2 py-1"
                              onClick={() => versesFileInputRef.current?.click()}
                              title="Optional: upload verses-formatted.json to see the exact unit text"
                            >
                              Upload Units Text
                            </button>
                          </div>
                        </div>
                      )}

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
                                {activeTab === 'reps' && (
                                  <input
                                    type="radio"
                                    name={`pick-${cluster.cluster_id}`}
                                    checked={isPicked}
                                    onChange={() =>
                                      setPicks((prev) => ({ ...prev, [cluster.cluster_id]: cand }))
                                    }
                                    className="mt-1"
                                  />
                                )}
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
                                  {activeTab === 'ops' && (
                                    <div className="mt-2 space-y-2 rounded border bg-white p-2">
                                      <div className="text-xs font-medium text-gray-700">Unit editor</div>
                                      <div className="flex flex-wrap items-center gap-2 text-xs">
                                        <input
                                          value={unitEdit.chapter}
                                          onChange={(e) => setUnitEdit({ ...unitEdit, chapter: e.target.value })}
                                          placeholder="chapter"
                                          className="w-20 rounded border px-2 py-1"
                                        />
                                        <input
                                          value={unitEdit.start}
                                          onChange={(e) => setUnitEdit({ ...unitEdit, start: e.target.value })}
                                          placeholder="start"
                                          className="w-20 rounded border px-2 py-1"
                                        />
                                        <input
                                          value={unitEdit.end}
                                          onChange={(e) => setUnitEdit({ ...unitEdit, end: e.target.value })}
                                          placeholder="end"
                                          className="w-20 rounded border px-2 py-1"
                                        />
                                        <button
                                          className="rounded border px-2 py-1"
                                          onClick={() => addUnitToCandidate(cluster.cluster_id, keyStr)}
                                        >
                                          Add unit
                                        </button>
                                      </div>
                                      <div className="text-xs">
                                        {(cand.units || []).length === 0 ? (
                                          <div className="text-gray-500">No units</div>
                                        ) : (
                                          <div className="space-y-1">
                                            {(cand.units || []).map((u, uIdx) => (
                                              <div key={uIdx} className="flex items-start justify-between gap-2 rounded border px-2 py-1">
                                                <div className="text-xs">
                                                  <div className="font-medium">{u.chapter}.{u.start}–{u.end}</div>
                                                  {(() => { const t = (typeof getUnitText === 'function') ? getUnitText(u) : ''; return t ? (<div className="mt-1 text-gray-700">{t}</div>) : null })()}
                                                </div>
                                                <div className="flex items-center gap-2">
                                                  {/* Move this unit to another candidate in cluster */}
                                                  <select
                                                    className="rounded border px-1 py-0.5 text-xs"
                                                    onChange={(e) => {
                                                      const toKey = e.target.value
                                                      if (!toKey) return
                                                      moveUnitsBetweenCandidates(cluster.cluster_id, keyStr, toKey, [uIdx])
                                                      e.currentTarget.selectedIndex = 0
                                                    }}
                                                  >
                                                    <option value="">Move to…</option>
                                                    {cluster.candidates
                                                      .filter((c2) => (typeof c2.lesson_id === 'string' ? c2.lesson_id : `old:${c2.old_cluster_id ?? -1}`) !== keyStr)
                                                      .map((c2) => {
                                                        const toKeyStr = typeof c2.lesson_id === 'string' ? c2.lesson_id : `old:${c2.old_cluster_id ?? -1}`
                                                        const label = (c2.text || '').slice(0, 40)
                                                        return (
                                                          <option key={toKeyStr} value={toKeyStr}>
                                                            {toKeyStr} · {label}
                                                          </option>
                                                        )
                                                      })}
                                                  </select>
                                                  <select
                                                    className="rounded border px-1 py-0.5 text-xs"
                                                    onChange={(e) => {
                                                      const val = e.target.value
                                                      if (!val) return
                                                      const target = parseInt(val, 10)
                                                      if (!Number.isFinite(target)) return
                                                      moveUnitToCluster(cluster.cluster_id, keyStr, uIdx, target)
                                                      e.currentTarget.selectedIndex = 0
                                                    }}
                                                  >
                                                    <option value="">Move to… (cluster id)</option>
                                                    {clusters
                                                      .filter((cl2) => cl2.cluster_id !== cluster.cluster_id)
                                                      .map((cl2) => (
                                                        <option key={cl2.cluster_id} value={cl2.cluster_id}>
                                                          {cl2.cluster_id}
                                                        </option>
                                                      ))}
                                                  </select>
                                                  <button
                                                    className="rounded border px-2 py-0.5 text-xs"
                                                    onClick={() => {
                                                      const answer = prompt('Move unit to cluster id:')
                                                      if (!answer) return
                                                      const target = parseInt(answer, 10)
                                                      if (!Number.isFinite(target)) return
                                                      moveUnitToCluster(cluster.cluster_id, keyStr, uIdx, target)
                                                    }}
                                                  >
                                                    Move (prompt)
                                                  </button>
                                                  <button
                                                    className="rounded border px-2 py-0.5 text-xs text-red-700"
                                                    onClick={() => deleteUnitFromCandidate(cluster.cluster_id, keyStr, uIdx)}
                                                  >
                                                    Delete
                                                  </button>
                                                </div>
                                              </div>
                                            ))}
                                          </div>
                                        )}
                                      </div>
                                    </div>
                                  )}
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
