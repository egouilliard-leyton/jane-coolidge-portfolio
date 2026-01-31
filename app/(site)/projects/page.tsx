// app/(site)/projects/page.tsx
import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

import { sanityFetch } from '@/sanity/lib/client'
import { urlFor } from '@/sanity/lib/image'
import {
  projectsQuery,
  projectCountByCategoryQuery,
  siteSettingsQuery,
  type ProjectListItem,
  type ProjectCategoryCountsResult,
  type SiteSettingsResult,
} from '@/sanity/lib/queries'
import type { ProjectCategory } from '@/types/sanity'

/**
 * Project category display names and metadata
 */
const CATEGORY_CONFIG: Record<ProjectCategory, { label: string; description: string }> = {
  editorial: { label: 'Editorial', description: 'Fashion editorial and magazine work' },
  campaign: { label: 'Campaign', description: 'Advertising and brand campaigns' },
  lookbook: { label: 'Lookbook', description: 'Seasonal lookbooks and collections' },
  styling: { label: 'Styling', description: 'Personal and celebrity styling' },
  personal: { label: 'Personal', description: 'Personal projects and creative explorations' },
}

const SHOW_FILTER_THRESHOLD = 5

interface ProjectsPageProps {
  searchParams: Promise<{ category?: string }>
}

/**
 * Generate metadata for the projects listing page
 */
export async function generateMetadata(): Promise<Metadata> {
  const settings = await sanityFetch<SiteSettingsResult | null>({
    query: siteSettingsQuery,
    tags: ['siteSettings'],
  })

  return {
    title: `Portfolio | ${settings?.siteName || 'Fashion Portfolio'}`,
    description: 'Explore a curated collection of fashion styling, editorial, and creative direction projects.',
    openGraph: {
      title: `Portfolio | ${settings?.siteName || 'Fashion Portfolio'}`,
      description: 'Explore a curated collection of fashion styling, editorial, and creative direction projects.',
    },
  }
}

/**
 * Projects Gallery Page - Server Component
 *
 * Displays a sophisticated masonry-inspired grid of projects with
 * elegant hover interactions, category filtering, and responsive layout.
 * Embodies a high-fashion editorial aesthetic with attention to typography
 * and visual hierarchy.
 */
export default async function ProjectsPage({ searchParams }: ProjectsPageProps) {
  const params = await searchParams
  const activeCategory = params.category as ProjectCategory | undefined

  // Fetch projects and category counts in parallel
  const [allProjects, categoryCounts] = await Promise.all([
    sanityFetch<ProjectListItem[]>({
      query: projectsQuery,
      tags: ['project'],
    }),
    sanityFetch<ProjectCategoryCountsResult>({
      query: projectCountByCategoryQuery,
      tags: ['project'],
    }),
  ])

  // Filter projects by category if specified
  const projects = activeCategory
    ? allProjects.filter((project) => project.category === activeCategory)
    : allProjects

  // Determine if we should show the category filter
  const showFilter = categoryCounts.all > SHOW_FILTER_THRESHOLD

  // Get active categories (ones that have projects)
  const activeCategories = (Object.keys(CATEGORY_CONFIG) as ProjectCategory[]).filter(
    (cat) => categoryCounts[cat] > 0
  )

  return (
    <article className="min-h-screen">
      {/* ============================================
          PAGE HEADER
          Editorial-style header with dramatic typography
          ============================================ */}
      <header className="relative py-20 md:py-28 lg:py-36 overflow-hidden">
        {/* Subtle grid pattern background */}
        <div
          className="absolute inset-0 opacity-[0.02] dark:opacity-[0.04]"
          style={{
            backgroundImage: `linear-gradient(to right, currentColor 1px, transparent 1px),
                             linear-gradient(to bottom, currentColor 1px, transparent 1px)`,
            backgroundSize: '80px 80px',
          }}
          aria-hidden="true"
        />

        {/* Floating accent element */}
        <div
          className="absolute -right-20 top-1/2 -translate-y-1/2 w-96 h-96 bg-brand-200/20 dark:bg-brand-800/10 rounded-full blur-3xl"
          aria-hidden="true"
        />

        <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
          <div className="max-w-3xl">
            {/* Section label with decorative line */}
            <div className="mb-6 flex items-center gap-4 animate-fade-up">
              <div className="w-12 h-px bg-brand-400" aria-hidden="true" />
              <span className="text-brand-500 text-xs tracking-[0.4em] uppercase font-medium">
                Portfolio
              </span>
            </div>

            {/* Main heading - dramatic serif */}
            <h1 className="font-display text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-neutral-900 dark:text-neutral-100 tracking-tight leading-[1.1] mb-6 animate-fade-up animation-delay-100">
              Selected Work
            </h1>

            {/* Subtitle */}
            <p className="text-lg md:text-xl text-neutral-600 dark:text-neutral-400 leading-relaxed max-w-xl animate-fade-up animation-delay-200">
              A curated collection of fashion editorial, campaigns, and styling projects that define my creative vision.
            </p>
          </div>
        </div>
      </header>

      {/* ============================================
          CATEGORY FILTER
          Elegant pill-style filter tabs
          ============================================ */}
      {showFilter && activeCategories.length > 1 && (
        <nav
          className="sticky top-0 z-20 bg-white/80 dark:bg-neutral-950/80 backdrop-blur-md border-b border-neutral-100 dark:border-neutral-900"
          aria-label="Project categories"
        >
          <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
            <div className="py-4 md:py-5 overflow-x-auto hide-scrollbar">
              <div className="flex items-center gap-2 md:gap-3 min-w-max">
                {/* All projects filter */}
                <CategoryFilterButton
                  href="/projects"
                  isActive={!activeCategory}
                  label="All"
                  count={categoryCounts.all}
                />

                {/* Category filters */}
                {activeCategories.map((category) => (
                  <CategoryFilterButton
                    key={category}
                    href={`/projects?category=${category}`}
                    isActive={activeCategory === category}
                    label={CATEGORY_CONFIG[category].label}
                    count={categoryCounts[category]}
                  />
                ))}
              </div>
            </div>
          </div>
        </nav>
      )}

      {/* ============================================
          PROJECTS GRID
          Responsive masonry-inspired gallery
          ============================================ */}
      <section className="py-16 md:py-24" aria-label="Projects gallery">
        <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
          {projects && projects.length > 0 ? (
            <>
              {/* Active category description */}
              {activeCategory && (
                <div className="mb-10 md:mb-14 animate-fade-up">
                  <p className="text-neutral-600 dark:text-neutral-400 text-lg max-w-2xl">
                    {CATEGORY_CONFIG[activeCategory].description}
                  </p>
                </div>
              )}

              {/* Projects Grid */}
              <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
                {projects.map((project, index) => (
                  <ProjectCard key={project._id} project={project} index={index} />
                ))}
              </div>

              {/* Results count */}
              <div className="mt-16 md:mt-20 text-center">
                <p className="text-sm text-neutral-500 dark:text-neutral-500 tracking-wide">
                  {projects.length} {projects.length === 1 ? 'project' : 'projects'}
                  {activeCategory && ` in ${CATEGORY_CONFIG[activeCategory].label.toLowerCase()}`}
                </p>
              </div>
            </>
          ) : (
            /* Empty State */
            <EmptyState activeCategory={activeCategory} />
          )}
        </div>
      </section>
    </article>
  )
}

