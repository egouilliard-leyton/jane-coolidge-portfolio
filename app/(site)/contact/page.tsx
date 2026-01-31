// app/(site)/contact/page.tsx
import type { Metadata } from 'next'
import Link from 'next/link'

import { sanityFetch } from '@/sanity/lib/client'
import { contactPageQuery, type ContactPageResult } from '@/sanity/lib/queries'
import type { SocialPlatform } from '@/types/sanity'

/**
 * Generate metadata for the contact page
 */
export async function generateMetadata(): Promise<Metadata> {
  const page = await sanityFetch<ContactPageResult | null>({
    query: contactPageQuery,
    tags: ['contactPage'],
  })

  return {
    title: page?.seo?.metaTitle || 'Contact',
    description: page?.seo?.metaDescription || 'Get in touch',
    openGraph: {
      images: page?.seo?.ogImage?.asset?.url
        ? [{ url: page.seo.ogImage.asset.url }]
        : [],
    },
  }
}

/**
 * Social media icons mapping
 */
const socialIcons: Record<SocialPlatform, React.ReactNode> = {
  instagram: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
      <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
      <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
      <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" strokeWidth={2} />
    </svg>
  ),
  twitter: (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
    </svg>
  ),
  linkedin: (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
    </svg>
  ),
  tiktok: (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
      <path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z" />
    </svg>
  ),
  pinterest: (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
      <path d="M12 0C5.373 0 0 5.372 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738.098.119.112.224.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12 0-6.628-5.373-12-12-12z" />
    </svg>
  ),
  youtube: (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
      <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
    </svg>
  ),
  facebook: (
    <svg viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
    </svg>
  ),
  email: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
      <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  ),
}

/**
 * Get human-readable label for platform
 */
function getPlatformLabel(platform: SocialPlatform): string {
  const labels: Record<SocialPlatform, string> = {
    instagram: 'Instagram',
    twitter: 'X (Twitter)',
    linkedin: 'LinkedIn',
    tiktok: 'TikTok',
    pinterest: 'Pinterest',
    youtube: 'YouTube',
    facebook: 'Facebook',
    email: 'Email',
  }
  return labels[platform] || platform
}

/**
 * ContactPage - Server Component
 *
 * An elegant, centered contact page featuring:
 * - Minimalist hero with decorative accents
 * - Clean contact information layout
 * - Beautiful social media links with hover effects
 * - Subtle background patterns for depth
 */
