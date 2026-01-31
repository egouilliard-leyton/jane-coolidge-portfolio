"""
Tests for T-015: Project gallery listing page

These tests verify that the projects gallery page is properly implemented according to requirements:
- Projects page fetches all projects via GROQ query
- Grid displays 2 columns on mobile, 3+ on desktop
- Each project card shows cover image, title, category, client, and date
- Hover effect provides visual feedback
- Cards link to individual project pages
- Category filter displays if more than 5 projects exist
- Empty state displays if no projects exist

Acceptance Criteria:
- Projects page fetches all projects via GROQ query
- Grid displays 2 columns on mobile, 3+ on desktop
- Each project card shows cover image, title, category, client, and date
- Hover effect provides visual feedback
- Cards link to individual project pages
- Category filter displays if more than 5 projects exist
- Empty state displays if no projects exist
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
PROJECTS_PAGE_FILE = PROJECT_ROOT / "app" / "(site)" / "projects" / "page.tsx"
QUERIES_FILE = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"


class TestProjectsPageFileExists:
    """Test that projects gallery page file exists and has proper structure."""

    def test_projects_page_file_exists(self):
        """app/(site)/projects/page.tsx should exist."""
        assert PROJECTS_PAGE_FILE.exists(), "app/(site)/projects/page.tsx not found"

    def test_projects_page_is_server_component(self):
        """Projects page should be an async Server Component."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "async function ProjectsPage" in content or "export default async function ProjectsPage" in content, (
            "Projects page should be an async function (Server Component)"
        )

    def test_projects_page_no_use_client_directive(self):
        """Projects page should NOT have 'use client' directive (Server Component)."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "'use client'" not in content and '"use client"' not in content, (
            "Projects page should be a Server Component without 'use client' directive"
        )

    def test_projects_page_exports_default(self):
        """Projects page should have a default export."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "export default" in content, (
            "Projects page should have a default export"
        )


class TestProjectsPageDataFetching:
    """Test that projects page fetches data correctly via GROQ query."""

    def test_projects_page_imports_sanity_fetch(self):
        """Projects page should import sanityFetch from Sanity client."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "sanityFetch" in content, "Projects page should import sanityFetch"
        assert "@/sanity/lib/client" in content, (
            "Projects page should import from @/sanity/lib/client"
        )

    def test_projects_page_imports_projects_query(self):
        """Projects page should import projectsQuery."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "projectsQuery" in content, "Projects page should import projectsQuery"

    def test_projects_page_imports_project_count_query(self):
        """Projects page should import projectCountByCategoryQuery."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "projectCountByCategoryQuery" in content, (
            "Projects page should import projectCountByCategoryQuery"
        )

    def test_projects_page_uses_parallel_fetching(self):
        """Projects page should fetch projects and counts in parallel."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "Promise.all" in content, (
            "Projects page should use Promise.all for parallel data fetching"
        )

    def test_projects_page_uses_cache_tags(self):
        """Projects page should use cache tags for revalidation."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "tags:" in content and "project" in content, (
            "Projects page should use 'project' tag for cache revalidation"
        )

    def test_projects_page_fetches_project_list_items(self):
        """Projects page should fetch ProjectListItem type."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "ProjectListItem" in content, (
            "Projects page should use ProjectListItem type"
        )

    def test_projects_page_fetches_category_counts(self):
        """Projects page should fetch ProjectCategoryCountsResult type."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "ProjectCategoryCountsResult" in content, (
            "Projects page should use ProjectCategoryCountsResult type"
        )


class TestProjectsPageGridLayout:
    """Test that projects page has responsive grid layout."""

    def test_projects_page_uses_grid(self):
        """Projects page should use CSS grid for layout."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "grid" in content, (
            "Projects page should use grid layout"
        )

    def test_projects_page_two_columns_mobile(self):
        """Projects page should have 2 columns on mobile."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "grid-cols-2" in content, (
            "Projects page should have grid-cols-2 for mobile"
        )

    def test_projects_page_three_columns_large(self):
        """Projects page should have 3+ columns on large screens (desktop)."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "lg:grid-cols-3" in content, (
            "Projects page should have lg:grid-cols-3 for desktop"
        )

    def test_projects_page_has_grid_gap(self):
        """Projects page should have gap between grid items."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "gap-" in content, (
            "Projects page should have gap between grid items"
        )


class TestProjectCardContent:
    """Test that project cards display correct content: cover image, title, category, client, date."""

    def test_project_card_component_exists(self):
        """Projects page should have ProjectCard component."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "ProjectCard" in content, (
            "Projects page should have ProjectCard component"
        )

    def test_project_card_displays_title(self):
        """Project card should display project title."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "project.title" in content, (
            "Project card should display project title"
        )

    def test_project_card_displays_category(self):
        """Project card should display project category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "project.category" in content, (
            "Project card should display project category"
        )

    def test_project_card_displays_client(self):
        """Project card should display project client."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "project.client" in content, (
            "Project card should display project client"
        )

    def test_project_card_displays_date(self):
        """Project card should display project date."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "project.date" in content, (
            "Project card should display project date"
        )

    def test_project_card_displays_cover_image(self):
        """Project card should display cover image."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "coverImage" in content, (
            "Project card should display cover image"
        )

    def test_project_card_uses_next_image(self):
        """Project card should use Next.js Image component."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "Projects page should import Next.js Image component"
        )

    def test_project_card_uses_urlfor(self):
        """Project card should use urlFor helper for images."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "urlFor" in content, (
            "Project card should use urlFor helper"
        )

    def test_project_card_imports_urlfor(self):
        """Projects page should import urlFor from Sanity lib."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "@/sanity/lib/image" in content, (
            "Projects page should import urlFor from @/sanity/lib/image"
        )