/**
 * Category Filter Button Component
 *
 * Elegant pill-style button for category navigation.
 */
function CategoryFilterButton({
  href,
  isActive,
  label,
  count,
}: {
  href: string
  isActive: boolean
  label: string
  count: number
}) {
  return (
    <Link
      href={href}
      className={`
        inline-flex items-center gap-2 px-4 py-2 md:px-5 md:py-2.5
        text-sm font-medium tracking-wide
        transition-all duration-300 ease-out
        ${
          isActive
            ? 'bg-neutral-900 dark:bg-neutral-100 text-white dark:text-neutral-900'
            : 'bg-neutral-100 dark:bg-neutral-900 text-neutral-600 dark:text-neutral-400 hover:bg-neutral-200 dark:hover:bg-neutral-800 hover:text-neutral-900 dark:hover:text-neutral-100'
        }
      `}
      aria-current={isActive ? 'page' : undefined}
    >
      <span>{label}</span>
      <span
        className={`
          text-xs tabular-nums
          ${isActive ? 'text-white/70 dark:text-neutral-900/70' : 'text-neutral-400 dark:text-neutral-600'}
        `}
      >
        {count}
      </span>
    </Link>
  )
}

/**
 * Project Card Component
 *
 * Sophisticated card with cover image and reveal-on-hover metadata.
 * Features elegant transitions and visual hierarchy appropriate
 * for a high-fashion portfolio.
 */
