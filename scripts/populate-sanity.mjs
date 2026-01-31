// Script to populate Sanity with portfolio content
import { createClient } from '@sanity/client'
import { readFileSync } from 'fs'
import { exec } from 'child_process'
import { promisify } from 'util'
import path from 'path'
import { fileURLToPath } from 'url'

const execAsync = promisify(exec)
const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Sanity client configuration
const client = createClient({
  projectId: 'xp9jnodv',
  dataset: 'production',
  apiVersion: '2024-01-01',
  token: process.env.SANITY_TOKEN,
  useCdn: false,
})

// Portfolio data extracted from PDF
const portfolioItems = [
  {
    title: 'Ethereal Vessel',
    slug: 'ethereal-vessel',
    category: 'personal',
    description: 'A hand sculpted coil pot with a glossy dark glaze. The design includes flowing elements at the top and diamond-shaped patterns in the middle. There is a dynamic interplay of negative space and structure throughout the piece. Its base consists of elongated vertical forms offering an almost ribcage-like appearance. The high-gloss finish enhances the texture, depth and history of the design. The glossy dark glaze is reminiscent of barro negro (black clay) pottery from Oaxaca. The geometric patterns and interwoven coils echo Pre-Columbian motifs, commonly seen in Zapotec and Mayan ceramics, reflecting the rich artistic heritage of Mesoamerican cultures.',
    medium: 'Hand-sculpted clay, glossy dark glaze',
    tags: ['Ceramics', 'Sculpture', 'Mesoamerican', 'Coil Pot'],
  },
  {
    title: 'Tidebound Top',
    slug: 'tidebound-top',
    category: 'personal',
    description: 'A crochet top made from recycled black yarn and resin shells. Created using a 6.75mm crochet hook with 3mm jump rings to attach the shells. This sustainable fashion piece represents the fish nets that get lost or abandoned by ships, which can be eaten by marine animals, cause micro plastic pollution, entangle and injure wildlife. The blue shells attached to the yarn represent mussel shells, tying in the aquatic theme and creating awareness around how important it is to care for our planet and protect our oceans.',
    medium: 'Recycled black yarn, resin shells, jump rings',
    tags: ['Fashion', 'Crochet', 'Sustainable', 'Ocean Conservation'],
  },
  {
    title: 'Fruitful Glass',
    slug: 'fruitful-glass',
    category: 'personal',
    description: 'Four wine glasses hand painted with acrylic paint featuring cherries, oranges, lemons, and limes. An experiment in painting on glass with a permanent finish. The fruit designs give a fun and lively feeling to the wine glasses. Sealed with dishwasher safe Mod Podge to make the paint permanent on the glass.',
    medium: 'Acrylic paint on glass, Mod Podge sealant',
    tags: ['Glass Painting', 'Functional Art', 'Home Decor'],
  },
  {
    title: 'Netborne Top',
    slug: 'netborne-top',
    category: 'personal',
    description: 'Another sustainable fashion piece bringing awareness to environmental impact through fashion. Features a different silhouette using smaller shells, brown recycled wool yarn, 3mm jump rings, and a 6.75mm crochet hook. The tighter knit creates an appearance similar to fish scales, evoking the same ocean conservation message as the Tidebound top but in a different way.',
    medium: 'Recycled brown wool yarn, shells, jump rings',
    tags: ['Fashion', 'Crochet', 'Sustainable', 'Ocean Conservation'],
  },
  {
    title: 'Walking Woods',
    slug: 'walking-woods',
    category: 'personal',
    description: 'A tranquil natural scene created with watercolor pencils on watercolor paper, inspired by Paul Cézanne and Claude Monet. The artwork portrays a winding path lined by tall trees leading into the distance. The small tree in the center draws the viewer\'s eye and balances the composition. The pond on the right reflects calmness. Soft colors and gentle transitions evoke a peaceful, dreamlike atmosphere, inviting the viewer to stumble upon this landscape during a walk.',
    medium: 'Watercolor pencils on watercolor paper',
    tags: ['Landscape', 'Watercolor', 'Impressionist', 'Nature'],
  },
  {
    title: 'Confidence Through Color',
    slug: 'confidence-through-color',
    category: 'personal',
    description: 'A vibrant drawing depicting a bold and stylish figure. The deep blue background contrasts beautifully with the warm orange tones of the hat and the subject\'s skin tone. The red lip and beauty mark add elegance. The harsh colors and lines give the piece a modern aesthetic that makes the viewer ask "who is she?"',
    medium: 'Color pencils',
    tags: ['Portrait', 'Fashion Illustration', 'Pop Art', 'Color Study'],
  },
  {
    title: 'FYP Beer Label',
    slug: 'fyp-beer-label',
    category: 'personal',
    description: 'A custom beer bottle label created for a family friend, incorporating his favorite things including his dogs and country club. Features a vibrant shade of red as the main color to stand out. The complete branding includes the name, layout, and a brief backstory about the person and his beer company.',
    medium: 'Digital design, print',
    tags: ['Graphic Design', 'Branding', 'Product Design', 'Label Design'],
  },
  {
    title: 'Primary Legends',
    slug: 'primary-legends',
    category: 'personal',
    description: 'A colorful image of the Beatles rendered in vibrant primary colors with permanent markers on canvas. Each member is represented in a simplified manner with only their iconic facial hair and 1960s style suits - no faces. The design emphasizes the playful and influential aesthetic of the Beatles\' era with a retro, pop-art vibe.',
    medium: 'Permanent markers on canvas',
    tags: ['Pop Art', 'Music', 'The Beatles', 'Illustration'],
  },
  {
    title: 'Natural Flow',
    slug: 'natural-flow',
    category: 'personal',
    description: 'A clay coil pot with earthy, modern charm. Two curved handles at the top accentuate its irregular form. Two different glazes were used - a gray blue glaze over the top half, then dipped into a blue green glaze. The dynamic glaze with dripping effects blends deep hues of gray, green, blue and yellow, giving the sculpture a sense of fluidity almost as if it\'s melting. The natural imperfections enhance the character.',
    medium: 'Clay, mixed glazes',
    tags: ['Ceramics', 'Sculpture', 'Coil Pot', 'Abstract'],
  },
  {
    title: 'Tilted',
    slug: 'tilted',
    category: 'personal',
    description: 'A self portrait drawn with burnt orange charcoal. Soft lines and blended areas create depth, with an eraser used to bring lighter areas back into the drawing. This highlights the facial structure including contemplative eyes and softly pursed lips. The slight head tilt causes the viewer to question the subject\'s feelings and story. The two-toned background helps maintain focus on the subject.',
    medium: 'Burnt orange charcoal',
    tags: ['Portrait', 'Self Portrait', 'Charcoal', 'Figurative'],
  },
  {
    title: 'Stable Reflection',
    slug: 'stable-reflection',
    category: 'personal',
    description: 'A painting of a white horse almost leaning over a wooden fence. The horse has soft, expressive eyes evoking a sense of timidness or fear. The delicate features are highlighted against the muted brown and black background which adds depth to the composition. The overall feeling evokes a quiet connection to the viewer and a moment of stillness.',
    medium: 'Paint on canvas',
    tags: ['Animal Portrait', 'Horse', 'Painting', 'Nature'],
  },
  {
    title: 'The Gaze',
    slug: 'the-gaze',
    category: 'personal',
    description: 'A black ink portrait drawing done with a pen on sketch book paper. The intense gaze is emphasized with bold lines focusing on the center of the face. Detailed line work captures different textures throughout the hair, beard, and shirt, creating an expressive yet raw feeling.',
    medium: 'Black ink pen on paper',
    tags: ['Portrait', 'Ink Drawing', 'Illustration', 'Figurative'],
  },
  {
    title: 'Cow?',
    slug: 'cow',
    category: 'personal',
    description: 'A colored pencil drawing of a cow, close up and front facing, focused on the eyes, snout and wide-spread ears. The blue two-toned gradient background contrasts with the cow. The drawing is almost lifelike but not quite, creating a different representation of the animal that makes the viewer think deeper about the drawing.',
    medium: 'Colored pencils',
    tags: ['Animal Portrait', 'Realism', 'Drawing', 'Nature'],
  },
  {
    title: 'Silence Red',
    slug: 'silence-red',
    category: 'personal',
    description: 'A portrait painting using a loose, expressive style with visible brush strokes. Created with acrylic paint on mixed media paper. Depth is added to the face using a mix of warm and cool tones. The hair is less detailed and more fluid with red hues falling down to create a careless or raw feeling. The dark lines on the lips look like they\'re being forced shut, creating mystery.',
    medium: 'Acrylic paint on mixed media paper',
    tags: ['Portrait', 'Expressionist', 'Acrylic', 'Figurative'],
  },
  {
    title: 'Childhood',
    slug: 'childhood',
    category: 'personal',
    description: 'A drawing depicting a playful and carefree moment at the beach, created on location with color pencils. Shows a cousin digging in the sand, almost half his body hidden in the hole. The sandy ground contrasts with the rich blue waves and sky in the background. The overall feeling is joyful and nostalgic, celebrating what it\'s like to be a kid enjoying simple pleasures.',
    medium: 'Color pencils',
    tags: ['Beach', 'Childhood', 'Figurative', 'Landscape'],
  },
]

