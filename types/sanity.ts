/**
 * Core Sanity Types
 *
 * Base types for Sanity CMS content including images, portable text,
 * and common object types used across all documents.
 */

// =============================================================================
// SANITY BASE TYPES
// =============================================================================

/**
 * Sanity document base type - all documents extend this
 */
export interface SanityDocument {
  _id: string
  _type: string
  _createdAt: string
  _updatedAt: string
  _rev: string
}

/**
 * Sanity reference type for document references
 */
export interface SanityReference {
  _type: 'reference'
  _ref: string
}

/**
 * Sanity slug type
 */
export interface SanitySlug {
  _type: 'slug'
  current: string
}

// =============================================================================
// IMAGE TYPES
// =============================================================================

/**
 * Sanity image asset reference
 */
export interface SanityImageAsset {
  _ref: string
  _type: 'reference'
}

/**
 * Sanity image hotspot configuration
 */
export interface SanityImageHotspot {
  x: number
  y: number
  height: number
  width: number
}

/**
 * Sanity image crop configuration
 */
export interface SanityImageCrop {
  top: number
  bottom: number
  left: number
  right: number
}

/**
 * Base Sanity image type as stored in Sanity
 */
export interface SanityImageBase {
  _type: 'image'
  asset: SanityImageAsset
  hotspot?: SanityImageHotspot
  crop?: SanityImageCrop
}

/**
 * Sanity image with alt text (standard image with required alt field)
 */
export interface SanityImage extends SanityImageBase {
  alt: string
}

/**
 * Sanity image with optional alt text (used for logos, favicons)
 */
export interface SanityImageOptionalAlt extends SanityImageBase {
  alt?: string
}

/**
 * Expanded image metadata returned when using asset->
 */
export interface SanityImageMetadata {
  dimensions: {
    width: number
    height: number
    aspectRatio: number
  }
  lqip?: string // Low-quality image placeholder (base64)
  palette?: {
    dominant: {
      background: string
      foreground: string
      title: string
    }
  }
}

/**
 * Full image object with expanded asset data (after GROQ expansion)
 */
export interface SanityImageExpanded {
  _type: 'image'
  alt: string
  asset: {
    _id: string
    url: string
    metadata: SanityImageMetadata
  }
  hotspot?: SanityImageHotspot
  crop?: SanityImageCrop
}

// =============================================================================
// PORTABLE TEXT TYPES
// =============================================================================

/**
 * Portable text mark definition for links
 */
export interface PortableTextLinkMark {
  _type: 'link'
  _key: string
  href: string
  openInNewTab?: boolean
}

/**
 * Portable text mark definition for internal links
 */
export interface PortableTextInternalLinkMark {
  _type: 'internalLink'
  _key: string
  reference: SanityReference
}

/**
 * Union of all mark definition types
 */
export type PortableTextMarkDefinition =
  | PortableTextLinkMark
  | PortableTextInternalLinkMark

/**
 * Portable text span (inline text with marks)
 */
export interface PortableTextSpan {
  _type: 'span'
  _key: string
  text: string
  marks: string[]
}

/**
 * Portable text block children can be spans or other inline content
 */
export type PortableTextChild = PortableTextSpan

/**
 * Block style types
 */
export type PortableTextBlockStyle =
  | 'normal'
  | 'h2'
  | 'h3'
  | 'h4'
  | 'blockquote'

/**
 * List item types
 */
export type PortableTextListItemType = 'bullet' | 'number'

/**
 * Portable text block (paragraph, heading, list item, etc.)
 */
export interface PortableTextBlock {
  _type: 'block'
  _key: string
  style: PortableTextBlockStyle
  listItem?: PortableTextListItemType
  level?: number
  children: PortableTextChild[]
  markDefs: PortableTextMarkDefinition[]
}

/**
 * Image with popup - custom block type for portable text
 */
export interface PortableTextImageWithPopup {
  _type: 'imageWithPopup'
  _key: string
  image: SanityImageBase
  alt: string
  caption?: string
  popup?: SanityReference
  size?: 'small' | 'medium' | 'large' | 'full'
}

/**
 * All possible portable text content types
 */
export type PortableTextContent = PortableTextBlock | PortableTextImageWithPopup

/**
 * Portable text array type
 */
export type PortableText = PortableTextContent[]

// =============================================================================
// OBJECT TYPES
// =============================================================================

/**
 * SEO object type
 */
export interface SEO {
  metaTitle?: string
  metaDescription?: string
  ogImage?: SanityImageBase
}

/**
 * Social platform options
 */
export type SocialPlatform =
  | 'instagram'
  | 'twitter'
  | 'linkedin'
  | 'tiktok'
  | 'pinterest'
  | 'youtube'
  | 'facebook'
  | 'email'