class TestProjectCardLink:
    """Test that project cards link to individual project pages."""

    def test_project_card_uses_link(self):
        """Project card should use Next.js Link component."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "import Link from 'next/link'" in content or 'import Link from "next/link"' in content, (
            "Projects page should import Next.js Link component"
        )

    def test_project_card_links_to_project(self):
        """Project card should link to individual project page."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "/projects/" in content and "slug" in content, (
            "Project card should link to individual project page"
        )


class TestProjectCardHoverEffects:
    """Test that project cards have hover effects for visual feedback."""

    def test_has_hover_effects(self):
        """Project cards should have hover effects."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "hover:" in content, (
            "Project cards should have hover effects"
        )

    def test_has_group_hover(self):
        """Project cards should use group hover for coordinated effects."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "group" in content and "group-hover:" in content, (
            "Project cards should use group hover"
        )

    def test_has_transition_effects(self):
        """Project cards should have transition effects."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "transition" in content, (
            "Project cards should have transition effects"
        )

    def test_hover_overlay_exists(self):
        """Project cards should have hover overlay."""
        content = PROJECTS_PAGE_FILE.read_text()
        # Check for opacity transition on hover
        assert "group-hover:opacity-" in content, (
            "Project cards should have opacity change on hover"
        )

    def test_hover_scale_transform(self):
        """Project cards should have scale transform on hover."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "group-hover:scale-" in content, (
            "Project cards should have scale transform on hover"
        )


