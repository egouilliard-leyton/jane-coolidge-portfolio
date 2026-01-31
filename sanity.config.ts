// sanity.config.ts
import { defineConfig } from 'sanity'
import { structureTool } from 'sanity/structure'
import { media } from 'sanity-plugin-media'

import { schemaTypes } from './sanity/schemas'
import { structure } from './sanity/structure'

const projectId = process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!
const dataset = process.env.NEXT_PUBLIC_SANITY_DATASET!

export default defineConfig({
  name: 'fashion-website',
  title: 'Fashion Website',

  projectId,
  dataset,

  basePath: '/studio', // Studio accessible at /studio

  plugins: [
    structureTool({
      structure, // Custom sidebar structure
    }),
    // Note: visionTool temporarily disabled due to React 19 compatibility issue
    // Can be re-enabled when @sanity/vision is updated for full React 19 support
    // visionTool({ defaultApiVersion: '2024-01-01' }),
    media(), // Media library plugin
  ],

  schema: {
    types: schemaTypes,
  },
})
