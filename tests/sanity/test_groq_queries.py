"""
Tests for T-007: Create GROQ queries for all content fetching

These tests verify that GROQ queries are properly defined according to the requirements:
- GROQ query functions created in sanity/lib/queries.ts
- Homepage query includes all necessary fields and relations
- Blog queries support pagination and slug-based fetching
- Project queries include gallery images with popup references
- Image fields properly resolve URLs using Sanity's image builder
- All queries are typed with return types

Acceptance Criteria:
- GROQ query functions created in lib/sanity/queries.ts
- Homepage query includes all necessary fields and relations
- Blog queries support pagination and slug-based fetching
- Project queries include gallery images with popup references
- Image fields properly resolve URLs using Sanity's image builder
- All queries are typed with return types
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
QUERIES_FILE = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"


class TestQueriesFileExists:
    """Test that the queries file exists and has proper structure."""

    def test_queries_file_exists(self):
        """sanity/lib/queries.ts should exist."""
        assert QUERIES_FILE.exists(), "sanity/lib/queries.ts not found"

    def test_queries_file_imports_groq(self):
        """queries.ts should import groq from next-sanity."""
        content = QUERIES_FILE.read_text()
        assert "from 'next-sanity'" in content or 'from "next-sanity"' in content, (
            "queries.ts should import from next-sanity"
        )
        assert "groq" in content, "queries.ts should import groq"

    def test_queries_file_has_exports(self):
        """queries.ts should export query constants."""
        content = QUERIES_FILE.read_text()
        assert "export const" in content or "export {" in content, (
            "queries.ts should export query constants"
        )


class TestCommonProjections:
    """Test that common projections are defined for reusability."""

    def test_image_projection_defined(self):
        """queries.ts should define an image projection for asset expansion."""
        content = QUERIES_FILE.read_text()
        assert "imageProjection" in content, (
            "queries.ts should define imageProjection for reusable image expansion"
        )

    def test_image_projection_expands_asset(self):
        """Image projection should expand asset reference with URL and metadata."""
        content = QUERIES_FILE.read_text()
        assert "asset->" in content, "Image projection should expand asset reference"
        assert "url" in content, "Image projection should include URL"

    def test_image_projection_includes_metadata(self):
        """Image projection should include metadata with dimensions and LQIP."""
        content = QUERIES_FILE.read_text()
        assert "metadata" in content, "Image projection should include metadata"
        assert "dimensions" in content, "Image projection should include dimensions"
        assert "lqip" in content, "Image projection should include LQIP for blur placeholders"

    def test_image_projection_includes_alt(self):
        """Image projection should include alt text."""
        content = QUERIES_FILE.read_text()
        # Check that alt is included in image projection
        assert "alt," in content or "alt\n" in content or '"alt"' in content, (
            "Image projection should include alt text"
        )

    def test_image_projection_includes_hotspot_and_crop(self):
        """Image projection should include hotspot and crop data."""
        content = QUERIES_FILE.read_text()
        assert "hotspot" in content, "Image projection should include hotspot"
        assert "crop" in content, "Image projection should include crop"

    def test_seo_projection_defined(self):
        """queries.ts should define an SEO projection."""
        content = QUERIES_FILE.read_text()
        assert "seoProjection" in content, (
            "queries.ts should define seoProjection for reusable SEO fields"
        )

    def test_seo_projection_includes_meta_fields(self):
        """SEO projection should include metaTitle and metaDescription."""
        content = QUERIES_FILE.read_text()
        assert "metaTitle" in content, "SEO projection should include metaTitle"
        assert "metaDescription" in content, "SEO projection should include metaDescription"

    def test_seo_projection_includes_og_image(self):
        """SEO projection should include ogImage with image projection."""
        content = QUERIES_FILE.read_text()
        assert "ogImage" in content, "SEO projection should include ogImage"

    def test_popup_projection_defined(self):
        """queries.ts should define a popup content projection."""
        content = QUERIES_FILE.read_text()
        assert "popupProjection" in content, (
            "queries.ts should define popupProjection for popup content"
        )

    def test_image_with_popup_projection_defined(self):
        """queries.ts should define an image with popup projection."""
        content = QUERIES_FILE.read_text()
        assert "imageWithPopupProjection" in content, (
            "queries.ts should define imageWithPopupProjection"
        )


class TestSiteSettingsQuery:
    """Test site settings GROQ query."""

    def test_site_settings_query_exists(self):
        """siteSettingsQuery should be defined and exported."""
        content = QUERIES_FILE.read_text()
        assert "siteSettingsQuery" in content, "siteSettingsQuery should be defined"
        assert "export" in content and "siteSettingsQuery" in content, (
            "siteSettingsQuery should be exported"
        )

    def test_site_settings_query_filters_by_type(self):
        """siteSettingsQuery should filter by _type == 'siteSettings'."""
        content = QUERIES_FILE.read_text()
        assert '_type == "siteSettings"' in content or "_type == 'siteSettings'" in content, (
            "siteSettingsQuery should filter by siteSettings type"
        )

    def test_site_settings_query_is_singleton(self):
        """siteSettingsQuery should select first item [0] as it's a singleton."""
        content = QUERIES_FILE.read_text()
        # Check for singleton pattern
        assert "[0]" in content, "siteSettingsQuery should use [0] for singleton"

    def test_site_settings_query_includes_site_name(self):
        """siteSettingsQuery should include siteName field."""
        content = QUERIES_FILE.read_text()
        assert "siteName" in content, "siteSettingsQuery should include siteName"

    def test_site_settings_query_includes_logo(self):
        """siteSettingsQuery should include logo with image expansion."""
        content = QUERIES_FILE.read_text()
        assert "logo" in content, "siteSettingsQuery should include logo"

    def test_site_settings_query_includes_social_links(self):
        """siteSettingsQuery should include socialLinks array."""
        content = QUERIES_FILE.read_text()
        assert "socialLinks" in content, "siteSettingsQuery should include socialLinks"

    def test_site_settings_query_includes_default_seo(self):
        """siteSettingsQuery should include defaultSeo."""
        content = QUERIES_FILE.read_text()
        assert "defaultSeo" in content, "siteSettingsQuery should include defaultSeo"


