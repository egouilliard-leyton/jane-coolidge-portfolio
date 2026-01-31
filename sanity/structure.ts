// sanity/structure.ts
import type { StructureResolver } from 'sanity/structure'
import {
  DocumentIcon,
  HomeIcon,
  CogIcon,
  ComposeIcon,
  ImageIcon,
  UsersIcon,
} from '@sanity/icons'

export const structure: StructureResolver = (S) =>
  S.list()
    .title('Content')
    .items([
      // Pages Section
      S.listItem()
        .title('Pages')
        .icon(DocumentIcon)
        .child(
          S.list()
            .title('Pages')
            .items([
              // Homepage (singleton)
              S.listItem()
                .title('Homepage')
                .icon(HomeIcon)
                .child(
                  S.document()
                    .schemaType('homepage')
                    .documentId('homepage')
                ),
              // About Page (singleton)
              S.listItem()
                .title('About')
                .icon(UsersIcon)
                .child(
                  S.document()
                    .schemaType('aboutPage')
                    .documentId('aboutPage')
                ),
              // Contact Page (singleton)
              S.listItem()
                .title('Contact')
                .icon(ComposeIcon)
                .child(
                  S.document()
                    .schemaType('contactPage')
                    .documentId('contactPage')
                ),
            ])
        ),

      S.divider(),

      // Blog Posts
      S.listItem()
        .title('Blog Posts')
        .icon(ComposeIcon)
        .child(
          S.documentTypeList('blogPost')
            .title('Blog Posts')
        ),

      // Projects/Portfolio
      S.listItem()
        .title('Projects')
        .icon(ImageIcon)
        .child(
          S.documentTypeList('project')
            .title('Projects')
        ),

      S.divider(),

      // Popup Content
      S.listItem()
        .title('Popup Content')
        .icon(ImageIcon)
        .child(
          S.documentTypeList('popupContent')
            .title('Popup Content')
        ),

      S.divider(),

      // Settings Section
      S.listItem()
        .title('Settings')
        .icon(CogIcon)
        .child(
          S.list()
            .title('Settings')
            .items([
              S.listItem()
                .title('Site Settings')
                .icon(CogIcon)
                .child(
                  S.document()
                    .schemaType('siteSettings')
                    .documentId('siteSettings')
                ),
              S.listItem()
                .title('Navigation')
                .child(
                  S.document()
                    .schemaType('navigation')
                    .documentId('navigation')
                ),
            ])
        ),
    ])
