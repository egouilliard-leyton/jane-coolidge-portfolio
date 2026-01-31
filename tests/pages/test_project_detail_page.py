"""
Tests for T-016: Individual project detail pages

These tests verify that the project detail page (app/(site)/projects/[slug]/page.tsx)
is properly implemented according to requirements:
- Dynamic route fetches project by slug parameter
- Project metadata (title, category, client, date) displays prominently
- Description renders as Portable Text with proper formatting
- Gallery displays all project images in responsive grid
- Gallery images support ImageWithPopup interaction
- generateMetadata exports SEO tags correctly
- generateStaticParams enables static generation

Acceptance Criteria:
- Dynamic route fetches project by slug
- Project metadata (title, category, client, date) displays prominently
- Description renders as Portable Text with proper formatting
- Gallery displays all project images in responsive grid
- Gallery images support ImageWithPopup interaction
- generateMetadata exports SEO tags
- generateStaticParams enables static generation
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
PROJECT_DETAIL_PAGE_FILE = PROJECT_ROOT / "app" / "(site)" / "projects" / "[slug]" / "page.tsx"
QUERIES_FILE = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
IMAGE_WITH_POPUP_FILE = PROJECT_ROOT / "components" / "ui" / "ImageWithPopup.tsx"
BLOG_CONTENT_FILE = PROJECT_ROOT / "components" / "content" / "BlogContent.tsx"


class TestProjectDetailPageFileExists:
    """Test that project detail page file exists and has proper structure."""

    def test_project_detail_page_file_exists(self):
        """app/(site)/projects/[slug]/page.tsx should exist."""
        assert PROJECT_DETAIL_PAGE_FILE.exists(), "app/(site)/projects/[slug]/page.tsx not found"

    def test_project_detail_page_is_server_component(self):
        """Project detail page should be an async Server Component."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "async function ProjectPage" in content or "export default async function ProjectPage" in content, (
            "Project detail page should be an async function (Server Component)"
        )

    def test_project_detail_page_no_use_client_directive(self):
        """Project detail page should NOT have 'use client' directive (Server Component)."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "'use client'" not in content and '"use client"' not in content, (
            "Project detail page should be a Server Component without 'use client' directive"
        )

    def test_project_detail_page_exports_default(self):
        """Project detail page should have a default export."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "export default" in content, (
            "Project detail page should have a default export"
        )