class TestNavigationQuery:
    """Test navigation GROQ query."""

    def test_navigation_query_exists(self):
        """navigationQuery should be defined and exported."""
        content = QUERIES_FILE.read_text()
        assert "navigationQuery" in content, "navigationQuery should be defined"
        assert "export" in content and "navigationQuery" in content, (
            "navigationQuery should be exported"
        )

    def test_navigation_query_filters_by_type(self):
        """navigationQuery should filter by _type == 'navigation'."""
        content = QUERIES_FILE.read_text()
        assert '_type == "navigation"' in content or "_type == 'navigation'" in content, (
            "navigationQuery should filter by navigation type"
        )

    def test_navigation_query_is_singleton(self):
        """navigationQuery should select first item [0] as it's a singleton."""
        content = QUERIES_FILE.read_text()
        # Find the navigation query and check for [0]
        assert "navigation" in content and "[0]" in content, (
            "navigationQuery should use [0] for singleton"
        )

    def test_navigation_query_includes_main_menu(self):
        """navigationQuery should include mainMenu array."""
        content = QUERIES_FILE.read_text()
        assert "mainMenu" in content, "navigationQuery should include mainMenu"

    def test_navigation_query_includes_menu_item_fields(self):
        """navigationQuery should include menu item fields (label, link)."""
        content = QUERIES_FILE.read_text()
        assert "label" in content, "navigationQuery should include label field"
        assert "link" in content, "navigationQuery should include link field"


