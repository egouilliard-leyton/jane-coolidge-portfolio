// app/(site)/about/page.tsx
import type { Metadata } from 'next'
import Image from 'next/image'
import { PortableText, type PortableTextBlock } from '@portabletext/react'

import { sanityFetch } from '@/sanity/lib/client'
import { urlFor } from '@/sanity/lib/image'
import { aboutPageQuery, type AboutPageResult } from '@/sanity/lib/queries'
import type { Credential } from '@/types/sanity'

/**
 * Generate metadata for the about page
 */
export async function generateMetadata(): Promise<Metadata> {
  const page = await sanityFetch<AboutPageResult | null>({
    query: aboutPageQuery,
    tags: ['aboutPage'],
  })

  return {
    title: page?.seo?.metaTitle || 'About',
    description: page?.seo?.metaDescription || page?.tagline || 'About the stylist',
    openGraph: {
      images: page?.seo?.ogImage?.asset?.url
        ? [{ url: page.seo.ogImage.asset.url }]
        : page?.profileImage?.asset?.url
          ? [{ url: page.profileImage.asset.url }]
          : [],
    },
  }
}

/**
 * AboutPage - Server Component
 *
 * A bold, editorial-style about page featuring:
 * - Asymmetric split-screen hero with profile image
 * - Elegant typography with display fonts
 * - Timeline-inspired credentials section
 * - Scattered client cloud with artistic placement
 */
