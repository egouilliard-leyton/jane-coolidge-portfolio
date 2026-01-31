// components/home/HomePageClient.tsx
'use client'

import Image from 'next/image'
import Link from 'next/link'
import { PortableText, type PortableTextBlock } from '@portabletext/react'
import { motion, useReducedMotion } from 'motion/react'

import { urlFor } from '@/sanity/lib/image'
import { ScrollReveal, StaggerReveal, StaggerItem } from '@/components/ui/animations'
import {
  AnimatedHeroContent,
  AnimatedPostCard,
  AnimatedProjectCard,
  AnimatedSectionHeader,
  AnimatedCTA,
} from './AnimatedSections'
import type {
  HomepageResult,
  BlogPostListItem,
  ProjectListItem,
} from '@/sanity/lib/queries'

interface HomePageClientProps {
  homepage: HomepageResult | null
  featuredPosts: BlogPostListItem[]
  featuredProjects: ProjectListItem[]
}

/**
 * HomePageClient
 *
 * Client component that renders the homepage with scroll-triggered
 * animations and hover effects. All animations respect prefers-reduced-motion.
 */
export default function HomePageClient({
  homepage,
  featuredPosts,
  featuredProjects,
}: HomePageClientProps) {
  const shouldReduceMotion = useReducedMotion()

  return (
    <article>
      {/* ============================================
          HERO SECTION
          Full-viewport height with dramatic imagery
          ============================================ */}
      <section className="relative h-[100svh] min-h-[600px] flex items-end" aria-label="Hero">
        {/* Hero Background Image */}
        {homepage?.heroImage?.asset?.url ? (
          <Image
            src={urlFor(homepage.heroImage).width(1920).height(1080).quality(90).auto('format').url()}
            alt=""
            fill
            priority
            fetchPriority="high"
            className="object-cover"
            placeholder={homepage.heroImage.asset.metadata?.lqip ? 'blur' : undefined}
            blurDataURL={homepage.heroImage.asset.metadata?.lqip}
            sizes="100vw"
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-brand-100 via-brand-50 to-neutral-100" />
        )}

        {/* Gradient Overlay - Editorial style fade */}
        <div
          className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"
          aria-hidden="true"
        />

        {/* Hero Content */}
        <div className="relative z-10 w-full pb-16 md:pb-24 lg:pb-32">
          <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
            <AnimatedHeroContent
              heading={homepage?.heroHeading || 'Fashion Forward'}
              subheading={homepage?.heroSubheading}
            />
          </div>
        </div>
      </section>

      {/* ============================================
          INTRODUCTION SECTION
          Rich text content in elegant container
          ============================================ */}
      {homepage?.introText && Array.isArray(homepage.introText) && homepage.introText.length > 0 && (
        <section className="py-24 md:py-32 lg:py-40" aria-labelledby="intro-heading">
          <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
            <div className="max-w-3xl mx-auto">
              {/* Decorative Element */}
              <ScrollReveal variant="fade-right" delay={0.1} duration={0.5}>
                <div className="mb-10 flex items-center gap-4" aria-hidden="true">
                  <div className="w-16 h-px bg-brand-400" />
                  <span className="text-brand-500 text-sm tracking-[0.3em] uppercase font-medium">
                    Welcome
                  </span>
                </div>
              </ScrollReveal>

              {/* Introduction Content */}
              <ScrollReveal variant="fade-up" delay={0.2} duration={0.7}>
                <div className="prose prose-xl prose-neutral dark:prose-invert max-w-none">
                  <div className="font-serif text-xl md:text-2xl lg:text-3xl leading-relaxed text-neutral-700 dark:text-neutral-300 [&>p:first-child]:first-letter:text-5xl [&>p:first-child]:first-letter:font-display [&>p:first-child]:first-letter:float-left [&>p:first-child]:first-letter:mr-3 [&>p:first-child]:first-letter:mt-1 [&>p:first-child]:first-letter:text-brand-600 dark:[&>p:first-child]:first-letter:text-brand-400">
                    <PortableText value={homepage.introText as PortableTextBlock[]} />
                  </div>
                </div>
              </ScrollReveal>
            </div>
          </div>
        </section>
      )}

      {/* ============================================
          FEATURED POSTS SECTION
          Editorial grid with hover effects
          ============================================ */}
      {featuredPosts && featuredPosts.length > 0 && (
        <section
          className="py-24 md:py-32 bg-neutral-50 dark:bg-neutral-950"
          aria-labelledby="posts-heading"
        >
          <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
            {/* Section Header */}
            <AnimatedSectionHeader
              label="From the Journal"
              title={homepage?.featuredPostsHeading || 'Latest Stories'}
              showLink
              linkHref="/blog"
              linkText="View all articles"
            />

            {/* Posts Grid */}
            <div className="grid md:grid-cols-3 gap-8 lg:gap-10">
              {featuredPosts.map((post, index) => (
                <AnimatedPostCard key={post._id} post={post} index={index} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ============================================
          FEATURED PROJECTS SECTION
          Masonry-inspired gallery with category badges
          ============================================ */}
      {featuredProjects && featuredProjects.length > 0 && (
        <section className="py-24 md:py-32" aria-labelledby="projects-heading">
          <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
            {/* Section Header */}
            <AnimatedSectionHeader
              label="Portfolio"
              title={homepage?.featuredProjectsHeading || 'Selected Work'}
              align="center"
            />

            {/* Projects Grid - Asymmetric Layout */}
            <div className="grid md:grid-cols-2 gap-6 lg:gap-8">
              {featuredProjects.map((project, index) => (
                <AnimatedProjectCard
                  key={project._id}
                  project={project}
                  index={index}
                  isLarge={index === 0}
                />
              ))}
            </div>

            {/* View All Link */}
            <ScrollReveal variant="fade-up" delay={0.3}>
              <div className="mt-12 md:mt-16 text-center">
                <Link
                  href="/projects"
                  className="
                    inline-flex items-center gap-3
                    px-8 py-4
                    border-2 border-neutral-900 dark:border-neutral-100
                    text-neutral-900 dark:text-neutral-100
                    font-medium tracking-wide
                    transition-all duration-300
                    hover:bg-neutral-900 hover:text-white
                    dark:hover:bg-neutral-100 dark:hover:text-neutral-900
                    focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
                    group
                  "
                >
                  <span>View All Projects</span>
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
              </div>
            </ScrollReveal>
          </div>
        </section>
      )}

      {/* ============================================
          CTA SECTION
          Full-width call to action
          ============================================ */}
      {homepage?.ctaText && homepage?.ctaLink && (
        <section
          className="relative py-32 md:py-40 lg:py-48 bg-neutral-900 dark:bg-black overflow-hidden"
          aria-label="Call to action"
        >
          {/* Background Decoration */}
          <div
            className="absolute inset-0 opacity-5"
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
            }}
            aria-hidden="true"
          />

          {/* Gradient Accent */}
          <div
            className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-brand-500/20 rounded-full blur-[120px]"
            aria-hidden="true"
          />

          <div className="relative z-10 mx-auto max-w-4xl px-6 md:px-8 lg:px-12 text-center">
            <AnimatedCTA
              label="Get in Touch"
              title={homepage.ctaText}
              link={homepage.ctaLink}
            />
          </div>
        </section>
      )}
    </article>
  )
}