class TestHomepageQuery:
    """Test homepage GROQ query."""

    def test_homepage_query_exists(self):
        """homepageQuery should be defined and exported."""
        content = QUERIES_FILE.read_text()
        assert "homepageQuery" in content, "homepageQuery should be defined"
        assert "export" in content and "homepageQuery" in content, (
            "homepageQuery should be exported"
        )

    def test_homepage_query_filters_by_type(self):
        """homepageQuery should filter by _type == 'homepage'."""
        content = QUERIES_FILE.read_text()
        assert '_type == "homepage"' in content or "_type == 'homepage'" in content, (
            "homepageQuery should filter by homepage type"
        )

    def test_homepage_query_is_singleton(self):
        """homepageQuery should select first item [0] as it's a singleton."""
        content = QUERIES_FILE.read_text()
        assert "[0]" in content, "homepageQuery should use [0] for singleton"

    def test_homepage_query_includes_hero_fields(self):
        """homepageQuery should include hero section fields."""
        content = QUERIES_FILE.read_text()
        assert "heroHeading" in content, "homepageQuery should include heroHeading"
        assert "heroSubheading" in content, "homepageQuery should include heroSubheading"
        assert "heroImage" in content, "homepageQuery should include heroImage"

    def test_homepage_query_includes_intro_text(self):
        """homepageQuery should include introText."""
        content = QUERIES_FILE.read_text()
        assert "introText" in content, "homepageQuery should include introText"

    def test_homepage_query_includes_featured_headings(self):
        """homepageQuery should include featured posts and projects headings."""
        content = QUERIES_FILE.read_text()
        assert "featuredPostsHeading" in content, (
            "homepageQuery should include featuredPostsHeading"
        )
        assert "featuredProjectsHeading" in content, (
            "homepageQuery should include featuredProjectsHeading"
        )

    def test_homepage_query_includes_cta_fields(self):
        """homepageQuery should include CTA fields."""
        content = QUERIES_FILE.read_text()
        assert "ctaText" in content, "homepageQuery should include ctaText"
        assert "ctaLink" in content, "homepageQuery should include ctaLink"

    def test_homepage_query_includes_seo(self):
        """homepageQuery should include SEO fields."""
        content = QUERIES_FILE.read_text()
        # Check that seo is in the homepage query projection
        assert "seo" in content, "homepageQuery should include seo"


class TestFeaturedContentQueries:
    """Test featured posts and projects queries for homepage."""

    def test_featured_posts_query_exists(self):
        """featuredPostsQuery should be defined and exported."""
        content = QUERIES_FILE.read_text()
        assert "featuredPostsQuery" in content, "featuredPostsQuery should be defined"

    def test_featured_posts_query_filters_by_featured(self):
        """featuredPostsQuery should filter by featured == true."""
        content = QUERIES_FILE.read_text()
        assert "featured == true" in content, (
            "featuredPostsQuery should filter by featured flag"
        )

    def test_featured_posts_query_orders_by_date(self):
        """featuredPostsQuery should order by publishedAt desc."""
        content = QUERIES_FILE.read_text()
        assert "order(publishedAt desc)" in content, (
            "featuredPostsQuery should order by publishedAt desc"
        )

    def test_featured_posts_query_limits_results(self):
        """featuredPostsQuery should limit results (0...3)."""
        content = QUERIES_FILE.read_text()
        assert "[0...3]" in content or "[0..3]" in content, (
            "featuredPostsQuery should limit to 3 results"
        )

    def test_featured_projects_query_exists(self):
        """featuredProjectsQuery should be defined and exported."""
        content = QUERIES_FILE.read_text()
        assert "featuredProjectsQuery" in content, "featuredProjectsQuery should be defined"

    def test_featured_projects_query_orders_by_date(self):
        """featuredProjectsQuery should order by date desc."""
        content = QUERIES_FILE.read_text()
        assert "order(date desc)" in content, (
            "featuredProjectsQuery should order by date desc"
        )


