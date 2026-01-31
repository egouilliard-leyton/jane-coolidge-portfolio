// components/ui/animations.tsx
'use client'

import { useRef, useEffect, useState, type ReactNode } from 'react'
import { motion, useInView, useReducedMotion, type Variants } from 'motion/react'

/**
 * Animation configuration respecting user preferences
 * All animations are disabled when prefers-reduced-motion is set
 */

// Elegant timing curves for fashion-forward animations
const TIMING = {
  // Smooth, refined easing for luxury feel
  fashion: [0.25, 0.1, 0.25, 1],
  // Dramatic exit for editorial impact
  exit: [0.65, 0, 0.35, 1],
  // Spring-like reveal for organic motion
  spring: { type: 'spring', damping: 25, stiffness: 120 },
} as const

/**
 * ScrollReveal - Animate elements when they enter viewport
 *
 * Wraps children in a motion component that reveals with a fade-up animation
 * when scrolled into view. Respects prefers-reduced-motion.
 */
export interface ScrollRevealProps {
  children: ReactNode
  /** Animation variant: 'fade' | 'fade-up' | 'fade-left' | 'fade-right' | 'scale' */
  variant?: 'fade' | 'fade-up' | 'fade-left' | 'fade-right' | 'scale'
  /** Delay before animation starts (in seconds) */
  delay?: number
  /** Duration of the animation (in seconds) */
  duration?: number
  /** How much of the element needs to be visible (0-1) */
  threshold?: number
  /** Only animate once? */
  once?: boolean
  /** Additional className */
  className?: string
  /** HTML element to render as */
  as?: 'div' | 'section' | 'article' | 'header' | 'footer' | 'aside' | 'main' | 'span'
}

const revealVariants: Record<string, Variants> = {
  fade: {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
  },
  'fade-up': {
    hidden: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0 },
  },
  'fade-left': {
    hidden: { opacity: 0, x: -40 },
    visible: { opacity: 1, x: 0 },
  },
  'fade-right': {
    hidden: { opacity: 0, x: 40 },
    visible: { opacity: 1, x: 0 },
  },
  scale: {
    hidden: { opacity: 0, scale: 0.92 },
    visible: { opacity: 1, scale: 1 },
  },
}

export function ScrollReveal({
  children,
  variant = 'fade-up',
  delay = 0,
  duration = 0.6,
  threshold = 0.15,
  once = true,
  className = '',
  as = 'div',
}: ScrollRevealProps) {
  const ref = useRef<HTMLDivElement>(null)
  const isInView = useInView(ref, { amount: threshold, once })
  const shouldReduceMotion = useReducedMotion()

  // Skip animation if user prefers reduced motion
  if (shouldReduceMotion) {
    const Component = as
    return <div ref={ref} className={className}>{children}</div>
  }

  const MotionComponent = motion[as] as typeof motion.div

  return (
    <MotionComponent
      ref={ref}
      initial="hidden"
      animate={isInView ? 'visible' : 'hidden'}
      variants={revealVariants[variant]}
      transition={{
        duration,
        delay,
        ease: TIMING.fashion,
      }}
      className={className}
    >
      {children}
    </MotionComponent>
  )
}

/**
 * StaggerReveal - Staggered animation for lists/grids
 *
 * Wraps a container whose children will animate in sequence
 */
export interface StaggerRevealProps {
  children: ReactNode
  /** Delay between each child animation */
  staggerDelay?: number
  /** Base delay before stagger starts */
  baseDelay?: number
  /** Animation variant */
  variant?: 'fade' | 'fade-up' | 'fade-left' | 'fade-right' | 'scale'
  /** How much of the element needs to be visible */
  threshold?: number
  /** Only animate once */
  once?: boolean
  /** Additional className */
  className?: string
}

const staggerContainerVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0,
    },
  },
}

export function StaggerReveal({
  children,
  staggerDelay = 0.08,
  baseDelay = 0,
  variant = 'fade-up',
  threshold = 0.1,
  once = true,
  className = '',
}: StaggerRevealProps) {
  const ref = useRef<HTMLDivElement>(null)
  const isInView = useInView(ref, { amount: threshold, once })
  const shouldReduceMotion = useReducedMotion()

  if (shouldReduceMotion) {
    return <div ref={ref} className={className}>{children}</div>
  }

  const containerVariants: Variants = {
    hidden: {},
    visible: {
      transition: {
        staggerChildren: staggerDelay,
        delayChildren: baseDelay,
      },
    },
  }

  return (
    <motion.div
      ref={ref}
      initial="hidden"
      animate={isInView ? 'visible' : 'hidden'}
      variants={containerVariants}
      className={className}
    >
      {children}
    </motion.div>
  )
}

/**
 * StaggerItem - Individual item within StaggerReveal
 */
export interface StaggerItemProps {
  children: ReactNode
  /** Animation variant */
  variant?: 'fade' | 'fade-up' | 'fade-left' | 'fade-right' | 'scale'
  /** Duration override */
  duration?: number
  /** Additional className */
  className?: string
}

