// app/(site)/SiteLayoutClient.tsx
'use client'

import { type ReactNode } from 'react'
import { motion, useReducedMotion } from 'motion/react'
import { usePathname } from 'next/navigation'

/**
 * SiteLayoutClient
 *
 * Client component that provides page transition animations.
 * Wraps page content with a fade/slide animation on route changes.
 * Respects prefers-reduced-motion user preference.
 */

// Elegant timing curve for fashion-forward transitions
const TRANSITION_EASE: [number, number, number, number] = [0.25, 0.1, 0.25, 1]

export default function SiteLayoutClient({
  children,
}: {
  children: ReactNode
}) {
  const pathname = usePathname()
  const shouldReduceMotion = useReducedMotion()

  // Animation configuration based on user preference
  const initialAnimation = shouldReduceMotion
    ? { opacity: 0 }
    : { opacity: 0, y: 16 }

  const animateState = shouldReduceMotion
    ? { opacity: 1 }
    : { opacity: 1, y: 0 }

  return (
    <motion.main
      id="main-content"
      tabIndex={-1}
      key={pathname}
      initial={initialAnimation}
      animate={animateState}
      transition={{
        duration: shouldReduceMotion ? 0.15 : 0.45,
        ease: TRANSITION_EASE,
      }}
      className="min-h-screen outline-none"
    >
      {children}
    </motion.main>
  )
}