class TestBlogQueries:
    """Test blog post GROQ queries."""

    def test_blog_posts_query_exists(self):
        """blogPostsQuery should be defined and exported."""
        content = QUERIES_FILE.read_text()
        assert "blogPostsQuery" in content, "blogPostsQuery should be defined"

    def test_blog_posts_query_filters_by_type(self):
        """blogPostsQuery should filter by _type == 'blogPost'."""
        content = QUERIES_FILE.read_text()
        assert '_type == "blogPost"' in content or "_type == 'blogPost'" in content, (
            "blogPostsQuery should filter by blogPost type"
        )

    def test_blog_posts_query_orders_by_date(self):
        """blogPostsQuery should order by publishedAt desc."""
        content = QUERIES_FILE.read_text()
        assert "order(publishedAt desc)" in content, (
            "blogPostsQuery should order by publishedAt desc"
        )

    def test_blog_posts_query_supports_pagination(self):
        """blogPostsQuery should support pagination with $start and $end params."""
        content = QUERIES_FILE.read_text()
        assert "$start" in content, "blogPostsQuery should support $start param for pagination"
        assert "$end" in content, "blogPostsQuery should support $end param for pagination"

    def test_blog_posts_query_includes_list_fields(self):
        """blogPostsQuery should include fields needed for list view."""
        content = QUERIES_FILE.read_text()
        assert "title" in content, "blogPostsQuery should include title"
        assert "slug" in content, "blogPostsQuery should include slug"
        assert "excerpt" in content, "blogPostsQuery should include excerpt"
        assert "coverImage" in content, "blogPostsQuery should include coverImage"
        assert "tags" in content, "blogPostsQuery should include tags"

    def test_blog_post_count_query_exists(self):
        """blogPostCountQuery should be defined for pagination."""
        content = QUERIES_FILE.read_text()
        assert "blogPostCountQuery" in content, (
            "blogPostCountQuery should be defined for pagination"
        )
        assert "count(" in content, "blogPostCountQuery should use count function"

    def test_blog_post_by_slug_query_exists(self):
        """blogPostBySlugQuery should be defined for detail pages."""
        content = QUERIES_FILE.read_text()
        assert "blogPostBySlugQuery" in content, (
            "blogPostBySlugQuery should be defined for detail pages"
        )

    def test_blog_post_by_slug_query_uses_slug_param(self):
        """blogPostBySlugQuery should filter by $slug parameter."""
        content = QUERIES_FILE.read_text()
        assert "$slug" in content, "blogPostBySlugQuery should use $slug parameter"
        assert "slug.current ==" in content, (
            "blogPostBySlugQuery should compare slug.current"
        )

    def test_blog_post_by_slug_query_includes_content(self):
        """blogPostBySlugQuery should include full content for detail view."""
        content = QUERIES_FILE.read_text()
        assert "content" in content, "blogPostBySlugQuery should include content"

    def test_blog_post_slugs_query_exists(self):
        """blogPostSlugsQuery should exist for static generation."""
        content = QUERIES_FILE.read_text()
        assert "blogPostSlugsQuery" in content, (
            "blogPostSlugsQuery should be defined for generateStaticParams"
        )

    def test_related_posts_query_exists(self):
        """relatedPostsQuery should be defined for related content."""
        content = QUERIES_FILE.read_text()
        assert "relatedPostsQuery" in content, "relatedPostsQuery should be defined"

    def test_blog_posts_by_tag_query_exists(self):
        """blogPostsByTagQuery should be defined for tag filtering."""
        content = QUERIES_FILE.read_text()
        assert "blogPostsByTagQuery" in content, (
            "blogPostsByTagQuery should be defined for tag filtering"
        )
        assert "$tag" in content, "blogPostsByTagQuery should use $tag parameter"

    def test_all_blog_tags_query_exists(self):
        """allBlogTagsQuery should be defined for tag cloud."""
        content = QUERIES_FILE.read_text()
        assert "allBlogTagsQuery" in content, (
            "allBlogTagsQuery should be defined for tag cloud"
        )


