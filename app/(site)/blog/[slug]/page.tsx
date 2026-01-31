// app/(site)/blog/[slug]/page.tsx
import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import { notFound } from 'next/navigation'

import { sanityFetch } from '@/sanity/lib/client'
import { urlFor } from '@/sanity/lib/image'
import {
  blogPostBySlugQuery,
  blogPostSlugsQuery,
  siteSettingsQuery,
  type BlogPostDetail,
  type SiteSettingsResult,
  type SlugItem,
} from '@/sanity/lib/queries'
import { BlogContent } from '@/components/content'
import type { PortableText as PortableTextType } from '@/types'

interface BlogPostPageProps {
  params: Promise<{ slug: string }>
}

/**
 * Generate static params for all blog posts
 * Enables static site generation for each post
 */
export async function generateStaticParams(): Promise<{ slug: string }[]> {
  const slugs = await sanityFetch<SlugItem[]>({
    query: blogPostSlugsQuery,
    tags: ['blogPost'],
  })

  return slugs.map((item) => ({
    slug: item.slug,
  }))
}

/**
 * Generate metadata for SEO
 * Uses post title, excerpt, and cover image for OpenGraph
 */
export async function generateMetadata({
  params,
}: BlogPostPageProps): Promise<Metadata> {
  const { slug } = await params

  const [post, settings] = await Promise.all([
    sanityFetch<BlogPostDetail | null>({
      query: blogPostBySlugQuery,
      params: { slug },
      tags: ['blogPost'],
    }),
    sanityFetch<SiteSettingsResult | null>({
      query: siteSettingsQuery,
      tags: ['siteSettings'],
    }),
  ])

  if (!post) {
    return {
      title: 'Post Not Found',
    }
  }

  const siteName = settings?.siteName || 'Fashion Blog'
  const title = post.seo?.metaTitle || post.title
  const description = post.seo?.metaDescription || post.excerpt || ''

  // Generate OG image URL
  let ogImage: string | undefined
  if (post.seo?.ogImage?.asset?.url) {
    ogImage = post.seo.ogImage.asset.url
  } else if (post.coverImage?.asset?.url) {
    ogImage = urlFor(post.coverImage).width(1200).height(630).quality(85).url()
  }

  return {
    title: `${title} | ${siteName}`,
    description,
    openGraph: {
      title,
      description,
      type: 'article',
      publishedTime: post.publishedAt,
      authors: [siteName],
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
 * Blog Post Detail Page
 *
 * An elegant, editorial-style blog post layout featuring:
 * - Full-width hero cover image with blur-up placeholder
 * - Refined typography with the display font for headings
 * - Tag pills linking to filtered views
 * - Rich Portable Text content with image popup support
 * - Sophisticated navigation back to the journal
 */
export default async function BlogPostPage({ params }: BlogPostPageProps) {
  const { slug } = await params

  const post = await sanityFetch<BlogPostDetail | null>({
    query: blogPostBySlugQuery,
    params: { slug },
    tags: ['blogPost'],
  })

  if (!post) {
    notFound()
  }

  // Format the publish date
  const formattedDate = post.publishedAt
    ? new Date(post.publishedAt).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : null

  // Estimate reading time (rough: 200 words per minute)
  const wordCount = post.content
    ? JSON.stringify(post.content).split(/\s+/).length
    : 0
  const readingTime = Math.max(1, Math.ceil(wordCount / 200))

  return (
    <article className="min-h-screen">
      {/* ============================================
          HERO SECTION
          Full-width cover image with elegant overlay
          ============================================ */}
      <header className="relative">
        {/* Cover Image */}
        {post.coverImage?.asset?.url ? (
          <div className="relative aspect-[21/9] md:aspect-[3/1] lg:aspect-[21/7] overflow-hidden bg-neutral-100 dark:bg-neutral-900">
            <Image
              src={urlFor(post.coverImage)
                .width(2000)
                .height(800)
                .quality(90)
                .auto('format')
                .url()}
              alt={post.coverImage.alt || post.title}
              fill
              priority
              className="object-cover"
              sizes="100vw"
              placeholder={post.coverImage.asset.metadata?.lqip ? 'blur' : undefined}
              blurDataURL={post.coverImage.asset.metadata?.lqip}
            />
            {/* Gradient overlay for text legibility */}
            <div
              className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent"
              aria-hidden="true"
            />
          </div>
        ) : (
          /* Fallback gradient when no cover image */
          <div className="relative aspect-[21/9] md:aspect-[3/1] lg:aspect-[21/7] bg-gradient-to-br from-brand-100 via-brand-50 to-neutral-100 dark:from-brand-950 dark:via-neutral-900 dark:to-neutral-950">
            {/* Decorative pattern */}
            <div
              className="absolute inset-0 opacity-[0.04] dark:opacity-[0.08]"
              style={{
                backgroundImage: `radial-gradient(circle at 1px 1px, currentColor 1px, transparent 0)`,
                backgroundSize: '40px 40px',
              }}
              aria-hidden="true"
            />
          </div>
        )}

        {/* Back Navigation - Floating over image */}
        <nav className="absolute top-6 left-6 md:top-8 md:left-8 lg:left-12 z-10">
          <Link
            href="/blog"
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
            <span>Back to Journal</span>
          </Link>
        </nav>
      </header>

      {/* ============================================
          ARTICLE HEADER
          Title, metadata, and tags
          ============================================ */}
      <div className="relative -mt-16 md:-mt-24 lg:-mt-32 z-10 pb-12 md:pb-16">
        <div className="mx-auto max-w-4xl px-6 md:px-8">
          {/* Content card with elegant shadow */}
          <div className="bg-white dark:bg-neutral-950 rounded-t-3xl shadow-2xl shadow-black/10 pt-10 md:pt-14 lg:pt-16 px-6 md:px-12 lg:px-16">
            {/* Tags */}
            {post.tags && post.tags.length > 0 && (
              <div className="mb-6 flex flex-wrap gap-2 animate-fade-up">
                {post.tags.map((tag) => (
                  <span
                    key={tag}
                    className="
                      inline-block
                      px-3 py-1.5
                      text-xs tracking-[0.2em] uppercase font-medium
                      text-brand-700 dark:text-brand-300
                      bg-brand-50 dark:bg-brand-950/40
                      border border-brand-100 dark:border-brand-900/50
                      rounded-full
                    "
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* Title */}
            <h1 className="font-display text-3xl sm:text-4xl md:text-5xl lg:text-6xl text-neutral-900 dark:text-neutral-100 tracking-tight leading-[1.15] mb-6 animate-fade-up animation-delay-100">
              {post.title}
            </h1>

            {/* Metadata Row */}
            <div className="flex flex-wrap items-center gap-4 md:gap-6 text-sm text-neutral-500 dark:text-neutral-400 animate-fade-up animation-delay-200">
              {/* Date */}
              {formattedDate && (
                <div className="flex items-center gap-2">
                  <svg
                    className="w-4 h-4 text-brand-400"
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
                  <time dateTime={post.publishedAt}>{formattedDate}</time>
                </div>
              )}

              {/* Divider */}
              <span className="hidden sm:block w-1 h-1 rounded-full bg-neutral-300 dark:bg-neutral-700" aria-hidden="true" />

              {/* Reading Time */}
              <div className="flex items-center gap-2">
                <svg
                  className="w-4 h-4 text-brand-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={1.5}
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>{readingTime} min read</span>
              </div>
            </div>

            {/* Excerpt */}
            {post.excerpt && (
              <p className="mt-8 text-lg md:text-xl text-neutral-600 dark:text-neutral-400 leading-relaxed font-serif italic animate-fade-up animation-delay-300">
                {post.excerpt}
              </p>
            )}

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
          ARTICLE CONTENT
          Portable Text rendered with BlogContent component
          ============================================ */}
      <div className="pb-20 md:pb-28 lg:pb-32">
        <div className="mx-auto max-w-4xl px-6 md:px-8">
          <div className="bg-white dark:bg-neutral-950 rounded-b-3xl shadow-2xl shadow-black/10 px-6 md:px-12 lg:px-16 pt-10 md:pt-14 pb-14 md:pb-20">
            {post.content && post.content.length > 0 ? (
              <BlogContent
                content={post.content as PortableTextType}
                className="
                  prose-headings:font-display
                  prose-h2:text-2xl prose-h2:md:text-3xl
                  prose-h3:text-xl prose-h3:md:text-2xl
                  prose-p:text-neutral-700 dark:prose-p:text-neutral-300
                  prose-a:text-brand-700 dark:prose-a:text-brand-400
                  prose-strong:text-neutral-900 dark:prose-strong:text-neutral-100
                  prose-blockquote:border-brand-400/50
                  prose-blockquote:bg-brand-50/30 dark:prose-blockquote:bg-brand-950/20
                "
              />
            ) : (
              /* Empty content state */
              <div className="text-center py-12 text-neutral-500 dark:text-neutral-400">
                <p className="font-serif italic">This article is coming soon...</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ============================================
          FOOTER NAVIGATION
          Links back to journal with elegant styling
          ============================================ */}
      <footer className="pb-20 md:pb-28">
        <div className="mx-auto max-w-4xl px-6 md:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-6 pt-10 border-t border-neutral-200 dark:border-neutral-800">
            {/* Share prompt */}
            <p className="text-sm text-neutral-500 dark:text-neutral-400 italic font-serif">
              Thank you for reading
            </p>

            {/* Back to Journal */}
            <Link
              href="/blog"
              className="
                inline-flex items-center gap-3
                px-6 py-3
                bg-neutral-900 dark:bg-white
                text-white dark:text-neutral-900
                font-medium
                rounded-full
                transition-all duration-300
                hover:bg-neutral-800 dark:hover:bg-neutral-100
                hover:shadow-lg
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
              <span>Back to Journal</span>
            </Link>
          </div>
        </div>
      </footer>
    </article>
  )
}
