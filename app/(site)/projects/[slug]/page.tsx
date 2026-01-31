// app/(site)/projects/[slug]/page.tsx
import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import { notFound } from 'next/navigation'

import { sanityFetch } from '@/sanity/lib/client'
import { urlFor } from '@/sanity/lib/image'
import {
  projectBySlugQuery,
  projectSlugsQuery,
  siteSettingsQuery,
  adjacentProjectsQuery,
  type ProjectDetail,
  type SiteSettingsResult,
  type SlugItem,
  type AdjacentProjectsResult,
} from '@/sanity/lib/queries'
import { BlogContent } from '@/components/content'
import { ImageWithPopup } from '@/components/ui'
import type { PortableText as PortableTextType, ProjectCategory, PopupContent } from '@/types'

interface ProjectPageProps {
  params: Promise<{ slug: string }>
}

/**
 * Project category display names
 */
const CATEGORY_LABELS: Record<ProjectCategory, string> = {
  editorial: 'Editorial',
  campaign: 'Campaign',
  lookbook: 'Lookbook',
  styling: 'Styling',
  personal: 'Personal',
}

/**
 * Generate static params for all projects
 * Enables static site generation for each project
 */
export async function generateStaticParams(): Promise<{ slug: string }[]> {
  const slugs = await sanityFetch<SlugItem[]>({
    query: projectSlugsQuery,
    tags: ['project'],
  })

  return slugs.map((item) => ({
    slug: item.slug,
  }))
}

/**
 * Generate metadata for SEO
 * Uses project title, description, and cover image for OpenGraph
 */
export async function generateMetadata({
  params,
}: ProjectPageProps): Promise<Metadata> {
  const { slug } = await params

  const [project, settings] = await Promise.all([
    sanityFetch<ProjectDetail | null>({
      query: projectBySlugQuery,
      params: { slug },
      tags: ['project'],
    }),
    sanityFetch<SiteSettingsResult | null>({
      query: siteSettingsQuery,
      tags: ['siteSettings'],
    }),
  ])

  if (!project) {
    return {
      title: 'Project Not Found',
    }
  }

  const siteName = settings?.siteName || 'Fashion Portfolio'
  const title = project.seo?.metaTitle || project.title
  const description =
    project.seo?.metaDescription ||
    (project.client ? `${project.category ? CATEGORY_LABELS[project.category] + ' project' : 'Project'} for ${project.client}` : '')

  // Generate OG image URL
  let ogImage: string | undefined
  if (project.seo?.ogImage?.asset?.url) {
    ogImage = project.seo.ogImage.asset.url
  } else if (project.coverImage?.asset?.url) {
    ogImage = urlFor(project.coverImage).width(1200).height(630).quality(85).url()
  }

  return {
    title: `${title} | ${siteName}`,
    description,
    openGraph: {
      title,
      description,
      type: 'article',
      publishedTime: project.date,
      images: ogImage ? [{ url: ogImage, width: 1200, height: 630 }] : [],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: ogImage ? [ogImage] : [],
    },
  }
}

/**
 * Project Detail Page
 *
 * An immersive, gallery-focused layout for showcasing fashion projects.
 * Features:
 * - Full-width hero with cover image
 * - Elegant metadata display (category, client, date)
 * - Rich description with Portable Text
 * - Responsive masonry-inspired image gallery
 * - ImageWithPopup support for styling notes
 * - Adjacent project navigation
 */