class TestCategoryFilter:
    """Test that category filter displays if more than 5 projects exist."""

    def test_category_filter_threshold_defined(self):
        """SHOW_FILTER_THRESHOLD constant should be defined."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "SHOW_FILTER_THRESHOLD" in content, (
            "SHOW_FILTER_THRESHOLD constant should be defined"
        )

    def test_category_filter_threshold_is_five(self):
        """SHOW_FILTER_THRESHOLD should be set to 5."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "SHOW_FILTER_THRESHOLD = 5" in content, (
            "SHOW_FILTER_THRESHOLD should be set to 5"
        )

    def test_show_filter_conditional_logic(self):
        """Projects page should conditionally show filter based on project count."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "showFilter" in content, (
            "Projects page should have showFilter logic"
        )

    def test_category_filter_checks_threshold(self):
        """Category filter should compare against threshold."""
        content = PROJECTS_PAGE_FILE.read_text()
        # Check that showFilter is based on SHOW_FILTER_THRESHOLD
        assert "categoryCounts.all > SHOW_FILTER_THRESHOLD" in content or "SHOW_FILTER_THRESHOLD" in content, (
            "Category filter should check against threshold"
        )

    def test_category_filter_button_exists(self):
        """CategoryFilterButton component should exist."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "CategoryFilterButton" in content, (
            "CategoryFilterButton component should exist"
        )

    def test_category_filter_uses_nav_element(self):
        """Category filter should use nav element."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "<nav" in content, (
            "Category filter should use nav element"
        )

    def test_category_filter_has_aria_label(self):
        """Category filter should have aria-label for accessibility."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert 'aria-label="Project categories"' in content, (
            "Category filter should have aria-label"
        )

    def test_category_filter_has_all_option(self):
        """Category filter should have 'All' option."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert '"All"' in content or "'All'" in content, (
            "Category filter should have 'All' option"
        )

    def test_category_filter_links_use_query_params(self):
        """Category filter links should use query parameters."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "/projects?category=" in content, (
            "Category filter links should use /projects?category= format"
        )

    def test_category_filter_accepts_search_params(self):
        """Projects page should accept searchParams prop for category filter."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "searchParams" in content, (
            "Projects page should accept searchParams prop"
        )

    def test_category_filter_highlights_active(self):
        """Category filter should highlight active category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "isActive" in content, (
            "Category filter should have isActive handling"
        )

    def test_category_filter_uses_aria_current(self):
        """Category filter should use aria-current for accessibility."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "aria-current" in content, (
            "Category filter should use aria-current for accessibility"
        )


class TestEmptyState:
    """Test empty state displays if no projects exist."""

    def test_empty_state_component_exists(self):
        """Projects page should have EmptyState component."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "EmptyState" in content, (
            "Projects page should have EmptyState component"
        )

    def test_empty_state_conditionally_renders(self):
        """Empty state should render when no projects exist."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert ("projects.length" in content or "projects &&" in content) and "EmptyState" in content, (
            "Empty state should render conditionally based on projects"
        )

    def test_empty_state_has_message(self):
        """Empty state should have a descriptive message."""
        content = PROJECTS_PAGE_FILE.read_text()
        # Check for common empty state phrases
        assert "no projects" in content.lower() or "coming soon" in content.lower(), (
            "Empty state should have a descriptive message"
        )

    def test_empty_state_different_for_category(self):
        """Empty state should differ based on active category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "activeCategory" in content and "EmptyState" in content, (
            "Empty state should handle different messages for category filter"
        )

    def test_empty_state_has_link_back(self):
        """Empty state should have a link back to projects or homepage."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert 'href="/"' in content or "href='/'" in content or 'href="/projects"' in content, (
            "Empty state should have navigation link"
        )


class TestProjectsPageMetadata:
    """Test that projects page generates proper metadata."""

    def test_exports_generate_metadata(self):
        """Projects page should export generateMetadata function."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "generateMetadata" in content, (
            "Projects page should export generateMetadata"
        )

    def test_generate_metadata_is_async(self):
        """generateMetadata should be async function."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "async function generateMetadata" in content or "export async function generateMetadata" in content, (
            "generateMetadata should be async"
        )

    def test_metadata_includes_title(self):
        """Metadata should include title."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "title:" in content, (
            "Metadata should include title"
        )

    def test_metadata_includes_description(self):
        """Metadata should include description."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "description:" in content, (
            "Metadata should include description"
        )

    def test_metadata_includes_open_graph(self):
        """Metadata should include Open Graph config."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "openGraph" in content, (
            "Metadata should include Open Graph configuration"
        )


class TestProjectsPageSemanticHTML:
    """Test that projects page uses proper semantic HTML."""

    def test_uses_article_wrapper(self):
        """Projects page should use article element as wrapper."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "<article" in content, (
            "Projects page should use article element"
        )

    def test_uses_section_element(self):
        """Projects page should use section element for gallery."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "<section" in content, (
            "Projects page should use section element"
        )

    def test_uses_header_element(self):
        """Projects page should use header element for page header."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "<header" in content, (
            "Projects page should use header element"
        )

    def test_uses_h1_heading(self):
        """Projects page should have h1 heading."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "<h1" in content, (
            "Projects page should have h1 heading"
        )

    def test_uses_h2_for_card_titles(self):
        """Project cards should use h2 for titles."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "<h2" in content, (
            "Project cards should use h2 for titles"
        )

    def test_section_has_aria_label(self):
        """Projects section should have aria-label."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert 'aria-label="Projects gallery"' in content or "aria-label='Projects gallery'" in content, (
            "Projects section should have aria-label"
        )


