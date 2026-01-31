// components/ui/PageTransition.tsx
'use client'

import { type ReactNode } from 'react'
import { motion, AnimatePresence, useReducedMotion } from 'motion/react'
import { usePathname } from 'next/navigation'

/**
 * Page transition configuration
 * Provides elegant fade and slide animations between route changes
 */

// Elegant timing curve for fashion-forward transitions (typed as tuple)
const TRANSITION_EASE: [number, number, number, number] = [0.25, 0.1, 0.25, 1]

// Page transition variants
const pageVariants = {
  initial: {
    opacity: 0,
    y: 20,
  },
  enter: {
    opacity: 1,
    y: 0,
  },
  exit: {
    opacity: 0,
    y: -10,
  },
}

// Reduced motion variants (opacity only)
const reducedMotionVariants = {
  initial: {
    opacity: 0,
  },
  enter: {
    opacity: 1,
  },
  exit: {
    opacity: 0,
  },
}

export interface PageTransitionProps {
  children: ReactNode
  /** Additional className for the wrapper */
  className?: string
}

/**
 * PageTransition Component
 *
 * Wraps page content to provide smooth fade/slide animations
 * when navigating between routes. Respects prefers-reduced-motion.
 *
 * Note: In Next.js App Router, this component should be placed
 * in the layout and receives children that change with routes.
 */
export default function PageTransition({
  children,
  className = '',
}: PageTransitionProps) {
  const pathname = usePathname()
  const shouldReduceMotion = useReducedMotion()

  const variants = shouldReduceMotion ? reducedMotionVariants : pageVariants
  const duration = shouldReduceMotion ? 0.15 : 0.4

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={pathname}
        initial="initial"
        animate="enter"
        exit="exit"
        variants={variants}
        transition={{
          duration,
          ease: TRANSITION_EASE,
        }}
        className={className}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}

/**
 * FadeTransition - Simple fade-only page transition
 *
 * A lighter alternative to PageTransition that only uses opacity
 */
export function FadeTransition({
  children,
  className = '',
}: PageTransitionProps) {
  const pathname = usePathname()
  const shouldReduceMotion = useReducedMotion()

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={pathname}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{
          duration: shouldReduceMotion ? 0.1 : 0.3,
          ease: 'easeInOut',
        }}
        className={className}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}

/**
 * SlideTransition - Slide-based page transition
 *
 * Provides a more dramatic slide effect for page changes
 */
export interface SlideTransitionProps extends PageTransitionProps {
  /** Direction of slide: 'left' | 'right' | 'up' | 'down' */
  direction?: 'left' | 'right' | 'up' | 'down'
}

export function SlideTransition({
  children,
  direction = 'left',
  className = '',
}: SlideTransitionProps) {
  const pathname = usePathname()
  const shouldReduceMotion = useReducedMotion()

  const getOffset = () => {
    switch (direction) {
      case 'left': return { x: 100, y: 0 }
      case 'right': return { x: -100, y: 0 }
      case 'up': return { x: 0, y: 100 }
      case 'down': return { x: 0, y: -100 }
    }
  }

  const offset = getOffset()

  if (shouldReduceMotion) {
    return (
      <motion.div
        key={pathname}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.15 }}
        className={className}
      >
        {children}
      </motion.div>
    )
  }

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={pathname}
        initial={{ opacity: 0, x: offset.x, y: offset.y }}
        animate={{ opacity: 1, x: 0, y: 0 }}
        exit={{ opacity: 0, x: -offset.x / 2, y: -offset.y / 2 }}
        transition={{
          type: 'spring',
          damping: 25,
          stiffness: 200,
        }}
        className={className}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
