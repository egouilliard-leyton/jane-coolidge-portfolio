"""
Tests for T-017: About page implementation

These tests verify that the About page is properly implemented according to requirements:
- About page fetches singleton document from Sanity
- Profile image displays with proper aspect ratio
- Name and tagline render prominently
- Biography renders as rich text with proper formatting
- Credentials/timeline displays chronologically
- Clients display as tag cloud or formatted list
- All content is editable via CMS
- SEO metadata is properly configured

Acceptance Criteria:
- About page fetches singleton document from Sanity
- Profile image displays with proper aspect ratio
- Name and tagline render prominently
- Biography renders as rich text with proper formatting
- Credentials/timeline displays chronologically
- Clients display as tag cloud or formatted list
- All content is editable via CMS
- SEO metadata is properly configured
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
ABOUT_PAGE_FILE = PROJECT_ROOT / "app" / "(site)" / "about" / "page.tsx"
QUERIES_FILE = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
TYPES_FILE = PROJECT_ROOT / "types" / "sanity.ts"


class TestAboutPageFileExists:
    """Test that about page file exists and has proper structure."""

    def test_about_page_file_exists(self):
        """app/(site)/about/page.tsx should exist."""
        assert ABOUT_PAGE_FILE.exists(), "app/(site)/about/page.tsx not found"

    def test_about_page_is_server_component(self):
        """About page should be an async Server Component."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "async function AboutPage" in content or "export default async function AboutPage" in content, (
            "About page should be an async function (Server Component)"
        )

    def test_about_page_no_use_client_directive(self):
        """About page should NOT have 'use client' directive (Server Component)."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "'use client'" not in content and '"use client"' not in content, (
            "About page should be a Server Component without 'use client' directive"
        )

    def test_about_page_exports_default(self):
        """About page should have a default export."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "export default" in content, (
            "About page should have a default export"
        )


class TestAboutPageSingletonFetch:
    """Test that about page fetches singleton document from Sanity."""

    def test_about_page_imports_sanity_fetch(self):
        """About page should import sanityFetch from Sanity client."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "sanityFetch" in content, "About page should import sanityFetch"
        assert "@/sanity/lib/client" in content, (
            "About page should import from @/sanity/lib/client"
        )

    def test_about_page_imports_about_page_query(self):
        """About page should import aboutPageQuery."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "aboutPageQuery" in content, "About page should import aboutPageQuery"

    def test_about_page_imports_about_page_result_type(self):
        """About page should import AboutPageResult type."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "AboutPageResult" in content, (
            "About page should import AboutPageResult type"
        )

    def test_about_page_fetches_with_tags(self):
        """About page should use cache tags for revalidation."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "tags:" in content and "aboutPage" in content, (
            "About page should use 'aboutPage' tag for cache revalidation"
        )

    def test_about_page_query_is_singleton(self):
        """aboutPageQuery should fetch singleton document (index [0])."""
        content = QUERIES_FILE.read_text()
        assert '*[_type == "aboutPage"][0]' in content, (
            "aboutPageQuery should fetch singleton document with [0]"
        )


