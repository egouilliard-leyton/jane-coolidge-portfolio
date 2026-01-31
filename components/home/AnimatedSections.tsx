// components/home/AnimatedSections.tsx
'use client'

import { type ReactNode } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { motion, useReducedMotion } from 'motion/react'
import { ScrollReveal, StaggerReveal, StaggerItem } from '@/components/ui/animations'
import { urlFor } from '@/sanity/lib/image'
import type { BlogPostListItem, ProjectListItem } from '@/sanity/lib/queries'

/**
 * Animated Homepage Sections
 *
 * Client components that wrap homepage content with scroll-triggered
 * animations and hover effects. All animations respect prefers-reduced-motion.
 */

// Elegant timing curve (typed as tuple for Motion compatibility)
const TIMING: [number, number, number, number] = [0.25, 0.1, 0.25, 1]

/**
 * AnimatedHeroContent - Staggered reveal for hero text
 */
export function AnimatedHeroContent({
  heading,
  subheading,
}: {
  heading: string
  subheading?: string
}) {
  const shouldReduceMotion = useReducedMotion()

  if (shouldReduceMotion) {
    return (
      <div className="max-w-3xl">
        <h1 className="font-display text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-white tracking-tight leading-[1.1] mb-6">
          {heading}
        </h1>
        {subheading && (
          <p className="text-lg sm:text-xl md:text-2xl text-white/85 font-light leading-relaxed max-w-2xl">
            {subheading}
          </p>
        )}
        <div className="mt-12 md:mt-16">
          <div className="flex items-center gap-3 text-white/60 text-sm tracking-widest uppercase">
            <span className="w-12 h-px bg-white/40" aria-hidden="true" />
            <span>Scroll to explore</span>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-3xl">
      <motion.h1
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: TIMING }}
        className="font-display text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-white tracking-tight leading-[1.1] mb-6"
      >
        {heading}
      </motion.h1>

      {subheading && (
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.15, ease: TIMING }}
          className="text-lg sm:text-xl md:text-2xl text-white/85 font-light leading-relaxed max-w-2xl"
        >
          {subheading}
        </motion.p>
      )}

      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3, ease: TIMING }}
        className="mt-12 md:mt-16"
      >
        <div className="flex items-center gap-3 text-white/60 text-sm tracking-widest uppercase">
          <motion.span
            initial={{ width: 0 }}
            animate={{ width: 48 }}
            transition={{ duration: 0.5, delay: 0.5, ease: TIMING }}
            className="h-px bg-white/40"
            aria-hidden="true"
          />
          <span>Scroll to explore</span>
        </div>
      </motion.div>
    </div>
  )
}

/**
 * AnimatedIntroSection - Scroll-triggered intro content
 */
export function AnimatedIntroSection({
  children,
}: {
  children: ReactNode
}) {
  return (
    <ScrollReveal variant="fade-up" duration={0.7} delay={0.1}>
      <div className="max-w-3xl mx-auto">
        {/* Decorative Element */}
        <ScrollReveal variant="fade-right" delay={0.2} duration={0.5}>
          <div className="mb-10 flex items-center gap-4" aria-hidden="true">
            <div className="w-16 h-px bg-brand-400" />
            <span className="text-brand-500 text-sm tracking-[0.3em] uppercase font-medium">
              Welcome
            </span>
          </div>
        </ScrollReveal>

        {/* Introduction Content */}
        <ScrollReveal variant="fade-up" delay={0.3} duration={0.6}>
          {children}
        </ScrollReveal>
      </div>
    </ScrollReveal>
  )
}

/**
 * AnimatedPostCard - Blog post card with hover animations
 */
