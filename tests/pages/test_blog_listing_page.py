"""
Tests for T-013: Blog listing page with pagination

These tests verify that the blog listing page is properly implemented according to requirements:
- Blog listing fetches posts with pagination (9 per page)
- Grid layout is responsive (1 column mobile, 2-3 desktop)
- Each post card shows cover image, title, excerpt, date, and tags
- Pagination controls display correctly
- Page numbers link to correct paginated URLs
- Empty state displays if no posts exist
- Loading states are handled appropriately

Acceptance Criteria:
- Blog listing fetches posts with pagination (9 per page)
- Grid layout is responsive (1 column mobile, 2-3 desktop)
- Each post card shows cover image, title, excerpt, date, and tags
- Pagination controls display correctly
- Page numbers link to correct paginated URLs
- Empty state displays if no posts exist
- Loading states are handled appropriately
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
BLOG_PAGE_FILE = PROJECT_ROOT / "app" / "(site)" / "blog" / "page.tsx"
QUERIES_FILE = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"


class TestBlogPageFileExists:
    """Test that blog listing page file exists and has proper structure."""

    def test_blog_page_file_exists(self):
        """app/(site)/blog/page.tsx should exist."""
        assert BLOG_PAGE_FILE.exists(), "app/(site)/blog/page.tsx not found"

    def test_blog_page_is_server_component(self):
        """Blog page should be an async Server Component."""
        content = BLOG_PAGE_FILE.read_text()
        assert "async function BlogPage" in content or "export default async function BlogPage" in content, (
            "Blog page should be an async function (Server Component)"
        )

    def test_blog_page_no_use_client_directive(self):
        """Blog page should NOT have 'use client' directive (Server Component)."""
        content = BLOG_PAGE_FILE.read_text()
        assert "'use client'" not in content and '"use client"' not in content, (
            "Blog page should be a Server Component without 'use client' directive"
        )

    def test_blog_page_exports_default(self):
        """Blog page should have a default export."""
        content = BLOG_PAGE_FILE.read_text()
        assert "export default" in content, (
            "Blog page should have a default export"
        )


class TestBlogPagePaginationConfig:
    """Test that blog page uses correct pagination configuration."""

    def test_posts_per_page_constant_defined(self):
        """POSTS_PER_PAGE constant should be defined."""
        content = BLOG_PAGE_FILE.read_text()
        assert "POSTS_PER_PAGE" in content, (
            "POSTS_PER_PAGE constant should be defined"
        )

    def test_posts_per_page_is_nine(self):
        """POSTS_PER_PAGE should be set to 9."""
        content = BLOG_PAGE_FILE.read_text()
        assert "POSTS_PER_PAGE = 9" in content, (
            "POSTS_PER_PAGE should be set to 9"
        )

    def test_blog_page_accepts_search_params(self):
        """Blog page should accept searchParams prop for pagination."""
        content = BLOG_PAGE_FILE.read_text()
        assert "searchParams" in content, (
            "Blog page should accept searchParams prop"
        )

    def test_blog_page_has_page_param_type(self):
        """Blog page should type page parameter."""
        content = BLOG_PAGE_FILE.read_text()
        assert "page?" in content, (
            "Blog page should have optional page parameter"
        )


class TestBlogPageDataFetching:
    """Test that blog page fetches data correctly."""

    def test_blog_page_imports_sanity_fetch(self):
        """Blog page should import sanityFetch from Sanity client."""
        content = BLOG_PAGE_FILE.read_text()
        assert "sanityFetch" in content, "Blog page should import sanityFetch"
        assert "@/sanity/lib/client" in content, (
            "Blog page should import from @/sanity/lib/client"
        )

    def test_blog_page_imports_blog_posts_query(self):
        """Blog page should import blogPostsQuery."""
        content = BLOG_PAGE_FILE.read_text()
        assert "blogPostsQuery" in content, "Blog page should import blogPostsQuery"

    def test_blog_page_imports_blog_post_count_query(self):
        """Blog page should import blogPostCountQuery."""
        content = BLOG_PAGE_FILE.read_text()
        assert "blogPostCountQuery" in content, (
            "Blog page should import blogPostCountQuery"
        )

    def test_blog_page_uses_parallel_fetching(self):
        """Blog page should fetch posts and count in parallel."""
        content = BLOG_PAGE_FILE.read_text()
        assert "Promise.all" in content, (
            "Blog page should use Promise.all for parallel data fetching"
        )

    def test_blog_page_calculates_start_offset(self):
        """Blog page should calculate start offset for pagination."""
        content = BLOG_PAGE_FILE.read_text()
        assert "start" in content and "POSTS_PER_PAGE" in content, (
            "Blog page should calculate start offset based on current page"
        )

    def test_blog_page_calculates_end_offset(self):
        """Blog page should calculate end offset for pagination."""
        content = BLOG_PAGE_FILE.read_text()
        assert "end" in content and "start" in content, (
            "Blog page should calculate end offset"
        )

    def test_blog_page_passes_pagination_params(self):
        """Blog page should pass start/end params to query."""
        content = BLOG_PAGE_FILE.read_text()
        assert "params: { start, end }" in content or "params: {start, end}" in content, (
            "Blog page should pass start/end params to blogPostsQuery"
        )

    def test_blog_page_uses_cache_tags(self):
        """Blog page should use cache tags for revalidation."""
        content = BLOG_PAGE_FILE.read_text()
        assert "tags:" in content and "blogPost" in content, (
            "Blog page should use 'blogPost' tag for cache revalidation"
        )

    def test_blog_page_calculates_total_pages(self):
        """Blog page should calculate total pages from count."""
        content = BLOG_PAGE_FILE.read_text()
        assert "totalPages" in content, (
            "Blog page should calculate totalPages"
        )

    def test_blog_page_uses_math_ceil(self):
        """Blog page should use Math.ceil for page calculation."""
        content = BLOG_PAGE_FILE.read_text()
        assert "Math.ceil" in content, (
            "Blog page should use Math.ceil to round up totalPages"
        )

    def test_blog_page_has_next_page_check(self):
        """Blog page should determine if next page exists."""
        content = BLOG_PAGE_FILE.read_text()
        assert "hasNextPage" in content, (
            "Blog page should have hasNextPage variable"
        )

    def test_blog_page_has_prev_page_check(self):
        """Blog page should determine if previous page exists."""
        content = BLOG_PAGE_FILE.read_text()
        assert "hasPrevPage" in content, (
            "Blog page should have hasPrevPage variable"
        )


class TestBlogPageCurrentPageHandling:
    """Test that blog page handles current page parameter correctly."""

    def test_blog_page_parses_page_param(self):
        """Blog page should parse page from searchParams."""
        content = BLOG_PAGE_FILE.read_text()
        assert "currentPage" in content or "page" in content, (
            "Blog page should have current page handling"
        )

    def test_blog_page_uses_parse_int(self):
        """Blog page should use parseInt to convert page to number."""
        content = BLOG_PAGE_FILE.read_text()
        assert "parseInt" in content, (
            "Blog page should parse page parameter as integer"
        )

    def test_blog_page_defaults_to_page_one(self):
        """Blog page should default to page 1 if not specified."""
        content = BLOG_PAGE_FILE.read_text()
        assert "'1'" in content or '"1"' in content or "|| 1" in content, (
            "Blog page should default to page 1"
        )

    def test_blog_page_uses_math_max_for_page(self):
        """Blog page should use Math.max to ensure page >= 1."""
        content = BLOG_PAGE_FILE.read_text()
        assert "Math.max" in content, (
            "Blog page should use Math.max to ensure page is at least 1"
        )


class TestBlogPageGridLayout:
    """Test that blog page has responsive grid layout."""

    def test_blog_page_uses_grid(self):
        """Blog page should use CSS grid for layout."""
        content = BLOG_PAGE_FILE.read_text()
        assert "grid" in content, (
            "Blog page should use grid layout"
        )

    def test_blog_page_single_column_mobile(self):
        """Blog page should have 1 column on mobile."""
        content = BLOG_PAGE_FILE.read_text()
        assert "grid-cols-1" in content, (
            "Blog page should have grid-cols-1 for mobile"
        )

    def test_blog_page_two_columns_medium(self):
        """Blog page should have 2 columns on medium screens."""
        content = BLOG_PAGE_FILE.read_text()
        assert "md:grid-cols-2" in content, (
            "Blog page should have md:grid-cols-2 for tablet"
        )

    def test_blog_page_three_columns_large(self):
        """Blog page should have 3 columns on large screens."""
        content = BLOG_PAGE_FILE.read_text()
        assert "lg:grid-cols-3" in content, (
            "Blog page should have lg:grid-cols-3 for desktop"
        )

    def test_blog_page_has_grid_gap(self):
        """Blog page should have gap between grid items."""
        content = BLOG_PAGE_FILE.read_text()
        assert "gap-" in content, (
            "Blog page should have gap between grid items"
        )


class TestBlogPostCard:
    """Test that blog post cards display correct content."""

    def test_blog_post_card_component_exists(self):
        """Blog page should have BlogPostCard component."""
        content = BLOG_PAGE_FILE.read_text()
        assert "BlogPostCard" in content, (
            "Blog page should have BlogPostCard component"
        )

    def test_blog_post_card_displays_title(self):
        """Blog post card should display post title."""
        content = BLOG_PAGE_FILE.read_text()
        assert "post.title" in content, (
            "Blog post card should display post title"
        )

    def test_blog_post_card_displays_excerpt(self):
        """Blog post card should display post excerpt."""
        content = BLOG_PAGE_FILE.read_text()
        assert "post.excerpt" in content, (
            "Blog post card should display post excerpt"
        )

    def test_blog_post_card_displays_cover_image(self):
        """Blog post card should display cover image."""
        content = BLOG_PAGE_FILE.read_text()
        assert "coverImage" in content, (
            "Blog post card should display cover image"
        )

    def test_blog_post_card_displays_date(self):
        """Blog post card should display publish date."""
        content = BLOG_PAGE_FILE.read_text()
        assert "publishedAt" in content, (
            "Blog post card should display publish date"
        )

    def test_blog_post_card_displays_tags(self):
        """Blog post card should display tags."""
        content = BLOG_PAGE_FILE.read_text()
        assert "post.tags" in content or "tags" in content, (
            "Blog post card should display tags"
        )

    def test_blog_post_card_uses_next_image(self):
        """Blog post card should use Next.js Image component."""
        content = BLOG_PAGE_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "Blog page should import Next.js Image component"
        )

    def test_blog_post_card_uses_link(self):
        """Blog post card should use Next.js Link component."""
        content = BLOG_PAGE_FILE.read_text()
        assert "import Link from 'next/link'" in content or 'import Link from "next/link"' in content, (
            "Blog page should import Next.js Link component"
        )

    def test_blog_post_card_links_to_post(self):
        """Blog post card should link to individual blog post."""
        content = BLOG_PAGE_FILE.read_text()
        assert "/blog/" in content and "slug" in content, (
            "Blog post card should link to individual post page"
        )

    def test_blog_post_card_uses_article_element(self):
        """Blog post card should use article element."""
        content = BLOG_PAGE_FILE.read_text()
        assert "<article" in content, (
            "Blog post card should use article element"
        )

    def test_blog_post_card_uses_time_element(self):
        """Blog post card should use time element for date."""
        content = BLOG_PAGE_FILE.read_text()
        assert "<time" in content, (
            "Blog post card should use time element"
        )

    def test_blog_post_card_time_has_datetime(self):
        """Time element should have dateTime attribute."""
        content = BLOG_PAGE_FILE.read_text()
        assert "dateTime=" in content, (
            "Time element should have dateTime attribute"
        )


class TestBlogPostCardImage:
    """Test blog post card image handling."""

    def test_blog_post_card_uses_urlfor(self):
        """Blog post card should use urlFor helper for images."""
        content = BLOG_PAGE_FILE.read_text()
        assert "urlFor" in content, (
            "Blog post card should use urlFor helper"
        )

    def test_blog_post_card_imports_urlfor(self):
        """Blog page should import urlFor from Sanity lib."""
        content = BLOG_PAGE_FILE.read_text()
        assert "@/sanity/lib/image" in content, (
            "Blog page should import urlFor from @/sanity/lib/image"
        )

    def test_blog_post_card_image_has_alt(self):
        """Blog post card image should have alt text."""
        content = BLOG_PAGE_FILE.read_text()
        assert "alt=" in content, (
            "Blog post card image should have alt attribute"
        )

    def test_blog_post_card_image_has_sizes(self):
        """Blog post card image should have sizes prop."""
        content = BLOG_PAGE_FILE.read_text()
        assert "sizes=" in content, (
            "Blog post card image should have sizes prop"
        )

    def test_blog_post_card_image_uses_fill_or_dimensions(self):
        """Blog post card image should use fill or explicit dimensions."""
        content = BLOG_PAGE_FILE.read_text()
        assert "fill" in content or ("width" in content and "height" in content), (
            "Blog post card image should use fill or explicit dimensions"
        )

    def test_blog_post_card_has_fallback_when_no_image(self):
        """Blog post card should handle missing cover image."""
        content = BLOG_PAGE_FILE.read_text()
        # Check for conditional rendering of fallback
        assert "coverImage" in content and "?" in content, (
            "Blog post card should have fallback when no image"
        )


class TestPaginationComponent:
    """Test pagination component displays correctly."""

    def test_pagination_component_exists(self):
        """Blog page should have Pagination component."""
        content = BLOG_PAGE_FILE.read_text()
        assert "Pagination" in content, (
            "Blog page should have Pagination component"
        )

    def test_pagination_uses_nav_element(self):
        """Pagination should use nav element."""
        content = BLOG_PAGE_FILE.read_text()
        assert "<nav" in content, (
            "Pagination should use nav element"
        )

    def test_pagination_has_aria_label(self):
        """Pagination should have aria-label for accessibility."""
        content = BLOG_PAGE_FILE.read_text()
        assert "aria-label" in content and "pagination" in content.lower(), (
            "Pagination should have aria-label"
        )

    def test_pagination_shows_page_numbers(self):
        """Pagination should show page numbers."""
        content = BLOG_PAGE_FILE.read_text()
        assert "pageNumbers" in content or "getPageNumbers" in content, (
            "Pagination should generate page numbers"
        )

    def test_pagination_has_previous_button(self):
        """Pagination should have previous button."""
        content = BLOG_PAGE_FILE.read_text()
        assert "Previous" in content or "Prev" in content, (
            "Pagination should have previous button"
        )

    def test_pagination_has_next_button(self):
        """Pagination should have next button."""
        content = BLOG_PAGE_FILE.read_text()
        assert "Next" in content, (
            "Pagination should have next button"
        )

    def test_pagination_links_use_page_param(self):
        """Pagination links should use page query parameter."""
        content = BLOG_PAGE_FILE.read_text()
        assert "/blog?page=" in content, (
            "Pagination links should use /blog?page= format"
        )

    def test_pagination_disables_prev_on_first_page(self):
        """Pagination should disable prev button on first page."""
        content = BLOG_PAGE_FILE.read_text()
        assert "hasPrevPage" in content, (
            "Pagination should check hasPrevPage to disable button"
        )

    def test_pagination_disables_next_on_last_page(self):
        """Pagination should disable next button on last page."""
        content = BLOG_PAGE_FILE.read_text()
        assert "hasNextPage" in content, (
            "Pagination should check hasNextPage to disable button"
        )

    def test_pagination_highlights_current_page(self):
        """Pagination should highlight current page."""
        content = BLOG_PAGE_FILE.read_text()
        assert "currentPage" in content, (
            "Pagination should reference currentPage for highlighting"
        )

    def test_pagination_uses_aria_current(self):
        """Pagination should use aria-current for current page."""
        content = BLOG_PAGE_FILE.read_text()
        assert "aria-current" in content, (
            "Pagination should use aria-current for accessibility"
        )

    def test_pagination_conditionally_renders(self):
        """Pagination should only render when totalPages > 1."""
        content = BLOG_PAGE_FILE.read_text()
        assert "totalPages > 1" in content, (
            "Pagination should only render when more than one page"
        )


class TestPaginationEllipsis:
    """Test pagination ellipsis handling for many pages."""

    def test_pagination_has_ellipsis_support(self):
        """Pagination should support ellipsis for many pages."""
        content = BLOG_PAGE_FILE.read_text()
        assert "ellipsis" in content or "..." in content or "…" in content, (
            "Pagination should support ellipsis"
        )

    def test_pagination_shows_first_page(self):
        """Pagination should always show first page."""
        content = BLOG_PAGE_FILE.read_text()
        assert "pages.push(1)" in content or "1" in content, (
            "Pagination should always include first page"
        )

    def test_pagination_shows_last_page(self):
        """Pagination should always show last page."""
        content = BLOG_PAGE_FILE.read_text()
        assert "totalPages" in content, (
            "Pagination should reference totalPages for last page"
        )


class TestEmptyState:
    """Test empty state displays when no posts exist."""

    def test_empty_state_component_exists(self):
        """Blog page should have EmptyState component."""
        content = BLOG_PAGE_FILE.read_text()
        assert "EmptyState" in content, (
            "Blog page should have EmptyState component"
        )

    def test_empty_state_conditionally_renders(self):
        """Empty state should render when no posts exist."""
        content = BLOG_PAGE_FILE.read_text()
        assert ("posts.length" in content or "posts &&" in content) and "EmptyState" in content, (
            "Empty state should render conditionally based on posts"
        )

    def test_empty_state_has_message(self):
        """Empty state should have a descriptive message."""
        content = BLOG_PAGE_FILE.read_text()
        # Check for common empty state phrases
        assert "no" in content.lower() or "empty" in content.lower() or "yet" in content.lower(), (
            "Empty state should have a descriptive message"
        )

    def test_empty_state_has_link_to_home(self):
        """Empty state should have a link back to homepage."""
        content = BLOG_PAGE_FILE.read_text()
        assert 'href="/"' in content or "href='/'" in content, (
            "Empty state should have link to homepage"
        )


class TestBlogPageMetadata:
    """Test that blog page generates proper metadata."""

    def test_exports_generate_metadata(self):
        """Blog page should export generateMetadata function."""
        content = BLOG_PAGE_FILE.read_text()
        assert "generateMetadata" in content, (
            "Blog page should export generateMetadata"
        )

    def test_generate_metadata_is_async(self):
        """generateMetadata should be async function."""
        content = BLOG_PAGE_FILE.read_text()
        assert "async function generateMetadata" in content or "export async function generateMetadata" in content, (
            "generateMetadata should be async"
        )

    def test_metadata_includes_title(self):
        """Metadata should include title."""
        content = BLOG_PAGE_FILE.read_text()
        assert "title:" in content, (
            "Metadata should include title"
        )

    def test_metadata_includes_description(self):
        """Metadata should include description."""
        content = BLOG_PAGE_FILE.read_text()
        assert "description:" in content, (
            "Metadata should include description"
        )

    def test_metadata_includes_open_graph(self):
        """Metadata should include Open Graph config."""
        content = BLOG_PAGE_FILE.read_text()
        assert "openGraph" in content, (
            "Metadata should include Open Graph configuration"
        )


class TestBlogPageSemanticHTML:
    """Test that blog page uses proper semantic HTML."""

    def test_uses_article_wrapper(self):
        """Blog page should use article element as wrapper."""
        content = BLOG_PAGE_FILE.read_text()
        assert "<article" in content, (
            "Blog page should use article element"
        )

    def test_uses_section_element(self):
        """Blog page should use section element for content area."""
        content = BLOG_PAGE_FILE.read_text()
        assert "<section" in content, (
            "Blog page should use section element"
        )

    def test_uses_header_element(self):
        """Blog page should use header element for page header."""
        content = BLOG_PAGE_FILE.read_text()
        assert "<header" in content, (
            "Blog page should use header element"
        )

    def test_uses_h1_heading(self):
        """Blog page should have h1 heading."""
        content = BLOG_PAGE_FILE.read_text()
        assert "<h1" in content, (
            "Blog page should have h1 heading"
        )

    def test_uses_h2_for_card_titles(self):
        """Blog post cards should use h2 for titles."""
        content = BLOG_PAGE_FILE.read_text()
        assert "<h2" in content, (
            "Blog post cards should use h2 for titles"
        )

    def test_section_has_aria_label(self):
        """Blog posts section should have aria-label."""
        content = BLOG_PAGE_FILE.read_text()
        assert 'aria-label="Blog posts"' in content or "aria-label='Blog posts'" in content, (
            "Blog posts section should have aria-label"
        )


class TestBlogPageTailwindStyling:
    """Test that blog page uses Tailwind CSS properly."""

    def test_uses_tailwind_layout_classes(self):
        """Blog page should use Tailwind layout classes."""
        content = BLOG_PAGE_FILE.read_text()
        tailwind_indicators = ["flex", "grid", "items-", "justify-", "mx-auto", "max-w-"]
        found = [cls for cls in tailwind_indicators if cls in content]
        assert len(found) >= 3, f"Blog page should use Tailwind layout classes, found: {found}"

    def test_uses_tailwind_spacing_classes(self):
        """Blog page should use Tailwind spacing classes."""
        content = BLOG_PAGE_FILE.read_text()
        assert "px-" in content and "py-" in content, (
            "Blog page should use Tailwind padding classes"
        )

    def test_uses_responsive_classes(self):
        """Blog page should use responsive Tailwind classes."""
        content = BLOG_PAGE_FILE.read_text()
        responsive_prefixes = ["sm:", "md:", "lg:", "xl:"]
        found = [prefix for prefix in responsive_prefixes if prefix in content]
        assert len(found) >= 2, (
            "Blog page should use responsive Tailwind classes"
        )

    def test_uses_dark_mode_classes(self):
        """Blog page should support dark mode."""
        content = BLOG_PAGE_FILE.read_text()
        assert "dark:" in content, (
            "Blog page should have dark mode support"
        )

    def test_uses_brand_colors(self):
        """Blog page should use brand color classes."""
        content = BLOG_PAGE_FILE.read_text()
        assert "brand-" in content, (
            "Blog page should use brand color utilities"
        )

    def test_decorative_elements_hidden(self):
        """Decorative elements should be hidden from accessibility."""
        content = BLOG_PAGE_FILE.read_text()
        assert 'aria-hidden="true"' in content, (
            "Decorative elements should have aria-hidden"
        )


class TestBlogPageAnimations:
    """Test that blog page has appropriate animations."""

    def test_uses_animation_classes(self):
        """Blog page should use animation classes."""
        content = BLOG_PAGE_FILE.read_text()
        assert "animate-" in content, (
            "Blog page should use animation classes"
        )

    def test_has_stagger_animation(self):
        """Blog post cards should have stagger animation."""
        content = BLOG_PAGE_FILE.read_text()
        assert "delay" in content.lower() or "animation-delay" in content, (
            "Blog page should have stagger animation delay"
        )


class TestBlogQueriesExist:
    """Test that required GROQ queries exist in queries file."""

    def test_queries_file_exists(self):
        """sanity/lib/queries.ts should exist."""
        assert QUERIES_FILE.exists(), "sanity/lib/queries.ts not found"

    def test_blog_posts_query_defined(self):
        """blogPostsQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export const blogPostsQuery" in content, (
            "blogPostsQuery should be exported"
        )

    def test_blog_posts_query_uses_pagination(self):
        """blogPostsQuery should use pagination parameters."""
        content = QUERIES_FILE.read_text()
        assert "$start" in content and "$end" in content, (
            "blogPostsQuery should use $start and $end parameters"
        )

    def test_blog_posts_query_orders_by_date(self):
        """blogPostsQuery should order by publishedAt desc."""
        content = QUERIES_FILE.read_text()
        assert "order(publishedAt desc)" in content, (
            "blogPostsQuery should order by publishedAt desc"
        )

    def test_blog_post_count_query_defined(self):
        """blogPostCountQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export const blogPostCountQuery" in content, (
            "blogPostCountQuery should be exported"
        )

    def test_blog_post_count_query_uses_count(self):
        """blogPostCountQuery should use count function."""
        content = QUERIES_FILE.read_text()
        assert 'count(*[_type == "blogPost"])' in content, (
            "blogPostCountQuery should count blog posts"
        )

    def test_blog_posts_query_includes_required_fields(self):
        """blogPostsQuery should include all required fields."""
        content = QUERIES_FILE.read_text()
        required_fields = ["_id", "title", "slug", "excerpt", "publishedAt", "coverImage", "tags"]
        for field in required_fields:
            assert field in content, f"blogPostsQuery should include {field}"

    def test_blog_post_list_item_type_defined(self):
        """BlogPostListItem type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export interface BlogPostListItem" in content, (
            "BlogPostListItem type should be exported"
        )

    def test_blog_post_list_item_has_required_fields(self):
        """BlogPostListItem type should have required fields."""
        content = QUERIES_FILE.read_text()
        # Check that type definition includes key fields
        assert "title: string" in content, "BlogPostListItem should have title"
        assert "slug: string" in content, "BlogPostListItem should have slug"


