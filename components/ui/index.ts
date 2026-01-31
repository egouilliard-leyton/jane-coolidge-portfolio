// components/ui/index.ts
export { default as ImageWithPopup } from './ImageWithPopup'
export type { ImageWithPopupProps } from './ImageWithPopup'

// Accessibility
export { default as SkipLink } from './SkipLink'

// Animation components
export {
  ScrollReveal,
  StaggerReveal,
  StaggerItem,
  HoverCard,
  ParallaxReveal,
  TextReveal,
  FloatingElement,
} from './animations'
export type {
  ScrollRevealProps,
  StaggerRevealProps,
  StaggerItemProps,
  HoverCardProps,
  ParallaxRevealProps,
  TextRevealProps,
  FloatingElementProps,
} from './animations'

// Page transitions
export { default as PageTransition, FadeTransition, SlideTransition } from './PageTransition'
export type { PageTransitionProps, SlideTransitionProps } from './PageTransition'