export default async function AboutPage() {
  const page = await sanityFetch<AboutPageResult | null>({
    query: aboutPageQuery,
    tags: ['aboutPage'],
  })

  return (
    <article className="relative">
      {/* ============================================
          HERO SECTION - Split Screen Editorial
          ============================================ */}
      <section className="relative min-h-[90vh] flex flex-col lg:flex-row" aria-label="Introduction">
        {/* Left: Profile Image with Overlap Effect */}
        <div className="relative lg:w-1/2 h-[60vh] lg:h-auto lg:min-h-[90vh] order-2 lg:order-1">
          {/* Decorative Background Shape */}
          <div
            className="absolute inset-0 bg-gradient-to-br from-brand-100 via-brand-50 to-neutral-100 dark:from-brand-950 dark:via-neutral-900 dark:to-neutral-950"
            aria-hidden="true"
          />

          {/* Profile Image Container */}
          <div className="relative h-full flex items-center justify-center p-8 lg:p-16">
            {page?.profileImage?.asset?.url ? (
              <div className="relative w-full max-w-md lg:max-w-lg xl:max-w-xl aspect-[3/4] animate-fade-up">
                {/* Image Shadow/Depth Effect */}
                <div
                  className="absolute -bottom-6 -right-6 w-full h-full bg-brand-300/30 dark:bg-brand-700/20 rounded-sm"
                  aria-hidden="true"
                />
                <div
                  className="absolute -bottom-3 -right-3 w-full h-full bg-brand-200/50 dark:bg-brand-800/30 rounded-sm"
                  aria-hidden="true"
                />

                {/* Main Image */}
                <div className="relative w-full h-full overflow-hidden rounded-sm shadow-2xl">
                  <Image
                    src={urlFor(page.profileImage).width(800).height(1067).quality(90).auto('format').url()}
                    alt={page.name || 'Profile'}
                    fill
                    priority
                    fetchPriority="high"
                    className="object-cover"
                    placeholder={page.profileImage.asset.metadata?.lqip ? 'blur' : undefined}
                    blurDataURL={page.profileImage.asset.metadata?.lqip}
                    sizes="(max-width: 1024px) 90vw, 45vw"
                  />
                </div>

                {/* Floating Accent Line */}
                <div
                  className="absolute -left-8 top-1/3 w-24 h-px bg-brand-500"
                  aria-hidden="true"
                />
              </div>
            ) : (
              <div className="w-full max-w-md aspect-[3/4] bg-neutral-200 dark:bg-neutral-800 rounded-sm" />
            )}
          </div>
        </div>

        {/* Right: Name, Tagline & Introduction */}
        <div className="lg:w-1/2 flex flex-col justify-center order-1 lg:order-2 bg-white dark:bg-neutral-950 px-8 py-16 lg:px-16 xl:px-24 min-h-[50vh] lg:min-h-0">
          <div className="max-w-xl animate-fade-up">
            {/* Decorative Label */}
            <div className="mb-8 flex items-center gap-4" aria-hidden="true">
              <div className="w-16 h-px bg-brand-400" />
              <span className="text-brand-500 text-xs tracking-[0.4em] uppercase font-medium">
                {page?.heading || 'About'}
              </span>
            </div>

            {/* Name - Large Display Typography */}
            {page?.name && (
              <h1 className="font-display text-5xl sm:text-6xl lg:text-7xl xl:text-8xl text-neutral-900 dark:text-neutral-100 tracking-tight leading-[0.9] mb-6 animate-fade-up animation-delay-100">
                {page.name.split(' ').map((word, i) => (
                  <span key={i} className="block">
                    {word}
                  </span>
                ))}
              </h1>
            )}

            {/* Tagline - Elegant Italic Serif */}
            {page?.tagline && (
              <p className="font-serif text-xl sm:text-2xl lg:text-3xl text-brand-700 dark:text-brand-400 italic leading-relaxed mb-8 animate-fade-up animation-delay-200">
                {page.tagline}
              </p>
            )}

            {/* Scroll Indicator */}
            <div className="mt-12 animate-fade-up animation-delay-400">
              <div className="flex items-center gap-3 text-neutral-400 dark:text-neutral-600 text-xs tracking-[0.3em] uppercase">
                <svg
                  className="w-4 h-4 animate-bounce"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                  aria-hidden="true"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                </svg>
                <span>Read my story</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ============================================
          BIOGRAPHY SECTION - Full Width Editorial
          ============================================ */}
      {page?.bio && Array.isArray(page.bio) && page.bio.length > 0 && (
        <section
          className="py-24 md:py-32 lg:py-40 bg-neutral-50 dark:bg-neutral-900"
          aria-labelledby="biography-heading"
        >
          <div className="mx-auto max-w-7xl px-8 lg:px-16">
            {/* Section Header */}
            <header className="mb-16 md:mb-20">
              <h2
                id="biography-heading"
                className="sr-only"
              >
                Biography
              </h2>
              <div className="flex items-center gap-6" aria-hidden="true">
                <span className="text-brand-500 text-8xl md:text-9xl font-display leading-none opacity-20 select-none">
                  &ldquo;
                </span>
              </div>
            </header>

            {/* Biography Content - Large, Elegant Typography */}
            <div className="grid lg:grid-cols-12 gap-12">
              {/* Main Bio Text */}
              <div className="lg:col-span-8 lg:col-start-3">
                <div className="prose prose-xl lg:prose-2xl prose-neutral dark:prose-invert max-w-none">
                  <div className="font-serif text-xl md:text-2xl lg:text-3xl leading-relaxed text-neutral-700 dark:text-neutral-300 [&>p:first-child]:first-letter:text-6xl [&>p:first-child]:first-letter:font-display [&>p:first-child]:first-letter:float-left [&>p:first-child]:first-letter:mr-4 [&>p:first-child]:first-letter:mt-2 [&>p:first-child]:first-letter:leading-[0.8] [&>p:first-child]:first-letter:text-brand-600 dark:[&>p:first-child]:first-letter:text-brand-400 [&>p]:mb-8">
                    <PortableText value={page.bio as PortableTextBlock[]} />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* ============================================
          CREDENTIALS SECTION - Timeline Style
          ============================================ */}
      {page?.credentials && page.credentials.length > 0 && (
        <section
          className="py-24 md:py-32 bg-white dark:bg-neutral-950"
          aria-labelledby="experience-heading"
        >
          <div className="mx-auto max-w-7xl px-8 lg:px-16">
            {/* Section Header */}
            <header className="mb-16 md:mb-24 max-w-3xl">
              <div className="flex items-center gap-4 mb-6" aria-hidden="true">
                <div className="w-12 h-px bg-brand-400" />
                <span className="text-brand-500 text-xs tracking-[0.4em] uppercase font-medium">
                  Career
                </span>
              </div>
              <h2
                id="experience-heading"
                className="font-display text-4xl md:text-5xl lg:text-6xl text-neutral-900 dark:text-neutral-100 tracking-tight"
              >
                Experience &<br />
                <span className="text-brand-600 dark:text-brand-400">Credentials</span>
              </h2>
            </header>

            {/* Timeline Grid */}
            <div className="relative">
              {/* Vertical Timeline Line */}
              <div
                className="absolute left-0 md:left-1/4 top-0 bottom-0 w-px bg-gradient-to-b from-brand-400 via-brand-300 to-transparent hidden md:block"
                aria-hidden="true"
              />

              {/* Credentials List */}
              <div className="space-y-0">
                {page.credentials.map((credential, index) => (
                  <CredentialItem
                    key={credential._key || index}
                    credential={credential}
                    index={index}
                    isLast={index === page.credentials!.length - 1}
                  />
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* ============================================
          CLIENTS SECTION - Artistic Tag Cloud
          ============================================ */}
      {page?.clients && page.clients.length > 0 && (
        <section
          className="py-24 md:py-32 lg:py-40 bg-neutral-900 dark:bg-black overflow-hidden relative"
          aria-labelledby="clients-heading"
        >
          {/* Background Pattern */}
          <div
            className="absolute inset-0 opacity-[0.03]"
            style={{
              backgroundImage: `radial-gradient(circle at 1px 1px, white 1px, transparent 0)`,
              backgroundSize: '40px 40px',
            }}
            aria-hidden="true"
          />

          <div className="relative mx-auto max-w-7xl px-8 lg:px-16">
            {/* Section Header */}
            <header className="mb-16 md:mb-24 text-center">
              <div className="flex items-center justify-center gap-4 mb-6" aria-hidden="true">
                <div className="w-12 h-px bg-brand-400" />
                <span className="text-brand-400 text-xs tracking-[0.4em] uppercase font-medium">
                  Collaborations
                </span>
                <div className="w-12 h-px bg-brand-400" />
              </div>
              <h2
                id="clients-heading"
                className="font-display text-4xl md:text-5xl lg:text-6xl text-white tracking-tight mb-6"
              >
                Notable Clients
              </h2>
              <p className="text-neutral-400 text-lg max-w-2xl mx-auto">
                Trusted by leading brands and publications across the fashion industry
              </p>
            </header>

            {/* Client Cloud - Artistic Scattered Layout */}
            <div className="relative">
              {/* Client Tags */}
              <div className="flex flex-wrap justify-center gap-4 md:gap-6">
                {page.clients.map((client, index) => (
                  <ClientTag key={client} client={client} index={index} />
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* ============================================
          CTA SECTION - Simple & Elegant
          ============================================ */}
      <section
        className="py-24 md:py-32 bg-brand-50 dark:bg-brand-950/30"
        aria-label="Contact call to action"
      >
        <div className="mx-auto max-w-4xl px-8 text-center">
          <p className="font-serif text-2xl md:text-3xl lg:text-4xl text-neutral-700 dark:text-neutral-300 italic leading-relaxed mb-10">
            Interested in working together?
          </p>
          <a
            href="/contact"
            className="
              inline-flex items-center gap-3
              px-10 py-5
              bg-neutral-900 dark:bg-white
              text-white dark:text-neutral-900
              font-medium text-lg tracking-wide
              transition-all duration-300
              hover:bg-brand-700 dark:hover:bg-brand-200
              focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
              group
            "
          >
            <span>Get in Touch</span>
            <svg
              className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </a>
        </div>
      </section>
    </article>
  )
}

/**
 * CredentialItem - Timeline-style credential entry
 */
function CredentialItem({
  credential,
  index,
  isLast
}: {
  credential: Credential
  index: number
  isLast: boolean
}) {
  return (
    <div className="relative grid md:grid-cols-4 gap-6 md:gap-12 py-8 md:py-12 group">
      {/* Timeline Dot */}
      <div
        className="hidden md:flex absolute left-1/4 top-12 -translate-x-1/2 items-center justify-center"
        aria-hidden="true"
      >
        <div className="w-4 h-4 rounded-full bg-white dark:bg-neutral-950 border-2 border-brand-400 group-hover:bg-brand-400 transition-colors duration-300" />
      </div>

      {/* Period - Left Column */}
      <div className="md:text-right md:pr-12">
        <span className="text-sm tracking-widest uppercase text-brand-600 dark:text-brand-400 font-medium">
          {credential.period}
        </span>
      </div>

      {/* Content - Right Columns */}
      <div className="md:col-span-3 md:pl-12">
        <h3 className="font-display text-2xl md:text-3xl text-neutral-900 dark:text-neutral-100 mb-2 group-hover:text-brand-700 dark:group-hover:text-brand-400 transition-colors duration-300">
          {credential.title}
        </h3>
        {credential.organization && (
          <p className="text-neutral-600 dark:text-neutral-400 text-lg">
            {credential.organization}
          </p>
        )}
      </div>

      {/* Separator Line */}
      {!isLast && (
        <div
          className="absolute bottom-0 left-0 right-0 h-px bg-neutral-200 dark:bg-neutral-800"
          aria-hidden="true"
        />
      )}
    </div>
  )
}

/**
 * ClientTag - Individual client badge with hover effect
 */
function ClientTag({ client, index }: { client: string; index: number }) {
  // Create varied sizes and subtle animation delays for visual interest
  const sizes = ['text-base', 'text-lg', 'text-xl', 'text-2xl']
  const sizeIndex = index % sizes.length
  const delays = ['animation-delay-100', 'animation-delay-200', 'animation-delay-300', 'animation-delay-400', 'animation-delay-500']
  const delayClass = delays[index % delays.length]

  // Alternate between filled and outlined styles
  const isOutlined = index % 3 === 0

  return (
    <span
      className={`
        inline-block px-6 py-3 md:px-8 md:py-4
        ${isOutlined
          ? 'border border-neutral-500 text-neutral-300 hover:border-brand-400 hover:text-white'
          : 'bg-neutral-800 text-neutral-200 hover:bg-brand-700 hover:text-white'
        }
        ${sizes[sizeIndex]}
        font-medium tracking-wide
        transition-all duration-300
        hover:scale-105
        rounded-full
        animate-fade-up ${delayClass}
      `}
    >
      {client}
    </span>
  )
}
