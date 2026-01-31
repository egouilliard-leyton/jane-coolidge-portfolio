// components/ui/SkipLink.tsx
'use client'

/**
 * SkipLink Component
 *
 * Provides keyboard users with a way to skip directly to the main content,
 * bypassing the navigation. This is a key WCAG 2.1 requirement for keyboard
 * accessibility (Success Criterion 2.4.1).
 *
 * The link is visually hidden but becomes visible when focused via keyboard.
 */
export default function SkipLink() {
  return (
    <a
      href="#main-content"
      className="
        sr-only
        focus:not-sr-only
        focus:fixed
        focus:top-4
        focus:left-4
        focus:z-[100]
        focus:px-6
        focus:py-3
        focus:bg-neutral-900
        focus:text-white
        focus:rounded-lg
        focus:shadow-lg
        focus:outline-none
        focus:ring-2
        focus:ring-brand-500
        focus:ring-offset-2
        dark:focus:bg-white
        dark:focus:text-neutral-900
        font-medium
        text-sm
        tracking-wide
      "
    >
      Skip to main content
    </a>
  )
}