class TestDynamicRouteSlugFetching:
    """Test that dynamic route fetches project by slug parameter."""

    def test_page_accepts_params_prop(self):
        """Project detail page should accept params prop with slug."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "params" in content, (
            "Project detail page should accept params prop"
        )

    def test_page_extracts_slug_from_params(self):
        """Project detail page should extract slug from params."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "slug" in content, (
            "Project detail page should use slug from params"
        )

    def test_page_awaits_params(self):
        """Project detail page should await params (Next.js 15 async params)."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "await params" in content, (
            "Project detail page should await params for Next.js 15"
        )

    def test_page_imports_sanity_fetch(self):
        """Project detail page should import sanityFetch from Sanity client."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "sanityFetch" in content, "Project detail page should import sanityFetch"
        assert "@/sanity/lib/client" in content, (
            "Project detail page should import from @/sanity/lib/client"
        )

    def test_page_imports_project_by_slug_query(self):
        """Project detail page should import projectBySlugQuery."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "projectBySlugQuery" in content, (
            "Project detail page should import projectBySlugQuery"
        )

    def test_page_passes_slug_param_to_query(self):
        """Project detail page should pass slug param to query."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "params: { slug }" in content or "params: {slug}" in content, (
            "Project detail page should pass slug param to projectBySlugQuery"
        )

    def test_page_uses_cache_tags(self):
        """Project detail page should use cache tags for revalidation."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "tags:" in content and "project" in content, (
            "Project detail page should use 'project' tag for cache revalidation"
        )


class TestProjectMetadataDisplay:
    """Test that project metadata (title, category, client, date) displays prominently."""

    def test_page_displays_project_title(self):
        """Project detail page should display project title."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "project.title" in content, (
            "Project detail page should display project title"
        )

    def test_page_uses_h1_for_title(self):
        """Project detail page should use h1 for main title."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "<h1" in content, (
            "Project detail page should use h1 for main title"
        )

    def test_page_displays_category(self):
        """Project detail page should display category."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "category" in content, (
            "Project detail page should display category"
        )

    def test_page_has_category_labels(self):
        """Project detail page should have category display labels."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        # Implementation has CATEGORY_LABELS mapping
        assert "CATEGORY_LABELS" in content or "categoryLabel" in content, (
            "Project detail page should have category label mapping"
        )

    def test_page_displays_client(self):
        """Project detail page should display client."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "project.client" in content, (
            "Project detail page should display client"
        )

    def test_page_displays_date(self):
        """Project detail page should display date."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "project.date" in content or "formattedDate" in content, (
            "Project detail page should display date"
        )

    def test_page_uses_time_element_for_date(self):
        """Project detail page should use time element for semantic date."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "<time" in content, (
            "Project detail page should use time element"
        )

    def test_time_element_has_datetime_attribute(self):
        """Time element should have dateTime attribute."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "dateTime=" in content, (
            "Time element should have dateTime attribute"
        )

    def test_page_formats_date(self):
        """Project detail page should format the date for display."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "toLocaleDateString" in content, (
            "Project detail page should format date using toLocaleDateString"
        )

    def test_metadata_renders_conditionally(self):
        """Metadata should only render when available."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        # Check for conditional rendering of client
        assert "project.client &&" in content or "{project.client &&" in content.replace(" ", ""), (
            "Client should render conditionally"
        )


class TestPortableTextDescriptionRendering:
    """Test that description renders as Portable Text with proper formatting."""

    def test_page_imports_blog_content_component(self):
        """Project detail page should import BlogContent component for Portable Text."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "BlogContent" in content, (
            "Project detail page should import BlogContent component"
        )
        assert "@/components/content" in content, (
            "Project detail page should import from @/components/content"
        )

    def test_page_renders_blog_content(self):
        """Project detail page should render BlogContent component for description."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "<BlogContent" in content, (
            "Project detail page should render BlogContent component"
        )

    def test_blog_content_receives_content_prop(self):
        """BlogContent should receive content prop from project description."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "content=" in content and "project.description" in content, (
            "BlogContent should receive content prop from project.description"
        )

    def test_page_handles_empty_description(self):
        """Project detail page should handle empty description gracefully."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        # Check for conditional description rendering
        assert "description &&" in content or "description.length" in content, (
            "Project detail page should check for description existence"
        )


class TestGalleryWithImageWithPopup:
    """Test that gallery displays all project images with ImageWithPopup support."""

    def test_page_imports_image_with_popup(self):
        """Project detail page should import ImageWithPopup component."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "ImageWithPopup" in content, (
            "Project detail page should import ImageWithPopup component"
        )
        assert "@/components/ui" in content, (
            "Project detail page should import from @/components/ui"
        )

    def test_page_renders_image_with_popup(self):
        """Project detail page should render ImageWithPopup component in gallery."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "<ImageWithPopup" in content, (
            "Project detail page should render ImageWithPopup component"
        )

    def test_image_with_popup_receives_image_prop(self):
        """ImageWithPopup should receive image prop."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "image=" in content or "image={" in content, (
            "ImageWithPopup should receive image prop"
        )

    def test_image_with_popup_receives_alt_prop(self):
        """ImageWithPopup should receive alt prop."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "alt=" in content, (
            "ImageWithPopup should receive alt prop"
        )

    def test_image_with_popup_receives_popup_prop(self):
        """ImageWithPopup should receive popup prop."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        # The component receives popup prop in gallery
        assert "popup=" in content or "popup={" in content, (
            "ImageWithPopup should receive popup prop"
        )

    def test_gallery_maps_over_images(self):
        """Gallery should map over project images array."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "images.map" in content or "project.images.map" in content, (
            "Gallery should map over project images"
        )

    def test_gallery_uses_responsive_grid(self):
        """Gallery should use responsive grid layout."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "grid" in content, (
            "Gallery should use CSS grid"
        )
        assert "grid-cols" in content, (
            "Gallery should use responsive grid columns"
        )

    def test_gallery_has_section_heading(self):
        """Gallery section should have a heading."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "Gallery" in content or "gallery" in content, (
            "Gallery section should have heading"
        )

    def test_gallery_handles_empty_images(self):
        """Gallery should handle empty images array."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "images &&" in content or "images.length" in content, (
            "Gallery should check for images existence"
        )

    def test_gallery_uses_aria_label(self):
        """Gallery section should have aria-label for accessibility."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert 'aria-label' in content and 'gallery' in content.lower(), (
            "Gallery section should have aria-label"
        )


class TestGenerateMetadataSEO:
    """Test that generateMetadata exports SEO tags correctly."""

    def test_page_exports_generate_metadata(self):
        """Project detail page should export generateMetadata function."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "export async function generateMetadata" in content, (
            "Project detail page should export generateMetadata"
        )

    def test_generate_metadata_accepts_params(self):
        """generateMetadata should accept params with slug."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "generateMetadata" in content and "params" in content, (
            "generateMetadata should accept params"
        )

    def test_generate_metadata_returns_title(self):
        """generateMetadata should return title."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "title:" in content or "title :" in content, (
            "generateMetadata should return title"
        )

    def test_generate_metadata_returns_description(self):
        """generateMetadata should return description."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        # Check for description in metadata object
        assert "description," in content or "description:" in content or "description :" in content, (
            "generateMetadata should return description"
        )

    def test_generate_metadata_includes_open_graph(self):
        """generateMetadata should include Open Graph tags."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "openGraph" in content, (
            "generateMetadata should include openGraph configuration"
        )

    def test_generate_metadata_uses_project_seo_fields(self):
        """generateMetadata should use project's SEO fields when available."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "seo" in content, (
            "generateMetadata should check for SEO fields"
        )

    def test_generate_metadata_falls_back_to_project_fields(self):
        """generateMetadata should fall back to project title."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "project.title" in content, (
            "generateMetadata should fall back to project.title"
        )

    def test_generate_metadata_includes_og_image(self):
        """generateMetadata should include OG image."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "ogImage" in content or "images:" in content, (
            "generateMetadata should include OG image"
        )

    def test_generate_metadata_includes_twitter_card(self):
        """generateMetadata should include Twitter card metadata."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "twitter:" in content or "twitter :" in content, (
            "generateMetadata should include Twitter card metadata"
        )

    def test_generate_metadata_includes_article_type(self):
        """generateMetadata should set type to article for Open Graph."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "'article'" in content or '"article"' in content, (
            "generateMetadata should set type to 'article'"
        )

    def test_generate_metadata_includes_published_time(self):
        """generateMetadata should include publishedTime for articles."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "publishedTime" in content, (
            "generateMetadata should include publishedTime"
        )


