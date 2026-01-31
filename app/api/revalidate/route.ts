// app/api/revalidate/route.ts
import { revalidateTag, revalidatePath } from 'next/cache'
import { type NextRequest, NextResponse } from 'next/server'
import { parseBody } from 'next-sanity/webhook'

// Define the webhook payload type
type WebhookPayload = {
  _type: string
  _id?: string
  slug?: { current?: string }
}

// Map document types to their cache tags
// This ensures consistency with how tags are used in sanityFetch calls
const documentTypeToTags: Record<string, string[]> = {
  // Single page types
  homepage: ['homepage'],
  aboutPage: ['aboutPage'],
  contactPage: ['contactPage'],
  siteSettings: ['siteSettings'],
  navigation: ['navigation'],
  // Collection types
  blogPost: ['blogPost'],
  project: ['project'],
  popupContent: ['popupContent'],
}

// Map document types to their detail page paths (for slug-based content)
const documentTypeToPath: Record<string, string> = {
  blogPost: '/blog',
  project: '/projects',
}

export async function POST(req: NextRequest) {
  try {
    // Check for the revalidation secret
    if (!process.env.SANITY_REVALIDATE_SECRET) {
      console.error('[Revalidate] Missing SANITY_REVALIDATE_SECRET environment variable')
      return new Response(
        JSON.stringify({ message: 'Missing environment variable SANITY_REVALIDATE_SECRET' }),
        { status: 500 }
      )
    }

    // Parse and validate the webhook payload
    // The third parameter (true) waits for Content Lake eventual consistency
    const { isValidSignature, body } = await parseBody<WebhookPayload>(
      req,
      process.env.SANITY_REVALIDATE_SECRET,
      true // Wait up to 3 seconds for Content Lake consistency
    )

    // Log the incoming webhook for debugging
    console.log('[Revalidate] Received webhook:', {
      isValidSignature,
      type: body?._type,
      id: body?._id,
      slug: body?.slug?.current,
      timestamp: new Date().toISOString(),
    })

    // Validate signature
    if (!isValidSignature) {
      console.warn('[Revalidate] Invalid signature received')
      return new Response(
        JSON.stringify({
          message: 'Invalid signature',
          isValidSignature,
        }),
        { status: 401 }
      )
    }

    // Validate payload
    if (!body?._type) {
      console.warn('[Revalidate] Bad request: missing _type')
      return new Response(
        JSON.stringify({ message: 'Bad Request: missing _type in payload' }),
        { status: 400 }
      )
    }

    const { _type, slug } = body
    const revalidatedTags: string[] = []
    const revalidatedPaths: string[] = []

    // Revalidate by document type tags
    const tags = documentTypeToTags[_type]
    if (tags) {
      for (const tag of tags) {
        revalidateTag(tag)
        revalidatedTags.push(tag)
      }
    } else {
      // For unknown types, use the type name as the tag
      revalidateTag(_type)
      revalidatedTags.push(_type)
    }

    // If the document has a slug, revalidate the specific page path
    if (slug?.current && documentTypeToPath[_type]) {
      const path = `${documentTypeToPath[_type]}/${slug.current}`
      revalidatePath(path)
      revalidatedPaths.push(path)
    }

    // For singleton pages, revalidate their specific paths
    const singletonPaths: Record<string, string> = {
      homepage: '/',
      aboutPage: '/about',
      contactPage: '/contact',
    }

    if (singletonPaths[_type]) {
      revalidatePath(singletonPaths[_type])
      revalidatedPaths.push(singletonPaths[_type])
    }

    // For settings/navigation, revalidate the entire site layout
    if (_type === 'siteSettings' || _type === 'navigation') {
      revalidatePath('/', 'layout')
      revalidatedPaths.push('/ (layout)')
    }

    // For blog posts or projects, also revalidate listing pages
    if (_type === 'blogPost') {
      revalidatePath('/blog')
      revalidatedPaths.push('/blog')
      // Homepage shows featured posts
      revalidatePath('/')
      revalidatedPaths.push('/')
    }

    if (_type === 'project') {
      revalidatePath('/projects')
      revalidatedPaths.push('/projects')
      // Homepage shows featured projects
      revalidatePath('/')
      revalidatedPaths.push('/')
    }

    console.log('[Revalidate] Successfully revalidated:', {
      type: _type,
      tags: revalidatedTags,
      paths: revalidatedPaths,
      timestamp: new Date().toISOString(),
    })

    return NextResponse.json({
      revalidated: true,
      now: Date.now(),
      type: _type,
      tags: revalidatedTags,
      paths: revalidatedPaths,
    })
  } catch (err) {
    console.error('[Revalidate] Error processing webhook:', err)
    return new Response(
      JSON.stringify({
        message: 'Error processing webhook',
        error: err instanceof Error ? err.message : 'Unknown error',
      }),
      { status: 500 }
    )
  }
}

// Handle GET requests for health checks / testing
export async function GET() {
  return NextResponse.json({
    status: 'ok',
    message: 'Revalidation webhook endpoint is active',
    timestamp: new Date().toISOString(),
  })
}