export default async function ContactPage() {
  const page = await sanityFetch<ContactPageResult | null>({
    query: contactPageQuery,
    tags: ['contactPage'],
  })

  return (
    <article className="relative min-h-screen">
      {/* ============================================
          DECORATIVE BACKGROUND ELEMENTS
          ============================================ */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        {/* Subtle gradient orb - top right */}
        <div
          className="absolute -top-40 -right-40 w-[600px] h-[600px] rounded-full opacity-[0.07]"
          style={{
            background: 'radial-gradient(circle, var(--color-brand-400) 0%, transparent 70%)',
          }}
        />
        {/* Subtle gradient orb - bottom left */}
        <div
          className="absolute -bottom-60 -left-60 w-[800px] h-[800px] rounded-full opacity-[0.05]"
          style={{
            background: 'radial-gradient(circle, var(--color-brand-300) 0%, transparent 60%)',
          }}
        />
        {/* Diagonal accent line */}
        <div
          className="absolute top-0 right-1/4 w-px h-96 bg-gradient-to-b from-brand-200 via-brand-400/30 to-transparent rotate-12 origin-top hidden lg:block"
        />
      </div>

      {/* ============================================
          MAIN CONTENT
          ============================================ */}
      <section
        className="relative py-24 md:py-32 lg:py-40"
        aria-label="Contact information"
      >
        <div className="mx-auto max-w-4xl px-8 lg:px-16">
          {/* ----------------------------------------
              HEADER SECTION
              ---------------------------------------- */}
          <header className="text-center mb-20 md:mb-28 animate-fade-up">
            {/* Decorative Label */}
            <div className="mb-8 flex items-center justify-center gap-4" aria-hidden="true">
              <div className="w-12 h-px bg-brand-400" />
              <span className="text-brand-500 text-xs tracking-[0.4em] uppercase font-medium">
                Get in Touch
              </span>
              <div className="w-12 h-px bg-brand-400" />
            </div>

            {/* Page Heading */}
            <h1 className="font-display text-5xl sm:text-6xl lg:text-7xl xl:text-8xl text-neutral-900 dark:text-neutral-100 tracking-tight leading-[0.9] mb-8">
              {page?.heading || 'Contact'}
            </h1>

            {/* Introduction Text */}
            {page?.introText && (
              <p className="font-serif text-xl md:text-2xl lg:text-3xl text-neutral-600 dark:text-neutral-400 leading-relaxed max-w-2xl mx-auto animate-fade-up animation-delay-100">
                {page.introText}
              </p>
            )}
          </header>

          {/* ----------------------------------------
              CONTACT DETAILS GRID
              ---------------------------------------- */}
          <div className="grid gap-16 md:gap-20 animate-fade-up animation-delay-200">
            {/* Primary Contact - Email */}
            {page?.email && (
              <div className="text-center">
                <div className="inline-flex flex-col items-center group">
                  {/* Email Icon */}
                  <div className="mb-6 p-4 rounded-full bg-brand-50 dark:bg-brand-950/30 text-brand-600 dark:text-brand-400 transition-all duration-300 group-hover:bg-brand-100 dark:group-hover:bg-brand-900/40 group-hover:scale-110">
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth={1.5}
                      className="w-8 h-8"
                    >
                      <path
                        d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>

                  {/* Label */}
                  <span className="text-xs tracking-[0.3em] uppercase text-neutral-500 dark:text-neutral-500 font-medium mb-3">
                    Email
                  </span>

                  {/* Email Link */}
                  <a
                    href={`mailto:${page.email}`}
                    className="font-display text-2xl md:text-3xl lg:text-4xl text-neutral-900 dark:text-neutral-100 transition-colors duration-300 hover:text-brand-600 dark:hover:text-brand-400 underline-animate"
                  >
                    {page.email}
                  </a>
                </div>
              </div>
            )}

            {/* Secondary Contact Info - Phone & Location */}
            <div className="grid md:grid-cols-2 gap-12 md:gap-8">
              {/* Phone */}
              {page?.phone && (
                <div className="text-center group">
                  {/* Phone Icon */}
                  <div className="mb-5 inline-flex p-3 rounded-full bg-neutral-100 dark:bg-neutral-900 text-neutral-600 dark:text-neutral-400 transition-all duration-300 group-hover:bg-brand-50 dark:group-hover:bg-brand-950/30 group-hover:text-brand-600 dark:group-hover:text-brand-400">
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth={1.5}
                      className="w-6 h-6"
                    >
                      <path
                        d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>

                  {/* Label */}
                  <span className="block text-xs tracking-[0.3em] uppercase text-neutral-500 dark:text-neutral-500 font-medium mb-2">
                    Phone
                  </span>

                  {/* Phone Link */}
                  <a
                    href={`tel:${page.phone.replace(/\s+/g, '')}`}
                    className="font-serif text-xl md:text-2xl text-neutral-700 dark:text-neutral-300 transition-colors duration-300 hover:text-brand-600 dark:hover:text-brand-400"
                  >
                    {page.phone}
                  </a>
                </div>
              )}

              {/* Location */}
              {page?.location && (
                <div className="text-center group">
                  {/* Location Icon */}
                  <div className="mb-5 inline-flex p-3 rounded-full bg-neutral-100 dark:bg-neutral-900 text-neutral-600 dark:text-neutral-400 transition-all duration-300 group-hover:bg-brand-50 dark:group-hover:bg-brand-950/30 group-hover:text-brand-600 dark:group-hover:text-brand-400">
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth={1.5}
                      className="w-6 h-6"
                    >
                      <path
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                      <path
                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>

                  {/* Label */}
                  <span className="block text-xs tracking-[0.3em] uppercase text-neutral-500 dark:text-neutral-500 font-medium mb-2">
                    Based in
                  </span>

                  {/* Location Text */}
                  <span className="font-serif text-xl md:text-2xl text-neutral-700 dark:text-neutral-300">
                    {page.location}
                  </span>
                </div>
              )}
            </div>

            {/* ----------------------------------------
                SOCIAL LINKS SECTION
                ---------------------------------------- */}
            {page?.socialLinks && page.socialLinks.length > 0 && (
              <div className="pt-12 md:pt-16 border-t border-neutral-200 dark:border-neutral-800">
                {/* Section Label */}
                <p className="text-center text-xs tracking-[0.3em] uppercase text-neutral-500 dark:text-neutral-500 font-medium mb-10">
                  Connect
                </p>

                {/* Social Links Grid */}
                <div className="flex flex-wrap justify-center gap-4 md:gap-6">
                  {page.socialLinks.map((social, index) => (
                    <a
                      key={social._key || index}
                      href={social.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      aria-label={`Follow on ${getPlatformLabel(social.platform)}`}
                      className={`
                        group flex items-center gap-3
                        px-6 py-4 md:px-8 md:py-5
                        bg-neutral-50 dark:bg-neutral-900
                        border border-neutral-200 dark:border-neutral-800
                        text-neutral-700 dark:text-neutral-300
                        font-medium tracking-wide
                        transition-all duration-300
                        hover:bg-neutral-900 dark:hover:bg-white
                        hover:text-white dark:hover:text-neutral-900
                        hover:border-neutral-900 dark:hover:border-white
                        hover:scale-[1.02] hover:shadow-lg
                        focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
                        animate-fade-up
                      `}
                      style={{ animationDelay: `${300 + index * 50}ms` }}
                    >
                      {/* Platform Icon */}
                      <span className="transition-transform duration-300 group-hover:scale-110">
                        {socialIcons[social.platform]}
                      </span>

                      {/* Platform Label */}
                      <span className="hidden sm:inline">
                        {getPlatformLabel(social.platform)}
                      </span>
                    </a>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* ----------------------------------------
              BACK TO HOME LINK
              ---------------------------------------- */}
          <div className="mt-24 md:mt-32 text-center animate-fade-up animation-delay-400">
            <Link
              href="/"
              className="
                inline-flex items-center gap-3
                text-neutral-500 dark:text-neutral-500
                text-sm tracking-wide uppercase
                transition-colors duration-300
                hover:text-neutral-900 dark:hover:text-neutral-100
                group
              "
            >
              <svg
                className="w-4 h-4 transition-transform duration-300 group-hover:-translate-x-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
              </svg>
              <span>Back to Home</span>
            </Link>
          </div>
        </div>
      </section>

      {/* ============================================
          DECORATIVE FOOTER ACCENT
          ============================================ */}
      <div
        className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-brand-300/50 to-transparent"
        aria-hidden="true"
      />
    </article>
  )
}
