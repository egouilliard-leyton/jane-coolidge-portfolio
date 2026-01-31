// app/(site)/page.tsx
import type { Metadata } from 'next'

import { sanityFetch } from '@/sanity/lib/client'
import {
  homepageQuery,
  featuredPostsQuery,
  featuredProjectsQuery,
  type HomepageResult,
  type BlogPostListItem,
  type ProjectListItem,
} from '@/sanity/lib/queries'
import HomePageClient from '@/components/home/HomePageClient'

/**
 * Generate metadata for the homepage
 */
export async function generateMetadata(): Promise<Metadata> {
  const homepage = await sanityFetch<HomepageResult | null>({
    query: homepageQuery,
    tags: ['homepage'],
  })

  return {
    title: homepage?.seo?.metaTitle || 'Home',
    description: homepage?.seo?.metaDescription || 'Fashion styling and creative direction',
    openGraph: {
      images: homepage?.seo?.ogImage?.asset?.url
        ? [{ url: homepage.seo.ogImage.asset.url }]
        : homepage?.heroImage?.asset?.url
          ? [{ url: homepage.heroImage.asset.url }]
          : [],
    },
  }
}

/**
 * Homepage - Server Component
 *
 * Fetches homepage content, featured posts, and featured projects from Sanity.
 * Renders through HomePageClient which provides scroll-triggered animations
 * and hover effects while respecting prefers-reduced-motion preferences.
 */
export default async function HomePage() {
  // Fetch all homepage data in parallel
  const [homepage, featuredPosts, featuredProjects] = await Promise.all([
    sanityFetch<HomepageResult | null>({
      query: homepageQuery,
      tags: ['homepage'],
    }),
    sanityFetch<BlogPostListItem[]>({
      query: featuredPostsQuery,
      tags: ['blogPost'],
    }),
    sanityFetch<ProjectListItem[]>({
      query: featuredProjectsQuery,
      tags: ['project'],
    }),
  ])

  return (
    <HomePageClient
      homepage={homepage}
      featuredPosts={featuredPosts}
      featuredProjects={featuredProjects}
    />
  )
}