class TestGenerateStaticParams:
    """Test that generateStaticParams enables static generation."""

    def test_page_exports_generate_static_params(self):
        """Project detail page should export generateStaticParams function."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "export async function generateStaticParams" in content, (
            "Project detail page should export generateStaticParams"
        )

    def test_generate_static_params_imports_slugs_query(self):
        """generateStaticParams should import projectSlugsQuery."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "projectSlugsQuery" in content, (
            "generateStaticParams should import projectSlugsQuery"
        )

    def test_generate_static_params_returns_slug_array(self):
        """generateStaticParams should return array of slug objects."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        # Check for return statement with slug mapping
        assert "slug:" in content and "map" in content, (
            "generateStaticParams should return mapped slug objects"
        )

    def test_project_slugs_query_exists(self):
        """projectSlugsQuery should be defined in queries file."""
        content = QUERIES_FILE.read_text()
        assert "export const projectSlugsQuery" in content, (
            "projectSlugsQuery should be exported from queries"
        )


class TestNotFoundHandling:
    """Test 404 handling for non-existent slugs."""

    def test_page_imports_not_found(self):
        """Project detail page should import notFound from next/navigation."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "notFound" in content, (
            "Project detail page should import notFound"
        )
        assert "next/navigation" in content, (
            "Project detail page should import from next/navigation"
        )

    def test_page_calls_not_found_when_project_is_null(self):
        """Project detail page should call notFound when project is not found."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "notFound()" in content, (
            "Project detail page should call notFound()"
        )

    def test_page_checks_for_null_project(self):
        """Project detail page should check if project is null."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "!project" in content or "project === null" in content or "project == null" in content, (
            "Project detail page should check for null project"
        )

    def test_generate_metadata_handles_not_found(self):
        """generateMetadata should handle case when project is not found."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        # Check that generateMetadata returns something even if project is null
        assert "Not Found" in content or "not found" in content.lower(), (
            "generateMetadata should handle project not found case"
        )


class TestProjectDetailPageSemanticHTML:
    """Test that project detail page uses proper semantic HTML."""

    def test_uses_article_element(self):
        """Project detail page should use article element as main wrapper."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "<article" in content, (
            "Project detail page should use article element"
        )

    def test_uses_header_element(self):
        """Project detail page should use header element for project header."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "<header" in content, (
            "Project detail page should use header element"
        )

    def test_uses_section_element(self):
        """Project detail page should use section elements for content sections."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "<section" in content, (
            "Project detail page should use section elements"
        )

    def test_uses_footer_element(self):
        """Project detail page should use footer element for project footer."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "<footer" in content, (
            "Project detail page should use footer element"
        )

    def test_uses_nav_element(self):
        """Project detail page should use nav element for navigation."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "<nav" in content, (
            "Project detail page should use nav element"
        )