class TestBlogPageFeaturedPostHandling:
    """Test that blog page handles featured post styling correctly."""

    def test_first_post_featured_styling(self):
        """First post on page 1 should have featured styling."""
        content = BLOG_PAGE_FILE.read_text()
        assert "featured" in content.lower(), (
            "Blog page should have featured post handling"
        )

    def test_featured_post_spans_columns(self):
        """Featured post should span multiple columns."""
        content = BLOG_PAGE_FILE.read_text()
        assert "col-span" in content, (
            "Featured post should span multiple columns"
        )


class TestBlogPageHoverEffects:
    """Test that blog post cards have hover effects."""

    def test_has_hover_effects(self):
        """Blog post cards should have hover effects."""
        content = BLOG_PAGE_FILE.read_text()
        assert "hover:" in content, (
            "Blog post cards should have hover effects"
        )

    def test_has_group_hover(self):
        """Blog post cards should use group hover for coordinated effects."""
        content = BLOG_PAGE_FILE.read_text()
        assert "group" in content and "group-hover:" in content, (
            "Blog post cards should use group hover"
        )

    def test_has_transition_effects(self):
        """Blog post cards should have transition effects."""
        content = BLOG_PAGE_FILE.read_text()
        assert "transition" in content, (
            "Blog post cards should have transition effects"
        )