function ProjectCard({ project, index }: { project: ProjectListItem; index: number }) {
  // Calculate stagger delay for animation (max 600ms)
  const delayClass = `animation-delay-${Math.min(Math.floor(index / 3) * 100, 300)}`

  // Format the date for display
  const formattedDate = project.date
    ? new Date(project.date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
      })
    : null

  return (
    <article className={`group animate-fade-up ${delayClass}`}>
      <Link href={`/projects/${project.slug}`} className="block">
        {/* Project Image Container */}
        <div className="relative aspect-[3/4] overflow-hidden bg-neutral-100 dark:bg-neutral-900">
          {project.coverImage?.asset?.url ? (
            <Image
              src={urlFor(project.coverImage).width(600).height(800).quality(85).auto('format').url()}
              alt={project.title}
              fill
              loading={index < 6 ? 'eager' : 'lazy'}
              className="object-cover transition-transform duration-700 ease-out group-hover:scale-105"
              sizes="(max-width: 768px) 50vw, (max-width: 1024px) 33vw, 33vw"
              placeholder={project.coverImage.asset.metadata?.lqip ? 'blur' : undefined}
              blurDataURL={project.coverImage.asset.metadata?.lqip}
            />
          ) : (
            <div className="absolute inset-0 bg-gradient-to-br from-brand-200 via-brand-100 to-neutral-100 dark:from-brand-950 dark:via-neutral-900 dark:to-neutral-950" />
          )}

          {/* Hover Overlay - Gradient reveal */}
          <div
            className="
              absolute inset-0
              bg-gradient-to-t from-black/70 via-black/20 to-transparent
              opacity-0 group-hover:opacity-100
              transition-opacity duration-500
            "
            aria-hidden="true"
          />

          {/* Hover Content - Project Details */}
          <div
            className="
              absolute inset-0 flex flex-col justify-end p-4 md:p-6
              opacity-0 group-hover:opacity-100
              transition-opacity duration-500 delay-75
            "
          >
            {/* Category Badge */}
            {project.category && (
              <span className="inline-block self-start mb-3 px-3 py-1 bg-white/90 dark:bg-white/90 text-neutral-900 text-xs tracking-widest uppercase font-medium">
                {CATEGORY_CONFIG[project.category]?.label || project.category}
              </span>
            )}

            {/* Project Title */}
            <h2 className="font-display text-xl md:text-2xl lg:text-3xl text-white tracking-tight leading-tight">
              {project.title}
            </h2>

            {/* Client & Date - Desktop only */}
            <div className="hidden md:flex items-center gap-3 mt-2 text-white/80 text-sm">
              {project.client && <span>{project.client}</span>}
              {project.client && formattedDate && (
                <span className="w-1 h-1 rounded-full bg-white/50" aria-hidden="true" />
              )}
              {formattedDate && <time dateTime={project.date}>{formattedDate}</time>}
            </div>
          </div>

          {/* View indicator - appears on hover */}
          <div
            className="
              absolute top-4 right-4 md:top-6 md:right-6
              opacity-0 group-hover:opacity-100
              transition-all duration-300 delay-100
              transform translate-y-2 group-hover:translate-y-0
            "
          >
            <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-white/90 dark:bg-white/90 flex items-center justify-center">
              <svg
                className="w-4 h-4 md:w-5 md:h-5 text-neutral-900"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </div>
          </div>
        </div>

        {/* Card Footer - Always visible metadata */}
        <div className="mt-4 space-y-1">
          {/* Title */}
          <h2 className="font-display text-base md:text-lg text-neutral-900 dark:text-neutral-100 group-hover:text-brand-700 dark:group-hover:text-brand-400 transition-colors duration-300 leading-tight">
            {project.title}
          </h2>

          {/* Metadata row */}
          <div className="flex items-center gap-2 text-sm text-neutral-500 dark:text-neutral-500">
            {project.category && (
              <span className="text-xs tracking-widest uppercase font-medium text-brand-600 dark:text-brand-400">
                {CATEGORY_CONFIG[project.category]?.label || project.category}
              </span>
            )}
            {project.category && (project.client || formattedDate) && (
              <span className="text-neutral-300 dark:text-neutral-700">·</span>
            )}
            {project.client && <span>{project.client}</span>}
            {project.client && formattedDate && (
              <span className="text-neutral-300 dark:text-neutral-700">·</span>
            )}
            {formattedDate && <time dateTime={project.date}>{formattedDate}</time>}
          </div>
        </div>
      </Link>
    </article>
  )
}

/**
 * Empty State Component
 *
 * Displayed when no projects exist or when a category filter
 * returns no results. Maintains the elegant, editorial aesthetic.
 */
function EmptyState({ activeCategory }: { activeCategory?: ProjectCategory }) {
  return (
    <div className="text-center py-16 md:py-24">
      {/* Decorative element */}
      <div className="mb-8 flex justify-center">
        <div className="w-24 h-24 rounded-full bg-neutral-100 dark:bg-neutral-900 flex items-center justify-center">
          <svg
            className="w-10 h-10 text-neutral-400 dark:text-neutral-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
            />
          </svg>
        </div>
      </div>

      {/* Message */}
      <h2 className="font-display text-2xl md:text-3xl text-neutral-900 dark:text-neutral-100 mb-4">
        {activeCategory ? 'No projects in this category' : 'Portfolio coming soon'}
      </h2>
      <p className="text-neutral-600 dark:text-neutral-400 max-w-md mx-auto mb-8">
        {activeCategory
          ? `There are no ${CATEGORY_CONFIG[activeCategory].label.toLowerCase()} projects to display yet. Check back soon or explore other categories.`
          : 'The portfolio is being curated. Check back soon to explore a collection of fashion styling and creative direction work.'}
      </p>

      {/* Action links */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
        {activeCategory ? (
          <Link
            href="/projects"
            className="
              inline-flex items-center gap-2
              px-6 py-3
              bg-neutral-900 dark:bg-neutral-100
              text-white dark:text-neutral-900
              font-medium tracking-wide
              transition-all duration-300
              hover:bg-neutral-800 dark:hover:bg-neutral-200
              focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
            "
          >
            View all projects
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </Link>
        ) : (
          <Link
            href="/"
            className="
              inline-flex items-center gap-2
              text-sm font-medium text-brand-600 dark:text-brand-400
              hover:text-brand-700 dark:hover:text-brand-300
              transition-colors
            "
          >
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
            </svg>
            Return to homepage
          </Link>
        )}
      </div>
    </div>
  )
}
