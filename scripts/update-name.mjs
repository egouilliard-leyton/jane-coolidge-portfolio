// Script to update name from Jane Gouilliard to Jane Coolidge
import { createClient } from '@sanity/client'

const client = createClient({
  projectId: 'xp9jnodv',
  dataset: 'production',
  apiVersion: '2024-01-01',
  token: process.env.SANITY_TOKEN,
  useCdn: false,
})

async function main() {
  console.log('Updating name from Jane Gouilliard to Jane Coolidge...\n')

  // Update Site Settings
  console.log('Updating Site Settings...')
  await client.patch('siteSettings')
    .set({ siteName: 'Jane Coolidge' })
    .commit()
  console.log('✓ Site Settings updated')

  // Update Homepage
  console.log('Updating Homepage...')
  await client.patch('homepage')
    .set({
      heroHeading: 'Jane Coolidge',
      seo: {
        metaTitle: 'Jane Coolidge | Artist & Designer Portfolio',
        metaDescription: 'Explore the portfolio of Jane Coolidge - ceramics, sustainable fashion, paintings, and illustrations that blend heritage with modern expression.',
      },
    })
    .commit()
  console.log('✓ Homepage updated')

  // Update About Page
  console.log('Updating About Page...')
  await client.patch('aboutPage')
    .set({
      name: 'Jane Coolidge',
      seo: {
        metaTitle: 'About Jane Coolidge | Artist & Designer',
        metaDescription: 'Learn about Jane Coolidge, a multidisciplinary artist working in ceramics, sustainable fashion, painting, and illustration.',
      },
    })
    .commit()
  console.log('✓ About Page updated')

  // Update Contact Page SEO
  console.log('Updating Contact Page...')
  await client.patch('contactPage')
    .set({
      seo: {
        metaTitle: 'Contact Jane Coolidge',
        metaDescription: 'Get in touch with Jane Coolidge for commissions, collaborations, or inquiries about her artwork.',
      },
    })
    .commit()
  console.log('✓ Contact Page updated')

  // Update all project SEO titles
  console.log('Updating Projects...')
  const projects = await client.fetch(`*[_type == "project"]{ _id, title }`)
  for (const project of projects) {
    await client.patch(project._id)
      .set({
        seo: {
          metaTitle: `${project.title} | Jane Coolidge`,
          metaDescription: `View ${project.title} by Jane Coolidge - part of her portfolio of ceramics, fashion, paintings, and illustrations.`,
        },
      })
      .commit()
  }
  console.log(`✓ ${projects.length} Projects updated`)

  // Update hero image alt text
  console.log('Updating image alt texts...')
  await client.patch('homepage')
    .set({ 'heroImage.alt': 'Jane Coolidge Portfolio' })
    .commit()

  await client.patch('aboutPage')
    .set({ 'profileImage.alt': 'Jane Coolidge - Artist self portrait' })
    .commit()
  console.log('✓ Image alt texts updated')

  console.log('\n' + '='.repeat(50))
  console.log('Name updated to Jane Coolidge!')
  console.log('='.repeat(50))
}

main().catch(console.error)
