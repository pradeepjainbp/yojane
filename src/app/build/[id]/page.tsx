import { redirect, notFound } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'
import BuildSimulator from './BuildSimulator'
import type { Build, Decision, BuildScores } from '@/types'

export default async function BuildPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  const { data: build } = await supabase
    .from('builds')
    .select('*')
    .eq('id', id)
    .eq('user_id', user.id)
    .single()

  if (!build) notFound()

  const { data: decisions } = await supabase
    .from('decisions')
    .select('*')
    .eq('build_id', id)
    .order('decision_id')

  const { data: scores } = await supabase
    .from('build_scores')
    .select('*')
    .eq('build_id', id)
    .single()

  return (
    <BuildSimulator
      build={build as Build}
      initialDecisions={(decisions ?? []) as Decision[]}
      initialScores={scores as BuildScores | null}
    />
  )
}