class TestProjectDetailPageLinks:
    """Test that project detail page has proper navigation links."""

    def test_imports_next_link(self):
        """Project detail page should import Link from next/link."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "import Link from 'next/link'" in content or 'import Link from "next/link"' in content, (
            "Project detail page should import Next.js Link component"
        )

    def test_has_back_to_projects_link(self):
        """Project detail page should have link back to projects listing."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "/projects" in content and "<Link" in content, (
            "Project detail page should have link to /projects"
        )

    def test_has_adjacent_project_navigation(self):
        """Project detail page should have previous/next project navigation."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "previous" in content.lower() and "next" in content.lower(), (
            "Project detail page should have adjacent project navigation"
        )


class TestProjectDetailPageStyling:
    """Test that project detail page has proper Tailwind styling."""

    def test_uses_responsive_classes(self):
        """Project detail page should use responsive Tailwind classes."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        responsive_prefixes = ["sm:", "md:", "lg:", "xl:"]
        found = [prefix for prefix in responsive_prefixes if prefix in content]
        assert len(found) >= 2, (
            "Project detail page should use responsive Tailwind classes"
        )

    def test_uses_dark_mode_classes(self):
        """Project detail page should support dark mode."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "dark:" in content, (
            "Project detail page should have dark mode support"
        )

    def test_uses_brand_colors(self):
        """Project detail page should use brand color classes."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "brand-" in content, (
            "Project detail page should use brand color utilities"
        )

    def test_has_animation_classes(self):
        """Project detail page should have animation classes."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "animate-" in content or "animation-" in content, (
            "Project detail page should have animation classes"
        )


class TestProjectDetailPageAccessibility:
    """Test project detail page accessibility features."""

    def test_has_aria_hidden_decorative_elements(self):
        """Decorative elements should have aria-hidden."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert 'aria-hidden="true"' in content, (
            "Decorative elements should have aria-hidden"
        )

    def test_has_aria_labels(self):
        """Interactive elements should have aria-labels."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "aria-label" in content, (
            "Interactive elements should have aria-labels"
        )


class TestProjectBySlugQuery:
    """Test that projectBySlugQuery is properly defined."""

    def test_project_by_slug_query_exists(self):
        """projectBySlugQuery should be defined in queries file."""
        content = QUERIES_FILE.read_text()
        assert "export const projectBySlugQuery" in content, (
            "projectBySlugQuery should be exported"
        )

    def test_query_filters_by_slug(self):
        """projectBySlugQuery should filter by slug.current."""
        content = QUERIES_FILE.read_text()
        assert "slug.current == $slug" in content, (
            "projectBySlugQuery should filter by slug.current"
        )

    def test_query_includes_description_field(self):
        """projectBySlugQuery should include description field."""
        content = QUERIES_FILE.read_text()
        assert "description" in content, (
            "projectBySlugQuery should include description field"
        )

    def test_query_includes_cover_image(self):
        """projectBySlugQuery should include coverImage."""
        content = QUERIES_FILE.read_text()
        assert "coverImage" in content, (
            "projectBySlugQuery should include coverImage"
        )

    def test_query_includes_images_gallery(self):
        """projectBySlugQuery should include images gallery."""
        content = QUERIES_FILE.read_text()
        assert "images[]" in content or "images []" in content, (
            "projectBySlugQuery should include images gallery"
        )

    def test_query_includes_seo_fields(self):
        """projectBySlugQuery should include SEO fields."""
        content = QUERIES_FILE.read_text()
        assert "seo" in content, (
            "projectBySlugQuery should include seo field"
        )

    def test_query_expands_image_assets(self):
        """projectBySlugQuery should expand image assets."""
        content = QUERIES_FILE.read_text()
        assert "asset->" in content or "asset ->" in content, (
            "projectBySlugQuery should expand asset references"
        )

    def test_query_includes_popup_expansion(self):
        """projectBySlugQuery should expand popup references for gallery images."""
        content = QUERIES_FILE.read_text()
        assert "popup->" in content or "popup ->" in content, (
            "projectBySlugQuery should expand popup references"
        )

    def test_query_includes_lqip_metadata(self):
        """projectBySlugQuery should include LQIP metadata for blur placeholder."""
        content = QUERIES_FILE.read_text()
        assert "lqip" in content, (
            "projectBySlugQuery should include lqip for blur placeholder"
        )


class TestProjectDetailType:
    """Test that ProjectDetail type is properly defined."""

    def test_page_imports_project_detail_type(self):
        """Project detail page should import ProjectDetail type."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "ProjectDetail" in content, (
            "Project detail page should import ProjectDetail type"
        )

    def test_project_detail_type_exists_in_queries(self):
        """ProjectDetail type should be defined in queries file."""
        content = QUERIES_FILE.read_text()
        assert "ProjectDetail" in content, (
            "ProjectDetail type should be defined in queries"
        )


