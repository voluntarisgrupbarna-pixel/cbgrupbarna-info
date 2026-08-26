'use client'

import { Search, X } from 'lucide-react'
import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback, useState } from 'react'

interface SearchBarProps {
  placeholder?: string
  className?: string
}

export function SearchBar({ placeholder = 'Cerca...', className = '' }: SearchBarProps) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const [value, setValue] = useState(searchParams.get('q') ?? '')

  const updateSearch = useCallback((query: string) => {
    const params = new URLSearchParams(searchParams.toString())
    if (query) {
      params.set('q', query)
    } else {
      params.delete('q')
    }
    router.push(`${pathname}?${params.toString()}`)
  }, [pathname, router, searchParams])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    updateSearch(value)
  }

  const handleClear = () => {
    setValue('')
    updateSearch('')
  }

  return (
    <form onSubmit={handleSubmit} className={`relative ${className}`}>
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/30" />
      <input
        type="search"
        value={value}
        onChange={e => setValue(e.target.value)}
        placeholder={placeholder}
        aria-label={placeholder}
        className="input pl-10 pr-10"
      />
      {value && (
        <button
          type="button"
          onClick={handleClear}
          aria-label="Esborrar la cerca"
          className="absolute right-3 top-1/2 -translate-y-1/2 text-white/30 hover:text-white/60 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </form>
  )
}