/**
 * Social link object type
 */
export interface SocialLink {
  _key?: string
  platform: SocialPlatform
  url: string
}

/**
 * Credential/experience object type (used in AboutPage)
 */
export interface Credential {
  _key: string
  _type: 'credential'
  title: string
  organization?: string
  period?: string
}

/**
 * Menu item object type (used in Navigation)
 */
export interface MenuItem {
  _key: string
  _type: 'menuItem'
  label: string
  link: string
  openInNewTab?: boolean
}

/**
 * Image with popup object type
 */
export interface ImageWithPopup {
  _key?: string
  _type: 'imageWithPopup'
  image: SanityImageBase
  alt: string
  caption?: string
  popup?: SanityReference
  size?: 'small' | 'medium' | 'large' | 'full'
}

/**
 * Image with popup - expanded version with popup content resolved
 */
export interface ImageWithPopupExpanded {
  _key?: string
  _type: 'imageWithPopup'
  image: SanityImageExpanded['asset']
  alt: string
  caption?: string
  popup?: PopupContent
  size?: 'small' | 'medium' | 'large' | 'full'
}

// =============================================================================
// DOCUMENT TYPES
// =============================================================================

/**
 * Homepage document type
 */
export interface Homepage extends SanityDocument {
  _type: 'homepage'
  heroHeading: string
  heroSubheading?: string
  heroImage?: SanityImage
  introText?: PortableText
  featuredPostsHeading?: string
  featuredProjectsHeading?: string
  ctaText?: string
  ctaLink?: string
  seo?: SEO
}

/**
 * Blog post document type
 */
export interface BlogPost extends SanityDocument {
  _type: 'blogPost'
  title: string
  slug: SanitySlug
  coverImage?: SanityImage
  excerpt?: string
  content?: PortableText
  publishedAt?: string
  tags?: string[]
  featured?: boolean
  seo?: SEO
}

/**
 * Project category options
 */
export type ProjectCategory =
  | 'editorial'
  | 'campaign'
  | 'lookbook'
  | 'styling'
  | 'personal'

/**
 * Project document type
 */
export interface Project extends SanityDocument {
  _type: 'project'
  title: string
  slug: SanitySlug
  coverImage: SanityImage
  images?: ImageWithPopup[]
  description?: PortableText
  client?: string
  date?: string
  category?: ProjectCategory
  seo?: SEO
}

/**
 * Popup content document type
 */
export interface PopupContent extends SanityDocument {
  _type: 'popupContent'
  title: string
  description?: string
  link?: string
  linkText?: string
  tags?: string[]
}

/**
 * About page document type
 */
export interface AboutPage extends SanityDocument {
  _type: 'aboutPage'
  heading?: string
  profileImage?: SanityImage
  name?: string
  tagline?: string
  bio?: PortableText
  credentials?: Credential[]
  clients?: string[]
  seo?: SEO
}

/**
 * Contact page document type
 */
export interface ContactPage extends SanityDocument {
  _type: 'contactPage'
  heading?: string
  introText?: string
  email?: string
  phone?: string
  location?: string
  socialLinks?: SocialLink[]
  formEnabled?: boolean
  seo?: SEO
}

/**
 * Site settings document type
 */
export interface SiteSettings extends SanityDocument {
  _type: 'siteSettings'
  siteName: string
  logo?: SanityImageOptionalAlt
  favicon?: SanityImageBase
  defaultSeo?: SEO
  socialLinks?: SocialLink[]
  footerText?: string
  googleAnalyticsId?: string
}

/**
 * Navigation document type
 */
export interface Navigation extends SanityDocument {
  _type: 'navigation'
  mainMenu?: MenuItem[]
}

// =============================================================================
// EXPANDED/RESOLVED DOCUMENT TYPES
// These types represent documents after GROQ queries expand references
// =============================================================================

/**
 * Homepage with expanded image data
 */
export interface HomepageExpanded extends Omit<Homepage, 'heroImage'> {
  heroImage?: SanityImageExpanded
}

/**
 * Blog post with expanded image data
 */
export interface BlogPostExpanded extends Omit<BlogPost, 'coverImage'> {
  coverImage?: SanityImageExpanded
}

/**
 * Project with expanded images and popup content
 */
export interface ProjectExpanded extends Omit<Project, 'coverImage' | 'images'> {
  coverImage: SanityImageExpanded
  images?: ImageWithPopupExpanded[]
}

/**
 * About page with expanded image data
 */
export interface AboutPageExpanded extends Omit<AboutPage, 'profileImage'> {
  profileImage?: SanityImageExpanded
}
