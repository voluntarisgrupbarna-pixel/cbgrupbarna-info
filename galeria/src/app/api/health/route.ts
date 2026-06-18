import { NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'

export async function GET() {
  const start = Date.now()

  try {
    const supabase = await createClient()
    await supabase.from('events').select('id').limit(1)
    return NextResponse.json({
      status: 'ok',
      db: 'ok',
      latency_ms: Date.now() - start,
      timestamp: new Date().toISOString(),
    })
  } catch {
    return NextResponse.json(
      { status: 'error', db: 'unreachable', timestamp: new Date().toISOString() },
      { status: 503 }
    )
  }
}
