// app/(site)/blog/page.tsx
import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

import { sanityFetch } from '@/sanity/lib/client'
import { urlFor } from '@/sanity/lib/image'
import {
  blogPostsQuery,
  blogPostCountQuery,
  siteSettingsQuery,
  type BlogPostListItem,
  type SiteSettingsResult,
} from '@/sanity/lib/queries'

const POSTS_PER_PAGE = 9

interface BlogPageProps {
  searchParams: Promise<{ page?: string }>
}

/**
 * Generate metadata for the blog listing page
 */
export async function generateMetadata(): Promise<Metadata> {
  const settings = await sanityFetch<SiteSettingsResult | null>({
    query: siteSettingsQuery,
    tags: ['siteSettings'],
  })

  return {
    title: `Journal | ${settings?.siteName || 'Fashion Blog'}`,
    description: 'Explore stories, insights, and inspirations from the world of fashion styling and creative direction.',
    openGraph: {
      title: `Journal | ${settings?.siteName || 'Fashion Blog'}`,
      description: 'Explore stories, insights, and inspirations from the world of fashion styling and creative direction.',
    },
  }
}

/**
 * Blog Listing Page - Server Component
 *
 * Displays a magazine-style grid of blog posts with pagination.
 * Features an elegant editorial layout with asymmetric cards,
 * distinctive typography, and sophisticated hover interactions.
 */
