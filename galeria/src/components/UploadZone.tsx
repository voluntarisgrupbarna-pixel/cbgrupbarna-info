'use client'

import { useCallback, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { Upload, X, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

interface UploadFile {
  file: File
  preview: string
  status: 'pending' | 'uploading' | 'done' | 'error'
  progress: number
  error?: string
}

interface UploadZoneProps {
  eventId: number
  userId: string
  onUploadComplete?: (count: number) => void
}

export function UploadZone({ eventId, userId, onUploadComplete }: UploadZoneProps) {
  const [files, setFiles] = useState<UploadFile[]>([])
  const [dragOver, setDragOver] = useState(false)
  const [uploading, setUploading] = useState(false)
  const supabase = createClient()

  const addFiles = useCallback((newFiles: FileList | File[]) => {
    const imageFiles = Array.from(newFiles).filter(f => f.type.startsWith('image/'))
    const uploadFiles: UploadFile[] = imageFiles.map(file => ({
      file,
      preview: URL.createObjectURL(file),
      status: 'pending',
      progress: 0,
    }))
    setFiles(prev => [...prev, ...uploadFiles])
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    addFiles(e.dataTransfer.files)
  }, [addFiles])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) addFiles(e.target.files)
  }

  const removeFile = (index: number) => {
    setFiles(prev => {
      URL.revokeObjectURL(prev[index].preview)
      return prev.filter((_, i) => i !== index)
    })
  }

  const uploadAll = async () => {
    const pending = files.filter(f => f.status === 'pending')
    if (pending.length === 0) return

    setUploading(true)
    let successCount = 0

    for (let i = 0; i < files.length; i++) {
      if (files[i].status !== 'pending') continue

      setFiles(prev => prev.map((f, idx) =>
        idx === i ? { ...f, status: 'uploading' } : f
      ))

      try {
        const file = files[i].file
        const ext = file.name.split('.').pop()
        const path = `events/${eventId}/${userId}/${Date.now()}-${Math.random().toString(36).slice(2)}.${ext}`

        const { error: storageError } = await supabase.storage
          .from('photos')
          .upload(path, file, { contentType: file.type, upsert: false })

        if (storageError) throw storageError

        // Get image dimensions from the preview
        const img = new window.Image()
        img.src = files[i].preview
        const { width, height } = await new Promise<{ width: number; height: number }>(resolve => {
          img.onload = () => resolve({ width: img.naturalWidth, height: img.naturalHeight })
          img.onerror = () => resolve({ width: 0, height: 0 })
        })

        const { error: dbError } = await supabase.from('photos').insert({
          event_id: eventId,
          storage_path: path,
          original_name: file.name,
          uploaded_by: userId,
          file_size: file.size,
          width: width || null,
          height: height || null,
        })

        if (dbError) throw dbError

        setFiles(prev => prev.map((f, idx) =>
          idx === i ? { ...f, status: 'done', progress: 100 } : f
        ))
        successCount++
      } catch (err) {
        setFiles(prev => prev.map((f, idx) =>
          idx === i
            ? { ...f, status: 'error', error: err instanceof Error ? err.message : 'Error en pujar' }
            : f
        ))
      }
    }

    setUploading(false)
    if (successCount > 0) onUploadComplete?.(successCount)
  }

  const pendingCount = files.filter(f => f.status === 'pending').length
  const doneCount = files.filter(f => f.status === 'done').length

  return (
    <div className="space-y-4">
      {/* Drop zone */}
      <div
        onDragOver={e => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-10 text-center transition-all duration-200 ${
          dragOver
            ? 'border-club-red bg-club-red/5'
            : 'border-white/10 hover:border-white/20 bg-club-gray-1/50'
        }`}
      >
        <Upload className="w-10 h-10 text-white/20 mx-auto mb-3" />
        <p className="text-white/60 font-body mb-2">
          Arrossega fotos aquí o{' '}
          <label className="text-club-red cursor-pointer hover:text-club-red-light transition-colors">
            selecciona-les
            <input
              type="file"
              multiple
              accept="image/*"
              className="hidden"
              onChange={handleFileInput}
            />
          </label>
        </p>
        <p className="text-white/30 text-sm font-body">
          JPG, PNG, WebP · Màx. 20 MB per foto
        </p>
      </div>

      {/* File list */}
      {files.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-mono text-xs text-white/40">
              {files.length} foto{files.length !== 1 ? 's' : ''} seleccionada{files.length !== 1 ? 's' : ''}
              {doneCount > 0 && ` · ${doneCount} pujada${doneCount !== 1 ? 's' : ''}`}
            </span>
            {pendingCount > 0 && !uploading && (
              <button onClick={uploadAll} className="btn-primary text-sm py-1.5 px-4">
                <Upload className="w-3.5 h-3.5" />
                Pujar {pendingCount} foto{pendingCount !== 1 ? 's' : ''}
              </button>
            )}
            {uploading && (
              <span className="flex items-center gap-2 text-white/40 text-sm font-body">
                <Loader2 className="w-4 h-4 animate-spin" />
                Pujant...
              </span>
            )}
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {files.map((f, i) => (
              <div key={i} className="relative rounded overflow-hidden bg-club-gray-2 aspect-square">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={f.preview}
                  alt={f.file.name}
                  className="w-full h-full object-cover"
                />

                {/* Status overlay */}
                <div className={`absolute inset-0 flex items-center justify-center transition-opacity duration-200 ${
                  f.status === 'pending' ? 'opacity-0' : 'opacity-100'
                } ${
                  f.status === 'uploading' ? 'bg-black/40' :
                  f.status === 'done' ? 'bg-black/30' :
                  f.status === 'error' ? 'bg-red-900/50' : ''
                }`}>
                  {f.status === 'uploading' && (
                    <Loader2 className="w-6 h-6 text-white animate-spin" />
                  )}
                  {f.status === 'done' && (
                    <CheckCircle className="w-6 h-6 text-green-400" />
                  )}
                  {f.status === 'error' && (
                    <AlertCircle className="w-6 h-6 text-red-400" />
                  )}
                </div>

                {/* Remove button */}
                {f.status !== 'uploading' && (
                  <button
                    onClick={() => removeFile(i)}
                    aria-label={`Treure ${f.file.name}`}
                    className="absolute top-1 right-1 bg-black/60 text-white/80 hover:text-white hover:bg-black/80 p-0.5 rounded transition-colors"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}

                {/* File name */}
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-1.5">
                  <p className="text-white/70 text-xs truncate font-mono">{f.file.name}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