export function StaggerItem({
  children,
  variant = 'fade-up',
  duration = 0.5,
  className = '',
}: StaggerItemProps) {
  const shouldReduceMotion = useReducedMotion()

  if (shouldReduceMotion) {
    return <div className={className}>{children}</div>
  }

  return (
    <motion.div
      variants={revealVariants[variant]}
      transition={{
        duration,
        ease: TIMING.fashion,
      }}
      className={className}
    >
      {children}
    </motion.div>
  )
}

/**
 * HoverCard - Card component with elegant hover animations
 *
 * Provides lift, scale, and shadow effects on hover
 */
export interface HoverCardProps {
  children: ReactNode
  /** Scale amount on hover */
  scale?: number
  /** Lift amount (Y translate in pixels) */
  lift?: number
  /** Additional className */
  className?: string
  /** Optional onClick handler */
  onClick?: () => void
}

export function HoverCard({
  children,
  scale = 1.02,
  lift = -4,
  className = '',
  onClick,
}: HoverCardProps) {
  const shouldReduceMotion = useReducedMotion()

  if (shouldReduceMotion) {
    return (
      <div className={className} onClick={onClick}>
        {children}
      </div>
    )
  }

  return (
    <motion.div
      className={className}
      onClick={onClick}
      whileHover={{
        scale,
        y: lift,
        transition: {
          duration: 0.3,
          ease: TIMING.fashion,
        },
      }}
      whileTap={{
        scale: 0.98,
        transition: {
          duration: 0.15,
        },
      }}
    >
      {children}
    </motion.div>
  )
}

/**
 * ParallaxReveal - Subtle parallax effect on scroll
 */
export interface ParallaxRevealProps {
  children: ReactNode
  /** Offset amount (positive = slower than scroll, negative = faster) */
  offset?: number
  /** Additional className */
  className?: string
}

export function ParallaxReveal({
  children,
  offset = 30,
  className = '',
}: ParallaxRevealProps) {
  const ref = useRef<HTMLDivElement>(null)
  const [scrollY, setScrollY] = useState(0)
  const shouldReduceMotion = useReducedMotion()

  useEffect(() => {
    if (shouldReduceMotion) return

    const handleScroll = () => {
      if (!ref.current) return
      const rect = ref.current.getBoundingClientRect()
      const windowHeight = window.innerHeight
      const elementTop = rect.top
      const elementHeight = rect.height

      // Calculate how far through the viewport the element is
      const progress = (windowHeight - elementTop) / (windowHeight + elementHeight)
      setScrollY(progress * offset - offset / 2)
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    handleScroll()

    return () => window.removeEventListener('scroll', handleScroll)
  }, [offset, shouldReduceMotion])

  if (shouldReduceMotion) {
    return <div ref={ref} className={className}>{children}</div>
  }

  return (
    <div ref={ref} className={className}>
      <motion.div
        style={{ y: scrollY }}
        transition={{ type: 'tween', ease: 'linear' }}
      >
        {children}
      </motion.div>
    </div>
  )
}

/**
 * TextReveal - Character or word-by-word text reveal animation
 */
export interface TextRevealProps {
  children: string
  /** Animate by 'word' or 'character' */
  by?: 'word' | 'character'
  /** Delay between each unit */
  staggerDelay?: number
  /** Additional className */
  className?: string
  /** Only animate once */
  once?: boolean
}

export function TextReveal({
  children,
  by = 'word',
  staggerDelay = 0.03,
  className = '',
  once = true,
}: TextRevealProps) {
  const ref = useRef<HTMLSpanElement>(null)
  const isInView = useInView(ref, { amount: 0.5, once })
  const shouldReduceMotion = useReducedMotion()

  const units = by === 'word' ? children.split(' ') : children.split('')

  if (shouldReduceMotion) {
    return <span ref={ref} className={className}>{children}</span>
  }

  return (
    <span ref={ref} className={className} aria-label={children}>
      {units.map((unit, i) => (
        <motion.span
          key={i}
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{
            duration: 0.4,
            delay: i * staggerDelay,
            ease: TIMING.fashion,
          }}
          style={{ display: 'inline-block', whiteSpace: by === 'word' ? 'pre' : 'normal' }}
          aria-hidden="true"
        >
          {unit}{by === 'word' && i < units.length - 1 ? ' ' : ''}
        </motion.span>
      ))}
    </span>
  )
}

/**
 * FloatingElement - Subtle floating animation for decorative elements
 */
export interface FloatingElementProps {
  children: ReactNode
  /** Amplitude of float (pixels) */
  amplitude?: number
  /** Duration of one cycle (seconds) */
  duration?: number
  /** Additional className */
  className?: string
}

export function FloatingElement({
  children,
  amplitude = 10,
  duration = 4,
  className = '',
}: FloatingElementProps) {
  const shouldReduceMotion = useReducedMotion()

  if (shouldReduceMotion) {
    return <div className={className}>{children}</div>
  }

  return (
    <motion.div
      className={className}
      animate={{
        y: [0, -amplitude, 0],
      }}
      transition={{
        duration,
        repeat: Infinity,
        repeatType: 'loop',
        ease: 'easeInOut',
      }}
    >
      {children}
    </motion.div>
  )
}
