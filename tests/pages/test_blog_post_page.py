"""
Tests for T-014: Individual blog post pages

These tests verify that the blog post detail page (app/(site)/blog/[slug]/page.tsx)
is properly implemented according to requirements:
- Dynamic route fetches post by slug parameter
- Cover image displays with blur-up placeholder
- Title, date, and tags render above content
- Portable Text content renders with all formatting
- Images within content support popup feature where defined
- generateMetadata exports SEO tags correctly
- generateStaticParams enables static generation
- 404 handling for non-existent slugs

Acceptance Criteria:
- Dynamic route fetches post by slug parameter
- Cover image displays with blur-up placeholder
- Title, date, and tags render above content
- Portable Text content renders with all formatting
- Images within content support popup feature where defined
- generateMetadata exports SEO tags correctly
- generateStaticParams enables static generation
- 404 handling for non-existent slugs
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
BLOG_POST_PAGE_FILE = PROJECT_ROOT / "app" / "(site)" / "blog" / "[slug]" / "page.tsx"
QUERIES_FILE = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
BLOG_CONTENT_FILE = PROJECT_ROOT / "components" / "content" / "BlogContent.tsx"


class TestBlogPostPageFileExists:
    """Test that blog post page file exists and has proper structure."""

    def test_blog_post_page_file_exists(self):
        """app/(site)/blog/[slug]/page.tsx should exist."""
        assert BLOG_POST_PAGE_FILE.exists(), "app/(site)/blog/[slug]/page.tsx not found"

    def test_blog_post_page_is_server_component(self):
        """Blog post page should be an async Server Component."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "async function BlogPostPage" in content or "export default async function BlogPostPage" in content, (
            "Blog post page should be an async function (Server Component)"
        )

    def test_blog_post_page_no_use_client_directive(self):
        """Blog post page should NOT have 'use client' directive (Server Component)."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "'use client'" not in content and '"use client"' not in content, (
            "Blog post page should be a Server Component without 'use client' directive"
        )

    def test_blog_post_page_exports_default(self):
        """Blog post page should have a default export."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "export default" in content, (
            "Blog post page should have a default export"
        )


class TestDynamicRouteSlugFetching:
    """Test that dynamic route fetches post by slug parameter."""

    def test_page_accepts_params_prop(self):
        """Blog post page should accept params prop with slug."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "params" in content, (
            "Blog post page should accept params prop"
        )

    def test_page_extracts_slug_from_params(self):
        """Blog post page should extract slug from params."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "slug" in content, (
            "Blog post page should use slug from params"
        )

    def test_page_imports_sanity_fetch(self):
        """Blog post page should import sanityFetch from Sanity client."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "sanityFetch" in content, "Blog post page should import sanityFetch"
        assert "@/sanity/lib/client" in content, (
            "Blog post page should import from @/sanity/lib/client"
        )

    def test_page_imports_blog_post_by_slug_query(self):
        """Blog post page should import blogPostBySlugQuery."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "blogPostBySlugQuery" in content, (
            "Blog post page should import blogPostBySlugQuery"
        )

    def test_page_passes_slug_param_to_query(self):
        """Blog post page should pass slug param to query."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "params: { slug }" in content or "params: {slug}" in content, (
            "Blog post page should pass slug param to blogPostBySlugQuery"
        )

    def test_page_uses_cache_tags(self):
        """Blog post page should use cache tags for revalidation."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "tags:" in content and "blogPost" in content, (
            "Blog post page should use 'blogPost' tag for cache revalidation"
        )


class TestCoverImageWithBlurUp:
    """Test that cover image displays with blur-up placeholder."""

    def test_page_uses_next_image(self):
        """Blog post page should use Next.js Image component."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "Blog post page should import Next.js Image component"
        )
        assert "<Image" in content, "Blog post page should use Image component"

    def test_page_uses_url_for_helper(self):
        """Blog post page should use urlFor helper for image URLs."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "urlFor" in content, (
            "Blog post page should use urlFor helper"
        )
        assert "@/sanity/lib/image" in content, (
            "Blog post page should import urlFor from @/sanity/lib/image"
        )

    def test_cover_image_has_blur_placeholder(self):
        """Cover image should use blur placeholder when LQIP is available."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "placeholder" in content, (
            "Cover image should support placeholder prop"
        )
        assert "blur" in content, (
            "Cover image should use blur placeholder"
        )

    def test_cover_image_has_blur_data_url(self):
        """Cover image should use blurDataURL from LQIP metadata."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "blurDataURL" in content, (
            "Cover image should use blurDataURL prop"
        )
        assert "lqip" in content, (
            "Cover image should use lqip from asset metadata"
        )

    def test_cover_image_has_priority(self):
        """Cover image should have priority prop for LCP optimization."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "priority" in content, (
            "Cover image should have priority prop"
        )

    def test_cover_image_has_fill_prop(self):
        """Cover image should use fill layout mode."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "fill" in content, (
            "Cover image should use fill prop for responsive sizing"
        )

    def test_cover_image_has_sizes_prop(self):
        """Cover image should have sizes prop for responsive images."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "sizes=" in content, (
            "Cover image should have sizes prop"
        )

    def test_cover_image_has_alt_text(self):
        """Cover image should have alt text."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "alt=" in content, (
            "Cover image should have alt attribute"
        )

    def test_cover_image_handles_missing_image(self):
        """Page should handle missing cover image gracefully."""
        content = BLOG_POST_PAGE_FILE.read_text()
        # Check for conditional rendering of cover image
        assert "coverImage" in content, (
            "Page should check for coverImage"
        )


