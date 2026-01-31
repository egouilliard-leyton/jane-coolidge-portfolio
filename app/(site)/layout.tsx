// app/(site)/layout.tsx
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import SiteLayoutClient from './SiteLayoutClient'
import SkipLink from '@/components/ui/SkipLink'

/**
 * Site Layout
 *
 * Wraps all public-facing pages with the Header and Footer components.
 * The Header and Footer are Server Components that fetch their own data.
 * Page content is wrapped in SiteLayoutClient for smooth page transitions.
 * Includes a skip link for keyboard accessibility.
 */
export default function SiteLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <SkipLink />
      <Header />
      <SiteLayoutClient>
        {children}
      </SiteLayoutClient>
      <Footer />
    </>
  )
}
