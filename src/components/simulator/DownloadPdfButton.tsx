'use client'

import { useState } from 'react'

export default function DownloadPdfButton({ buildName }: { buildName: string }) {
  const [loading, setLoading] = useState(false)

  async function handleDownload() {
    setLoading(true)
    try {
      const html2canvas = (await import('html2canvas')).default
      const { jsPDF } = await import('jspdf')

      const reportEl = document.getElementById('yojane-report')
      if (!reportEl) return

      // Capture the full report div as a canvas
      const canvas = await html2canvas(reportEl, {
        scale: 2,                    // retina quality
        useCORS: true,
        backgroundColor: '#0d1117',
        logging: false,
      })

      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4',
      })

      const pageWidth = pdf.internal.pageSize.getWidth()
      const pageHeight = pdf.internal.pageSize.getHeight()
      const imgWidth = pageWidth
      const imgHeight = (canvas.height * imgWidth) / canvas.width

      // If the content is taller than one page, split across pages
      let yOffset = 0
      let remaining = imgHeight

      while (remaining > 0) {
        if (yOffset > 0) pdf.addPage()
        pdf.addImage(imgData, 'PNG', 0, -yOffset, imgWidth, imgHeight)
        yOffset += pageHeight
        remaining -= pageHeight
      }

      const filename = `Yojane_${buildName.replace(/\s+/g, '_')}_Report.pdf`
      pdf.save(filename)
    } catch (err) {
      console.error('PDF generation failed:', err)
      alert('PDF generation failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <button
      onClick={handleDownload}
      disabled={loading}
      className="px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer disabled:opacity-60 transition-opacity"
      style={{ background: '#4ade80', color: '#0d1117' }}
    >
      {loading ? (
        <span className="flex items-center gap-1.5">
          <svg className="animate-spin w-3 h-3" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Generating…
        </span>
      ) : (
        'Download PDF'
      )}
    </button>
  )
}