class TestTitleDateTagsRendering:
    """Test that title, date, and tags render above content."""

    def test_page_displays_post_title(self):
        """Blog post page should display post title."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "post.title" in content, (
            "Blog post page should display post title"
        )

    def test_page_uses_h1_for_title(self):
        """Blog post page should use h1 for main title."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "<h1" in content, (
            "Blog post page should use h1 for main title"
        )

    def test_page_displays_publish_date(self):
        """Blog post page should display publish date."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "publishedAt" in content, (
            "Blog post page should display publish date"
        )

    def test_page_uses_time_element_for_date(self):
        """Blog post page should use time element for semantic date."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "<time" in content, (
            "Blog post page should use time element"
        )

    def test_time_element_has_datetime_attribute(self):
        """Time element should have dateTime attribute."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "dateTime=" in content, (
            "Time element should have dateTime attribute"
        )

    def test_page_formats_date(self):
        """Blog post page should format the date for display."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "toLocaleDateString" in content, (
            "Blog post page should format date using toLocaleDateString"
        )

    def test_page_displays_tags(self):
        """Blog post page should display tags."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "post.tags" in content or "tags" in content, (
            "Blog post page should display tags"
        )

    def test_tags_render_conditionally(self):
        """Tags should only render when available."""
        content = BLOG_POST_PAGE_FILE.read_text()
        # Check for conditional tags rendering
        assert "tags &&" in content or "tags.length" in content, (
            "Tags should render conditionally"
        )


class TestPortableTextContentRendering:
    """Test that Portable Text content renders with all formatting."""

    def test_page_imports_blog_content_component(self):
        """Blog post page should import BlogContent component."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "BlogContent" in content, (
            "Blog post page should import BlogContent component"
        )
        assert "@/components/content" in content, (
            "Blog post page should import from @/components/content"
        )

    def test_page_renders_blog_content(self):
        """Blog post page should render BlogContent component."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "<BlogContent" in content, (
            "Blog post page should render BlogContent component"
        )

    def test_blog_content_receives_content_prop(self):
        """BlogContent should receive content prop."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "content=" in content and "post.content" in content, (
            "BlogContent should receive content prop from post"
        )

    def test_page_handles_empty_content(self):
        """Blog post page should handle empty content gracefully."""
        content = BLOG_POST_PAGE_FILE.read_text()
        # Check for conditional content rendering or empty state
        assert "content &&" in content or "content.length" in content, (
            "Blog post page should check for content existence"
        )


