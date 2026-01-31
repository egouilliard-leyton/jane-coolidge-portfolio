// sanity/lib/queries.ts
/**
 * GROQ Queries for Sanity CMS Content Fetching
 *
 * This module contains all GROQ queries used throughout the application.
 * Queries are organized by content type and include proper projections
 * for image URLs and related content expansion.
 */

import { groq } from 'next-sanity'

// =============================================================================
// COMMON PROJECTIONS
// These are reusable projections for frequently accessed fields
// =============================================================================

/**
 * Standard image projection with asset expansion
 * Includes URL, dimensions, and LQIP for blur placeholder
 */
const imageProjection = `{
  asset-> {
    _id,
    url,
    metadata {
      dimensions {
        width,
        height,
        aspectRatio
      },
      lqip
    }
  },
  alt,
  hotspot,
  crop
}`

/**
 * SEO fields projection with OG image expansion
 */
const seoProjection = `{
  metaTitle,
  metaDescription,
  ogImage ${imageProjection}
}`

/**
 * Popup content projection for resolved references
 */
const popupProjection = `{
  _id,
  title,
  description,
  link,
  linkText,
  tags
}`

/**
 * Image with popup projection - expands both image asset and popup reference
 */
const imageWithPopupProjection = `{
  _key,
  _type,
  image ${imageProjection},
  alt,
  caption,
  popup-> ${popupProjection},
  size
}`

// =============================================================================
// SITE SETTINGS & NAVIGATION
// =============================================================================

/**
 * Fetches global site settings
 * Used for site title, logo, default SEO, social links, footer
 */
export const siteSettingsQuery = groq`
  *[_type == "siteSettings"][0] {
    _id,
    siteName,
    logo ${imageProjection},
    favicon {
      asset-> {
        _id,
        url
      }
    },
    defaultSeo ${seoProjection},
    socialLinks[] {
      _key,
      platform,
      url
    },
    footerText,
    googleAnalyticsId
  }
`

/**
 * Fetches navigation menu items
 * Used in header component for main navigation
 */
export const navigationQuery = groq`
  *[_type == "navigation"][0] {
    _id,
    mainMenu[] {
      _key,
      label,
      link,
      openInNewTab
    }
  }
`

// =============================================================================
// HOMEPAGE
// =============================================================================

/**
 * Fetches homepage content
 * Includes hero section, intro text, section headings, and CTA
 */
export const homepageQuery = groq`
  *[_type == "homepage"][0] {
    _id,
    heroHeading,
    heroSubheading,
    heroImage ${imageProjection},
    introText,
    featuredPostsHeading,
    featuredProjectsHeading,
    ctaText,
    ctaLink,
    seo ${seoProjection}
  }
`

/**
 * Fetches featured blog posts for homepage
 * Returns the 3 most recent posts marked as featured
 */
export const featuredPostsQuery = groq`
  *[_type == "blogPost" && featured == true] | order(publishedAt desc)[0...3] {
    _id,
    title,
    "slug": slug.current,
    excerpt,
    publishedAt,
    coverImage ${imageProjection},
    tags
  }
`

/**
 * Fetches featured projects for homepage
 * Returns the 4 most recent projects
 */
export const featuredProjectsQuery = groq`
  *[_type == "project"] | order(date desc)[0...4] {
    _id,
    title,
    "slug": slug.current,
    category,
    coverImage ${imageProjection}
  }
`

// =============================================================================
// BLOG
// =============================================================================

/**
 * Fetches paginated blog posts for listing page
 * @param start - Starting index for pagination
 * @param end - Ending index for pagination
 */
export const blogPostsQuery = groq`
  *[_type == "blogPost"] | order(publishedAt desc)[$start...$end] {
    _id,
    title,
    "slug": slug.current,
    excerpt,
    publishedAt,
    coverImage ${imageProjection},
    tags
  }
`

/**
 * Fetches total count of blog posts
 * Used for pagination calculations
 */
export const blogPostCountQuery = groq`
  count(*[_type == "blogPost"])
`

