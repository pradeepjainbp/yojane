import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'
import Link from 'next/link'
import type { Build } from '@/types'
import BuildCard from '@/components/dashboard/BuildCard'

export default async function DashboardPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  const { data: builds } = await supabase
    .from('builds')
    .select('*')
    .eq('user_id', user.id)
    .order('updated_at', { ascending: false })

  const firstName = user.user_metadata?.full_name?.split(' ')[0] ?? 'there'

  return (
    <div className="min-h-screen" style={{ background: '#0d1117' }}>
      {/* Header */}
      <header className="border-b" style={{ borderColor: '#21262d', background: '#161b22' }}>
        <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded flex items-center justify-center text-sm font-bold"
              style={{ background: 'linear-gradient(135deg, #4ade80, #22c55e)', color: '#0d1117' }}>ಯ</div>
            <span className="font-semibold text-sm" style={{ color: '#e6edf3' }}>Yojane</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm" style={{ color: '#7d8590' }}>
              {user.user_metadata?.full_name ?? user.email}
            </span>
            <form action="/auth/signout" method="post">
              <button type="submit" className="text-xs px-3 py-1.5 rounded border cursor-pointer"
                style={{ borderColor: '#30363d', color: '#7d8590' }}>
                Sign out
              </button>
            </form>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-10">
        {/* Welcome */}
        <div className="flex items-start justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold mb-1" style={{ color: '#e6edf3' }}>
              Good to see you, {firstName}.
            </h1>
            <p className="text-sm" style={{ color: '#7d8590' }}>
              {builds && builds.length > 0
                ? `You have ${builds.length} build${builds.length > 1 ? 's' : ''} in progress.`
                : 'Start your first build — it takes about 15 minutes.'}
            </p>
          </div>
          <Link
            href="/dashboard/new"
            className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            style={{ background: '#4ade80', color: '#0d1117' }}
          >
            <span>+</span> New Build
          </Link>
        </div>

        {/* Builds grid */}
        {builds && builds.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {(builds as Build[]).map((build) => (
              <BuildCard key={build.id} build={build} />
            ))}

          </div>
        ) : (
          <EmptyState />
        )}
      </main>
    </div>
  )
}


function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <div className="w-16 h-16 rounded-2xl mb-6 flex items-center justify-center text-3xl"
        style={{ background: '#1c2128', border: '1px dashed #30363d' }}>
        🏗
      </div>
      <h2 className="text-lg font-semibold mb-2" style={{ color: '#e6edf3' }}>No builds yet</h2>
      <p className="text-sm mb-6 max-w-xs" style={{ color: '#7d8590' }}>
        Start by pinning your plot location, then walk through 45 construction decisions — guided at every step.
      </p>
      <Link href="/dashboard/new"
        className="px-5 py-2.5 rounded-lg font-medium text-sm"
        style={{ background: '#4ade80', color: '#0d1117' }}>
        Start your first build
      </Link>
    </div>
  )
}