class TestProjectsPageTailwindStyling:
    """Test that projects page uses Tailwind CSS properly."""

    def test_uses_tailwind_layout_classes(self):
        """Projects page should use Tailwind layout classes."""
        content = PROJECTS_PAGE_FILE.read_text()
        tailwind_indicators = ["flex", "grid", "items-", "justify-", "mx-auto", "max-w-"]
        found = [cls for cls in tailwind_indicators if cls in content]
        assert len(found) >= 3, f"Projects page should use Tailwind layout classes, found: {found}"

    def test_uses_tailwind_spacing_classes(self):
        """Projects page should use Tailwind spacing classes."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "px-" in content and "py-" in content, (
            "Projects page should use Tailwind padding classes"
        )

    def test_uses_responsive_classes(self):
        """Projects page should use responsive Tailwind classes."""
        content = PROJECTS_PAGE_FILE.read_text()
        responsive_prefixes = ["sm:", "md:", "lg:", "xl:"]
        found = [prefix for prefix in responsive_prefixes if prefix in content]
        assert len(found) >= 2, (
            "Projects page should use responsive Tailwind classes"
        )

    def test_uses_dark_mode_classes(self):
        """Projects page should support dark mode."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "dark:" in content, (
            "Projects page should have dark mode support"
        )

    def test_uses_brand_colors(self):
        """Projects page should use brand color classes."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "brand-" in content, (
            "Projects page should use brand color utilities"
        )

    def test_decorative_elements_hidden(self):
        """Decorative elements should be hidden from accessibility."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert 'aria-hidden="true"' in content, (
            "Decorative elements should have aria-hidden"
        )


class TestProjectsPageAnimations:
    """Test that projects page has appropriate animations."""

    def test_uses_animation_classes(self):
        """Projects page should use animation classes."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "animate-" in content, (
            "Projects page should use animation classes"
        )

    def test_has_stagger_animation(self):
        """Project cards should have stagger animation."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "delay" in content.lower() or "animation-delay" in content, (
            "Projects page should have stagger animation delay"
        )


class TestProjectCardImage:
    """Test project card image handling."""

    def test_project_card_image_has_alt(self):
        """Project card image should have alt text."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "alt=" in content, (
            "Project card image should have alt attribute"
        )

    def test_project_card_image_has_sizes(self):
        """Project card image should have sizes prop."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "sizes=" in content, (
            "Project card image should have sizes prop"
        )

    def test_project_card_image_uses_fill(self):
        """Project card image should use fill for responsive sizing."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "fill" in content, (
            "Project card image should use fill"
        )

    def test_project_card_has_fallback_when_no_image(self):
        """Project card should handle missing cover image."""
        content = PROJECTS_PAGE_FILE.read_text()
        # Check for conditional rendering of fallback
        assert "coverImage" in content and "?" in content, (
            "Project card should have fallback when no image"
        )

    def test_project_card_image_has_blur_placeholder(self):
        """Project card image should support blur placeholder."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "lqip" in content or "blurDataURL" in content, (
            "Project card should support blur placeholder"
        )


class TestProjectQueriesExist:
    """Test that required GROQ queries exist in queries file."""

    def test_queries_file_exists(self):
        """sanity/lib/queries.ts should exist."""
        assert QUERIES_FILE.exists(), "sanity/lib/queries.ts not found"

    def test_projects_query_defined(self):
        """projectsQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export const projectsQuery" in content, (
            "projectsQuery should be exported"
        )

    def test_projects_query_orders_by_date(self):
        """projectsQuery should order by date desc."""
        content = QUERIES_FILE.read_text()
        assert "order(date desc)" in content, (
            "projectsQuery should order by date desc"
        )

    def test_project_count_query_defined(self):
        """projectCountByCategoryQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export const projectCountByCategoryQuery" in content, (
            "projectCountByCategoryQuery should be exported"
        )

    def test_project_count_query_counts_all(self):
        """projectCountByCategoryQuery should count all projects."""
        content = QUERIES_FILE.read_text()
        assert '"all": count(*[_type == "project"])' in content, (
            "projectCountByCategoryQuery should count all projects"
        )

    def test_projects_query_includes_required_fields(self):
        """projectsQuery should include all required fields."""
        content = QUERIES_FILE.read_text()
        required_fields = ["_id", "title", "slug", "category", "client", "date", "coverImage"]
        for field in required_fields:
            assert field in content, f"projectsQuery should include {field}"

    def test_project_list_item_type_defined(self):
        """ProjectListItem type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export interface ProjectListItem" in content, (
            "ProjectListItem type should be exported"
        )

    def test_project_category_counts_type_defined(self):
        """ProjectCategoryCountsResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "export interface ProjectCategoryCountsResult" in content, (
            "ProjectCategoryCountsResult type should be exported"
        )