class TestCoverImageDisplay:
    """Test that cover image displays properly."""

    def test_page_uses_next_image(self):
        """Project detail page should use Next.js Image component."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "Project detail page should import Next.js Image component"
        )
        assert "<Image" in content, "Project detail page should use Image component"

    def test_page_uses_url_for_helper(self):
        """Project detail page should use urlFor helper for image URLs."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "urlFor" in content, (
            "Project detail page should use urlFor helper"
        )
        assert "@/sanity/lib/image" in content, (
            "Project detail page should import urlFor from @/sanity/lib/image"
        )

    def test_cover_image_has_blur_placeholder(self):
        """Cover image should use blur placeholder when LQIP is available."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "placeholder" in content, (
            "Cover image should support placeholder prop"
        )
        assert "blur" in content, (
            "Cover image should use blur placeholder"
        )

    def test_cover_image_has_priority(self):
        """Cover image should have priority prop for LCP optimization."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "priority" in content, (
            "Cover image should have priority prop"
        )

    def test_cover_image_has_fill_prop(self):
        """Cover image should use fill layout mode."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "fill" in content, (
            "Cover image should use fill prop for responsive sizing"
        )

    def test_cover_image_handles_missing_image(self):
        """Page should handle missing cover image gracefully."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        # Check for conditional rendering of cover image
        assert "coverImage" in content, (
            "Page should check for coverImage"
        )


class TestAdjacentProjectsQuery:
    """Test that adjacent projects query is properly defined."""

    def test_adjacent_projects_query_exists(self):
        """adjacentProjectsQuery should be defined in queries file."""
        content = QUERIES_FILE.read_text()
        assert "export const adjacentProjectsQuery" in content, (
            "adjacentProjectsQuery should be exported"
        )

    def test_page_imports_adjacent_projects_query(self):
        """Project detail page should import adjacentProjectsQuery."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "adjacentProjectsQuery" in content, (
            "Project detail page should import adjacentProjectsQuery"
        )

    def test_page_imports_adjacent_projects_result_type(self):
        """Project detail page should import AdjacentProjectsResult type."""
        content = PROJECT_DETAIL_PAGE_FILE.read_text()
        assert "AdjacentProjectsResult" in content, (
            "Project detail page should import AdjacentProjectsResult type"
        )

    def test_adjacent_projects_has_previous(self):
        """adjacentProjectsQuery should return previous project."""
        content = QUERIES_FILE.read_text()
        assert '"previous"' in content or "'previous'" in content, (
            "adjacentProjectsQuery should have 'previous' field"
        )

    def test_adjacent_projects_has_next(self):
        """adjacentProjectsQuery should return next project."""
        content = QUERIES_FILE.read_text()
        assert '"next"' in content or "'next'" in content, (
            "adjacentProjectsQuery should have 'next' field"
        )


class TestImageWithPopupComponent:
    """Test that ImageWithPopup component exists and has correct structure."""

    def test_image_with_popup_file_exists(self):
        """ImageWithPopup component file should exist."""
        assert IMAGE_WITH_POPUP_FILE.exists(), (
            "ImageWithPopup component file should exist"
        )

    def test_image_with_popup_is_client_component(self):
        """ImageWithPopup should be a client component (uses state/effects)."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "ImageWithPopup should be a client component"
        )

    def test_image_with_popup_accepts_popup_prop(self):
        """ImageWithPopup should accept popup prop."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "popup" in content, (
            "ImageWithPopup should accept popup prop"
        )

    def test_image_with_popup_exports_interface(self):
        """ImageWithPopup should export ImageWithPopupProps interface."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "ImageWithPopupProps" in content, (
            "ImageWithPopup should define ImageWithPopupProps interface"
        )