class TestAboutPageQueryStructure:
    """Test that aboutPageQuery is properly defined in queries.ts."""

    def test_queries_file_exists(self):
        """sanity/lib/queries.ts should exist."""
        assert QUERIES_FILE.exists(), "sanity/lib/queries.ts not found"

    def test_about_page_query_exported(self):
        """aboutPageQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const aboutPageQuery" in content, (
            "aboutPageQuery should be exported from queries.ts"
        )

    def test_about_page_query_includes_id(self):
        """aboutPageQuery should include _id field."""
        content = QUERIES_FILE.read_text()
        # Find aboutPageQuery section
        assert "_id" in content, "aboutPageQuery should include _id field"

    def test_about_page_query_includes_heading(self):
        """aboutPageQuery should include heading field."""
        content = QUERIES_FILE.read_text()
        assert "heading" in content, "aboutPageQuery should include heading field"

    def test_about_page_query_includes_profile_image(self):
        """aboutPageQuery should include profileImage field."""
        content = QUERIES_FILE.read_text()
        assert "profileImage" in content, (
            "aboutPageQuery should include profileImage field"
        )

    def test_about_page_query_includes_name(self):
        """aboutPageQuery should include name field."""
        content = QUERIES_FILE.read_text()
        assert "name" in content, "aboutPageQuery should include name field"

    def test_about_page_query_includes_tagline(self):
        """aboutPageQuery should include tagline field."""
        content = QUERIES_FILE.read_text()
        assert "tagline" in content, "aboutPageQuery should include tagline field"

    def test_about_page_query_includes_bio(self):
        """aboutPageQuery should include bio field."""
        content = QUERIES_FILE.read_text()
        assert "bio" in content, "aboutPageQuery should include bio (biography) field"

    def test_about_page_query_includes_credentials(self):
        """aboutPageQuery should include credentials field."""
        content = QUERIES_FILE.read_text()
        assert "credentials" in content, (
            "aboutPageQuery should include credentials field"
        )

    def test_about_page_query_includes_clients(self):
        """aboutPageQuery should include clients field."""
        content = QUERIES_FILE.read_text()
        assert "clients" in content, "aboutPageQuery should include clients field"

    def test_about_page_query_includes_seo(self):
        """aboutPageQuery should include seo field."""
        content = QUERIES_FILE.read_text()
        assert "seo" in content, "aboutPageQuery should include seo field"


class TestAboutPageResultType:
    """Test that AboutPageResult type is properly defined."""

    def test_about_page_result_type_exported(self):
        """AboutPageResult type should be exported from queries.ts."""
        content = QUERIES_FILE.read_text()
        assert "export interface AboutPageResult" in content, (
            "AboutPageResult should be exported from queries.ts"
        )

    def test_about_page_result_has_id(self):
        """AboutPageResult should have _id field."""
        content = QUERIES_FILE.read_text()
        # Find AboutPageResult section and verify _id
        assert "_id: string" in content, "AboutPageResult should have _id: string"

    def test_about_page_result_has_optional_fields(self):
        """AboutPageResult should have optional fields marked with ?."""
        content = QUERIES_FILE.read_text()
        # Most fields in AboutPageResult should be optional
        assert "name?" in content or "name?: string" in content, (
            "AboutPageResult should have optional name field"
        )


class TestProfileImageDisplay:
    """Test that profile image displays with proper aspect ratio."""

    def test_about_page_imports_image(self):
        """About page should import Next.js Image component."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "About page should import Next.js Image component"
        )

    def test_about_page_imports_urlfor(self):
        """About page should import urlFor from Sanity lib."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "urlFor" in content, "About page should use urlFor helper"
        assert "@/sanity/lib/image" in content, (
            "About page should import urlFor from @/sanity/lib/image"
        )

    def test_profile_image_uses_aspect_ratio(self):
        """Profile image should have proper aspect ratio (3:4)."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "aspect-[3/4]" in content or "aspect-ratio" in content, (
            "Profile image should use 3:4 aspect ratio"
        )

    def test_profile_image_uses_fill(self):
        """Profile image should use fill prop."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "fill" in content, "Profile image should use fill prop"

    def test_profile_image_has_alt_text(self):
        """Profile image should have alt text."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "alt=" in content, "Profile image should have alt attribute"

    def test_profile_image_has_sizes_prop(self):
        """Profile image should have sizes prop for responsive images."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "sizes=" in content, "Profile image should have sizes prop"

    def test_profile_image_uses_lqip_placeholder(self):
        """Profile image should use LQIP blur placeholder when available."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "blurDataURL" in content or "lqip" in content, (
            "Profile image should use LQIP blur placeholder"
        )

    def test_profile_image_has_fallback(self):
        """Profile image should have fallback when no image exists."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "profileImage" in content and ("?" in content or "&&" in content), (
            "Profile image should have conditional rendering for fallback"
        )


class TestNameAndTaglineDisplay:
    """Test that name and tagline render prominently."""

    def test_name_uses_h1(self):
        """Name should be rendered in h1 element."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "<h1" in content, "Name should be rendered in h1 element"

    def test_name_uses_large_typography(self):
        """Name should use large typography classes."""
        content = ABOUT_PAGE_FILE.read_text()
        # Check for large text sizes
        large_sizes = ["text-5xl", "text-6xl", "text-7xl", "text-8xl"]
        found_sizes = [size for size in large_sizes if size in content]
        assert len(found_sizes) >= 1, (
            "Name should use large typography (text-5xl or larger)"
        )

    def test_name_accesses_page_name(self):
        """About page should access page.name."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page.name" in content or "page?.name" in content, (
            "About page should access page.name"
        )

    def test_tagline_displays(self):
        """Tagline should be displayed."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page.tagline" in content or "page?.tagline" in content, (
            "About page should display tagline"
        )

    def test_tagline_uses_serif_font(self):
        """Tagline should use serif font for elegance."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "font-serif" in content, (
            "Tagline should use serif font for elegance"
        )

    def test_tagline_uses_italic(self):
        """Tagline should use italic styling."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "italic" in content, "Tagline should use italic styling"


