'use client'

import { createClient } from '@/lib/supabase/client'
import { useState } from 'react'

export default function LoginPage() {
  const [loading, setLoading] = useState(false)
  const supabase = createClient()

  async function signInWithGoogle() {
    setLoading(true)
    await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
        queryParams: {
          access_type: 'offline',
          prompt: 'consent',
        },
      },
    })
  }

  return (
    <div className="min-h-screen blueprint-grid flex flex-col items-center justify-center px-4 relative overflow-hidden"
      style={{ background: '#0d1117' }}>

      {/* Background glow */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full opacity-10 blur-3xl pointer-events-none"
        style={{ background: 'radial-gradient(circle, #4ade80 0%, transparent 70%)' }} />

      {/* Floating stage labels — decorative */}
      <div className="absolute top-12 left-12 text-xs font-mono opacity-20 text-green-400 hidden lg:block">
        A · Foundation<br />
        B · Walls<br />
        C · Roofing<br />
        D · Interiors<br />
        E · MEP<br />
        F · Landscape
      </div>
      <div className="absolute bottom-12 right-12 text-xs font-mono opacity-20 text-green-400 text-right hidden lg:block">
        Comfort · 82<br />
        Durability · 76<br />
        TCO · ₹4,200/sqft<br />
        Resilience · 91<br />
        Carbon · 38 kg
      </div>

      {/* Card */}
      <div className="relative z-10 w-full max-w-sm">

        {/* Brand */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center text-xl font-bold"
              style={{ background: 'linear-gradient(135deg, #4ade80, #22c55e)', color: '#0d1117' }}>
              ಯ
            </div>
            <div className="text-left">
              <h1 className="text-2xl font-bold tracking-tight" style={{ color: '#e6edf3' }}>
                Yojane
              </h1>
              <p className="text-xs font-mono" style={{ color: '#4ade80' }}>ಯೋಜನೆ</p>
            </div>
          </div>
          <p className="text-sm" style={{ color: '#7d8590' }}>Plan Before You Build</p>
        </div>

        {/* Login card */}
        <div className="rounded-xl border p-8" style={{ background: '#161b22', borderColor: '#30363d' }}>
          <h2 className="text-lg font-semibold mb-2" style={{ color: '#e6edf3' }}>
            Start your build
          </h2>
          <p className="text-sm mb-6" style={{ color: '#7d8590' }}>
            Sign in to save builds, generate reports, and share with your contractor.
          </p>

          <button
            onClick={signInWithGoogle}
            disabled={loading}
            className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-lg font-medium text-sm transition-all duration-200 disabled:opacity-60 cursor-pointer"
            style={{
              background: loading ? '#1c2128' : '#ffffff',
              color: '#0d1117',
              border: '1px solid #30363d',
            }}
          >
            {loading ? (
              <>
                <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                <span style={{ color: '#7d8590' }}>Signing in…</span>
              </>
            ) : (
              <>
                <svg width="18" height="18" viewBox="0 0 48 48">
                  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.36-8.16 2.36-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                </svg>
                Continue with Google
              </>
            )}
          </button>

          <p className="text-center text-xs mt-5" style={{ color: '#7d8590' }}>
            No password. No email signup. Just Google.
          </p>
        </div>

        {/* Demo note */}
        <p className="text-center text-xs mt-4" style={{ color: '#7d8590' }}>
          Want to explore first?{' '}
          <a href="/demo" className="underline" style={{ color: '#4ade80' }}>
            Try demo mode →
          </a>
        </p>
      </div>

      {/* Bottom tagline */}
      <p className="absolute bottom-6 text-xs font-mono opacity-30" style={{ color: '#7d8590' }}>
        Built by Pradeep Jain · Bangalore · 2026
      </p>
    </div>
  )
}
