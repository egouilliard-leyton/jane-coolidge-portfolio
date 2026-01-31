// sanity/schemas/documents/aboutPage.ts
import { defineType, defineField } from 'sanity'
import { UsersIcon } from '@sanity/icons'

export const aboutPage = defineType({
  name: 'aboutPage',
  title: 'About Page',
  type: 'document',
  icon: UsersIcon,
  fields: [
    defineField({
      name: 'heading',
      title: 'Page Heading',
      type: 'string',
      initialValue: 'About',
    }),
    defineField({
      name: 'profileImage',
      title: 'Profile Image',
      type: 'image',
      options: {
        hotspot: true,
      },
      fields: [
        {
          name: 'alt',
          type: 'string',
          title: 'Alt Text',
          validation: (Rule) => Rule.required(),
        },
      ],
    }),
    defineField({
      name: 'name',
      title: 'Name',
      type: 'string',
    }),
    defineField({
      name: 'tagline',
      title: 'Tagline',
      type: 'string',
      description: 'e.g., "Fashion Stylist & Creative Director"',
    }),
    defineField({
      name: 'bio',
      title: 'Biography',
      type: 'portableText',
    }),
    defineField({
      name: 'credentials',
      title: 'Credentials / Experience',
      type: 'array',
      of: [
        {
          type: 'object',
          name: 'credential',
          fields: [
            {
              name: 'title',
              type: 'string',
              title: 'Title/Role',
              validation: (Rule) => Rule.required(),
            },
            {
              name: 'organization',
              type: 'string',
              title: 'Organization',
            },
            {
              name: 'period',
              type: 'string',
              title: 'Time Period',
            },
          ],
          preview: {
            select: {
              title: 'title',
              organization: 'organization',
            },
            prepare({ title, organization }) {
              return {
                title,
                subtitle: organization,
              }
            },
          },
        },
      ],
    }),
    defineField({
      name: 'clients',
      title: 'Notable Clients',
      type: 'array',
      of: [{ type: 'string' }],
      options: {
        layout: 'tags',
      },
    }),
    defineField({
      name: 'seo',
      title: 'SEO',
      type: 'seo',
    }),
  ],
  preview: {
    prepare() {
      return {
        title: 'About Page',
      }
    },
  },
})
