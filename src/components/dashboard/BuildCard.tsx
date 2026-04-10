'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { createClient } from '@/lib/supabase/client'
import type { Build } from '@/types'

export default function BuildCard({ build }: { build: Build }) {
  const router = useRouter()
  const [confirming, setConfirming] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const typeBadge: Record<string, { label: string; color: string }> = {
    residential:  { label: 'House',       color: '#4ade80' },
    apartment:    { label: 'Apartment',   color: '#60a5fa' },
    commercial:   { label: 'Commercial',  color: '#f59e0b' },
    agricultural: { label: 'Farm',        color: '#a3e635' },
    utility:      { label: 'Utility',     color: '#c084fc' },
  }
  const badge = typeBadge[build.building_type] ?? { label: build.building_type, color: '#7d8590' }

  async function handleDelete(e: React.MouseEvent) {
    e.preventDefault()
    e.stopPropagation()
    if (!confirming) { setConfirming(true); return }
    setDeleting(true)
    const supabase = createClient()
    await supabase.from('builds').delete().eq('id', build.id)
    router.refresh()
  }

  function handleCancelDelete(e: React.MouseEvent) {
    e.preventDefault()
    e.stopPropagation()
    setConfirming(false)
  }

  return (
    <div className="relative">
      <Link href={`/build/${build.id}`}
        className="block rounded-xl p-5 transition-colors"
        style={{ background: '#161b22', border: '1px solid #30363d' }}>

        <div className="flex items-start justify-between mb-3 pr-8">
          <span className="text-xs px-2 py-0.5 rounded-full font-mono"
            style={{ background: `${badge.color}20`, color: badge.color }}>
            {badge.label}
          </span>
          <span className="text-xs" style={{ color: '#7d8590' }}>
            {build.status === 'complete' ? '✓ Complete' : '● Draft'}
          </span>
        </div>

        <h3 className="font-semibold mb-1 pr-8" style={{ color: '#e6edf3' }}>
          {build.name}
        </h3>
        <p className="text-xs" style={{ color: '#7d8590' }}>
          {build.plot_config?.plot_area_sqft
            ? `${build.plot_config.plot_area_sqft} sqft · ${build.plot_config.floors ?? 1} floor${(build.plot_config.floors ?? 1) > 1 ? 's' : ''}`
            : 'Plot not configured'}
        </p>
        <p className="text-xs mt-2" suppressHydrationWarning style={{ color: '#7d8590' }}>
          Updated {new Date(build.updated_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
        </p>
      </Link>

      {/* Delete button — always visible in top-right corner */}
      {!confirming ? (
        <button
          onClick={handleDelete}
          className="absolute top-4 right-4 w-7 h-7 rounded flex items-center justify-center cursor-pointer text-base leading-none"
          style={{ background: '#ef444425', color: '#ef4444', border: '1px solid #ef444430' }}
          title="Delete build">
          ×
        </button>
      ) : (
        <div className="absolute inset-0 rounded-xl flex flex-col items-center justify-center gap-3 p-4"
          style={{ background: '#161b22f0', border: '1px solid #ef444440' }}>
          <p className="text-sm font-medium text-center" style={{ color: '#e6edf3' }}>
            Delete "{build.name}"?
          </p>
          <p className="text-xs text-center" style={{ color: '#7d8590' }}>
            This cannot be undone.
          </p>
          <div className="flex gap-2">
            <button
              onClick={handleCancelDelete}
              className="px-3 py-1.5 rounded-lg text-xs cursor-pointer"
              style={{ border: '1px solid #30363d', color: '#7d8590' }}>
              Cancel
            </button>
            <button
              onClick={handleDelete}
              disabled={deleting}
              className="px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer"
              style={{ background: '#ef4444', color: '#fff', opacity: deleting ? 0.6 : 1 }}>
              {deleting ? 'Deleting…' : 'Yes, delete'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