class TestProjectQueries:
    """Test project GROQ queries."""

    def test_projects_query_exists(self):
        """projectsQuery should be defined and exported."""
        content = QUERIES_FILE.read_text()
        assert "projectsQuery" in content, "projectsQuery should be defined"

    def test_projects_query_filters_by_type(self):
        """projectsQuery should filter by _type == 'project'."""
        content = QUERIES_FILE.read_text()
        assert '_type == "project"' in content or "_type == 'project'" in content, (
            "projectsQuery should filter by project type"
        )

    def test_projects_query_orders_by_date(self):
        """projectsQuery should order by date desc."""
        content = QUERIES_FILE.read_text()
        assert "order(date desc)" in content, "projectsQuery should order by date desc"

    def test_projects_query_includes_list_fields(self):
        """projectsQuery should include fields needed for gallery listing."""
        content = QUERIES_FILE.read_text()
        assert "title" in content, "projectsQuery should include title"
        assert "slug" in content, "projectsQuery should include slug"
        assert "category" in content, "projectsQuery should include category"
        assert "coverImage" in content, "projectsQuery should include coverImage"

    def test_projects_by_category_query_exists(self):
        """projectsByCategoryQuery should be defined for category filtering."""
        content = QUERIES_FILE.read_text()
        assert "projectsByCategoryQuery" in content, (
            "projectsByCategoryQuery should be defined"
        )
        assert "$category" in content, (
            "projectsByCategoryQuery should use $category parameter"
        )

    def test_project_by_slug_query_exists(self):
        """projectBySlugQuery should be defined for detail pages."""
        content = QUERIES_FILE.read_text()
        assert "projectBySlugQuery" in content, (
            "projectBySlugQuery should be defined for detail pages"
        )

    def test_project_by_slug_query_includes_gallery_images(self):
        """projectBySlugQuery should include images array with popup references."""
        content = QUERIES_FILE.read_text()
        assert "images" in content, "projectBySlugQuery should include images gallery"

    def test_project_by_slug_query_resolves_popup_references(self):
        """projectBySlugQuery should resolve popup references in images."""
        content = QUERIES_FILE.read_text()
        # Check that popup reference is expanded (popup->)
        assert "popup->" in content, (
            "projectBySlugQuery should resolve popup references with ->"
        )

    def test_project_slugs_query_exists(self):
        """projectSlugsQuery should exist for static generation."""
        content = QUERIES_FILE.read_text()
        assert "projectSlugsQuery" in content, (
            "projectSlugsQuery should be defined for generateStaticParams"
        )

    def test_project_count_by_category_query_exists(self):
        """projectCountByCategoryQuery should exist for category counts."""
        content = QUERIES_FILE.read_text()
        assert "projectCountByCategoryQuery" in content, (
            "projectCountByCategoryQuery should be defined for category counts"
        )

    def test_adjacent_projects_query_exists(self):
        """adjacentProjectsQuery should exist for project navigation."""
        content = QUERIES_FILE.read_text()
        assert "adjacentProjectsQuery" in content, (
            "adjacentProjectsQuery should be defined for previous/next navigation"
        )


class TestAboutPageQuery:
    """Test about page GROQ query."""

    def test_about_page_query_exists(self):
        """aboutPageQuery should be defined and exported."""
        content = QUERIES_FILE.read_text()
        assert "aboutPageQuery" in content, "aboutPageQuery should be defined"

    def test_about_page_query_filters_by_type(self):
        """aboutPageQuery should filter by _type == 'aboutPage'."""
        content = QUERIES_FILE.read_text()
        assert '_type == "aboutPage"' in content or "_type == 'aboutPage'" in content, (
            "aboutPageQuery should filter by aboutPage type"
        )

    def test_about_page_query_is_singleton(self):
        """aboutPageQuery should select first item [0] as it's a singleton."""
        content = QUERIES_FILE.read_text()
        assert "[0]" in content, "aboutPageQuery should use [0] for singleton"

    def test_about_page_query_includes_profile_image(self):
        """aboutPageQuery should include profileImage with expansion."""
        content = QUERIES_FILE.read_text()
        assert "profileImage" in content, "aboutPageQuery should include profileImage"

    def test_about_page_query_includes_bio(self):
        """aboutPageQuery should include bio portable text."""
        content = QUERIES_FILE.read_text()
        assert "bio" in content, "aboutPageQuery should include bio"

    def test_about_page_query_includes_credentials(self):
        """aboutPageQuery should include credentials array."""
        content = QUERIES_FILE.read_text()
        assert "credentials" in content, "aboutPageQuery should include credentials"

    def test_about_page_query_includes_clients(self):
        """aboutPageQuery should include clients list."""
        content = QUERIES_FILE.read_text()
        assert "clients" in content, "aboutPageQuery should include clients"

    def test_about_page_query_includes_seo(self):
        """aboutPageQuery should include SEO fields."""
        content = QUERIES_FILE.read_text()
        assert "seo" in content, "aboutPageQuery should include seo"