/**
 * Fetches a single blog post by slug
 * Includes full content with expanded image popups
 * @param slug - The post's URL slug
 */
export const blogPostBySlugQuery = groq`
  *[_type == "blogPost" && slug.current == $slug][0] {
    _id,
    title,
    "slug": slug.current,
    excerpt,
    publishedAt,
    coverImage ${imageProjection},
    content[] {
      ...,
      _type == "imageWithPopup" => ${imageWithPopupProjection}
    },
    tags,
    featured,
    seo ${seoProjection}
  }
`

/**
 * Fetches all blog post slugs
 * Used for static site generation (generateStaticParams)
 */
export const blogPostSlugsQuery = groq`
  *[_type == "blogPost" && defined(slug.current)] {
    "slug": slug.current
  }
`

/**
 * Fetches related blog posts based on matching tags
 * Excludes the current post and returns up to 3 related posts
 * @param id - Current post ID to exclude
 * @param tags - Array of tags to match against
 */
export const relatedPostsQuery = groq`
  *[_type == "blogPost" && _id != $id && count((tags[])[@ in $tags]) > 0] | order(publishedAt desc)[0...3] {
    _id,
    title,
    "slug": slug.current,
    excerpt,
    publishedAt,
    coverImage ${imageProjection},
    tags
  }
`

/**
 * Fetches blog posts filtered by tag
 * @param tag - Tag to filter by
 * @param start - Starting index for pagination
 * @param end - Ending index for pagination
 */
export const blogPostsByTagQuery = groq`
  *[_type == "blogPost" && $tag in tags] | order(publishedAt desc)[$start...$end] {
    _id,
    title,
    "slug": slug.current,
    excerpt,
    publishedAt,
    coverImage ${imageProjection},
    tags
  }
`

/**
 * Fetches count of blog posts with specific tag
 * @param tag - Tag to filter by
 */
export const blogPostCountByTagQuery = groq`
  count(*[_type == "blogPost" && $tag in tags])
`

/**
 * Fetches all unique tags from blog posts
 * Used for tag cloud or filter UI
 */
export const allBlogTagsQuery = groq`
  array::unique(*[_type == "blogPost" && defined(tags)].tags[])
`

// =============================================================================
// PROJECTS
// =============================================================================

/**
 * Fetches all projects for gallery listing
 * Ordered by date, includes cover image and category
 */
export const projectsQuery = groq`
  *[_type == "project"] | order(date desc) {
    _id,
    title,
    "slug": slug.current,
    category,
    client,
    date,
    coverImage ${imageProjection}
  }
`

/**
 * Fetches projects filtered by category
 * @param category - Category to filter by
 */
export const projectsByCategoryQuery = groq`
  *[_type == "project" && category == $category] | order(date desc) {
    _id,
    title,
    "slug": slug.current,
    category,
    client,
    date,
    coverImage ${imageProjection}
  }
`

/**
 * Fetches a single project by slug
 * Includes full gallery with popup content for each image
 * @param slug - The project's URL slug
 */
export const projectBySlugQuery = groq`
  *[_type == "project" && slug.current == $slug][0] {
    _id,
    title,
    "slug": slug.current,
    description,
    client,
    date,
    category,
    coverImage ${imageProjection},
    images[] ${imageWithPopupProjection},
    seo ${seoProjection}
  }
`

/**
 * Fetches all project slugs
 * Used for static site generation (generateStaticParams)
 */
export const projectSlugsQuery = groq`
  *[_type == "project" && defined(slug.current)] {
    "slug": slug.current
  }
`

/**
 * Fetches project count by category
 * Used for category filter with counts
 */
export const projectCountByCategoryQuery = groq`
  {
    "all": count(*[_type == "project"]),
    "editorial": count(*[_type == "project" && category == "editorial"]),
    "campaign": count(*[_type == "project" && category == "campaign"]),
    "lookbook": count(*[_type == "project" && category == "lookbook"]),
    "styling": count(*[_type == "project" && category == "styling"]),
    "personal": count(*[_type == "project" && category == "personal"])
  }
`

