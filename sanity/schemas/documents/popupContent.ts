// sanity/schemas/documents/popupContent.ts
import { defineType, defineField } from 'sanity'
import { SparklesIcon } from '@sanity/icons'

export const popupContent = defineType({
  name: 'popupContent',
  title: 'Popup Content',
  type: 'document',
  icon: SparklesIcon,
  description: 'Reusable content that appears when clicking on images',
  fields: [
    defineField({
      name: 'title',
      title: 'Title',
      type: 'string',
      description: 'e.g., "Vintage Dior Jacket"',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'description',
      title: 'Description',
      type: 'text',
      rows: 4,
      description: 'Details about the item, styling notes, etc.',
    }),
    defineField({
      name: 'link',
      title: 'Link URL',
      type: 'url',
      description: 'Optional link to more info',
      validation: (Rule) =>
        Rule.uri({
          scheme: ['http', 'https'],
        }),
    }),
    defineField({
      name: 'linkText',
      title: 'Link Text',
      type: 'string',
      description: 'e.g., "View Collection", "Shop Now"',
    }),
    defineField({
      name: 'tags',
      title: 'Tags',
      type: 'array',
      of: [{ type: 'string' }],
      options: {
        layout: 'tags',
      },
      description: 'e.g., "Designer", "Vintage", "SS22"',
    }),
  ],
  preview: {
    select: {
      title: 'title',
      description: 'description',
    },
    prepare({ title, description }) {
      return {
        title,
        subtitle: description?.slice(0, 50) + (description?.length > 50 ? '...' : '') || 'No description',
      }
    },
  },
})