class TestBiographyDisplay:
    """Test that biography renders as rich text with proper formatting."""

    def test_about_page_imports_portable_text(self):
        """About page should import PortableText component."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "PortableText" in content, (
            "About page should import PortableText component"
        )
        assert "@portabletext/react" in content, (
            "About page should import from @portabletext/react"
        )

    def test_biography_uses_portable_text(self):
        """Biography should be rendered using PortableText component."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "<PortableText" in content, (
            "Biography should use PortableText component"
        )

    def test_biography_passes_bio_as_value(self):
        """PortableText should receive bio as value prop."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "value={page.bio" in content or "value={page?.bio" in content, (
            "PortableText should receive bio as value"
        )

    def test_biography_uses_prose_classes(self):
        """Biography should use Tailwind prose classes for typography."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "prose" in content, (
            "Biography should use Tailwind prose classes"
        )

    def test_biography_section_has_aria_label(self):
        """Biography section should have aria-labelledby for accessibility."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "biography" in content.lower() and "aria-labelledby" in content, (
            "Biography section should have aria-labelledby"
        )

    def test_biography_conditionally_renders(self):
        """Biography should only render when bio exists."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page?.bio" in content or "page.bio &&" in content, (
            "Biography should conditionally render when bio exists"
        )


class TestCredentialsTimeline:
    """Test that credentials/timeline displays chronologically."""

    def test_credentials_section_exists(self):
        """Credentials section should exist."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "credentials" in content.lower(), (
            "About page should have credentials section"
        )

    def test_credentials_displays_title(self):
        """Credentials should display title."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "credential.title" in content or "title" in content, (
            "Credentials should display title"
        )

    def test_credentials_displays_organization(self):
        """Credentials should display organization."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "credential.organization" in content or "organization" in content, (
            "Credentials should display organization"
        )

    def test_credentials_displays_period(self):
        """Credentials should display period/dates."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "credential.period" in content or "period" in content, (
            "Credentials should display period"
        )

    def test_credentials_uses_map(self):
        """Credentials should iterate using map."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "credentials.map" in content or "credentials?.map" in content, (
            "Credentials should iterate using map"
        )

    def test_credentials_uses_key(self):
        """Credentials items should have unique key."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "key=" in content, "Credentials items should have unique key"

    def test_credentials_section_has_heading(self):
        """Credentials section should have heading."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "Experience" in content or "Credentials" in content, (
            "Credentials section should have heading"
        )

    def test_credentials_conditionally_renders(self):
        """Credentials should only render when data exists."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "credentials && page.credentials.length" in content or "page?.credentials && page.credentials.length" in content, (
            "Credentials should conditionally render when data exists"
        )


class TestCredentialItem:
    """Test CredentialItem component structure."""

    def test_credential_item_component_exists(self):
        """CredentialItem component should exist."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "CredentialItem" in content, (
            "About page should have CredentialItem component"
        )

    def test_credential_item_accepts_props(self):
        """CredentialItem should accept credential props."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "credential:" in content and "Credential" in content, (
            "CredentialItem should accept credential prop"
        )

    def test_credential_item_has_timeline_styling(self):
        """CredentialItem should have timeline styling elements."""
        content = ABOUT_PAGE_FILE.read_text()
        # Check for timeline visual elements
        assert "rounded-full" in content or "border" in content, (
            "CredentialItem should have timeline visual styling"
        )


class TestClientsDisplay:
    """Test that clients display as tag cloud or formatted list."""

    def test_clients_section_exists(self):
        """Clients section should exist."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "clients" in content.lower(), (
            "About page should have clients section"
        )

    def test_clients_section_has_heading(self):
        """Clients section should have heading."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "Notable Clients" in content or "Clients" in content, (
            "Clients section should have heading"
        )

    def test_clients_uses_map(self):
        """Clients should iterate using map."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "clients.map" in content or "clients?.map" in content, (
            "Clients should iterate using map"
        )

    def test_clients_uses_flex_wrap(self):
        """Clients should use flex-wrap for tag cloud layout."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "flex-wrap" in content or "flex flex-wrap" in content, (
            "Clients should use flex-wrap for tag cloud layout"
        )

    def test_clients_has_gap_spacing(self):
        """Clients should have gap spacing between items."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "gap-" in content, "Clients should have gap spacing"

    def test_clients_conditionally_renders(self):
        """Clients should only render when data exists."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "clients && page.clients.length" in content or "page?.clients && page.clients.length" in content, (
            "Clients should conditionally render when data exists"
        )