/**
 * Fetches adjacent projects for navigation
 * Returns previous and next projects based on date
 * @param date - Current project's date
 * @param slug - Current project's slug to exclude
 */
export const adjacentProjectsQuery = groq`
  {
    "previous": *[_type == "project" && date > $date] | order(date asc)[0] {
      _id,
      title,
      "slug": slug.current,
      coverImage ${imageProjection}
    },
    "next": *[_type == "project" && date < $date && slug.current != $slug] | order(date desc)[0] {
      _id,
      title,
      "slug": slug.current,
      coverImage ${imageProjection}
    }
  }
`

// =============================================================================
// ABOUT PAGE
// =============================================================================

/**
 * Fetches about page content
 * Includes profile image, bio, credentials, and client list
 */
export const aboutPageQuery = groq`
  *[_type == "aboutPage"][0] {
    _id,
    heading,
    profileImage ${imageProjection},
    name,
    tagline,
    bio,
    credentials[] {
      _key,
      title,
      organization,
      period
    },
    clients,
    seo ${seoProjection}
  }
`

// =============================================================================
// CONTACT PAGE
// =============================================================================

/**
 * Fetches contact page content
 * Includes contact info, social links, and form settings
 */
export const contactPageQuery = groq`
  *[_type == "contactPage"][0] {
    _id,
    heading,
    introText,
    email,
    phone,
    location,
    socialLinks[] {
      _key,
      platform,
      url
    },
    formEnabled,
    seo ${seoProjection}
  }
`

// =============================================================================
// POPUP CONTENT
// =============================================================================

/**
 * Fetches a single popup content by ID
 * Used when popup needs to be loaded on demand
 * @param id - The popup content document ID
 */
export const popupContentByIdQuery = groq`
  *[_type == "popupContent" && _id == $id][0] ${popupProjection}
`

/**
 * Fetches all popup content documents
 * Used for admin/preview purposes
 */
export const allPopupContentQuery = groq`
  *[_type == "popupContent"] | order(title asc) ${popupProjection}
`

// =============================================================================
// SEARCH
// =============================================================================

/**
 * Searches across blog posts and projects
 * Simple text search in titles and excerpts/descriptions
 * @param searchTerm - The search query string
 */
export const searchQuery = groq`
  {
    "posts": *[_type == "blogPost" && (title match $searchTerm || excerpt match $searchTerm)] | order(publishedAt desc)[0...10] {
      _id,
      _type,
      title,
      "slug": slug.current,
      excerpt,
      publishedAt,
      coverImage ${imageProjection}
    },
    "projects": *[_type == "project" && (title match $searchTerm || client match $searchTerm)] | order(date desc)[0...10] {
      _id,
      _type,
      title,
      "slug": slug.current,
      category,
      client,
      coverImage ${imageProjection}
    }
  }
`

// =============================================================================
// SITEMAP
// =============================================================================

/**
 * Fetches all content for sitemap generation
 * Returns slugs and update timestamps for all indexable content
 */
export const sitemapQuery = groq`
  {
    "posts": *[_type == "blogPost" && defined(slug.current)] | order(publishedAt desc) {
      "slug": slug.current,
      _updatedAt,
      publishedAt
    },
    "projects": *[_type == "project" && defined(slug.current)] | order(date desc) {
      "slug": slug.current,
      _updatedAt,
      date
    }
  }
`

// =============================================================================
// TYPE EXPORTS FOR QUERY RESULTS
// These types match the shape of data returned by each query
// =============================================================================

import type {
  SiteSettings,
  Navigation,
  Homepage,
  BlogPost,
  Project,
  AboutPage,
  ContactPage,
  PopupContent,
  SanityImageExpanded,
  ImageWithPopupExpanded,
  SEO,
  SocialLink,
  Credential,
  MenuItem,
  ProjectCategory,
} from '@/types/sanity'

/**
 * Expanded image type as returned by GROQ queries
 */