class TestContactPageQuery:
    """Test contact page GROQ query."""

    def test_contact_page_query_exists(self):
        """contactPageQuery should be defined and exported."""
        content = QUERIES_FILE.read_text()
        assert "contactPageQuery" in content, "contactPageQuery should be defined"

    def test_contact_page_query_filters_by_type(self):
        """contactPageQuery should filter by _type == 'contactPage'."""
        content = QUERIES_FILE.read_text()
        assert '_type == "contactPage"' in content or "_type == 'contactPage'" in content, (
            "contactPageQuery should filter by contactPage type"
        )

    def test_contact_page_query_is_singleton(self):
        """contactPageQuery should select first item [0] as it's a singleton."""
        content = QUERIES_FILE.read_text()
        assert "[0]" in content, "contactPageQuery should use [0] for singleton"

    def test_contact_page_query_includes_contact_info(self):
        """contactPageQuery should include contact information fields."""
        content = QUERIES_FILE.read_text()
        assert "email" in content, "contactPageQuery should include email"
        assert "phone" in content, "contactPageQuery should include phone"
        assert "location" in content, "contactPageQuery should include location"

    def test_contact_page_query_includes_social_links(self):
        """contactPageQuery should include socialLinks."""
        content = QUERIES_FILE.read_text()
        assert "socialLinks" in content, "contactPageQuery should include socialLinks"

    def test_contact_page_query_includes_form_enabled(self):
        """contactPageQuery should include formEnabled flag."""
        content = QUERIES_FILE.read_text()
        assert "formEnabled" in content, "contactPageQuery should include formEnabled"

    def test_contact_page_query_includes_seo(self):
        """contactPageQuery should include SEO fields."""
        content = QUERIES_FILE.read_text()
        assert "seo" in content, "contactPageQuery should include seo"


class TestPopupContentQueries:
    """Test popup content GROQ queries."""

    def test_popup_content_by_id_query_exists(self):
        """popupContentByIdQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "popupContentByIdQuery" in content, (
            "popupContentByIdQuery should be defined"
        )

    def test_popup_content_by_id_uses_id_param(self):
        """popupContentByIdQuery should filter by $id parameter."""
        content = QUERIES_FILE.read_text()
        assert "$id" in content, "popupContentByIdQuery should use $id parameter"

    def test_all_popup_content_query_exists(self):
        """allPopupContentQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "allPopupContentQuery" in content, (
            "allPopupContentQuery should be defined"
        )


