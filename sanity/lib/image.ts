// sanity/lib/image.ts
import imageUrlBuilder from '@sanity/image-url'
import type { SanityImageSource } from '@sanity/image-url'
import { client } from './client'

const builder = imageUrlBuilder(client)

/**
 * Generate optimized image URL from Sanity image source
 */
export function urlFor(source: SanityImageSource) {
  return builder.image(source)
}

/**
 * Extract dimensions from Sanity image asset reference
 * Format: image-{id}-{width}x{height}-{format}
 */
export function getImageDimensions(image: SanityImageSource & { asset?: { _ref?: string } }) {
  if (!image?.asset?._ref) {
    return { width: 0, height: 0, aspectRatio: 1 }
  }

  const ref = image.asset._ref
  const dimensions = ref.split('-')[2]
  if (!dimensions) {
    return { width: 0, height: 0, aspectRatio: 1 }
  }

  const [width, height] = dimensions.split('x').map(Number)

  return {
    width: width || 0,
    height: height || 0,
    aspectRatio: height ? width / height : 1,
  }
}

/**
 * Image optimization presets for consistent quality and sizing
 */
export const IMAGE_PRESETS = {
  // Hero images - full width, high quality
  hero: { width: 1920, height: 1080, quality: 90 },
  // Cover images for cards and thumbnails
  cover: { width: 800, height: 1067, quality: 85 },
  // Blog post featured images
  blogFeatured: { width: 1200, height: 600, quality: 85 },
  // Standard blog card images
  blogCard: { width: 600, height: 750, quality: 85 },
  // Project gallery images
  projectGallery: { width: 1600, quality: 90 },
  // Project card images
  projectCard: { width: 600, height: 800, quality: 85 },
  // Thumbnail images for navigation
  thumbnail: { width: 200, height: 200, quality: 80 },
  // OG/social sharing images
  ogImage: { width: 1200, height: 630, quality: 85 },
} as const

type ImagePreset = keyof typeof IMAGE_PRESETS

/**
 * Generate optimized image URL with preset configuration
 */
export function getOptimizedImageUrl(
  source: SanityImageSource,
  preset: ImagePreset
): string {
  const config = IMAGE_PRESETS[preset]
  let imageBuilder = builder.image(source)

  if ('width' in config) {
    imageBuilder = imageBuilder.width(config.width)
  }
  if ('height' in config && config.height) {
    imageBuilder = imageBuilder.height(config.height)
  }
  if ('quality' in config) {
    imageBuilder = imageBuilder.quality(config.quality)
  }

  return imageBuilder.auto('format').url()
}

/**
 * Get responsive image sizes attribute based on viewport breakpoints
 */
export function getResponsiveSizes(variant: 'hero' | 'card' | 'thumbnail' | 'gallery' | 'full'): string {
  switch (variant) {
    case 'hero':
      return '100vw'
    case 'full':
      return '100vw'
    case 'card':
      return '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw'
    case 'gallery':
      return '(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 800px'
    case 'thumbnail':
      return '96px'
    default:
      return '100vw'
  }
}

/**
 * Interface for images with expanded metadata (from GROQ queries)
 */
export interface SanityImageWithMetadata {
  asset?: {
    url?: string
    _id?: string
    metadata?: {
      lqip?: string
      dimensions?: {
        width: number
        height: number
        aspectRatio: number
      }
    }
  }
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
  alt?: string
}

/**
 * Get blur placeholder props for Next.js Image component
 * Returns placeholder and blurDataURL if LQIP is available
 */
export function getBlurPlaceholder(image: SanityImageWithMetadata): {
  placeholder?: 'blur'
  blurDataURL?: string
} {
  const lqip = image?.asset?.metadata?.lqip

  if (lqip) {
    return {
      placeholder: 'blur',
      blurDataURL: lqip,
    }
  }

  return {}
}

/**
 * Complete image props for Next.js Image component
 * Combines URL generation, sizing, and blur placeholder
 */
export function getImageProps(
  image: SanityImageSource & SanityImageWithMetadata,
  options: {
    width?: number
    height?: number
    quality?: number
    sizes?: string
  } = {}
): {
  src: string
  placeholder?: 'blur'
  blurDataURL?: string
  sizes?: string
} {
  const { width = 1200, height, quality = 85, sizes } = options

  let imageBuilder = builder.image(image).width(width).quality(quality)

  if (height) {
    imageBuilder = imageBuilder.height(height)
  }

  const src = imageBuilder.auto('format').url()
  const blurProps = getBlurPlaceholder(image)

  return {
    src,
    ...blurProps,
    ...(sizes && { sizes }),
  }
}
