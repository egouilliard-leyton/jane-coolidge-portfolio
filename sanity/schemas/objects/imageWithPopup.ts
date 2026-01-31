// sanity/schemas/objects/imageWithPopup.ts
import { defineType, defineField } from 'sanity'
import { ImageIcon } from '@sanity/icons'

export const imageWithPopup = defineType({
  name: 'imageWithPopup',
  title: 'Image',
  type: 'object',
  icon: ImageIcon,
  fields: [
    defineField({
      name: 'image',
      title: 'Image',
      type: 'image',
      options: {
        hotspot: true, // Enables image cropping
      },
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'alt',
      title: 'Alt Text',
      type: 'string',
      description: 'Important for SEO and accessibility',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'caption',
      title: 'Caption',
      type: 'string',
      description: 'Optional caption shown below the image',
    }),
    defineField({
      name: 'popup',
      title: 'Popup Content',
      type: 'reference',
      to: [{ type: 'popupContent' }],
      description: 'Optional: Link to popup content that appears on click',
    }),
    defineField({
      name: 'size',
      title: 'Display Size',
      type: 'string',
      options: {
        list: [
          { title: 'Small (50%)', value: 'small' },
          { title: 'Medium (75%)', value: 'medium' },
          { title: 'Large (100%)', value: 'large' },
          { title: 'Full Width', value: 'full' },
        ],
        layout: 'radio',
      },
      initialValue: 'large',
    }),
  ],
  preview: {
    select: {
      media: 'image',
      title: 'alt',
      hasPopup: 'popup',
    },
    prepare({ media, title, hasPopup }) {
      return {
        title: title || 'Image',
        subtitle: hasPopup ? 'Has popup' : 'No popup',
        media,
      }
    },
  },
})
