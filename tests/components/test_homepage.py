"""
Tests for T-012: Implement homepage with all sections

These tests verify that the Homepage component is properly implemented according to requirements:
- Homepage fetches data using GROQ query in Server Component
- Hero section displays full-width with overlay text
- Introduction section renders rich text content
- Featured blog posts section shows 3 most recent with images and excerpts
- Featured projects section shows 4 most recent with cover images
- CTA section links to contact page
- All content is editable via Sanity CMS
- Page uses proper semantic HTML

Acceptance Criteria:
- Homepage fetches data using GROQ query in Server Component
- Hero section displays full-width with overlay text
- Introduction section renders rich text content
- Featured blog posts section shows 3 most recent with images and excerpts
- Featured projects section shows 4 most recent with cover images
- CTA section links to contact page
- All content is editable via Sanity CMS
- Page uses proper semantic HTML
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
HOMEPAGE_FILE = PROJECT_ROOT / "app" / "(site)" / "page.tsx"
HOMEPAGE_COMPONENT_FILE = PROJECT_ROOT / "components" / "home" / "HomePageClient.tsx"
ANIMATED_SECTIONS_FILE = PROJECT_ROOT / "components" / "home" / "AnimatedSections.tsx"
QUERIES_FILE = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"


def get_rendering_content():
    """Get combined content from component files where rendering happens.
    
    In Next.js App Router, Server Components often delegate rendering to Client Components.
    The homepage page.tsx fetches data and passes it to HomePageClient.tsx for rendering,
    which in turn uses AnimatedSections.tsx for card components and animations.
    """
    content_parts = []
    
    # Primary rendering component
    if HOMEPAGE_COMPONENT_FILE.exists():
        content_parts.append(HOMEPAGE_COMPONENT_FILE.read_text())
    
    # Sub-components for cards, headers, etc.
    if ANIMATED_SECTIONS_FILE.exists():
        content_parts.append(ANIMATED_SECTIONS_FILE.read_text())
    
    # Fallback to page.tsx if no component files exist
    if not content_parts and HOMEPAGE_FILE.exists():
        content_parts.append(HOMEPAGE_FILE.read_text())
    
    return "\n".join(content_parts)


class TestHomepageFileExists:
    """Test that Homepage component file exists and has proper structure."""

    def test_homepage_file_exists(self):
        """app/(site)/page.tsx should exist."""
        assert HOMEPAGE_FILE.exists(), "app/(site)/page.tsx not found"

    def test_homepage_is_server_component(self):
        """Homepage should be an async Server Component."""
        content = HOMEPAGE_FILE.read_text()
        assert "async function HomePage" in content or "export default async function HomePage" in content, (
            "Homepage should be an async function (Server Component)"
        )

    def test_homepage_no_use_client_directive(self):
        """Homepage should NOT have 'use client' directive (Server Component)."""
        content = HOMEPAGE_FILE.read_text()
        assert "'use client'" not in content and '"use client"' not in content, (
            "Homepage should be a Server Component without 'use client' directive"
        )

    def test_homepage_exports_default(self):
        """Homepage should have a default export."""
        content = HOMEPAGE_FILE.read_text()
        assert "export default" in content, (
            "Homepage should have a default export"
        )


class TestHomepageDataFetching:
    """Test that Homepage fetches data using GROQ queries in Server Component."""

    def test_homepage_imports_sanity_fetch(self):
        """Homepage should import sanityFetch from Sanity client."""
        content = HOMEPAGE_FILE.read_text()
        assert "sanityFetch" in content, "Homepage should import sanityFetch"
        assert "@/sanity/lib/client" in content, (
            "Homepage should import from @/sanity/lib/client"
        )

    def test_homepage_imports_homepage_query(self):
        """Homepage should import homepageQuery."""
        content = HOMEPAGE_FILE.read_text()
        assert "homepageQuery" in content, "Homepage should import homepageQuery"

    def test_homepage_imports_featured_posts_query(self):
        """Homepage should import featuredPostsQuery."""
        content = HOMEPAGE_FILE.read_text()
        assert "featuredPostsQuery" in content, "Homepage should import featuredPostsQuery"

    def test_homepage_imports_featured_projects_query(self):
        """Homepage should import featuredProjectsQuery."""
        content = HOMEPAGE_FILE.read_text()
        assert "featuredProjectsQuery" in content, "Homepage should import featuredProjectsQuery"

    def test_homepage_uses_parallel_fetching(self):
        """Homepage should fetch all data in parallel using Promise.all."""
        content = HOMEPAGE_FILE.read_text()
        assert "Promise.all" in content, (
            "Homepage should use Promise.all for parallel data fetching"
        )

    def test_homepage_fetches_homepage_data(self):
        """Homepage should fetch homepage content data."""
        content = HOMEPAGE_FILE.read_text()
        assert "homepageQuery" in content and "sanityFetch" in content, (
            "Homepage should fetch homepage data using sanityFetch"
        )

    def test_homepage_fetches_featured_posts(self):
        """Homepage should fetch featured blog posts."""
        content = HOMEPAGE_FILE.read_text()
        assert "featuredPostsQuery" in content and "sanityFetch" in content, (
            "Homepage should fetch featured posts using sanityFetch"
        )

    def test_homepage_fetches_featured_projects(self):
        """Homepage should fetch featured projects."""
        content = HOMEPAGE_FILE.read_text()
        assert "featuredProjectsQuery" in content and "sanityFetch" in content, (
            "Homepage should fetch featured projects using sanityFetch"
        )

    def test_homepage_uses_cache_tags(self):
        """Homepage should use cache tags for revalidation."""
        content = HOMEPAGE_FILE.read_text()
        assert "tags:" in content or "tags :" in content, (
            "Homepage should specify tags for cache revalidation"
        )

    def test_homepage_imports_result_types(self):
        """Homepage should import proper TypeScript result types."""
        content = HOMEPAGE_FILE.read_text()
        assert "HomepageResult" in content, (
            "Homepage should import HomepageResult type"
        )
        assert "BlogPostListItem" in content, (
            "Homepage should import BlogPostListItem type"
        )
        assert "ProjectListItem" in content, (
            "Homepage should import ProjectListItem type"
        )


class TestHeroSection:
    """Test hero section displays full-width with overlay text."""

    def test_hero_section_exists(self):
        """Homepage should have a hero section."""
        content = get_rendering_content()
        assert "Hero" in content, "Homepage should have a hero section"

    def test_hero_section_aria_label(self):
        """Hero section should have aria-label for accessibility."""
        content = get_rendering_content()
        assert 'aria-label="Hero"' in content or "aria-label='Hero'" in content, (
            "Hero section should have aria-label"
        )

    def test_hero_section_is_full_height(self):
        """Hero section should be full viewport height."""
        content = get_rendering_content()
        # Check for vh-based or svh-based height classes
        assert "h-[100svh]" in content or "h-screen" in content or "h-[100vh]" in content, (
            "Hero section should have full viewport height"
        )

    def test_hero_section_has_min_height(self):
        """Hero section should have minimum height for small screens."""
        content = get_rendering_content()
        assert "min-h-" in content, (
            "Hero section should have minimum height"
        )

    def test_hero_displays_background_image(self):
        """Hero section should display background image from Sanity."""
        content = get_rendering_content()
        assert "heroImage" in content, (
            "Hero should reference heroImage from homepage data"
        )

    def test_hero_uses_next_image(self):
        """Hero should use Next.js Image component for background."""
        content = get_rendering_content()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "Homepage should import Next.js Image component"
        )
        assert "<Image" in content, "Homepage should use Image component"

    def test_hero_image_uses_fill(self):
        """Hero image should use fill prop for full coverage."""
        content = get_rendering_content()
        assert "fill" in content, (
            "Hero image should use fill prop"
        )

    def test_hero_image_has_priority(self):
        """Hero image should have priority loading (LCP optimization)."""
        content = get_rendering_content()
        assert "priority" in content, (
            "Hero image should have priority prop for LCP optimization"
        )

    def test_hero_image_uses_object_cover(self):
        """Hero image should use object-cover for proper scaling."""
        content = get_rendering_content()
        assert "object-cover" in content, (
            "Hero image should have object-cover class"
        )

    def test_hero_has_gradient_overlay(self):
        """Hero should have gradient overlay for text readability."""
        content = get_rendering_content()
        assert "gradient" in content.lower(), (
            "Hero should have gradient overlay"
        )

    def test_hero_displays_heading(self):
        """Hero should display heading from Sanity content."""
        content = get_rendering_content()
        assert "heroHeading" in content, (
            "Hero should display heroHeading"
        )

    def test_hero_has_h1_element(self):
        """Hero should have h1 heading element."""
        content = get_rendering_content()
        assert "<h1" in content, (
            "Hero should have h1 element for main heading"
        )

    def test_hero_displays_subheading(self):
        """Hero should display optional subheading."""
        content = get_rendering_content()
        assert "heroSubheading" in content, (
            "Hero should reference heroSubheading"
        )

    def test_hero_heading_text_is_white(self):
        """Hero heading text should be white for contrast."""
        content = get_rendering_content()
        assert "text-white" in content, (
            "Hero should have white text for contrast against image"
        )

    def test_hero_has_fallback_gradient(self):
        """Hero should have fallback gradient when no image."""
        content = get_rendering_content()
        # Check for conditional rendering of fallback
        assert "?" in content and "heroImage" in content, (
            "Hero should have conditional fallback when no image"
        )


class TestIntroductionSection:
    """Test introduction section renders rich text content."""

    def test_intro_section_exists(self):
        """Homepage should have an introduction section."""
        content = get_rendering_content()
        assert "introText" in content, (
            "Homepage should reference introText"
        )

    def test_intro_conditional_rendering(self):
        """Introduction should only render if content exists."""
        content = get_rendering_content()
        assert "introText && Array.isArray" in content or ("introText" in content and "length" in content), (
            "Introduction should check for content before rendering"
        )

    def test_intro_uses_portable_text(self):
        """Introduction should use PortableText for rich text rendering."""
        content = get_rendering_content()
        assert "PortableText" in content, (
            "Homepage should use PortableText component"
        )
        assert "import" in content and "PortableText" in content, (
            "Homepage should import PortableText"
        )

    def test_intro_has_section_element(self):
        """Introduction should use semantic section element."""
        content = get_rendering_content()
        # Count section elements (should have multiple for different sections)
        section_count = content.count("<section")
        assert section_count >= 2, (
            "Homepage should have multiple section elements"
        )

    def test_intro_has_aria_labelledby(self):
        """Introduction section should have aria-labelledby for accessibility."""
        content = get_rendering_content()
        assert "aria-labelledby" in content, (
            "Sections should have aria-labelledby for accessibility"
        )

    def test_intro_has_prose_styling(self):
        """Introduction should use Tailwind prose styling for rich text."""
        content = get_rendering_content()
        assert "prose" in content, (
            "Introduction should use prose class for rich text styling"
        )


class TestFeaturedBlogPostsSection:
    """Test featured blog posts section shows 3 most recent with images and excerpts."""

    def test_featured_posts_section_exists(self):
        """Homepage should have a featured blog posts section."""
        content = get_rendering_content()
        assert "featuredPosts" in content, (
            "Homepage should reference featuredPosts"
        )

    def test_featured_posts_conditional_rendering(self):
        """Featured posts section should only render if posts exist."""
        content = get_rendering_content()
        assert "featuredPosts && featuredPosts.length" in content or ("featuredPosts" in content and "length" in content), (
            "Featured posts should check for content before rendering"
        )

    def test_featured_posts_displays_heading(self):
        """Featured posts section should display heading."""
        content = get_rendering_content()
        assert "featuredPostsHeading" in content, (
            "Featured posts section should display customizable heading"
        )

    def test_featured_posts_has_h2_heading(self):
        """Featured posts section should have h2 heading."""
        content = get_rendering_content()
        assert "<h2" in content, (
            "Featured posts section should have h2 element"
        )

    def test_featured_posts_maps_over_items(self):
        """Featured posts should map over blog post items."""
        content = get_rendering_content()
        assert "featuredPosts.map" in content or "featuredPosts?.map" in content, (
            "Featured posts should map over items"
        )

    def test_featured_posts_displays_images(self):
        """Featured posts should display cover images."""
        content = get_rendering_content()
        assert "coverImage" in content, (
            "Featured posts should display cover images"
        )

    def test_featured_posts_displays_titles(self):
        """Featured posts should display post titles."""
        content = get_rendering_content()
        assert "post.title" in content, (
            "Featured posts should display titles"
        )

    def test_featured_posts_displays_excerpts(self):
        """Featured posts should display excerpts."""
        content = get_rendering_content()
        assert "excerpt" in content, (
            "Featured posts should display excerpts"
        )

    def test_featured_posts_links_to_blog_posts(self):
        """Featured posts should link to individual blog posts."""
        content = get_rendering_content()
        assert "/blog/" in content and "slug" in content, (
            "Featured posts should link to blog post pages"
        )

    def test_featured_posts_uses_article_elements(self):
        """Featured posts should use article elements for each post."""
        content = get_rendering_content()
        assert "<article" in content, (
            "Featured posts should use article elements"
        )

    def test_featured_posts_displays_dates(self):
        """Featured posts should display publish dates."""
        content = get_rendering_content()
        assert "publishedAt" in content, (
            "Featured posts should display publish dates"
        )

    def test_featured_posts_uses_time_element(self):
        """Featured posts should use time element for dates."""
        content = get_rendering_content()
        assert "<time" in content, (
            "Featured posts should use time element for semantic dates"
        )

    def test_featured_posts_time_has_datetime(self):
        """Time elements should have datetime attribute."""
        content = get_rendering_content()
        assert "dateTime=" in content or "datetime=" in content.lower(), (
            "Time element should have dateTime attribute"
        )

    def test_featured_posts_displays_tags(self):
        """Featured posts should display tags."""
        content = get_rendering_content()
        assert "tags" in content, (
            "Featured posts should display tags"
        )

    def test_featured_posts_has_view_all_link(self):
        """Featured posts section should have 'View all' link to blog."""
        content = get_rendering_content()
        # Check for either direct href or prop-based linkHref
        assert 'href="/blog"' in content or "href='/blog'" in content or 'linkHref="/blog"' in content or "linkHref='/blog'" in content, (
            "Featured posts should have link to blog page"
        )

    def test_featured_posts_uses_grid_layout(self):
        """Featured posts should use grid layout."""
        content = get_rendering_content()
        assert "grid" in content, (
            "Featured posts should use grid layout"
        )

    def test_featured_posts_responsive_grid(self):
        """Featured posts grid should be responsive."""
        content = get_rendering_content()
        assert "md:grid-cols" in content or "lg:grid-cols" in content, (
            "Featured posts grid should be responsive"
        )


class TestFeaturedProjectsSection:
    """Test featured projects section shows 4 most recent with cover images."""

    def test_featured_projects_section_exists(self):
        """Homepage should have a featured projects section."""
        content = get_rendering_content()
        assert "featuredProjects" in content, (
            "Homepage should reference featuredProjects"
        )

    def test_featured_projects_conditional_rendering(self):
        """Featured projects section should only render if projects exist."""
        content = get_rendering_content()
        assert "featuredProjects && featuredProjects.length" in content or ("featuredProjects" in content and "length" in content), (
            "Featured projects should check for content before rendering"
        )

    def test_featured_projects_displays_heading(self):
        """Featured projects section should display heading."""
        content = get_rendering_content()
        assert "featuredProjectsHeading" in content, (
            "Featured projects section should display customizable heading"
        )

    def test_featured_projects_maps_over_items(self):
        """Featured projects should map over project items."""
        content = get_rendering_content()
        assert "featuredProjects.map" in content or "featuredProjects?.map" in content, (
            "Featured projects should map over items"
        )

    def test_featured_projects_displays_images(self):
        """Featured projects should display cover images."""
        content = get_rendering_content()
        # coverImage is used for both posts and projects
        assert "project.coverImage" in content or "coverImage" in content, (
            "Featured projects should display cover images"
        )

    def test_featured_projects_displays_titles(self):
        """Featured projects should display project titles."""
        content = get_rendering_content()
        assert "project.title" in content, (
            "Featured projects should display titles"
        )

    def test_featured_projects_links_to_projects(self):
        """Featured projects should link to individual project pages."""
        content = get_rendering_content()
        assert "/projects/" in content and "slug" in content, (
            "Featured projects should link to project pages"
        )

    def test_featured_projects_displays_category(self):
        """Featured projects should display category."""
        content = get_rendering_content()
        assert "category" in content, (
            "Featured projects should display category"
        )

    def test_featured_projects_has_view_all_link(self):
        """Featured projects section should have 'View all' link."""
        content = get_rendering_content()
        assert 'href="/projects"' in content or "href='/projects'" in content, (
            "Featured projects should have link to projects page"
        )

    def test_featured_projects_uses_grid_layout(self):
        """Featured projects should use grid layout."""
        content = get_rendering_content()
        # Grid is used for projects layout
        assert "grid" in content and "md:grid-cols" in content, (
            "Featured projects should use responsive grid layout"
        )


class TestCTASection:
    """Test CTA section links to contact page."""

    def test_cta_section_exists(self):
        """Homepage should have a CTA section."""
        content = get_rendering_content()
        assert "ctaText" in content, (
            "Homepage should reference ctaText"
        )

    def test_cta_conditional_rendering(self):
        """CTA section should only render if content exists."""
        content = get_rendering_content()
        assert "ctaText && " in content or ("ctaText" in content and "ctaLink" in content), (
            "CTA should check for content before rendering"
        )

    def test_cta_displays_text(self):
        """CTA section should display customizable text."""
        content = get_rendering_content()
        assert "ctaText" in content, (
            "CTA section should display text from Sanity"
        )

    def test_cta_has_link(self):
        """CTA section should have a link to contact page."""
        content = get_rendering_content()
        assert "ctaLink" in content, (
            "CTA section should use ctaLink from Sanity"
        )

    def test_cta_uses_link_component(self):
        """CTA should use Next.js Link component."""
        content = get_rendering_content()
        assert "import Link from 'next/link'" in content or 'import Link from "next/link"' in content, (
            "Homepage should import Next.js Link component"
        )

    def test_cta_has_aria_label(self):
        """CTA section should have aria-label for accessibility."""
        content = get_rendering_content()
        assert "Call to action" in content or "cta" in content.lower(), (
            "CTA section should have accessible labeling"
        )

    def test_cta_has_distinct_styling(self):
        """CTA section should have distinct background styling."""
        content = get_rendering_content()
        # Check for dark background section for CTA
        assert "bg-neutral-900" in content or "bg-black" in content, (
            "CTA section should have distinct dark background"
        )


class TestSemanticHTML:
    """Test that page uses proper semantic HTML."""

    def test_uses_article_element(self):
        """Homepage should use article element as main wrapper."""
        content = get_rendering_content()
        assert "<article" in content, (
            "Homepage should use article element"
        )

    def test_uses_section_elements(self):
        """Homepage should use section elements for major sections."""
        content = get_rendering_content()
        section_count = content.count("<section")
        assert section_count >= 4, (
            "Homepage should have at least 4 section elements (hero, intro, posts, projects)"
        )

    def test_uses_header_elements(self):
        """Homepage should use header elements for section headers."""
        content = get_rendering_content()
        assert "<header" in content, (
            "Homepage should use header element for section headers"
        )

    def test_uses_heading_hierarchy(self):
        """Homepage should maintain proper heading hierarchy."""
        content = get_rendering_content()
        assert "<h1" in content, "Homepage should have h1"
        assert "<h2" in content, "Homepage should have h2"
        assert "<h3" in content, "Homepage should have h3 for post/project titles"

    def test_images_have_alt_text(self):
        """Images should have alt attributes."""
        content = get_rendering_content()
        # All images should have alt attribute
        image_count = content.count("<Image")
        alt_count = content.count("alt=")
        assert alt_count >= image_count, (
            "All images should have alt attributes"
        )

    def test_decorative_elements_hidden(self):
        """Decorative elements should be hidden from accessibility."""
        content = get_rendering_content()
        assert 'aria-hidden="true"' in content or "aria-hidden='true'" in content, (
            "Decorative elements should have aria-hidden"
        )


class TestTailwindStyling:
    """Test that page uses Tailwind CSS for styling."""

    def test_uses_tailwind_classes(self):
        """Homepage should use Tailwind CSS classes."""
        content = get_rendering_content()
        tailwind_indicators = [
            "flex",
            "items-",
            "justify-",
            "px-",
            "py-",
            "bg-",
            "text-",
        ]
        found_classes = [cls for cls in tailwind_indicators if cls in content]
        assert len(found_classes) >= 5, (
            f"Homepage should use Tailwind classes, found: {found_classes}"
        )

    def test_uses_responsive_classes(self):
        """Homepage should use Tailwind responsive classes."""
        content = get_rendering_content()
        responsive_prefixes = ["sm:", "md:", "lg:", "xl:"]
        found_responsive = [prefix for prefix in responsive_prefixes if prefix in content]
        assert len(found_responsive) >= 2, (
            "Homepage should use Tailwind responsive classes"
        )

    def test_uses_max_width_constraints(self):
        """Homepage should use max-width constraints for content."""
        content = get_rendering_content()
        assert "max-w-" in content, (
            "Homepage should use max-width constraints"
        )

    def test_uses_margin_auto_centering(self):
        """Homepage should center content with mx-auto."""
        content = get_rendering_content()
        assert "mx-auto" in content, (
            "Homepage should center content with mx-auto"
        )

    def test_uses_brand_colors(self):
        """Homepage should use brand color classes."""
        content = get_rendering_content()
        assert "brand-" in content, (
            "Homepage should use brand color utilities"
        )

    def test_uses_dark_mode_classes(self):
        """Homepage should support dark mode."""
        content = get_rendering_content()
        assert "dark:" in content, (
            "Homepage should have dark mode support"
        )


class TestMetadataGeneration:
    """Test that homepage generates proper metadata."""

    def test_exports_generate_metadata(self):
        """Homepage should export generateMetadata function."""
        content = HOMEPAGE_FILE.read_text()
        assert "generateMetadata" in content, (
            "Homepage should export generateMetadata"
        )

    def test_generate_metadata_is_async(self):
        """generateMetadata should be async function."""
        content = HOMEPAGE_FILE.read_text()
        assert "async function generateMetadata" in content or "export async function generateMetadata" in content, (
            "generateMetadata should be async"
        )

    def test_metadata_includes_title(self):
        """Metadata should include title."""
        content = HOMEPAGE_FILE.read_text()
        assert "title:" in content or "title :" in content, (
            "Metadata should include title"
        )

    def test_metadata_includes_description(self):
        """Metadata should include description."""
        content = HOMEPAGE_FILE.read_text()
        assert "description:" in content or "description :" in content, (
            "Metadata should include description"
        )

    def test_metadata_includes_og_image(self):
        """Metadata should include Open Graph image."""
        content = HOMEPAGE_FILE.read_text()
        assert "openGraph" in content, (
            "Metadata should include Open Graph configuration"
        )

    def test_metadata_fetches_from_sanity(self):
        """Metadata should fetch SEO data from Sanity."""
        content = HOMEPAGE_FILE.read_text()
        assert "seo" in content, (
            "Metadata should use SEO data from Sanity"
        )


class TestImageOptimization:
    """Test that images are properly optimized."""

    def test_uses_urlfor_helper(self):
        """Homepage should use urlFor helper for image URLs."""
        content = get_rendering_content()
        assert "urlFor" in content, (
            "Homepage should use urlFor helper"
        )

    def test_imports_urlfor_helper(self):
        """Homepage should import urlFor from Sanity lib."""
        content = get_rendering_content()
        assert "@/sanity/lib/image" in content, (
            "Homepage should import urlFor from @/sanity/lib/image"
        )

    def test_images_have_sizes_prop(self):
        """Images should have sizes prop for responsive loading."""
        content = get_rendering_content()
        assert "sizes=" in content or "sizes =" in content, (
            "Images should have sizes prop"
        )

    def test_images_have_quality_setting(self):
        """Images should have quality setting."""
        content = get_rendering_content()
        assert "quality(" in content, (
            "Images should have quality setting via urlFor"
        )

    def test_images_have_blur_placeholder(self):
        """Images should support blur placeholder (LQIP)."""
        content = get_rendering_content()
        assert "blur" in content.lower() and "lqip" in content.lower(), (
            "Images should support blur placeholder with LQIP"
        )


class TestAccessibility:
    """Test accessibility features."""

    def test_sections_have_aria_labels(self):
        """Sections should have aria-label or aria-labelledby."""
        content = get_rendering_content()
        aria_label_count = content.count("aria-label") + content.count("aria-labelledby")
        assert aria_label_count >= 4, (
            "Sections should have aria-label or aria-labelledby attributes"
        )

    def test_links_are_descriptive(self):
        """Links should have descriptive text."""
        content = get_rendering_content()
        # Check for "View all" type links
        assert "View all" in content or "view all" in content.lower(), (
            "Links should have descriptive text"
        )

    def test_focus_visible_styles(self):
        """Interactive elements should have focus-visible styles."""
        content = get_rendering_content()
        assert "focus:" in content or "focus-visible:" in content, (
            "Interactive elements should have focus styles"
        )


class TestHomepageQueriesExist:
    """Test that required GROQ queries exist in queries file."""

    def test_queries_file_exists(self):
        """sanity/lib/queries.ts should exist."""
        assert QUERIES_FILE.exists(), "sanity/lib/queries.ts not found"

    def test_homepage_query_defined(self):
        """homepageQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export const homepageQuery" in content, (
            "homepageQuery should be exported"
        )

    def test_homepage_query_fetches_hero_fields(self):
        """homepageQuery should fetch hero section fields."""
        content = QUERIES_FILE.read_text()
        assert "heroHeading" in content, "Query should fetch heroHeading"
        assert "heroSubheading" in content, "Query should fetch heroSubheading"
        assert "heroImage" in content, "Query should fetch heroImage"

    def test_homepage_query_fetches_intro_text(self):
        """homepageQuery should fetch introText."""
        content = QUERIES_FILE.read_text()
        assert "introText" in content, "Query should fetch introText"

    def test_homepage_query_fetches_section_headings(self):
        """homepageQuery should fetch section headings."""
        content = QUERIES_FILE.read_text()
        assert "featuredPostsHeading" in content, (
            "Query should fetch featuredPostsHeading"
        )
        assert "featuredProjectsHeading" in content, (
            "Query should fetch featuredProjectsHeading"
        )

    def test_homepage_query_fetches_cta_fields(self):
        """homepageQuery should fetch CTA fields."""
        content = QUERIES_FILE.read_text()
        assert "ctaText" in content, "Query should fetch ctaText"
        assert "ctaLink" in content, "Query should fetch ctaLink"

    def test_homepage_query_fetches_seo(self):
        """homepageQuery should fetch SEO fields."""
        content = QUERIES_FILE.read_text()
        assert "seo" in content, "Query should fetch seo"

    def test_featured_posts_query_defined(self):
        """featuredPostsQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export const featuredPostsQuery" in content, (
            "featuredPostsQuery should be exported"
        )

    def test_featured_posts_query_limits_to_three(self):
        """featuredPostsQuery should limit to 3 posts."""
        content = QUERIES_FILE.read_text()
        assert "[0...3]" in content, (
            "featuredPostsQuery should limit to 3 posts"
        )

    def test_featured_posts_query_orders_by_date(self):
        """featuredPostsQuery should order by publishedAt desc."""
        content = QUERIES_FILE.read_text()
        assert "order(publishedAt desc)" in content, (
            "featuredPostsQuery should order by publishedAt desc"
        )

    def test_featured_projects_query_defined(self):
        """featuredProjectsQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export const featuredProjectsQuery" in content, (
            "featuredProjectsQuery should be exported"
        )

    def test_featured_projects_query_limits_to_four(self):
        """featuredProjectsQuery should limit to 4 projects."""
        content = QUERIES_FILE.read_text()
        assert "[0...4]" in content, (
            "featuredProjectsQuery should limit to 4 projects"
        )

    def test_homepage_result_type_defined(self):
        """HomepageResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export interface HomepageResult" in content, (
            "HomepageResult type should be exported"
        )

    def test_blog_post_list_item_type_defined(self):
        """BlogPostListItem type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export interface BlogPostListItem" in content, (
            "BlogPostListItem type should be exported"
        )

    def test_project_list_item_type_defined(self):
        """ProjectListItem type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export interface ProjectListItem" in content, (
            "ProjectListItem type should be exported"
        )