class TestSearchQuery:
    """Test search GROQ query."""

    def test_search_query_exists(self):
        """searchQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "searchQuery" in content, "searchQuery should be defined"

    def test_search_query_searches_posts_and_projects(self):
        """searchQuery should search both posts and projects."""
        content = QUERIES_FILE.read_text()
        # Check for both blogPost and project in search
        assert "posts" in content, "searchQuery should include posts results"
        assert "projects" in content, "searchQuery should include projects results"

    def test_search_query_uses_search_term(self):
        """searchQuery should use $searchTerm parameter."""
        content = QUERIES_FILE.read_text()
        assert "$searchTerm" in content, "searchQuery should use $searchTerm parameter"

    def test_search_query_uses_match_operator(self):
        """searchQuery should use match operator for text search."""
        content = QUERIES_FILE.read_text()
        assert "match" in content, "searchQuery should use match operator"


class TestSitemapQuery:
    """Test sitemap GROQ query."""

    def test_sitemap_query_exists(self):
        """sitemapQuery should be defined."""
        content = QUERIES_FILE.read_text()
        assert "sitemapQuery" in content, "sitemapQuery should be defined"

    def test_sitemap_query_includes_slugs(self):
        """sitemapQuery should include slugs for all content."""
        content = QUERIES_FILE.read_text()
        assert "slug" in content, "sitemapQuery should include slug"

    def test_sitemap_query_includes_timestamps(self):
        """sitemapQuery should include update timestamps."""
        content = QUERIES_FILE.read_text()
        assert "_updatedAt" in content, "sitemapQuery should include _updatedAt"


class TestSlugProjection:
    """Test that slug fields are properly projected."""

    def test_slug_uses_current_accessor(self):
        """Queries should project slug.current as slug."""
        content = QUERIES_FILE.read_text()
        assert '"slug": slug.current' in content or "'slug': slug.current" in content, (
            "Queries should project slug.current as slug"
        )


class TestQueryReturnTypes:
    """Test that all queries have proper TypeScript return types."""

    def test_types_are_imported(self):
        """queries.ts should import types from @/types/sanity."""
        content = QUERIES_FILE.read_text()
        assert "@/types/sanity" in content or "types/sanity" in content, (
            "queries.ts should import types from @/types/sanity"
        )

    def test_site_settings_result_type_exists(self):
        """SiteSettingsResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "SiteSettingsResult" in content, (
            "SiteSettingsResult type should be defined"
        )

    def test_navigation_result_type_exists(self):
        """NavigationResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "NavigationResult" in content, "NavigationResult type should be defined"

    def test_homepage_result_type_exists(self):
        """HomepageResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "HomepageResult" in content, "HomepageResult type should be defined"

    def test_blog_post_list_item_type_exists(self):
        """BlogPostListItem type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "BlogPostListItem" in content, "BlogPostListItem type should be defined"

    def test_blog_post_detail_type_exists(self):
        """BlogPostDetail type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "BlogPostDetail" in content, "BlogPostDetail type should be defined"

    def test_project_list_item_type_exists(self):
        """ProjectListItem type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "ProjectListItem" in content, "ProjectListItem type should be defined"

    def test_project_detail_type_exists(self):
        """ProjectDetail type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "ProjectDetail" in content, "ProjectDetail type should be defined"

    def test_about_page_result_type_exists(self):
        """AboutPageResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "AboutPageResult" in content, "AboutPageResult type should be defined"

    def test_contact_page_result_type_exists(self):
        """ContactPageResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "ContactPageResult" in content, "ContactPageResult type should be defined"

    def test_query_image_type_exists(self):
        """QueryImage type should be defined for expanded images."""
        content = QUERIES_FILE.read_text()
        assert "QueryImage" in content, (
            "QueryImage type should be defined for expanded images"
        )

    def test_query_seo_type_exists(self):
        """QuerySEO type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "QuerySEO" in content, "QuerySEO type should be defined"

    def test_image_with_popup_result_type_exists(self):
        """ImageWithPopupResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "ImageWithPopupResult" in content, (
            "ImageWithPopupResult type should be defined"
        )

    def test_popup_content_result_type_exists(self):
        """PopupContentResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "PopupContentResult" in content, (
            "PopupContentResult type should be defined"
        )

    def test_search_results_type_exists(self):
        """SearchResults type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "SearchResults" in content, "SearchResults type should be defined"

    def test_sitemap_content_type_exists(self):
        """SitemapContent type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "SitemapContent" in content, "SitemapContent type should be defined"

    def test_slug_item_type_exists(self):
        """SlugItem type should be defined for generateStaticParams."""
        content = QUERIES_FILE.read_text()
        assert "SlugItem" in content, (
            "SlugItem type should be defined for generateStaticParams"
        )


class TestResultTypeInterfaces:
    """Test that result type interfaces have proper fields."""

    def test_query_image_type_has_asset(self):
        """QueryImage type should have asset property."""
        content = QUERIES_FILE.read_text()
        # Check that QueryImage interface includes asset
        assert "QueryImage" in content and "asset" in content, (
            "QueryImage type should have asset property"
        )

    def test_blog_post_detail_extends_list_item(self):
        """BlogPostDetail should extend BlogPostListItem."""
        content = QUERIES_FILE.read_text()
        assert "BlogPostDetail extends BlogPostListItem" in content, (
            "BlogPostDetail should extend BlogPostListItem"
        )

    def test_project_detail_extends_list_item(self):
        """ProjectDetail should extend ProjectListItem."""
        content = QUERIES_FILE.read_text()
        assert "ProjectDetail extends ProjectListItem" in content, (
            "ProjectDetail should extend ProjectListItem"
        )


class TestAdjacentProjectsResultType:
    """Test adjacent projects result type."""

    def test_adjacent_projects_result_type_exists(self):
        """AdjacentProjectsResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "AdjacentProjectsResult" in content, (
            "AdjacentProjectsResult type should be defined"
        )

    def test_adjacent_projects_has_previous_and_next(self):
        """AdjacentProjectsResult should have previous and next properties."""
        content = QUERIES_FILE.read_text()
        assert "previous" in content, (
            "AdjacentProjectsResult should have previous property"
        )
        assert "next" in content, "AdjacentProjectsResult should have next property"