export function AnimatedPostCard({
  post,
  index,
}: {
  post: BlogPostListItem
  index: number
}) {
  const shouldReduceMotion = useReducedMotion()

  const cardContent = (
    <Link href={`/blog/${post.slug}`} className="block">
      {/* Post Image */}
      <div className="aspect-[4/5] relative overflow-hidden bg-neutral-200 dark:bg-neutral-800 mb-6">
        {post.coverImage?.asset?.url ? (
          <Image
            src={urlFor(post.coverImage).width(600).height(750).quality(85).auto('format').url()}
            alt={post.coverImage.alt || post.title}
            fill
            loading={index < 3 ? 'eager' : 'lazy'}
            className="object-cover transition-transform duration-700 ease-out group-hover:scale-105"
            sizes="(max-width: 768px) 100vw, 33vw"
            placeholder={post.coverImage.asset.metadata?.lqip ? 'blur' : undefined}
            blurDataURL={post.coverImage.asset.metadata?.lqip}
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-brand-200 to-brand-100" />
        )}

        {/* Image Overlay on Hover */}
        <div
          className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-500"
          aria-hidden="true"
        />
      </div>

      {/* Post Content */}
      <div>
        {/* Tags */}
        {post.tags && post.tags.length > 0 && (
          <div className="mb-3">
            <span className="text-xs tracking-widest uppercase text-brand-600 dark:text-brand-400 font-medium">
              {post.tags[0]}
            </span>
          </div>
        )}

        {/* Title */}
        <h3 className="font-display text-xl md:text-2xl text-neutral-900 dark:text-neutral-100 mb-3 group-hover:text-brand-700 dark:group-hover:text-brand-400 transition-colors duration-300">
          {post.title}
        </h3>

        {/* Excerpt */}
        {post.excerpt && (
          <p className="text-neutral-600 dark:text-neutral-400 line-clamp-2 leading-relaxed">
            {post.excerpt}
          </p>
        )}

        {/* Date */}
        {post.publishedAt && (
          <time
            dateTime={post.publishedAt}
            className="mt-4 block text-sm text-neutral-500 dark:text-neutral-500"
          >
            {new Date(post.publishedAt).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </time>
        )}
      </div>
    </Link>
  )

  if (shouldReduceMotion) {
    return <article className="group">{cardContent}</article>
  }

  return (
    <motion.article
      className="group"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{
        duration: 0.6,
        delay: index * 0.1,
        ease: TIMING,
      }}
      whileHover={{
        y: -8,
        transition: { duration: 0.3, ease: TIMING },
      }}
    >
      {cardContent}
    </motion.article>
  )
}

/**
 * AnimatedProjectCard - Project card with hover reveal
 */
export function AnimatedProjectCard({
  project,
  index,
  isLarge = false,
}: {
  project: ProjectListItem
  index: number
  isLarge?: boolean
}) {
  const shouldReduceMotion = useReducedMotion()

  const cardContent = (
    <Link href={`/projects/${project.slug}`} className="block relative">
      {/* Project Image */}
      <div
        className={`
          relative overflow-hidden bg-neutral-200 dark:bg-neutral-800
          ${isLarge ? 'aspect-[3/4]' : 'aspect-[4/3]'}
        `}
      >
        {project.coverImage?.asset?.url ? (
          <Image
            src={urlFor(project.coverImage)
              .width(isLarge ? 800 : 600)
              .height(isLarge ? 1067 : 450)
              .quality(85)
              .auto('format')
              .url()}
            alt={project.title}
            fill
            loading={index < 2 ? 'eager' : 'lazy'}
            className="object-cover transition-transform duration-700 ease-out group-hover:scale-105"
            sizes={isLarge ? '(max-width: 768px) 100vw, 50vw' : '(max-width: 768px) 100vw, 25vw'}
            placeholder={project.coverImage.asset.metadata?.lqip ? 'blur' : undefined}
            blurDataURL={project.coverImage.asset.metadata?.lqip}
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-brand-300 to-brand-100" />
        )}

        {/* Hover Overlay with Content */}
        <div
          className="
            absolute inset-0
            bg-gradient-to-t from-black/80 via-black/40 to-transparent
            opacity-0 group-hover:opacity-100
            transition-opacity duration-500
            flex flex-col justify-end p-6 md:p-8
          "
        >
          {/* Category Badge */}
          {project.category && (
            <span className="inline-block self-start mb-3 px-3 py-1 bg-white/90 text-neutral-900 text-xs tracking-widest uppercase font-medium rounded-full">
              {project.category}
            </span>
          )}

          {/* Title */}
          <h3 className="font-display text-2xl md:text-3xl text-white tracking-tight">
            {project.title}
          </h3>
        </div>
      </div>

      {/* Mobile-visible content (hidden on hover-capable devices) */}
      <div className="mt-4 md:hidden">
        {project.category && (
          <span className="text-xs tracking-widest uppercase text-brand-600 font-medium mb-2 block">
            {project.category}
          </span>
        )}
        <h3 className="font-display text-xl text-neutral-900 dark:text-neutral-100">
          {project.title}
        </h3>
      </div>
    </Link>
  )

  if (shouldReduceMotion) {
    return (
      <article className={`group ${isLarge ? 'md:row-span-2' : ''}`}>
        {cardContent}
      </article>
    )
  }

  return (
    <motion.article
      className={`group ${isLarge ? 'md:row-span-2' : ''}`}
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-80px' }}
      transition={{
        duration: 0.7,
        delay: index * 0.12,
        ease: TIMING,
      }}
      whileHover={{
        scale: 1.02,
        transition: { duration: 0.35, ease: TIMING },
      }}
    >
      {cardContent}
    </motion.article>
  )
}

