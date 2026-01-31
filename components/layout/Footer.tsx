// components/layout/Footer.tsx
import { sanityFetch } from '@/sanity/lib/client'
import {
  siteSettingsQuery,
  type SiteSettingsResult,
} from '@/sanity/lib/queries'
import FooterClient from './FooterClient'

/**
 * Footer component - Server Component wrapper
 *
 * Fetches site settings from Sanity CMS (including footer text,
 * social links, and site name), then renders the FooterClient component.
 *
 * Data is cached and revalidated based on the tags provided.
 */
export default async function Footer() {
  const settings = await sanityFetch<SiteSettingsResult | null>({
    query: siteSettingsQuery,
    tags: ['siteSettings'],
  })

  return <FooterClient settings={settings} />
}
