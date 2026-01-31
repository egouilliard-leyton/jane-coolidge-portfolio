# AGENTS.md

> This file captures codebase patterns and conventions discovered during automated development.
> AI agents read this file to understand project-specific context.
> Updates are made by automation runs - manual edits may be overwritten.

## Codebase Patterns

### Architecture

- **App Router Pattern**: Use Next.js 15 App Router with route groups `(site)` for public pages, `studio/[[...tool]]` for Sanity Studio
- **Data Fetching**: Server Components fetch data via `sanityFetch()` helper with cache tags for revalidation
- **Content Model**: Singletons for pages (homepage, about, contact), Collections for blog/projects
- **Image Handling**: Use `urlFor()` from `@sanity/image-url` with LQIP blur placeholders from Sanity metadata
- **Portable Text**: Custom renderers via `@portabletext/react` with typed components
- **Interactive Popups**: `imageWithPopup` schema links to `popupContent` documents, rendered as click-triggered modals

### Naming Conventions

- **Schema Files**: camelCase (e.g., `blogPost.ts`, `imageWithPopup.ts`)
- **Components**: PascalCase with descriptive names (e.g., `ImageWithPopup.tsx`, `BlogContent.tsx`)
- **GROQ Queries**: Descriptive names ending in `Query` (e.g., `homepageQuery`, `blogPostBySlugQuery`)
- **TypeScript Types**: PascalCase interfaces matching Sanity document types (e.g., `BlogPost`, `Homepage`)
- **CSS Variables**: kebab-case with `--` prefix (e.g., `--font-playfair`, `--color-background`)

### Testing Patterns

- No testing framework specified in documentation
- Manual verification workflow: run `npm run build` locally before deployment
- Preview deployments on Vercel for PR review

### Common Gotchas

- **Client Components**: Add `'use client'` directive for components using hooks, motion, or interactivity
- **Sanity CORS**: Must add localhost:3000 and production domain in Sanity dashboard
- **Webhook Secret**: Must match exactly between Vercel env var and Sanity webhook config
- **Image URLs**: Always use `urlFor()` helper, never raw asset URLs
- **Dynamic Routes**: Use `generateStaticParams` for static generation, set `dynamicParams = true` for fallback

---

## Technology Stack

- **Frontend**: Next.js 15 (App Router) + React 19
- **CMS**: Sanity (Content Lake + embedded Studio at /studio)
- **Styling**: Tailwind CSS 4 + @tailwindcss/typography
- **Animations**: Motion (Framer Motion)
- **Deployment**: Vercel (auto CI/CD from GitHub)
- **Fonts**: Google Fonts (Inter, Playfair Display)

---

## File Organization

```
fashion-website/
├── app/
│   ├── (site)/                   # Public routes with shared layout
│   │   ├── page.tsx              # Homepage
│   │   ├── about/page.tsx
│   │   ├── contact/page.tsx
│   │   ├── blog/
│   │   │   ├── page.tsx          # Listing with pagination
│   │   │   └── [slug]/page.tsx   # Dynamic post pages
│   │   └── layout.tsx            # Header/Footer wrapper
│   ├── studio/[[...tool]]/       # Sanity Studio catch-all
│   ├── api/revalidate/route.ts   # Webhook endpoint
│   ├── layout.tsx                # Root layout (fonts, metadata)
│   └── globals.css               # Tailwind imports + CSS vars
├── components/
│   ├── layout/                   # Header.tsx, Footer.tsx
│   ├── blog/                     # BlogContent.tsx
│   ├── ui/                       # ImageWithPopup.tsx, Button.tsx
│   └── animations/               # Motion-based components
├── sanity/
│   ├── schemas/
│   │   ├── documents/            # blogPost, project, homepage, etc.
│   │   ├── objects/              # portableText, imageWithPopup, seo
│   │   └── index.ts              # Schema exports
│   ├── lib/
│   │   ├── client.ts             # Sanity client + sanityFetch
│   │   ├── queries.ts            # All GROQ queries
│   │   ├── image.ts              # urlFor() helper
│   │   ├── live.ts               # Live content API
│   │   └── types.ts              # TypeScript interfaces
│   └── structure.ts              # Studio sidebar config
├── sanity.config.ts              # Studio plugins + schema
├── tailwind.config.ts            # Theme + brand colors
└── .env.local                    # Environment variables
```

---

## Recent Learnings

### T-001 - Documentation Review (2026-01-31)

- Complete 8-doc technical specification reviewed
- Architecture: Next.js 15 + Sanity CMS + Vercel
- Key feature: Interactive image popups for styling notes
- Content model uses singletons for pages, collections for blog/projects
- Data flow: Sanity → GROQ → Server Components → Webhooks for revalidation

---

*Last updated: 2026-01-31 by T-001 documentation review task*
