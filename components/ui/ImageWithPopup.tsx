// components/ui/ImageWithPopup.tsx
'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import Image from 'next/image'
import { motion, AnimatePresence, useReducedMotion } from 'motion/react'
import { urlFor, getResponsiveSizes } from '@/sanity/lib/image'
import type { SanityImageBase, PopupContent } from '@/types'

/**
 * Props for the ImageWithPopup component
 */
export interface ImageWithPopupProps {
  /** Sanity image object */
  image: SanityImageBase | { url: string; _id?: string; lqip?: string }
  /** Alt text for accessibility */
  alt: string
  /** Optional caption displayed below the image */
  caption?: string
  /** Popup content with title, description, tags, and link */
  popup?: PopupContent | null
  /** Image display size */
  size?: 'small' | 'medium' | 'large' | 'full'
  /** Additional class names */
  className?: string
  /** Low-quality image placeholder (base64 string) for blur-up effect */
  lqip?: string
  /** Priority loading for above-the-fold images */
  priority?: boolean
}

/**
 * ImageWithPopup Component
 *
 * An interactive image component that displays fashion imagery with an elegant
 * modal popup for styling notes, product details, and purchase links.
 *
 * Features:
 * - Visual indicator showing image has popup content
 * - Smooth scale/fade animations using Motion
 * - Accessible: ESC key close, focus trapping, reduced motion support
 * - Touch-friendly with proper tap targets
 * - Click outside to dismiss
 */