class TestImageWithPopupSupport:
    """Test that images within content support popup feature where defined."""

    def test_blog_content_supports_image_with_popup(self):
        """BlogContent component should support imageWithPopup type."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "imageWithPopup" in content, (
            "BlogContent should define imageWithPopup type handler"
        )

    def test_blog_content_imports_image_with_popup(self):
        """BlogContent should import ImageWithPopup component."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "ImageWithPopup" in content, (
            "BlogContent should import ImageWithPopup component"
        )

    def test_image_with_popup_component_exists(self):
        """ImageWithPopup component should exist."""
        image_with_popup_file = PROJECT_ROOT / "components" / "ui" / "ImageWithPopup.tsx"
        assert image_with_popup_file.exists(), (
            "ImageWithPopup component should exist"
        )

    def test_blog_post_query_includes_popup_expansion(self):
        """blogPostBySlugQuery should expand popup references."""
        content = QUERIES_FILE.read_text()
        assert "popup->" in content or "popup ->" in content, (
            "blogPostBySlugQuery should expand popup references"
        )

    def test_blog_content_passes_popup_to_component(self):
        """BlogContent should pass popup data to ImageWithPopup."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "popup" in content, (
            "BlogContent should pass popup prop to ImageWithPopup"
        )


class TestGenerateMetadataSEO:
    """Test that generateMetadata exports SEO tags correctly."""

    def test_page_exports_generate_metadata(self):
        """Blog post page should export generateMetadata function."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "export async function generateMetadata" in content, (
            "Blog post page should export generateMetadata"
        )

    def test_generate_metadata_accepts_params(self):
        """generateMetadata should accept params with slug."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "generateMetadata" in content and "params" in content, (
            "generateMetadata should accept params"
        )

    def test_generate_metadata_returns_title(self):
        """generateMetadata should return title."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "title:" in content or "title :" in content, (
            "generateMetadata should return title"
        )

    def test_generate_metadata_returns_description(self):
        """generateMetadata should return description."""
        content = BLOG_POST_PAGE_FILE.read_text()
        # Check for description in metadata object (shorthand or full property)
        assert "description," in content or "description:" in content or "description :" in content, (
            "generateMetadata should return description"
        )

    def test_generate_metadata_includes_open_graph(self):
        """generateMetadata should include Open Graph tags."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "openGraph" in content, (
            "generateMetadata should include openGraph configuration"
        )

    def test_generate_metadata_uses_post_seo_fields(self):
        """generateMetadata should use post's SEO fields when available."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "seo" in content, (
            "generateMetadata should check for SEO fields"
        )

    def test_generate_metadata_falls_back_to_post_fields(self):
        """generateMetadata should fall back to post title/excerpt."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "post.title" in content, (
            "generateMetadata should fall back to post.title"
        )
        assert "post.excerpt" in content, (
            "generateMetadata should fall back to post.excerpt"
        )

    def test_generate_metadata_includes_og_image(self):
        """generateMetadata should include OG image."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "ogImage" in content or "images:" in content, (
            "generateMetadata should include OG image"
        )

    def test_generate_metadata_includes_twitter_card(self):
        """generateMetadata should include Twitter card metadata."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "twitter:" in content or "twitter :" in content, (
            "generateMetadata should include Twitter card metadata"
        )

    def test_generate_metadata_includes_article_type(self):
        """generateMetadata should set type to article for Open Graph."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "'article'" in content or '"article"' in content, (
            "generateMetadata should set type to 'article'"
        )

    def test_generate_metadata_includes_published_time(self):
        """generateMetadata should include publishedTime for articles."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "publishedTime" in content, (
            "generateMetadata should include publishedTime"
        )


class TestGenerateStaticParams:
    """Test that generateStaticParams enables static generation."""

    def test_page_exports_generate_static_params(self):
        """Blog post page should export generateStaticParams function."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "export async function generateStaticParams" in content, (
            "Blog post page should export generateStaticParams"
        )

    def test_generate_static_params_imports_slugs_query(self):
        """generateStaticParams should import blogPostSlugsQuery."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "blogPostSlugsQuery" in content, (
            "generateStaticParams should import blogPostSlugsQuery"
        )

    def test_generate_static_params_returns_slug_array(self):
        """generateStaticParams should return array of slug objects."""
        content = BLOG_POST_PAGE_FILE.read_text()
        # Check for return statement with slug mapping
        assert "slug:" in content and "map" in content, (
            "generateStaticParams should return mapped slug objects"
        )

    def test_blog_post_slugs_query_exists(self):
        """blogPostSlugsQuery should be defined in queries file."""
        content = QUERIES_FILE.read_text()
        assert "export const blogPostSlugsQuery" in content, (
            "blogPostSlugsQuery should be exported from queries"
        )


class TestNotFoundHandling:
    """Test 404 handling for non-existent slugs."""

    def test_page_imports_not_found(self):
        """Blog post page should import notFound from next/navigation."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "notFound" in content, (
            "Blog post page should import notFound"
        )
        assert "next/navigation" in content, (
            "Blog post page should import from next/navigation"
        )

    def test_page_calls_not_found_when_post_is_null(self):
        """Blog post page should call notFound when post is not found."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "notFound()" in content, (
            "Blog post page should call notFound()"
        )

    def test_page_checks_for_null_post(self):
        """Blog post page should check if post is null."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "!post" in content or "post === null" in content or "post == null" in content, (
            "Blog post page should check for null post"
        )

    def test_generate_metadata_handles_not_found(self):
        """generateMetadata should handle case when post is not found."""
        content = BLOG_POST_PAGE_FILE.read_text()
        # Check that generateMetadata returns something even if post is null
        assert "Not Found" in content or "not found" in content.lower(), (
            "generateMetadata should handle post not found case"
        )


