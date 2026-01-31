// Script to upload images to Sanity and link to projects
import { createClient } from '@sanity/client'
import { readFileSync, readdirSync } from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Sanity client configuration
const client = createClient({
  projectId: 'xp9jnodv',
  dataset: 'production',
  apiVersion: '2024-01-01',
  token: process.env.SANITY_TOKEN,
  useCdn: false,
})

// Mapping of image files to projects (based on PDF page order)
const imageMapping = [
  { file: 'img-0000.jpg', projectId: 'project-ethereal-vessel', alt: 'Ethereal Vessel - Hand sculpted coil pot with glossy dark glaze' },
  { file: 'img-0001.jpg', projectId: 'project-tidebound-top', alt: 'Tidebound Top - Black crochet top with resin shells' },
  { file: 'img-0002.jpg', projectId: 'project-fruitful-glass', alt: 'Fruitful Glass - Hand painted wine glasses with fruit designs' },
  { file: 'img-0003.jpg', projectId: 'project-netborne-top', alt: 'Netborne Top - Brown crochet top with shells' },
  { file: 'img-0004.jpg', projectId: 'project-walking-woods', alt: 'Walking Woods - Watercolor landscape with winding path' },
  { file: 'img-0005.jpg', projectId: 'project-confidence-through-color', alt: 'Confidence Through Color - Bold portrait with orange hat' },
  { file: 'img-0006.jpg', projectId: 'project-fyp-beer-label', alt: 'FYP Beer Label - Custom beer bottle label design' },
  { file: 'img-0008.jpg', projectId: 'project-primary-legends', alt: 'Primary Legends - The Beatles pop art illustration' },
  { file: 'img-0009.jpg', projectId: 'project-natural-flow', alt: 'Natural Flow - Clay coil pot with dripping glazes' },
  { file: 'img-0010.jpg', projectId: 'project-tilted', alt: 'Tilted - Self portrait in burnt orange charcoal' },
  { file: 'img-0011.jpg', projectId: 'project-stable-reflection', alt: 'Stable Reflection - White horse painting' },
  { file: 'img-0012.jpg', projectId: 'project-the-gaze', alt: 'The Gaze - Black ink portrait drawing' },
  { file: 'img-0013.jpg', projectId: 'project-cow', alt: 'Cow? - Colored pencil drawing of a cow' },
  { file: 'img-0014.jpg', projectId: 'project-silence-red', alt: 'Silence Red - Expressive portrait with red hair' },
  { file: 'img-0015.jpg', projectId: 'project-childhood', alt: 'Childhood - Beach scene with child digging in sand' },
]

// Use one of the nice images for homepage hero
const heroImage = { file: 'img-0005.jpg', alt: 'Jane Gouilliard Portfolio' }

// Use the self-portrait for about page
const aboutImage = { file: 'img-0010.jpg', alt: 'Jane Gouilliard - Artist self portrait' }

async function uploadImage(filePath, alt) {
  const imageBuffer = readFileSync(filePath)
  const asset = await client.assets.upload('image', imageBuffer, {
    filename: path.basename(filePath),
  })
  return {
    _type: 'image',
    asset: {
      _type: 'reference',
      _ref: asset._id,
    },
    alt: alt,
  }
}

async function main() {
  console.log('Starting image upload to Sanity...\n')
  const imagesDir = path.join(__dirname, 'extracted-images')

  // Upload and link project cover images
  console.log('Uploading project images...')
  for (const mapping of imageMapping) {
    const filePath = path.join(imagesDir, mapping.file)
    try {
      console.log(`  Uploading ${mapping.file} for ${mapping.projectId}...`)
      const imageData = await uploadImage(filePath, mapping.alt)

      // Update the project with the cover image
      await client.patch(mapping.projectId)
        .set({ coverImage: imageData })
        .commit()

      console.log(`  ✓ ${mapping.file} uploaded and linked`)
    } catch (error) {
      console.error(`  ✗ Error uploading ${mapping.file}:`, error.message)
    }
  }

  // Upload hero image for homepage
  console.log('\nUploading homepage hero image...')
  try {
    const heroFilePath = path.join(imagesDir, heroImage.file)
    const heroImageData = await uploadImage(heroFilePath, heroImage.alt)
    await client.patch('homepage')
      .set({ heroImage: heroImageData })
      .commit()
    console.log('✓ Homepage hero image uploaded')
  } catch (error) {
    console.error('✗ Error uploading hero image:', error.message)
  }

  // Upload profile image for about page
  console.log('\nUploading about page profile image...')
  try {
    const aboutFilePath = path.join(imagesDir, aboutImage.file)
    const aboutImageData = await uploadImage(aboutFilePath, aboutImage.alt)
    await client.patch('aboutPage')
      .set({ profileImage: aboutImageData })
      .commit()
    console.log('✓ About page profile image uploaded')
  } catch (error) {
    console.error('✗ Error uploading about image:', error.message)
  }

  console.log('\n' + '='.repeat(50))
  console.log('Image upload complete!')
  console.log('='.repeat(50))
  console.log('\nYour website should now display all images.')
  console.log('Visit: https://jane-website-one.vercel.app')
}

main().catch(console.error)