class TestProjectCategoryCountsType:
    """Test project category counts result type."""

    def test_project_category_counts_type_exists(self):
        """ProjectCategoryCountsResult type should be defined."""
        content = QUERIES_FILE.read_text()
        assert "ProjectCategoryCountsResult" in content, (
            "ProjectCategoryCountsResult type should be defined"
        )


class TestGROQSyntax:
    """Test that GROQ queries use correct syntax."""

    def test_uses_groq_template_literal(self):
        """All queries should use groq template literal."""
        content = QUERIES_FILE.read_text()
        # Count groq template literals
        groq_count = content.count("groq`")
        # Should have multiple queries using groq template literal
        assert groq_count >= 10, (
            f"Expected at least 10 queries using groq template literal, found {groq_count}"
        )

    def test_filters_use_square_brackets(self):
        """GROQ filters should use square bracket syntax."""
        content = QUERIES_FILE.read_text()
        assert "*[" in content, "GROQ queries should use *[filter] syntax"

    def test_projections_use_curly_braces(self):
        """GROQ projections should use curly brace syntax."""
        content = QUERIES_FILE.read_text()
        # Check for projection pattern
        assert "{" in content and "}" in content, (
            "GROQ queries should use {projection} syntax"
        )

    def test_references_use_arrow_syntax(self):
        """GROQ reference expansion should use -> arrow syntax."""
        content = QUERIES_FILE.read_text()
        assert "->" in content, "GROQ queries should use -> for reference expansion"

    def test_ordering_uses_pipe_operator(self):
        """GROQ ordering should use | (pipe) operator."""
        content = QUERIES_FILE.read_text()
        assert "| order(" in content, "GROQ queries should use | order() syntax"


class TestQueryExports:
    """Test that all required queries are properly exported."""

    def test_exports_site_settings_query(self):
        """siteSettingsQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const siteSettingsQuery" in content, (
            "siteSettingsQuery should be exported"
        )

    def test_exports_navigation_query(self):
        """navigationQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const navigationQuery" in content, (
            "navigationQuery should be exported"
        )

    def test_exports_homepage_query(self):
        """homepageQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const homepageQuery" in content, (
            "homepageQuery should be exported"
        )

    def test_exports_featured_posts_query(self):
        """featuredPostsQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const featuredPostsQuery" in content, (
            "featuredPostsQuery should be exported"
        )

    def test_exports_featured_projects_query(self):
        """featuredProjectsQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const featuredProjectsQuery" in content, (
            "featuredProjectsQuery should be exported"
        )

    def test_exports_blog_posts_query(self):
        """blogPostsQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const blogPostsQuery" in content, (
            "blogPostsQuery should be exported"
        )

    def test_exports_blog_post_by_slug_query(self):
        """blogPostBySlugQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const blogPostBySlugQuery" in content, (
            "blogPostBySlugQuery should be exported"
        )

    def test_exports_projects_query(self):
        """projectsQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const projectsQuery" in content, (
            "projectsQuery should be exported"
        )

    def test_exports_project_by_slug_query(self):
        """projectBySlugQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const projectBySlugQuery" in content, (
            "projectBySlugQuery should be exported"
        )

    def test_exports_about_page_query(self):
        """aboutPageQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const aboutPageQuery" in content, (
            "aboutPageQuery should be exported"
        )

    def test_exports_contact_page_query(self):
        """contactPageQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const contactPageQuery" in content, (
            "contactPageQuery should be exported"
        )