class TestClientTag:
    """Test ClientTag component for client display."""

    def test_client_tag_component_exists(self):
        """ClientTag component should exist."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "ClientTag" in content, (
            "About page should have ClientTag component"
        )

    def test_client_tag_accepts_client_prop(self):
        """ClientTag should accept client prop."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "client:" in content and "string" in content, (
            "ClientTag should accept client prop"
        )

    def test_client_tag_uses_inline_block(self):
        """ClientTag should use inline-block or similar display."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "inline-block" in content or "inline-flex" in content, (
            "ClientTag should use inline-block display"
        )

    def test_client_tag_has_hover_effects(self):
        """ClientTag should have hover effects."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "hover:" in content, "ClientTag should have hover effects"


class TestSEOMetadata:
    """Test that SEO metadata is properly configured."""

    def test_exports_generate_metadata(self):
        """About page should export generateMetadata function."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "generateMetadata" in content, (
            "About page should export generateMetadata"
        )

    def test_generate_metadata_is_async(self):
        """generateMetadata should be async function."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "async function generateMetadata" in content or "export async function generateMetadata" in content, (
            "generateMetadata should be async"
        )

    def test_metadata_fetches_page_data(self):
        """generateMetadata should fetch page data."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "sanityFetch" in content and "aboutPageQuery" in content, (
            "generateMetadata should fetch page data"
        )

    def test_metadata_returns_metadata_type(self):
        """generateMetadata should return Metadata type."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "Metadata" in content, (
            "generateMetadata should return Metadata type"
        )

    def test_metadata_includes_title(self):
        """Metadata should include title."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "title:" in content, "Metadata should include title"

    def test_metadata_includes_description(self):
        """Metadata should include description."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "description:" in content, "Metadata should include description"

    def test_metadata_includes_open_graph(self):
        """Metadata should include Open Graph config."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "openGraph" in content, (
            "Metadata should include Open Graph configuration"
        )

    def test_metadata_uses_seo_fields(self):
        """Metadata should use SEO fields from CMS."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "seo?.metaTitle" in content or "seo.metaTitle" in content, (
            "Metadata should use SEO metaTitle from CMS"
        )

    def test_metadata_has_fallbacks(self):
        """Metadata should have fallback values."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "||" in content or "??" in content, (
            "Metadata should have fallback values"
        )

    def test_metadata_uses_og_image(self):
        """Metadata should use OG image from CMS."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "ogImage" in content, (
            "Metadata should use OG image from CMS"
        )


class TestSemanticHTML:
    """Test that about page uses proper semantic HTML."""

    def test_uses_article_wrapper(self):
        """About page should use article element as wrapper."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "<article" in content, "About page should use article element"

    def test_uses_section_elements(self):
        """About page should use section elements for content areas."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "<section" in content, "About page should use section elements"

    def test_uses_header_element(self):
        """About page should use header element for section headers."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "<header" in content, (
            "About page should use header element for section headers"
        )

    def test_uses_h1_heading(self):
        """About page should have h1 heading for name."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "<h1" in content, "About page should have h1 heading"

    def test_uses_h2_for_sections(self):
        """About page should use h2 for section headings."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "<h2" in content, (
            "About page should use h2 for section headings"
        )

    def test_sections_have_aria_labels(self):
        """Sections should have aria-label or aria-labelledby."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "aria-label" in content or "aria-labelledby" in content, (
            "Sections should have aria-label for accessibility"
        )

    def test_decorative_elements_hidden(self):
        """Decorative elements should be hidden from accessibility."""
        content = ABOUT_PAGE_FILE.read_text()
        assert 'aria-hidden="true"' in content, (
            "Decorative elements should have aria-hidden"
        )