export default async function ProjectPage({ params }: ProjectPageProps) {
  const { slug } = await params

  const [project, adjacentProjects] = await Promise.all([
    sanityFetch<ProjectDetail | null>({
      query: projectBySlugQuery,
      params: { slug },
      tags: ['project'],
    }),
    sanityFetch<AdjacentProjectsResult>({
      query: adjacentProjectsQuery,
      params: { date: new Date().toISOString(), slug },
      tags: ['project'],
    }),
  ])

  if (!project) {
    notFound()
  }

  // Format the date for display
  const formattedDate = project.date
    ? new Date(project.date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
      })
    : null

  // Get category label
  const categoryLabel = project.category
    ? CATEGORY_LABELS[project.category]
    : null

  return (
    <article className="min-h-screen">
      {/* ============================================
          HERO SECTION
          Full-width cover image with immersive presentation
          ============================================ */}
      <header className="relative">
        {/* Cover Image */}
        {project.coverImage?.asset?.url ? (
          <div className="relative aspect-[4/3] md:aspect-[21/9] lg:aspect-[3/1] overflow-hidden bg-neutral-100 dark:bg-neutral-900">
            <Image
              src={urlFor(project.coverImage)
                .width(2400)
                .height(900)
                .quality(90)
                .auto('format')
                .url()}
              alt={project.coverImage.alt || project.title}
              fill
              priority
              className="object-cover"
              sizes="100vw"
              placeholder={project.coverImage.asset.metadata?.lqip ? 'blur' : undefined}
              blurDataURL={project.coverImage.asset.metadata?.lqip}
            />
            {/* Gradient overlay for text legibility */}
            <div
              className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"
              aria-hidden="true"
            />
          </div>
        ) : (
          /* Fallback gradient when no cover image */
          <div className="relative aspect-[4/3] md:aspect-[21/9] lg:aspect-[3/1] bg-gradient-to-br from-brand-200 via-brand-100 to-neutral-100 dark:from-brand-950 dark:via-neutral-900 dark:to-neutral-950">
            {/* Decorative pattern */}
            <div
              className="absolute inset-0 opacity-[0.03] dark:opacity-[0.06]"
              style={{
                backgroundImage: `linear-gradient(45deg, currentColor 1px, transparent 1px),
                                 linear-gradient(-45deg, currentColor 1px, transparent 1px)`,
                backgroundSize: '60px 60px',
              }}
              aria-hidden="true"
            />
          </div>
        )}

        {/* Back Navigation - Floating over image */}
        <nav className="absolute top-6 left-6 md:top-8 md:left-8 lg:left-12 z-10">
          <Link
            href="/projects"
            className="
              inline-flex items-center gap-2
              px-4 py-2.5
              bg-white/90 dark:bg-neutral-900/90
              backdrop-blur-md
              rounded-full
              text-sm font-medium
              text-neutral-800 dark:text-neutral-200
              shadow-lg shadow-black/10
              transition-all duration-300
              hover:bg-white dark:hover:bg-neutral-800
              hover:shadow-xl
              focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
              group
            "
          >
            <svg
              className="w-4 h-4 transition-transform duration-300 group-hover:-translate-x-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
            </svg>
            <span>All Projects</span>
          </Link>
        </nav>
      </header>

      {/* ============================================
          PROJECT HEADER
          Title, metadata, and description
          ============================================ */}
      <div className="relative -mt-20 md:-mt-28 lg:-mt-36 z-10 pb-12 md:pb-16">
        <div className="mx-auto max-w-5xl px-6 md:px-8 lg:px-12">
          {/* Content card with elegant shadow */}
          <div className="bg-white dark:bg-neutral-950 rounded-t-3xl shadow-2xl shadow-black/10 pt-10 md:pt-14 lg:pt-16 px-6 md:px-12 lg:px-16">
            {/* Category Badge */}
            {categoryLabel && (
              <div className="mb-6 animate-fade-up">
                <span
                  className="
                    inline-block
                    px-4 py-2
                    text-xs tracking-[0.25em] uppercase font-medium
                    text-brand-700 dark:text-brand-300
                    bg-brand-50 dark:bg-brand-950/40
                    border border-brand-100 dark:border-brand-900/50
                    rounded-full
                  "
                >
                  {categoryLabel}
                </span>
              </div>
            )}

            {/* Title */}
            <h1 className="font-display text-3xl sm:text-4xl md:text-5xl lg:text-6xl text-neutral-900 dark:text-neutral-100 tracking-tight leading-[1.1] mb-8 animate-fade-up animation-delay-100">
              {project.title}
            </h1>

            {/* Metadata Row - Client & Date */}
            <div className="flex flex-wrap items-center gap-6 md:gap-8 text-sm md:text-base text-neutral-600 dark:text-neutral-400 animate-fade-up animation-delay-200">
              {/* Client */}
              {project.client && (
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center">
                    <svg
                      className="w-5 h-5 text-brand-500"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={1.5}
                      aria-hidden="true"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z"
                      />
                    </svg>
                  </div>
                  <div>
                    <span className="block text-xs uppercase tracking-wider text-neutral-400 dark:text-neutral-500 mb-0.5">
                      Client
                    </span>
                    <span className="font-medium text-neutral-900 dark:text-neutral-100">
                      {project.client}
                    </span>
                  </div>
                </div>
              )}

              {/* Date */}
              {formattedDate && (
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center">
                    <svg
                      className="w-5 h-5 text-brand-500"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={1.5}
                      aria-hidden="true"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5"
                      />
                    </svg>
                  </div>
                  <div>
                    <span className="block text-xs uppercase tracking-wider text-neutral-400 dark:text-neutral-500 mb-0.5">
                      Date
                    </span>
                    <time dateTime={project.date} className="font-medium text-neutral-900 dark:text-neutral-100">
                      {formattedDate}
                    </time>
                  </div>
                </div>
              )}
            </div>

            {/* Decorative divider */}
            <div className="mt-10 md:mt-14 flex items-center gap-4" aria-hidden="true">
              <div className="flex-1 h-px bg-gradient-to-r from-transparent via-neutral-200 dark:via-neutral-800 to-transparent" />
              <div className="w-2 h-2 rotate-45 bg-brand-400/60" />
              <div className="flex-1 h-px bg-gradient-to-r from-transparent via-neutral-200 dark:via-neutral-800 to-transparent" />
            </div>
          </div>
        </div>
      </div>

      {/* ============================================
          PROJECT DESCRIPTION
          Portable Text rendered with BlogContent component
          ============================================ */}
      {project.description && project.description.length > 0 && (
        <section className="pb-16 md:pb-20" aria-label="Project description">
          <div className="mx-auto max-w-5xl px-6 md:px-8 lg:px-12">
            <div className="bg-white dark:bg-neutral-950 shadow-2xl shadow-black/10 px-6 md:px-12 lg:px-16 py-10 md:py-14">
              <BlogContent
                content={project.description as PortableTextType}
                className="
                  prose-headings:font-display
                  prose-h2:text-2xl prose-h2:md:text-3xl
                  prose-h3:text-xl prose-h3:md:text-2xl
                  prose-p:text-neutral-700 dark:prose-p:text-neutral-300
                  prose-a:text-brand-700 dark:prose-a:text-brand-400
                  prose-strong:text-neutral-900 dark:prose-strong:text-neutral-100
                "
              />
            </div>
          </div>
        </section>
      )}

      {/* ============================================
          IMAGE GALLERY
          Responsive masonry-inspired grid with popup support
          ============================================ */}
      {project.images && project.images.length > 0 && (
        <section className="pb-20 md:pb-28" aria-label="Project gallery">
          <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
            {/* Section heading */}
            <div className="mb-10 md:mb-14">
              <div className="flex items-center gap-4 mb-4 animate-fade-up">
                <div className="w-12 h-px bg-brand-400" aria-hidden="true" />
                <span className="text-brand-500 text-xs tracking-[0.4em] uppercase font-medium">
                  Gallery
                </span>
              </div>
              <h2 className="font-display text-2xl md:text-3xl lg:text-4xl text-neutral-900 dark:text-neutral-100 tracking-tight animate-fade-up animation-delay-100">
                Project Images
              </h2>
            </div>

            {/* Gallery Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 lg:gap-10">
              {project.images.map((item, index) => {
                const imageUrl = item.image?.asset?.url
                if (!imageUrl) return null

                // Determine if image should span full width
                // Make every 3rd image (index 0, 3, 6...) full width for visual interest
                const isFullWidth = index % 3 === 0 && project.images && project.images.length > 2

                return (
                  <div
                    key={item._key || `image-${index}`}
                    className={`
                      animate-fade-up
                      ${isFullWidth ? 'md:col-span-2' : ''}
                    `}
                    style={{ animationDelay: `${Math.min(index * 100, 500)}ms` }}
                  >
                    <ImageWithPopup
                      image={{
                        url: urlFor(item.image!).width(isFullWidth ? 1600 : 900).quality(90).auto('format').url(),
                        _id: item.image?.asset?._id,
                        lqip: item.image?.asset?.metadata?.lqip,
                      }}
                      alt={item.alt || project.title}
                      caption={item.caption}
                      popup={item.popup as PopupContent | null | undefined}
                      size={isFullWidth ? 'full' : 'large'}
                      className="!my-0"
                      priority={index === 0}
                    />
                  </div>
                )
              })}
            </div>
          </div>
        </section>
      )}

      {/* ============================================
          ADJACENT PROJECT NAVIGATION
          Navigate to previous/next projects
          ============================================ */}
      <nav className="border-t border-neutral-200 dark:border-neutral-800" aria-label="Project navigation">
        <div className="mx-auto max-w-7xl">
          <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-neutral-200 dark:divide-neutral-800">
            {/* Previous Project */}
            <div className="group">
              {adjacentProjects?.previous ? (
                <Link
                  href={`/projects/${adjacentProjects.previous.slug}`}
                  className="flex items-center gap-6 p-8 md:p-12 transition-colors duration-300 hover:bg-neutral-50 dark:hover:bg-neutral-900/50"
                >
                  {/* Arrow */}
                  <div className="hidden sm:flex w-12 h-12 rounded-full bg-neutral-100 dark:bg-neutral-800 items-center justify-center transition-all duration-300 group-hover:bg-brand-100 dark:group-hover:bg-brand-900/30">
                    <svg
                      className="w-5 h-5 text-neutral-600 dark:text-neutral-400 transition-transform duration-300 group-hover:-translate-x-1"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={2}
                      aria-hidden="true"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
                    </svg>
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <span className="block text-xs uppercase tracking-wider text-neutral-400 dark:text-neutral-500 mb-2">
                      Previous Project
                    </span>
                    <span className="block font-display text-lg md:text-xl text-neutral-900 dark:text-neutral-100 truncate group-hover:text-brand-700 dark:group-hover:text-brand-400 transition-colors">
                      {adjacentProjects.previous.title}
                    </span>
                  </div>

                  {/* Thumbnail */}
                  {adjacentProjects.previous.coverImage?.asset?.url && (
                    <div className="hidden lg:block relative w-24 h-24 rounded-lg overflow-hidden bg-neutral-100 dark:bg-neutral-800 flex-shrink-0">
                      <Image
                        src={urlFor(adjacentProjects.previous.coverImage).width(200).height(200).quality(80).auto('format').url()}
                        alt=""
                        fill
                        loading="lazy"
                        className="object-cover transition-transform duration-500 group-hover:scale-110"
                        sizes="96px"
                        placeholder={adjacentProjects.previous.coverImage.asset.metadata?.lqip ? 'blur' : undefined}
                        blurDataURL={adjacentProjects.previous.coverImage.asset.metadata?.lqip}
                      />
                    </div>
                  )}
                </Link>
              ) : (
                <div className="flex items-center gap-6 p-8 md:p-12 text-neutral-400 dark:text-neutral-600">
                  <span className="text-sm">No previous project</span>
                </div>
              )}
            </div>

            {/* Next Project */}
            <div className="group">
              {adjacentProjects?.next ? (
                <Link
                  href={`/projects/${adjacentProjects.next.slug}`}
                  className="flex items-center gap-6 p-8 md:p-12 transition-colors duration-300 hover:bg-neutral-50 dark:hover:bg-neutral-900/50 text-right"
                >
                  {/* Thumbnail */}
                  {adjacentProjects.next.coverImage?.asset?.url && (
                    <div className="hidden lg:block relative w-24 h-24 rounded-lg overflow-hidden bg-neutral-100 dark:bg-neutral-800 flex-shrink-0">
                      <Image
                        src={urlFor(adjacentProjects.next.coverImage).width(200).height(200).quality(80).auto('format').url()}
                        alt=""
                        fill
                        loading="lazy"
                        className="object-cover transition-transform duration-500 group-hover:scale-110"
                        sizes="96px"
                        placeholder={adjacentProjects.next.coverImage.asset.metadata?.lqip ? 'blur' : undefined}
                        blurDataURL={adjacentProjects.next.coverImage.asset.metadata?.lqip}
                      />
                    </div>
                  )}

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <span className="block text-xs uppercase tracking-wider text-neutral-400 dark:text-neutral-500 mb-2">
                      Next Project
                    </span>
                    <span className="block font-display text-lg md:text-xl text-neutral-900 dark:text-neutral-100 truncate group-hover:text-brand-700 dark:group-hover:text-brand-400 transition-colors">
                      {adjacentProjects.next.title}
                    </span>
                  </div>

                  {/* Arrow */}
                  <div className="hidden sm:flex w-12 h-12 rounded-full bg-neutral-100 dark:bg-neutral-800 items-center justify-center transition-all duration-300 group-hover:bg-brand-100 dark:group-hover:bg-brand-900/30">
                    <svg
                      className="w-5 h-5 text-neutral-600 dark:text-neutral-400 transition-transform duration-300 group-hover:translate-x-1"
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
              ) : (
                <div className="flex items-center justify-end gap-6 p-8 md:p-12 text-neutral-400 dark:text-neutral-600">
                  <span className="text-sm">No next project</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* ============================================
          FOOTER CTA
          Links back to portfolio with elegant styling
          ============================================ */}
      <footer className="py-16 md:py-20 bg-neutral-50 dark:bg-neutral-900/30">
        <div className="mx-auto max-w-4xl px-6 md:px-8 text-center">
          <p className="font-serif italic text-neutral-500 dark:text-neutral-400 mb-6">
            Thank you for viewing this project
          </p>
          <Link
            href="/projects"
            className="
              inline-flex items-center gap-3
              px-8 py-4
              bg-neutral-900 dark:bg-white
              text-white dark:text-neutral-900
              font-medium
              rounded-full
              transition-all duration-300
              hover:bg-neutral-800 dark:hover:bg-neutral-100
              hover:shadow-xl hover:shadow-black/10
              focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
              group
            "
          >
            <svg
              className="w-4 h-4 transition-transform duration-300 group-hover:-translate-x-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
            </svg>
            <span>View All Projects</span>
          </Link>
        </div>
      </footer>
    </article>
  )
}
