/**
 * Central Type Exports
 *
 * All TypeScript types for the fashion website project.
 * Import from 'types' or 'types/sanity' for Sanity-specific types.
 */

// =============================================================================
// SANITY CMS TYPES
// =============================================================================

// Base types
export type {
  SanityDocument,
  SanityReference,
  SanitySlug,
} from './sanity'

// Image types
export type {
  SanityImageAsset,
  SanityImageHotspot,
  SanityImageCrop,
  SanityImageBase,
  SanityImage,
  SanityImageOptionalAlt,
  SanityImageMetadata,
  SanityImageExpanded,
} from './sanity'

// Portable text types
export type {
  PortableTextLinkMark,
  PortableTextInternalLinkMark,
  PortableTextMarkDefinition,
  PortableTextSpan,
  PortableTextChild,
  PortableTextBlockStyle,
  PortableTextListItemType,
  PortableTextBlock,
  PortableTextImageWithPopup,
  PortableTextContent,
  PortableText,
} from './sanity'

// Object types
export type {
  SEO,
  SocialPlatform,
  SocialLink,
  Credential,
  MenuItem,
  ImageWithPopup,
  ImageWithPopupExpanded,
} from './sanity'

// Document types
export type {
  Homepage,
  BlogPost,
  ProjectCategory,
  Project,
  PopupContent,
  AboutPage,
  ContactPage,
  SiteSettings,
  Navigation,
} from './sanity'

// Expanded document types (with resolved references)
export type {
  HomepageExpanded,
  BlogPostExpanded,
  ProjectExpanded,
  AboutPageExpanded,
} from './sanity'