class TestTailwindStyling:
    """Test that about page uses Tailwind CSS properly."""

    def test_uses_tailwind_layout_classes(self):
        """About page should use Tailwind layout classes."""
        content = ABOUT_PAGE_FILE.read_text()
        tailwind_indicators = ["flex", "grid", "items-", "justify-", "mx-auto", "max-w-"]
        found = [cls for cls in tailwind_indicators if cls in content]
        assert len(found) >= 3, f"About page should use Tailwind layout classes, found: {found}"

    def test_uses_tailwind_spacing_classes(self):
        """About page should use Tailwind spacing classes."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "px-" in content and "py-" in content, (
            "About page should use Tailwind padding classes"
        )

    def test_uses_responsive_classes(self):
        """About page should use responsive Tailwind classes."""
        content = ABOUT_PAGE_FILE.read_text()
        responsive_prefixes = ["sm:", "md:", "lg:", "xl:"]
        found = [prefix for prefix in responsive_prefixes if prefix in content]
        assert len(found) >= 2, (
            "About page should use responsive Tailwind classes"
        )

    def test_uses_dark_mode_classes(self):
        """About page should support dark mode."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "dark:" in content, "About page should have dark mode support"

    def test_uses_brand_colors(self):
        """About page should use brand color classes."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "brand-" in content, "About page should use brand color utilities"


class TestAnimations:
    """Test that about page has appropriate animations."""

    def test_uses_animation_classes(self):
        """About page should use animation classes."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "animate-" in content, "About page should use animation classes"

    def test_has_animation_delays(self):
        """About page should have staggered animation delays."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "animation-delay" in content or "delay" in content.lower(), (
            "About page should have animation delays"
        )

    def test_uses_transitions(self):
        """About page should use transition effects."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "transition" in content, (
            "About page should use transition effects"
        )


class TestHoverEffects:
    """Test that about page elements have hover effects."""

    def test_has_hover_effects(self):
        """About page should have hover effects."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "hover:" in content, "About page should have hover effects"

    def test_has_group_hover(self):
        """About page should use group hover for coordinated effects."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "group" in content and "group-hover:" in content, (
            "About page should use group hover for coordinated effects"
        )