class TestCategoryConfiguration:
    """Test that category configuration is properly defined."""

    def test_category_config_defined(self):
        """CATEGORY_CONFIG constant should be defined."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "CATEGORY_CONFIG" in content, (
            "CATEGORY_CONFIG constant should be defined"
        )

    def test_category_config_has_editorial(self):
        """CATEGORY_CONFIG should include editorial category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "editorial" in content and "Editorial" in content, (
            "CATEGORY_CONFIG should include editorial category"
        )

    def test_category_config_has_campaign(self):
        """CATEGORY_CONFIG should include campaign category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "campaign" in content and "Campaign" in content, (
            "CATEGORY_CONFIG should include campaign category"
        )

    def test_category_config_has_lookbook(self):
        """CATEGORY_CONFIG should include lookbook category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "lookbook" in content and "Lookbook" in content, (
            "CATEGORY_CONFIG should include lookbook category"
        )

    def test_category_config_has_styling(self):
        """CATEGORY_CONFIG should include styling category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "styling" in content and "Styling" in content, (
            "CATEGORY_CONFIG should include styling category"
        )

    def test_category_config_has_personal(self):
        """CATEGORY_CONFIG should include personal category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "personal" in content and "Personal" in content, (
            "CATEGORY_CONFIG should include personal category"
        )

    def test_category_config_has_labels(self):
        """CATEGORY_CONFIG should have labels for each category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "label:" in content, (
            "CATEGORY_CONFIG should have labels"
        )

    def test_category_config_has_descriptions(self):
        """CATEGORY_CONFIG should have descriptions for each category."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "description:" in content, (
            "CATEGORY_CONFIG should have descriptions"
        )


class TestProjectCardDateFormatting:
    """Test that project cards format dates correctly."""

    def test_date_uses_time_element(self):
        """Project card should use time element for date."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "<time" in content, (
            "Project card should use time element"
        )

    def test_time_has_datetime_attribute(self):
        """Time element should have dateTime attribute."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "dateTime=" in content, (
            "Time element should have dateTime attribute"
        )

    def test_date_formatting_with_tolocale(self):
        """Project card should format date with toLocaleDateString."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "toLocaleDateString" in content, (
            "Project card should format date with toLocaleDateString"
        )

    def test_date_shows_year_and_month(self):
        """Project card should show year and month in date."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "year:" in content and "month:" in content, (
            "Date formatting should include year and month"
        )


class TestResultsCount:
    """Test that projects page shows results count."""

    def test_shows_project_count(self):
        """Projects page should show project count."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "projects.length" in content and ("project" in content.lower() or "projects" in content.lower()), (
            "Projects page should show project count"
        )

    def test_handles_singular_plural(self):
        """Projects page should handle singular/plural project count."""
        content = PROJECTS_PAGE_FILE.read_text()
        # Check for conditional text based on count
        assert "projects.length === 1" in content or '1 ? "project"' in content or "1 ? 'project'" in content, (
            "Projects page should handle singular/plural"
        )


class TestCategoryDescription:
    """Test that category description displays when filter is active."""

    def test_shows_category_description(self):
        """Projects page should show category description when filtered."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "activeCategory" in content and "description" in content, (
            "Projects page should show category description"
        )

    def test_category_description_uses_config(self):
        """Category description should come from CATEGORY_CONFIG."""
        content = PROJECTS_PAGE_FILE.read_text()
        assert "CATEGORY_CONFIG[activeCategory]" in content or "CATEGORY_CONFIG[activeCategory].description" in content, (
            "Category description should use CATEGORY_CONFIG"
        )