/**
 * AnimatedSectionHeader - Section header with scroll reveal
 */
export function AnimatedSectionHeader({
  label,
  title,
  align = 'left',
  showLink,
  linkHref,
  linkText,
}: {
  label: string
  title: string
  align?: 'left' | 'center'
  showLink?: boolean
  linkHref?: string
  linkText?: string
}) {
  const shouldReduceMotion = useReducedMotion()

  const content = (
    <>
      <div className={align === 'center' ? 'text-center' : ''}>
        <ScrollReveal variant="fade-up" delay={0.05}>
          <span className="text-brand-500 text-sm tracking-[0.3em] uppercase font-medium mb-4 block">
            {label}
          </span>
        </ScrollReveal>
        <ScrollReveal variant="fade-up" delay={0.15}>
          <h2 className="font-display text-3xl md:text-4xl lg:text-5xl text-neutral-900 dark:text-neutral-100 tracking-tight">
            {title}
          </h2>
        </ScrollReveal>
      </div>
      {showLink && linkHref && (
        <ScrollReveal variant="fade-left" delay={0.25}>
          <Link
            href={linkHref}
            className="group inline-flex items-center gap-2 text-sm font-medium text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors"
          >
            {linkText}
            <svg
              className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </Link>
        </ScrollReveal>
      )}
    </>
  )

  if (align === 'center') {
    return (
      <header className="mb-16 md:mb-20 text-center">
        {content}
        {align === 'center' && (
          <ScrollReveal variant="scale" delay={0.25}>
            <div className="w-24 h-px bg-brand-400 mx-auto mt-6" aria-hidden="true" />
          </ScrollReveal>
        )}
      </header>
    )
  }

  return (
    <header className="mb-16 md:mb-20">
      <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-6">
        {content}
      </div>
    </header>
  )
}

/**
 * AnimatedCTA - Call-to-action section with reveal animation
 */
export function AnimatedCTA({
  label,
  title,
  link,
}: {
  label: string
  title: string
  link: string
}) {
  const shouldReduceMotion = useReducedMotion()

  const content = (
    <Link href={link} className="group inline-block">
      <span className="text-brand-400 text-sm tracking-[0.3em] uppercase font-medium mb-6 block">
        {label}
      </span>
      <h2 className="font-display text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-white tracking-tight leading-[1.1] mb-8">
        {title}
      </h2>
      <div className="inline-flex items-center gap-3 text-white/80 group-hover:text-white transition-colors">
        <span className="text-lg font-medium">Let's Collaborate</span>
        <svg
          className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
        </svg>
      </div>
    </Link>
  )

  if (shouldReduceMotion) {
    return <div className="relative z-10">{content}</div>
  }

  return (
    <motion.div
      className="relative z-10"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.8, ease: TIMING }}
    >
      {content}
    </motion.div>
  )
}