export default function ImageWithPopup({
  image,
  alt,
  caption,
  popup,
  size = 'large',
  className = '',
  lqip,
  priority = false,
}: ImageWithPopupProps) {
  const [isOpen, setIsOpen] = useState(false)
  const shouldReduceMotion = useReducedMotion()
  const modalRef = useRef<HTMLDivElement>(null)
  const triggerRef = useRef<HTMLButtonElement>(null)
  const closeButtonRef = useRef<HTMLButtonElement>(null)

  const hasPopup = popup && (popup.title || popup.description)

  // Size classes for different image widths
  const sizeClasses: Record<string, string> = {
    small: 'max-w-sm mx-auto',
    medium: 'max-w-xl mx-auto',
    large: 'max-w-3xl mx-auto',
    full: 'w-full',
  }

  // Generate image URL - handle both Sanity images and pre-resolved URLs
  const imageUrl =
    'url' in image && image.url
      ? image.url
      : 'asset' in image && image.asset
        ? urlFor(image).width(1200).quality(90).auto('format').url()
        : ''

  // Determine blur placeholder - check props, then image object
  const blurDataURL = lqip || ('lqip' in image ? image.lqip : undefined)
  const hasBlurPlaceholder = Boolean(blurDataURL)

  // Get responsive sizes based on image size prop
  const responsiveSizes = size === 'full'
    ? getResponsiveSizes('full')
    : getResponsiveSizes('gallery')

  // Close modal handler
  const closeModal = useCallback(() => {
    setIsOpen(false)
    // Return focus to trigger element
    setTimeout(() => {
      triggerRef.current?.focus()
    }, 0)
  }, [])

  // Open modal handler
  const openModal = useCallback(() => {
    if (!hasPopup) return
    setIsOpen(true)
  }, [hasPopup])

  // Handle ESC key to close modal
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        closeModal()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown)
      // Prevent body scroll when modal is open
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.body.style.overflow = ''
    }
  }, [isOpen, closeModal])

  // Focus trap within modal
  useEffect(() => {
    if (isOpen && closeButtonRef.current) {
      // Focus the close button when modal opens
      closeButtonRef.current.focus()
    }
  }, [isOpen])

  // Handle tab key for focus trapping
  useEffect(() => {
    const handleTabKey = (e: KeyboardEvent) => {
      if (!isOpen || e.key !== 'Tab') return

      const modal = modalRef.current
      if (!modal) return

      const focusableElements = modal.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      const firstElement = focusableElements[0]
      const lastElement = focusableElements[focusableElements.length - 1]

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault()
          lastElement?.focus()
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault()
          firstElement?.focus()
        }
      }
    }

    document.addEventListener('keydown', handleTabKey)
    return () => document.removeEventListener('keydown', handleTabKey)
  }, [isOpen])

  // Animation variants
  const overlayVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
  }

  const modalVariants = {
    hidden: {
      opacity: 0,
      scale: shouldReduceMotion ? 1 : 0.92,
      y: shouldReduceMotion ? 0 : 20,
    },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
    },
  }

  const indicatorVariants = {
    initial: { scale: 1 },
    hover: { scale: 1.05 },
    tap: { scale: 0.95 },
  }

  if (!imageUrl) {
    return null
  }

  return (
    <figure className={`my-10 ${sizeClasses[size]} ${className}`}>
      {/* Image Container */}
      <div className="relative group">
        {/* Main Image */}
        <div
          className={`
            relative overflow-hidden rounded-lg
            bg-neutral-100 dark:bg-neutral-800
            ${hasPopup ? 'cursor-pointer' : ''}
          `}
          onClick={hasPopup ? openModal : undefined}
          role={hasPopup ? 'button' : undefined}
          tabIndex={hasPopup ? -1 : undefined}
          aria-label={hasPopup ? `View details for ${alt}` : undefined}
        >
          <Image
            src={imageUrl}
            alt={alt}
            width={1200}
            height={800}
            className={`
              w-full h-auto object-cover
              transition-transform duration-700 ease-out
              ${hasPopup ? 'group-hover:scale-[1.02]' : ''}
            `}
            sizes={responsiveSizes}
            placeholder={hasBlurPlaceholder ? 'blur' : undefined}
            blurDataURL={blurDataURL}
            priority={priority}
            loading={priority ? undefined : 'lazy'}
          />

          {/* Subtle hover overlay */}
          {hasPopup && (
            <div
              className="
                absolute inset-0
                bg-gradient-to-t from-black/30 via-transparent to-transparent
                opacity-0 group-hover:opacity-100
                transition-opacity duration-500
              "
              aria-hidden="true"
            />
          )}
        </div>

        {/* Popup Indicator Badge */}
        {hasPopup && (
          <motion.button
            ref={triggerRef}
            onClick={openModal}
            className="
              absolute bottom-4 right-4
              flex items-center gap-2
              px-4 py-2.5
              bg-white/95 dark:bg-neutral-900/95
              backdrop-blur-md
              rounded-full
              shadow-lg shadow-black/10
              border border-white/20 dark:border-neutral-700/50
              text-sm font-medium
              text-neutral-800 dark:text-neutral-200
              transition-all duration-300
              hover:shadow-xl hover:shadow-black/15
              focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
            "
            variants={indicatorVariants}
            initial="initial"
            whileHover="hover"
            whileTap="tap"
            aria-label={`View styling details for ${alt}`}
          >
            {/* Sparkle Icon */}
            <svg
              className="w-4 h-4 text-brand-600 dark:text-brand-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z"
              />
            </svg>
            <span>View Details</span>
          </motion.button>
        )}
      </div>

      {/* Caption */}
      {caption && (
        <figcaption className="mt-4 text-center text-sm text-neutral-500 dark:text-neutral-400 italic font-serif">
          {caption}
        </figcaption>
      )}

      {/* Modal Popup */}
      <AnimatePresence>
        {isOpen && popup && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
            initial="hidden"
            animate="visible"
            exit="hidden"
            role="dialog"
            aria-modal="true"
            aria-labelledby="popup-title"
          >
            {/* Backdrop */}
            <motion.div
              className="absolute inset-0 bg-black/60 backdrop-blur-sm"
              variants={overlayVariants}
              transition={{ duration: shouldReduceMotion ? 0.1 : 0.3 }}
              onClick={closeModal}
              aria-hidden="true"
            />

            {/* Modal Content */}
            <motion.div
              ref={modalRef}
              className="
                relative z-10
                w-full max-w-lg
                bg-white dark:bg-neutral-900
                rounded-2xl
                shadow-2xl shadow-black/25
                overflow-hidden
              "
              variants={modalVariants}
              transition={{
                type: 'spring',
                duration: shouldReduceMotion ? 0.1 : 0.4,
                bounce: shouldReduceMotion ? 0 : 0.15,
              }}
              onClick={(e) => e.stopPropagation()}
            >
              {/* Decorative top accent */}
              <div
                className="h-1 w-full bg-gradient-to-r from-brand-400 via-brand-500 to-brand-600"
                aria-hidden="true"
              />

              {/* Content Container */}
              <div className="p-6 sm:p-8">
                {/* Close Button */}
                <button
                  ref={closeButtonRef}
                  onClick={closeModal}
                  className="
                    absolute top-4 right-4
                    p-2
                    text-neutral-400 dark:text-neutral-500
                    hover:text-neutral-600 dark:hover:text-neutral-300
                    rounded-full
                    transition-colors duration-200
                    focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500
                  "
                  aria-label="Close popup"
                >
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    strokeWidth={1.5}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>

                {/* Title */}
                {popup.title && (
                  <h3
                    id="popup-title"
                    className="
                      font-display text-2xl sm:text-3xl
                      text-neutral-900 dark:text-neutral-100
                      tracking-tight
                      pr-10
                      mb-4
                    "
                  >
                    {popup.title}
                  </h3>
                )}

                {/* Description */}
                {popup.description && (
                  <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
                    {popup.description}
                  </p>
                )}

                {/* Tags */}
                {popup.tags && popup.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-6" role="list" aria-label="Tags">
                    {popup.tags.map((tag, index) => (
                      <span
                        key={`${tag}-${index}`}
                        role="listitem"
                        className="
                          inline-flex items-center
                          px-3 py-1.5
                          text-xs font-medium tracking-wide uppercase
                          bg-brand-50 dark:bg-brand-950/40
                          text-brand-700 dark:text-brand-300
                          rounded-full
                          border border-brand-100 dark:border-brand-900/50
                        "
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}

                {/* Link Button */}
                {popup.link && (
                  <a
                    href={popup.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="
                      inline-flex items-center gap-2
                      px-5 py-3
                      bg-neutral-900 dark:bg-white
                      text-white dark:text-neutral-900
                      font-medium
                      rounded-lg
                      transition-all duration-300
                      hover:bg-neutral-800 dark:hover:bg-neutral-100
                      hover:shadow-lg
                      focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
                      group
                    "
                  >
                    <span>{popup.linkText || 'Shop Now'}</span>
                    <svg
                      className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      strokeWidth={2}
                      aria-hidden="true"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
                      />
                    </svg>
                    <span className="sr-only">(opens in new tab)</span>
                  </a>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </figure>
  )
}