export default async function BlogPage({ searchParams }: BlogPageProps) {
  const params = await searchParams
  const currentPage = Math.max(1, parseInt(params.page || '1', 10))
  const start = (currentPage - 1) * POSTS_PER_PAGE
  const end = start + POSTS_PER_PAGE

  // Fetch posts and total count in parallel
  const [posts, totalCount] = await Promise.all([
    sanityFetch<BlogPostListItem[]>({
      query: blogPostsQuery,
      params: { start, end },
      tags: ['blogPost'],
    }),
    sanityFetch<number>({
      query: blogPostCountQuery,
      tags: ['blogPost'],
    }),
  ])

  const totalPages = Math.ceil(totalCount / POSTS_PER_PAGE)
  const hasNextPage = currentPage < totalPages
  const hasPrevPage = currentPage > 1

  return (
    <article className="min-h-screen">
      {/* ============================================
          PAGE HEADER
          Elegant editorial-style header with decorative elements
          ============================================ */}
      <header className="relative py-20 md:py-28 lg:py-36 overflow-hidden">
        {/* Subtle background pattern */}
        <div
          className="absolute inset-0 opacity-[0.03] dark:opacity-[0.05]"
          style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, currentColor 1px, transparent 0)`,
            backgroundSize: '32px 32px',
          }}
          aria-hidden="true"
        />

        {/* Decorative accent line */}
        <div
          className="absolute left-0 top-1/2 -translate-y-1/2 w-px h-24 bg-gradient-to-b from-transparent via-brand-400 to-transparent hidden lg:block"
          aria-hidden="true"
        />

        <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
          <div className="max-w-3xl">
            {/* Section label */}
            <div className="mb-6 flex items-center gap-4 animate-fade-up">
              <div className="w-12 h-px bg-brand-400" aria-hidden="true" />
              <span className="text-brand-500 text-xs tracking-[0.4em] uppercase font-medium">
                The Journal
              </span>
            </div>

            {/* Main heading */}
            <h1 className="font-display text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-neutral-900 dark:text-neutral-100 tracking-tight leading-[1.1] mb-6 animate-fade-up animation-delay-100">
              Stories & Insights
            </h1>

            {/* Subtitle */}
            <p className="text-lg md:text-xl text-neutral-600 dark:text-neutral-400 leading-relaxed max-w-xl animate-fade-up animation-delay-200">
              A curated collection of thoughts on fashion, styling, and the creative process.
            </p>
          </div>
        </div>
      </header>

      {/* ============================================
          BLOG POSTS GRID
          Asymmetric editorial layout with varied card sizes
          ============================================ */}
      <section className="pb-24 md:pb-32" aria-label="Blog posts">
        <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
          {posts && posts.length > 0 ? (
            <>
              {/* Posts Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 lg:gap-10">
                {posts.map((post, index) => (
                  <BlogPostCard
                    key={post._id}
                    post={post}
                    index={index}
                    featured={index === 0 && currentPage === 1}
                  />
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  hasNextPage={hasNextPage}
                  hasPrevPage={hasPrevPage}
                />
              )}
            </>
          ) : (
            /* Empty State */
            <EmptyState />
          )}
        </div>
      </section>
    </article>
  )
}

/**
 * Blog Post Card Component
 *
 * Elegant card with image, metadata, and hover effects.
 * The first card on page 1 is featured with a larger display.
 */
function BlogPostCard({
  post,
  index,
  featured = false,
}: {
  post: BlogPostListItem
  index: number
  featured?: boolean
}) {
  // Calculate stagger delay for animation (max 500ms)
  const delayClass = `animation-delay-${Math.min(index * 100, 500)}`

  return (
    <article
      className={`
        group animate-fade-up ${delayClass}
        ${featured ? 'md:col-span-2 lg:col-span-2' : ''}
      `}
    >
      <Link href={`/blog/${post.slug}`} className="block">
        {/* Post Image */}
        <div
          className={`
            relative overflow-hidden bg-neutral-100 dark:bg-neutral-900 mb-5
            ${featured ? 'aspect-[16/9] md:aspect-[2/1]' : 'aspect-[4/5]'}
          `}
        >
          {post.coverImage?.asset?.url ? (
            <Image
              src={urlFor(post.coverImage)
                .width(featured ? 1200 : 600)
                .height(featured ? 600 : 750)
                .quality(85)
                .auto('format')
                .url()}
              alt={post.coverImage.alt || post.title}
              fill
              loading={index < 3 ? 'eager' : 'lazy'}
              className="object-cover transition-transform duration-700 ease-out group-hover:scale-105"
              sizes={featured ? '(max-width: 768px) 100vw, 66vw' : '(max-width: 768px) 100vw, 33vw'}
              placeholder={post.coverImage.asset.metadata?.lqip ? 'blur' : undefined}
              blurDataURL={post.coverImage.asset.metadata?.lqip}
            />
          ) : (
            <div className="absolute inset-0 bg-gradient-to-br from-brand-100 via-brand-50 to-neutral-100 dark:from-brand-950 dark:via-neutral-900 dark:to-neutral-950" />
          )}

          {/* Hover overlay */}
          <div
            className="absolute inset-0 bg-black/0 group-hover:bg-black/10 dark:group-hover:bg-black/20 transition-colors duration-500"
            aria-hidden="true"
          />

          {/* Read indicator on hover */}
          <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-white/90 dark:bg-neutral-900/90 text-neutral-900 dark:text-neutral-100 text-sm font-medium backdrop-blur-sm">
              Read article
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
            </span>
          </div>
        </div>

        {/* Post Content */}
        <div className={featured ? 'max-w-2xl' : ''}>
          {/* Tags */}
          {post.tags && post.tags.length > 0 && (
            <div className="mb-3 flex flex-wrap gap-2">
              {post.tags.slice(0, 2).map((tag) => (
                <span
                  key={tag}
                  className="text-xs tracking-widest uppercase text-brand-600 dark:text-brand-400 font-medium"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Title */}
          <h2
            className={`
              font-display text-neutral-900 dark:text-neutral-100 mb-3
              group-hover:text-brand-700 dark:group-hover:text-brand-400
              transition-colors duration-300 leading-tight
              ${featured ? 'text-2xl md:text-3xl lg:text-4xl' : 'text-xl md:text-2xl'}
            `}
          >
            {post.title}
          </h2>

          {/* Excerpt */}
          {post.excerpt && (
            <p
              className={`
                text-neutral-600 dark:text-neutral-400 leading-relaxed
                ${featured ? 'line-clamp-3 text-base md:text-lg' : 'line-clamp-2'}
              `}
            >
              {post.excerpt}
            </p>
          )}

          {/* Date */}
          {post.publishedAt && (
            <div className="mt-4 flex items-center gap-3">
              <div className="w-8 h-px bg-neutral-300 dark:bg-neutral-700" aria-hidden="true" />
              <time
                dateTime={post.publishedAt}
                className="text-sm text-neutral-500 dark:text-neutral-500 tracking-wide"
              >
                {new Date(post.publishedAt).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </time>
            </div>
          )}
        </div>
      </Link>
    </article>
  )
}

/**
 * Pagination Component
 *
 * Elegant, minimalist pagination with clear navigation.
 */
function Pagination({
  currentPage,
  totalPages,
  hasNextPage,
  hasPrevPage,
}: {
  currentPage: number
  totalPages: number
  hasNextPage: boolean
  hasPrevPage: boolean
}) {
  // Generate array of page numbers to display
  const getPageNumbers = () => {
    const pages: (number | 'ellipsis')[] = []
    const showPages = 5 // Max visible page numbers

    if (totalPages <= showPages) {
      // Show all pages if total is small
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      // Always show first page
      pages.push(1)

      if (currentPage > 3) {
        pages.push('ellipsis')
      }

      // Show pages around current
      const start = Math.max(2, currentPage - 1)
      const end = Math.min(totalPages - 1, currentPage + 1)

      for (let i = start; i <= end; i++) {
        pages.push(i)
      }

      if (currentPage < totalPages - 2) {
        pages.push('ellipsis')
      }

      // Always show last page
      pages.push(totalPages)
    }

    return pages
  }

  const pageNumbers = getPageNumbers()

  return (
    <nav
      className="mt-16 md:mt-24 flex items-center justify-center"
      aria-label="Blog pagination"
    >
      <div className="flex items-center gap-2 md:gap-4">
        {/* Previous Button */}
        {hasPrevPage ? (
          <Link
            href={`/blog?page=${currentPage - 1}`}
            className="
              inline-flex items-center gap-2 px-4 py-2
              text-sm font-medium text-neutral-600 dark:text-neutral-400
              hover:text-neutral-900 dark:hover:text-neutral-100
              transition-colors duration-200
            "
            aria-label="Previous page"
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
            <span className="hidden sm:inline">Previous</span>
          </Link>
        ) : (
          <span className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-neutral-300 dark:text-neutral-700 cursor-not-allowed">
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
            <span className="hidden sm:inline">Previous</span>
          </span>
        )}

        {/* Page Numbers */}
        <div className="flex items-center gap-1">
          {pageNumbers.map((page, index) =>
            page === 'ellipsis' ? (
              <span
                key={`ellipsis-${index}`}
                className="w-10 h-10 flex items-center justify-center text-neutral-400 dark:text-neutral-600"
                aria-hidden="true"
              >
                …
              </span>
            ) : (
              <Link
                key={page}
                href={`/blog?page=${page}`}
                className={`
                  w-10 h-10 flex items-center justify-center
                  text-sm font-medium transition-all duration-200
                  ${
                    page === currentPage
                      ? 'bg-neutral-900 dark:bg-neutral-100 text-white dark:text-neutral-900'
                      : 'text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800 hover:text-neutral-900 dark:hover:text-neutral-100'
                  }
                `}
                aria-label={`Page ${page}`}
                aria-current={page === currentPage ? 'page' : undefined}
              >
                {page}
              </Link>
            )
          )}
        </div>

        {/* Next Button */}
        {hasNextPage ? (
          <Link
            href={`/blog?page=${currentPage + 1}`}
            className="
              inline-flex items-center gap-2 px-4 py-2
              text-sm font-medium text-neutral-600 dark:text-neutral-400
              hover:text-neutral-900 dark:hover:text-neutral-100
              transition-colors duration-200
            "
            aria-label="Next page"
          >
            <span className="hidden sm:inline">Next</span>
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
          <span className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-neutral-300 dark:text-neutral-700 cursor-not-allowed">
            <span className="hidden sm:inline">Next</span>
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
          </span>
        )}
      </div>
    </nav>
  )
}

/**
 * Empty State Component
 *
 * Displayed when no blog posts exist.
 */
function EmptyState() {
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
              d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
            />
          </svg>
        </div>
      </div>

      {/* Message */}
      <h2 className="font-display text-2xl md:text-3xl text-neutral-900 dark:text-neutral-100 mb-4">
        No stories yet
      </h2>
      <p className="text-neutral-600 dark:text-neutral-400 max-w-md mx-auto mb-8">
        The journal is waiting for its first entry. Check back soon for insights on fashion, styling, and creative inspiration.
      </p>

      {/* Return home link */}
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
    </div>
  )
}
