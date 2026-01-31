// components/layout/Header.tsx
import { sanityFetch } from '@/sanity/lib/client'
import {
  siteSettingsQuery,
  navigationQuery,
  type SiteSettingsResult,
  type NavigationResult,
} from '@/sanity/lib/queries'
import HeaderClient from './HeaderClient'

/**
 * Header component - Server Component wrapper
 *
 * Fetches navigation and site settings from Sanity CMS,
 * then renders the interactive HeaderClient component.
 *
 * Data is cached and revalidated based on the tags provided.
 */
export default async function Header() {
  // Fetch site settings and navigation in parallel
  const [settings, navigation] = await Promise.all([
    sanityFetch<SiteSettingsResult | null>({
      query: siteSettingsQuery,
      tags: ['siteSettings'],
    }),
    sanityFetch<NavigationResult | null>({
      query: navigationQuery,
      tags: ['navigation'],
    }),
  ])

  return <HeaderClient settings={settings} navigation={navigation} />
}