class TestBlogPostPageSemanticHTML:
    """Test that blog post page uses proper semantic HTML."""

    def test_uses_article_element(self):
        """Blog post page should use article element as main wrapper."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "<article" in content, (
            "Blog post page should use article element"
        )

    def test_uses_header_element(self):
        """Blog post page should use header element for post header."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "<header" in content, (
            "Blog post page should use header element"
        )

    def test_uses_footer_element(self):
        """Blog post page should use footer element for post footer."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "<footer" in content, (
            "Blog post page should use footer element"
        )

    def test_uses_nav_element(self):
        """Blog post page should use nav element for navigation."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "<nav" in content, (
            "Blog post page should use nav element"
        )


class TestBlogPostPageLinks:
    """Test that blog post page has proper navigation links."""

    def test_imports_next_link(self):
        """Blog post page should import Link from next/link."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "import Link from 'next/link'" in content or 'import Link from "next/link"' in content, (
            "Blog post page should import Next.js Link component"
        )

    def test_has_back_to_blog_link(self):
        """Blog post page should have link back to blog listing."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "/blog" in content and "<Link" in content, (
            "Blog post page should have link to /blog"
        )


class TestBlogPostPageStyling:
    """Test that blog post page has proper Tailwind styling."""

    def test_uses_responsive_classes(self):
        """Blog post page should use responsive Tailwind classes."""
        content = BLOG_POST_PAGE_FILE.read_text()
        responsive_prefixes = ["sm:", "md:", "lg:", "xl:"]
        found = [prefix for prefix in responsive_prefixes if prefix in content]
        assert len(found) >= 2, (
            "Blog post page should use responsive Tailwind classes"
        )

    def test_uses_dark_mode_classes(self):
        """Blog post page should support dark mode."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "dark:" in content, (
            "Blog post page should have dark mode support"
        )

    def test_uses_brand_colors(self):
        """Blog post page should use brand color classes."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "brand-" in content, (
            "Blog post page should use brand color utilities"
        )

    def test_has_animation_classes(self):
        """Blog post page should have animation classes."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "animate-" in content or "animation-" in content, (
            "Blog post page should have animation classes"
        )


class TestBlogPostPageAccessibility:
    """Test blog post page accessibility features."""

    def test_has_aria_hidden_decorative_elements(self):
        """Decorative elements should have aria-hidden."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert 'aria-hidden="true"' in content, (
            "Decorative elements should have aria-hidden"
        )


class TestBlogPostBySlugQuery:
    """Test that blogPostBySlugQuery is properly defined."""

    def test_blog_post_by_slug_query_exists(self):
        """blogPostBySlugQuery should be defined in queries file."""
        content = QUERIES_FILE.read_text()
        assert "export const blogPostBySlugQuery" in content, (
            "blogPostBySlugQuery should be exported"
        )

    def test_query_filters_by_slug(self):
        """blogPostBySlugQuery should filter by slug.current."""
        content = QUERIES_FILE.read_text()
        assert "slug.current == $slug" in content, (
            "blogPostBySlugQuery should filter by slug.current"
        )

    def test_query_includes_content_field(self):
        """blogPostBySlugQuery should include content field."""
        content = QUERIES_FILE.read_text()
        assert "content" in content, (
            "blogPostBySlugQuery should include content field"
        )

    def test_query_includes_cover_image(self):
        """blogPostBySlugQuery should include coverImage."""
        content = QUERIES_FILE.read_text()
        assert "coverImage" in content, (
            "blogPostBySlugQuery should include coverImage"
        )

    def test_query_includes_seo_fields(self):
        """blogPostBySlugQuery should include SEO fields."""
        content = QUERIES_FILE.read_text()
        assert "seo" in content, (
            "blogPostBySlugQuery should include seo field"
        )

    def test_query_expands_image_assets(self):
        """blogPostBySlugQuery should expand image assets."""
        content = QUERIES_FILE.read_text()
        assert "asset->" in content or "asset ->" in content, (
            "blogPostBySlugQuery should expand asset references"
        )

    def test_query_includes_lqip_metadata(self):
        """blogPostBySlugQuery should include LQIP metadata for blur placeholder."""
        content = QUERIES_FILE.read_text()
        assert "lqip" in content, (
            "blogPostBySlugQuery should include lqip for blur placeholder"
        )


class TestBlogPostDetailType:
    """Test that BlogPostDetail type is properly defined."""

    def test_page_imports_blog_post_detail_type(self):
        """Blog post page should import BlogPostDetail type."""
        content = BLOG_POST_PAGE_FILE.read_text()
        assert "BlogPostDetail" in content, (
            "Blog post page should import BlogPostDetail type"
        )

    def test_blog_post_detail_type_exists_in_queries(self):
        """BlogPostDetail type should be defined in queries file."""
        content = QUERIES_FILE.read_text()
        assert "BlogPostDetail" in content, (
            "BlogPostDetail type should be defined in queries"
        )
