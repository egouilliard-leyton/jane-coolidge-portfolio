// sanity/schemas/index.ts

// Document types
import { blogPost } from './documents/blogPost'
import { project } from './documents/project'
import { popupContent } from './documents/popupContent'
import { homepage } from './documents/homepage'
import { aboutPage } from './documents/aboutPage'
import { contactPage } from './documents/contactPage'
import { siteSettings } from './documents/siteSettings'
import { navigation } from './documents/navigation'

// Object types
import { portableText } from './objects/portableText'
import { imageWithPopup } from './objects/imageWithPopup'
import { seo } from './objects/seo'
import { socialLink } from './objects/socialLink'

export const schemaTypes = [
  // Documents
  blogPost,
  project,
  popupContent,
  homepage,
  aboutPage,
  contactPage,
  siteSettings,
  navigation,
  // Objects
  portableText,
  imageWithPopup,
  seo,
  socialLink,
]