// Helper function to create portable text block
function createPortableText(text) {
  return [
    {
      _type: 'block',
      _key: Math.random().toString(36).substring(7),
      style: 'normal',
      markDefs: [],
      children: [
        {
          _type: 'span',
          _key: Math.random().toString(36).substring(7),
          text: text,
          marks: [],
        },
      ],
    },
  ]
}

async function main() {
  console.log('Starting Sanity content population...\n')

  // 1. Create Site Settings
  console.log('Creating Site Settings...')
  const siteSettings = await client.createOrReplace({
    _id: 'siteSettings',
    _type: 'siteSettings',
    siteName: 'Jane Gouilliard',
    footerText: 'All rights reserved.',
    defaultSeo: {
      metaTitle: 'Jane Gouilliard | Artist & Designer',
      metaDescription: 'Portfolio of Jane Gouilliard - a multidisciplinary artist working in ceramics, fashion design, painting, and illustration.',
    },
    socialLinks: [
      {
        _type: 'socialLink',
        _key: 'instagram',
        platform: 'instagram',
        url: 'https://instagram.com/',
      },
    ],
  })
  console.log('✓ Site Settings created\n')

  // 2. Create Navigation
  console.log('Creating Navigation...')
  const navigation = await client.createOrReplace({
    _id: 'navigation',
    _type: 'navigation',
    mainMenu: [
      { _type: 'menuItem', _key: 'home', label: 'Home', link: '/', openInNewTab: false },
      { _type: 'menuItem', _key: 'projects', label: 'Portfolio', link: '/projects', openInNewTab: false },
      { _type: 'menuItem', _key: 'about', label: 'About', link: '/about', openInNewTab: false },
      { _type: 'menuItem', _key: 'contact', label: 'Contact', link: '/contact', openInNewTab: false },
    ],
  })
  console.log('✓ Navigation created\n')

  // 3. Create Homepage
  console.log('Creating Homepage...')
  const homepage = await client.createOrReplace({
    _id: 'homepage',
    _type: 'homepage',
    heroHeading: 'Jane Gouilliard',
    heroSubheading: 'Multidisciplinary Artist & Designer',
    introText: createPortableText('Welcome to my creative portfolio. I explore the intersection of traditional craftsmanship and contemporary design through ceramics, sustainable fashion, painting, and illustration. Each piece tells a story and invites connection.'),
    featuredPostsHeading: 'Latest Stories',
    featuredProjectsHeading: 'Selected Work',
    ctaText: 'Get in Touch',
    ctaLink: '/contact',
    seo: {
      metaTitle: 'Jane Gouilliard | Artist & Designer Portfolio',
      metaDescription: 'Explore the portfolio of Jane Gouilliard - ceramics, sustainable fashion, paintings, and illustrations that blend heritage with modern expression.',
    },
  })
  console.log('✓ Homepage created\n')

  // 4. Create About Page
  console.log('Creating About Page...')
  const aboutPage = await client.createOrReplace({
    _id: 'aboutPage',
    _type: 'aboutPage',
    heading: 'About',
    name: 'Jane Gouilliard',
    tagline: 'Multidisciplinary Artist & Designer',
    bio: createPortableText('I am a multidisciplinary artist passionate about creating meaningful work that connects tradition with contemporary expression. My practice spans ceramics, sustainable fashion, painting, and illustration.\n\nIn my ceramic work, I draw inspiration from Mesoamerican cultures, particularly the barro negro pottery tradition from Oaxaca. The geometric patterns and coil techniques in my pieces pay homage to Pre-Columbian artistry while expressing my own creative vision.\n\nMy sustainable fashion pieces address environmental concerns, particularly ocean conservation. Through crochet tops made with recycled materials and shell embellishments, I create wearable art that raises awareness about the impact of abandoned fishing nets on marine life.\n\nMy paintings and drawings range from impressionist landscapes inspired by Cézanne and Monet to bold pop-art portraits. I work across various mediums including watercolor, acrylic, charcoal, and ink, each offering unique possibilities for expression.\n\nEvery piece I create is an invitation to look deeper, feel more, and connect with the stories embedded in the work.'),
    credentials: [
      {
        _type: 'credential',
        _key: 'art1',
        title: 'Fine Arts',
        organization: 'Visual Arts Program',
        period: 'Ongoing',
      },
    ],
    clients: ['Personal Commissions', 'Family & Friends', 'Local Exhibitions'],
    seo: {
      metaTitle: 'About Jane Gouilliard | Artist & Designer',
      metaDescription: 'Learn about Jane Gouilliard, a multidisciplinary artist working in ceramics, sustainable fashion, painting, and illustration.',
    },
  })
  console.log('✓ About Page created\n')

  // 5. Create Contact Page
  console.log('Creating Contact Page...')
  const contactPage = await client.createOrReplace({
    _id: 'contactPage',
    _type: 'contactPage',
    heading: 'Contact',
    introText: 'I would love to hear from you! Whether you have a question about my work, are interested in a commission, or just want to connect, please reach out.',
    email: 'jane@example.com',
    location: 'United States',
    formEnabled: false,
    seo: {
      metaTitle: 'Contact Jane Gouilliard',
      metaDescription: 'Get in touch with Jane Gouilliard for commissions, collaborations, or inquiries about her artwork.',
    },
  })
  console.log('✓ Contact Page created\n')

  // 6. Create Projects
  console.log('Creating Projects...')
  for (const item of portfolioItems) {
    console.log(`  Creating project: ${item.title}`)

    await client.createOrReplace({
      _id: `project-${item.slug}`,
      _type: 'project',
      title: item.title,
      slug: { _type: 'slug', current: item.slug },
      category: item.category,
      description: createPortableText(item.description),
      client: item.medium,
      date: '2024-01-01',
      seo: {
        metaTitle: `${item.title} | Jane Gouilliard`,
        metaDescription: item.description.substring(0, 160) + '...',
      },
    })
  }
  console.log(`✓ ${portfolioItems.length} Projects created\n`)

  console.log('='.repeat(50))
  console.log('Content population complete!')
  console.log('='.repeat(50))
  console.log('\nNote: Images need to be uploaded manually through Sanity Studio.')
  console.log('Visit: https://jane-website-one.vercel.app/studio')
  console.log('\nTo add images:')
  console.log('1. Go to each Project in the Studio')
  console.log('2. Upload the corresponding image as the Cover Image')
  console.log('3. The images are in the Portfolio.pdf file')
}

main().catch(console.error)
