// components/ui/ImageLightbox.tsx
'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import Image from 'next/image'
import { motion, AnimatePresence, useReducedMotion } from 'motion/react'

interface ImageLightboxProps {
  src: string
  alt: string
  children: React.ReactNode
  blurDataURL?: string
}

/**
 * ImageLightbox Component
 *
 * Wraps an element and makes it clickable to open a fullscreen lightbox view.
 * Perfect for viewing artwork at full resolution.
 */
export default function ImageLightbox({ src, alt, children, blurDataURL }: ImageLightboxProps) {
  const [isOpen, setIsOpen] = useState(false)
  const shouldReduceMotion = useReducedMotion()
  const closeButtonRef = useRef<HTMLButtonElement>(null)

  const closeModal = useCallback(() => {
    setIsOpen(false)
  }, [])

  const openModal = useCallback(() => {
    setIsOpen(true)
  }, [])

  // Handle ESC key to close
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        closeModal()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown)
      document.body.style.overflow = 'hidden'
      // Focus close button when opened
      setTimeout(() => closeButtonRef.current?.focus(), 100)
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.body.style.overflow = ''
    }
  }, [isOpen, closeModal])

  const overlayVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
  }

  const imageVariants = {
    hidden: {
      opacity: 0,
      scale: shouldReduceMotion ? 1 : 0.9,
    },
    visible: {
      opacity: 1,
      scale: 1,
    },
  }

  return (
    <>
      {/* Clickable wrapper */}
      <div
        onClick={openModal}
        className="cursor-zoom-in"
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && openModal()}
        aria-label={`View ${alt} full size`}
      >
        {children}
      </div>

      {/* Lightbox Modal */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center"
            initial="hidden"
            animate="visible"
            exit="hidden"
            role="dialog"
            aria-modal="true"
            aria-label="Image lightbox"
          >
            {/* Backdrop */}
            <motion.div
              className="absolute inset-0 bg-black/90"
              variants={overlayVariants}
              transition={{ duration: shouldReduceMotion ? 0.1 : 0.3 }}
              onClick={closeModal}
              aria-hidden="true"
            />

            {/* Close Button */}
            <button
              ref={closeButtonRef}
              onClick={closeModal}
              className="
                absolute top-4 right-4 z-20
                p-3
                bg-white/10 hover:bg-white/20
                text-white
                rounded-full
                backdrop-blur-sm
                transition-colors duration-200
                focus:outline-none focus-visible:ring-2 focus-visible:ring-white
              "
              aria-label="Close lightbox"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>

            {/* Hint text */}
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-20 text-white/60 text-sm">
              Press ESC or click outside to close
            </div>

            {/* Image Container */}
            <motion.div
              className="relative z-10 w-full h-full flex items-center justify-center p-4 sm:p-8 md:p-12"
              variants={imageVariants}
              transition={{
                type: 'spring',
                duration: shouldReduceMotion ? 0.1 : 0.4,
                bounce: shouldReduceMotion ? 0 : 0.1,
              }}
              onClick={closeModal}
            >
              <div
                className="relative max-w-full max-h-full"
                onClick={(e) => e.stopPropagation()}
              >
                <Image
                  src={src}
                  alt={alt}
                  width={1800}
                  height={1200}
                  className="max-w-full max-h-[85vh] w-auto h-auto object-contain rounded-lg"
                  placeholder={blurDataURL ? 'blur' : undefined}
                  blurDataURL={blurDataURL}
                  priority
                />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