export interface QueryImage {
  asset: {
    _id: string
    url: string
    metadata: {
      dimensions: {
        width: number
        height: number
        aspectRatio: number
      }
      lqip?: string
    }
  } | null
  alt?: string
  hotspot?: {
    x: number
    y: number
    height: number
    width: number
  }
  crop?: {
    top: number
    bottom: number
    left: number
    right: number
  }
}

/**
 * SEO fields as returned by GROQ queries
 */
export interface QuerySEO {
  metaTitle?: string
  metaDescription?: string
  ogImage?: QueryImage
}

/**
 * Site settings result type
 */
export interface SiteSettingsResult {
  _id: string
  siteName: string
  logo?: QueryImage
  favicon?: {
    asset: {
      _id: string
      url: string
    } | null
  }
  defaultSeo?: QuerySEO
  socialLinks?: SocialLink[]
  footerText?: string
  googleAnalyticsId?: string
}

/**
 * Navigation result type
 */
export interface NavigationResult {
  _id: string
  mainMenu?: MenuItem[]
}

/**
 * Homepage result type
 */
export interface HomepageResult {
  _id: string
  heroHeading: string
  heroSubheading?: string
  heroImage?: QueryImage
  introText?: unknown[] // Portable Text blocks
  featuredPostsHeading?: string
  featuredProjectsHeading?: string
  ctaText?: string
  ctaLink?: string
  seo?: QuerySEO
}

/**
 * Blog post list item result type
 */
export interface BlogPostListItem {
  _id: string
  title: string
  slug: string
  excerpt?: string
  publishedAt?: string
  coverImage?: QueryImage
  tags?: string[]
}

/**
 * Blog post detail result type
 */
export interface BlogPostDetail extends BlogPostListItem {
  content?: unknown[] // Portable Text blocks with custom types
  featured?: boolean
  seo?: QuerySEO
}

/**
 * Project list item result type
 */
export interface ProjectListItem {
  _id: string
  title: string
  slug: string
  category?: ProjectCategory
  client?: string
  date?: string
  coverImage?: QueryImage
}

/**
 * Image with popup result type (resolved)
 */
export interface ImageWithPopupResult {
  _key?: string
  _type: 'imageWithPopup'
  image?: QueryImage
  alt: string
  caption?: string
  popup?: PopupContentResult
  size?: 'small' | 'medium' | 'large' | 'full'
}

/**
 * Popup content result type
 */
export interface PopupContentResult {
  _id?: string
  title: string
  description?: string
  link?: string
  linkText?: string
  tags?: string[]
}

/**
 * Project detail result type
 */
export interface ProjectDetail extends ProjectListItem {
  description?: unknown[] // Portable Text blocks
  images?: ImageWithPopupResult[]
  seo?: QuerySEO
}

/**
 * About page result type
 */
export interface AboutPageResult {
  _id: string
  heading?: string
  profileImage?: QueryImage
  name?: string
  tagline?: string
  bio?: unknown[] // Portable Text blocks
  credentials?: Credential[]
  clients?: string[]
  seo?: QuerySEO
}

/**
 * Contact page result type
 */
export interface ContactPageResult {
  _id: string
  heading?: string
  introText?: string
  email?: string
  phone?: string
  location?: string
  socialLinks?: SocialLink[]
  formEnabled?: boolean
  seo?: QuerySEO
}

/**
 * Adjacent projects result type
 */
export interface AdjacentProjectsResult {
  previous?: ProjectListItem | null
  next?: ProjectListItem | null
}

/**
 * Project counts by category result type
 */
export interface ProjectCategoryCountsResult {
  all: number
  editorial: number
  campaign: number
  lookbook: number
  styling: number
  personal: number
}

/**
 * Search results type
 */
export interface SearchResults {
  posts: BlogPostListItem[]
  projects: ProjectListItem[]
}

/**
 * Sitemap content type
 */
export interface SitemapContent {
  posts: {
    slug: string
    _updatedAt: string
    publishedAt?: string
  }[]
  projects: {
    slug: string
    _updatedAt: string
    date?: string
  }[]
}

/**
 * Slug item type (for generateStaticParams)
 */
export interface SlugItem {
  slug: string
}