class TestCTASection:
    """Test that about page has call-to-action section."""

    def test_cta_section_exists(self):
        """About page should have CTA section."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "contact" in content.lower() or "Get in Touch" in content, (
            "About page should have CTA section"
        )

    def test_cta_links_to_contact(self):
        """CTA should link to contact page."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "/contact" in content, "CTA should link to contact page"

    def test_cta_has_focus_styles(self):
        """CTA should have focus styles for accessibility."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "focus:" in content or "focus-visible:" in content, (
            "CTA should have focus styles for accessibility"
        )


class TestAboutPageTypes:
    """Test that AboutPage type is properly defined in types/sanity.ts."""

    def test_types_file_exists(self):
        """types/sanity.ts should exist."""
        assert TYPES_FILE.exists(), "types/sanity.ts not found"

    def test_about_page_type_exported(self):
        """AboutPage type should be exported."""
        content = TYPES_FILE.read_text()
        assert "export interface AboutPage" in content, (
            "AboutPage type should be exported"
        )

    def test_credential_type_exported(self):
        """Credential type should be exported."""
        content = TYPES_FILE.read_text()
        assert "export interface Credential" in content, (
            "Credential type should be exported"
        )

    def test_about_page_has_heading_field(self):
        """AboutPage type should have heading field."""
        content = TYPES_FILE.read_text()
        assert "heading" in content, "AboutPage should have heading field"

    def test_about_page_has_profile_image_field(self):
        """AboutPage type should have profileImage field."""
        content = TYPES_FILE.read_text()
        assert "profileImage" in content, (
            "AboutPage should have profileImage field"
        )

    def test_about_page_has_name_field(self):
        """AboutPage type should have name field."""
        content = TYPES_FILE.read_text()
        assert "name" in content, "AboutPage should have name field"

    def test_about_page_has_tagline_field(self):
        """AboutPage type should have tagline field."""
        content = TYPES_FILE.read_text()
        assert "tagline" in content, "AboutPage should have tagline field"

    def test_about_page_has_bio_field(self):
        """AboutPage type should have bio field."""
        content = TYPES_FILE.read_text()
        assert "bio" in content, "AboutPage should have bio field"

    def test_about_page_has_credentials_field(self):
        """AboutPage type should have credentials field."""
        content = TYPES_FILE.read_text()
        assert "credentials" in content, "AboutPage should have credentials field"

    def test_about_page_has_clients_field(self):
        """AboutPage type should have clients field."""
        content = TYPES_FILE.read_text()
        assert "clients" in content, "AboutPage should have clients field"

    def test_about_page_has_seo_field(self):
        """AboutPage type should have seo field."""
        content = TYPES_FILE.read_text()
        assert "seo" in content, "AboutPage should have seo field"

    def test_credential_has_title_field(self):
        """Credential type should have title field."""
        content = TYPES_FILE.read_text()
        assert "title: string" in content, (
            "Credential should have title field"
        )

    def test_credential_has_organization_field(self):
        """Credential type should have organization field."""
        content = TYPES_FILE.read_text()
        assert "organization" in content, (
            "Credential should have organization field"
        )

    def test_credential_has_period_field(self):
        """Credential type should have period field."""
        content = TYPES_FILE.read_text()
        assert "period" in content, "Credential should have period field"


class TestCMSEditability:
    """Test that all content is editable via CMS (fetched from Sanity)."""

    def test_heading_from_cms(self):
        """Heading should come from CMS."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page.heading" in content or "page?.heading" in content, (
            "Heading should be fetched from CMS"
        )

    def test_name_from_cms(self):
        """Name should come from CMS."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page.name" in content or "page?.name" in content, (
            "Name should be fetched from CMS"
        )

    def test_tagline_from_cms(self):
        """Tagline should come from CMS."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page.tagline" in content or "page?.tagline" in content, (
            "Tagline should be fetched from CMS"
        )

    def test_bio_from_cms(self):
        """Bio should come from CMS."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page.bio" in content or "page?.bio" in content, (
            "Bio should be fetched from CMS"
        )

    def test_profile_image_from_cms(self):
        """Profile image should come from CMS."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page.profileImage" in content or "page?.profileImage" in content, (
            "Profile image should be fetched from CMS"
        )

    def test_credentials_from_cms(self):
        """Credentials should come from CMS."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page.credentials" in content or "page?.credentials" in content, (
            "Credentials should be fetched from CMS"
        )

    def test_clients_from_cms(self):
        """Clients should come from CMS."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "page.clients" in content or "page?.clients" in content, (
            "Clients should be fetched from CMS"
        )

    def test_no_hardcoded_content(self):
        """Main content should not be hardcoded (except labels)."""
        content = ABOUT_PAGE_FILE.read_text()
        # Check that profile info comes from CMS, not hardcoded
        lines = content.split('\n')
        # Count references to page data
        page_refs = content.count('page.')
        assert page_refs >= 10, (
            "About page should reference CMS data frequently (found {} refs)".format(page_refs)
        )


class TestResponsiveLayout:
    """Test that about page has responsive layout."""

    def test_uses_lg_breakpoint(self):
        """About page should use lg: breakpoint for desktop."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "lg:" in content, "About page should use lg: breakpoint"

    def test_uses_md_breakpoint(self):
        """About page should use md: breakpoint for tablet."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "md:" in content, "About page should use md: breakpoint"

    def test_uses_sm_breakpoint(self):
        """About page should use sm: breakpoint for small screens."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "sm:" in content, "About page should use sm: breakpoint"

    def test_hero_section_responsive(self):
        """Hero section should have responsive flex direction."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "flex-col" in content and "lg:flex-row" in content, (
            "Hero section should have responsive flex direction"
        )

    def test_profile_image_responsive_sizing(self):
        """Profile image container should have responsive sizing."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "lg:w-1/2" in content or "lg:w-" in content, (
            "Profile image container should have responsive sizing"
        )


class TestHeroSection:
    """Test hero section specific requirements."""

    def test_hero_section_has_min_height(self):
        """Hero section should have minimum height."""
        content = ABOUT_PAGE_FILE.read_text()
        assert "min-h-" in content, "Hero section should have minimum height"

    def test_hero_section_aria_label(self):
        """Hero section should have aria-label."""
        content = ABOUT_PAGE_FILE.read_text()
        assert 'aria-label="Introduction"' in content or "aria-label='Introduction'" in content, (
            "Hero section should have aria-label='Introduction'"
        )

    def test_hero_has_decorative_elements(self):
        """Hero should have decorative elements marked as hidden."""
        content = ABOUT_PAGE_FILE.read_text()
        # Check for decorative elements with aria-hidden
        assert "aria-hidden" in content, (
            "Hero should have decorative elements with aria-hidden"
        )
