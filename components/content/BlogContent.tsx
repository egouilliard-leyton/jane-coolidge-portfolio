// components/content/BlogContent.tsx
'use client'

import { PortableText, type PortableTextComponents } from '@portabletext/react'
import Link from 'next/link'
import type {
  PortableText as PortableTextType,
  PortableTextLinkMark,
  PortableTextInternalLinkMark,
  PortableTextImageWithPopup,
  PopupContent,
} from '@/types'
import { ImageWithPopup } from '@/components/ui'

interface BlogContentProps {
  content: PortableTextType
  className?: string
}

/**
 * BlogContent - Renders Portable Text content with custom serializers
 *
 * Handles all standard block types (paragraphs, headings, lists)
 * as well as custom types (images with popups, links).
 * Styled using Tailwind Typography plugin for optimal readability.
 */
export default function BlogContent({ content, className = '' }: BlogContentProps) {
  return (
    <div className={`prose prose-lg max-w-none ${className}`}>
      <PortableText value={content} components={components} />
    </div>
  )
}

/**
 * Custom PortableText components for rendering different block types
 */
const components: PortableTextComponents = {
  // Block-level components (paragraphs, headings, etc.)
  block: {
    // Standard paragraph - uses default prose styling
    normal: ({ children }) => (
      <p className="text-neutral-700 dark:text-neutral-300 leading-relaxed mb-6">
        {children}
      </p>
    ),

    // Heading 2 - Primary section headers
    h2: ({ children, value }) => (
      <h2
        id={generateSlug(value)}
        className="font-display text-3xl md:text-4xl font-semibold text-neutral-900 dark:text-neutral-100 mt-12 mb-6 tracking-tight scroll-mt-24"
      >
        {children}
      </h2>
    ),

    // Heading 3 - Secondary section headers
    h3: ({ children, value }) => (
      <h3
        id={generateSlug(value)}
        className="font-display text-2xl md:text-3xl font-semibold text-neutral-900 dark:text-neutral-100 mt-10 mb-5 tracking-tight scroll-mt-24"
      >
        {children}
      </h3>
    ),

    // Heading 4 - Tertiary headers
    h4: ({ children, value }) => (
      <h4
        id={generateSlug(value)}
        className="font-display text-xl md:text-2xl font-medium text-neutral-900 dark:text-neutral-100 mt-8 mb-4 scroll-mt-24"
      >
        {children}
      </h4>
    ),

    // Block quote - Distinctive styling for fashion/editorial feel
    blockquote: ({ children }) => (
      <blockquote className="relative my-10 pl-8 py-4 border-l-4 border-brand-400/60 bg-brand-50/30 dark:bg-brand-950/20 rounded-r-lg">
        <span
          className="absolute -left-2 -top-4 text-6xl text-brand-300/40 font-serif leading-none select-none"
          aria-hidden="true"
        >
          "
        </span>
        <div className="font-display text-xl md:text-2xl text-neutral-700 dark:text-neutral-300 italic leading-relaxed">
          {children}
        </div>
      </blockquote>
    ),
  },

  // List components
  list: {
    // Unordered list
    bullet: ({ children }) => (
      <ul className="my-6 ml-6 space-y-3 list-none">
        {children}
      </ul>
    ),

    // Ordered list
    number: ({ children }) => (
      <ol className="my-6 ml-6 space-y-3 list-none counter-reset-item">
        {children}
      </ol>
    ),
  },

  // List item components
  listItem: {
    // Bullet list item with custom marker
    bullet: ({ children }) => (
      <li className="relative pl-6 text-neutral-700 dark:text-neutral-300 leading-relaxed">
        <span
          className="absolute left-0 top-3 w-1.5 h-1.5 rounded-full bg-brand-500"
          aria-hidden="true"
        />
        {children}
      </li>
    ),

    // Numbered list item with custom counter
    number: ({ children }) => (
      <li className="relative pl-8 text-neutral-700 dark:text-neutral-300 leading-relaxed counter-increment-item before:content-[counter(item)] before:absolute before:left-0 before:top-0 before:font-display before:font-semibold before:text-brand-600 dark:before:text-brand-400">
        {children}
      </li>
    ),
  },

  // Inline mark components (bold, italic, links, etc.)
  marks: {
    // Bold text
    strong: ({ children }) => (
      <strong className="font-semibold text-neutral-900 dark:text-neutral-100">
        {children}
      </strong>
    ),

    // Italic/emphasis text
    em: ({ children }) => (
      <em className="italic">{children}</em>
    ),

    // Underline
    underline: ({ children }) => (
      <span className="underline underline-offset-2 decoration-brand-400/60">
        {children}
      </span>
    ),

    // Strikethrough
    'strike-through': ({ children }) => (
      <span className="line-through text-neutral-500">{children}</span>
    ),

    // External link
    link: ({ children, value }) => {
      const mark = value as PortableTextLinkMark
      const isExternal = mark.href?.startsWith('http')
      const openInNewTab = mark.openInNewTab ?? isExternal

      if (openInNewTab) {
        return (
          <a
            href={mark.href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-brand-700 dark:text-brand-400 underline decoration-brand-400/40 underline-offset-2 transition-colors duration-200 hover:text-brand-900 dark:hover:text-brand-300 hover:decoration-brand-600"
          >
            {children}
            <span className="sr-only"> (opens in new tab)</span>
            <ExternalLinkIcon />
          </a>
        )
      }

      return (
        <a
          href={mark.href}
          className="text-brand-700 dark:text-brand-400 underline decoration-brand-400/40 underline-offset-2 transition-colors duration-200 hover:text-brand-900 dark:hover:text-brand-300 hover:decoration-brand-600"
        >
          {children}
        </a>
      )
    },

    // Internal link (to other pages/posts)
    internalLink: ({ children, value }) => {
      const mark = value as PortableTextInternalLinkMark
      // Note: The actual URL resolution would happen in the query
      // For now, we use the reference which should be resolved in the GROQ query
      const href = (value as { href?: string }).href || '#'

      return (
        <Link
          href={href}
          className="text-brand-700 dark:text-brand-400 underline decoration-brand-400/40 underline-offset-2 transition-colors duration-200 hover:text-brand-900 dark:hover:text-brand-300 hover:decoration-brand-600"
        >
          {children}
        </Link>
      )
    },
  },

  // Custom block types
  types: {
    // Image with optional popup - uses the ImageWithPopup component
    imageWithPopup: ({ value }) => {
      const block = value as PortableTextImageWithPopup & { popup?: PopupContent }
      const { image, alt, caption, popup, size = 'large' } = block

      if (!image?.asset) {
        return null
      }

      return (
        <ImageWithPopup
          image={image}
          alt={alt || ''}
          caption={caption}
          popup={popup}
          size={size}
        />
      )
    },
  },
}

/**
 * Generate a URL-friendly slug from block content for anchor links
 */
function generateSlug(value: unknown): string {
  // Type guard to extract text from portable text block children
  const block = value as { children?: Array<{ text?: string; _type?: string }> }
  if (!block?.children) return ''

  const text = block.children
    .filter((child) => child?._type === 'span' && typeof child?.text === 'string')
    .map((child) => child.text)
    .join('')

  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

/**
 * External link icon component
 */
function ExternalLinkIcon() {
  return (
    <svg
      className="inline-block ml-1 w-3.5 h-3.5 opacity-60"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
      />
    </svg>
  )
}
