"""
Tests for T-006: Create TypeScript types for all Sanity content

These tests verify that TypeScript interfaces are properly defined for all 8 document types:
Homepage, BlogPost, Project, PopupContent, AboutPage, ContactPage, SiteSettings, Navigation

Acceptance Criteria:
- TypeScript interfaces created for all 8 document types
- PortableTextBlock type is properly defined
- SanityImage interface includes all required fields (url, alt, dimensions)
- Types are exported from a central types/ directory
- Types match exactly with Sanity schema definitions
"""

import re
from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
TYPES_DIR = PROJECT_ROOT / "types"
SANITY_SCHEMAS_DIR = PROJECT_ROOT / "sanity" / "schemas"


class TestTypesDirectoryStructure:
    """Test that types directory exists and has proper structure."""

    def test_types_directory_exists(self):
        """types/ directory should exist."""
        assert TYPES_DIR.exists(), "types/ directory not found"
        assert TYPES_DIR.is_dir(), "types should be a directory"

    def test_types_index_exists(self):
        """types/index.ts should exist as central export."""
        index_path = TYPES_DIR / "index.ts"
        assert index_path.exists(), "types/index.ts not found - central export file required"

    def test_sanity_types_file_exists(self):
        """types/sanity.ts should exist with Sanity type definitions."""
        sanity_path = TYPES_DIR / "sanity.ts"
        assert sanity_path.exists(), "types/sanity.ts not found"


class TestCentralTypesExport:
    """Test that types are exported from central types/ directory."""

    def test_index_exports_document_types(self):
        """types/index.ts should export all 8 document types."""
        index_path = TYPES_DIR / "index.ts"
        content = index_path.read_text()

        document_types = [
            "Homepage",
            "BlogPost",
            "Project",
            "PopupContent",
            "AboutPage",
            "ContactPage",
            "SiteSettings",
            "Navigation",
        ]

        for doc_type in document_types:
            assert doc_type in content, f"types/index.ts should export {doc_type}"

    def test_index_exports_portable_text_block(self):
        """types/index.ts should export PortableTextBlock."""
        index_path = TYPES_DIR / "index.ts"
        content = index_path.read_text()
        assert "PortableTextBlock" in content, (
            "types/index.ts should export PortableTextBlock"
        )

    def test_index_exports_sanity_image(self):
        """types/index.ts should export SanityImage types."""
        index_path = TYPES_DIR / "index.ts"
        content = index_path.read_text()
        assert "SanityImage" in content, (
            "types/index.ts should export SanityImage"
        )

    def test_index_exports_from_sanity_module(self):
        """types/index.ts should export from ./sanity module."""
        index_path = TYPES_DIR / "index.ts"
        content = index_path.read_text()
        assert "./sanity" in content or "'./sanity'" in content, (
            "types/index.ts should export from './sanity'"
        )


class TestHomepageInterface:
    """Test Homepage interface matches Sanity schema."""

    def test_homepage_interface_exists(self):
        """Homepage interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface Homepage" in content or "export interface Homepage" in content, (
            "Homepage interface not found"
        )

    def test_homepage_extends_sanity_document(self):
        """Homepage should extend SanityDocument."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "Homepage extends SanityDocument" in content, (
            "Homepage should extend SanityDocument"
        )

    def test_homepage_has_type_field(self):
        """Homepage should have _type: 'homepage' field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        # Check for _type field with 'homepage' value
        homepage_section = _extract_interface_content(content, "Homepage")
        assert "_type: 'homepage'" in homepage_section or '_type: "homepage"' in homepage_section, (
            "Homepage should have _type: 'homepage'"
        )

    def test_homepage_has_required_hero_heading(self):
        """Homepage should have heroHeading field (required in schema)."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        homepage_section = _extract_interface_content(content, "Homepage")
        # Required field should not have ?
        assert "heroHeading:" in homepage_section, (
            "Homepage should have heroHeading field"
        )
        # Check it's not optional
        hero_heading_line = [l for l in homepage_section.split('\n') if 'heroHeading' in l][0]
        assert "heroHeading?" not in hero_heading_line, (
            "heroHeading should be required (not optional)"
        )

    def test_homepage_has_optional_fields(self):
        """Homepage should have optional fields with ? marker."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        homepage_section = _extract_interface_content(content, "Homepage")

        optional_fields = [
            "heroSubheading",
            "heroImage",
            "introText",
            "featuredPostsHeading",
            "featuredProjectsHeading",
            "ctaText",
            "ctaLink",
            "seo",
        ]

        for field in optional_fields:
            assert f"{field}?" in homepage_section, (
                f"Homepage.{field} should be optional"
            )

    def test_homepage_hero_image_uses_sanity_image(self):
        """Homepage heroImage should use SanityImage type."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        homepage_section = _extract_interface_content(content, "Homepage")
        assert "heroImage?:" in homepage_section and "SanityImage" in homepage_section, (
            "Homepage.heroImage should use SanityImage type"
        )

    def test_homepage_intro_text_uses_portable_text(self):
        """Homepage introText should use PortableText type."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        homepage_section = _extract_interface_content(content, "Homepage")
        assert "introText?:" in homepage_section and "PortableText" in homepage_section, (
            "Homepage.introText should use PortableText type"
        )


class TestBlogPostInterface:
    """Test BlogPost interface matches Sanity schema."""

    def test_blogpost_interface_exists(self):
        """BlogPost interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface BlogPost" in content, "BlogPost interface not found"

    def test_blogpost_extends_sanity_document(self):
        """BlogPost should extend SanityDocument."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "BlogPost extends SanityDocument" in content, (
            "BlogPost should extend SanityDocument"
        )

    def test_blogpost_has_type_field(self):
        """BlogPost should have _type: 'blogPost' field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        blogpost_section = _extract_interface_content(content, "BlogPost")
        assert "_type: 'blogPost'" in blogpost_section or '_type: "blogPost"' in blogpost_section, (
            "BlogPost should have _type: 'blogPost'"
        )

    def test_blogpost_has_required_title(self):
        """BlogPost should have required title field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        blogpost_section = _extract_interface_content(content, "BlogPost")
        # title should not be optional
        title_lines = [l for l in blogpost_section.split('\n') if re.match(r'\s+title\s*[?:]', l)]
        assert len(title_lines) > 0, "BlogPost should have title field"
        assert "title?" not in title_lines[0], "BlogPost.title should be required"

    def test_blogpost_has_required_slug(self):
        """BlogPost should have required slug field using SanitySlug."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        blogpost_section = _extract_interface_content(content, "BlogPost")
        assert "slug:" in blogpost_section and "SanitySlug" in blogpost_section, (
            "BlogPost should have slug: SanitySlug field"
        )

    def test_blogpost_has_optional_fields(self):
        """BlogPost should have optional fields."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        blogpost_section = _extract_interface_content(content, "BlogPost")

        optional_fields = [
            "coverImage",
            "excerpt",
            "content",
            "publishedAt",
            "tags",
            "featured",
            "seo",
        ]

        for field in optional_fields:
            assert f"{field}?" in blogpost_section, (
                f"BlogPost.{field} should be optional"
            )

    def test_blogpost_tags_is_string_array(self):
        """BlogPost tags should be string array."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        blogpost_section = _extract_interface_content(content, "BlogPost")
        assert "tags?:" in blogpost_section and "string[]" in blogpost_section, (
            "BlogPost.tags should be string[]"
        )

    def test_blogpost_featured_is_boolean(self):
        """BlogPost featured should be boolean."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        blogpost_section = _extract_interface_content(content, "BlogPost")
        assert "featured?:" in blogpost_section and "boolean" in blogpost_section, (
            "BlogPost.featured should be boolean"
        )


class TestProjectInterface:
    """Test Project interface matches Sanity schema."""

    def test_project_interface_exists(self):
        """Project interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface Project" in content, "Project interface not found"

    def test_project_extends_sanity_document(self):
        """Project should extend SanityDocument."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "Project extends SanityDocument" in content, (
            "Project should extend SanityDocument"
        )

    def test_project_has_type_field(self):
        """Project should have _type: 'project' field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        project_section = _extract_interface_content(content, "Project")
        assert "_type: 'project'" in project_section or '_type: "project"' in project_section, (
            "Project should have _type: 'project'"
        )

    def test_project_has_required_cover_image(self):
        """Project should have required coverImage field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        project_section = _extract_interface_content(content, "Project")
        # coverImage should NOT have ? (required in schema)
        cover_lines = [l for l in project_section.split('\n') if 'coverImage' in l]
        assert len(cover_lines) > 0, "Project should have coverImage field"
        assert "coverImage?:" not in cover_lines[0], (
            "Project.coverImage should be required (not optional)"
        )

    def test_project_has_category_type(self):
        """Project should have category field with ProjectCategory type."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "ProjectCategory" in content, (
            "ProjectCategory type should be defined"
        )
        # ProjectCategory should include all schema values
        assert "'editorial'" in content, "ProjectCategory should include 'editorial'"
        assert "'campaign'" in content, "ProjectCategory should include 'campaign'"
        assert "'lookbook'" in content, "ProjectCategory should include 'lookbook'"
        assert "'styling'" in content, "ProjectCategory should include 'styling'"
        assert "'personal'" in content, "ProjectCategory should include 'personal'"

    def test_project_has_images_array(self):
        """Project should have optional images array with ImageWithPopup."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        project_section = _extract_interface_content(content, "Project")
        assert "images?:" in project_section and "ImageWithPopup[]" in project_section, (
            "Project.images should be ImageWithPopup[]"
        )


class TestPopupContentInterface:
    """Test PopupContent interface matches Sanity schema."""

    def test_popupcontent_interface_exists(self):
        """PopupContent interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface PopupContent" in content, "PopupContent interface not found"

    def test_popupcontent_extends_sanity_document(self):
        """PopupContent should extend SanityDocument."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "PopupContent extends SanityDocument" in content, (
            "PopupContent should extend SanityDocument"
        )

    def test_popupcontent_has_type_field(self):
        """PopupContent should have _type: 'popupContent' field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        popup_section = _extract_interface_content(content, "PopupContent")
        assert "_type: 'popupContent'" in popup_section or '_type: "popupContent"' in popup_section, (
            "PopupContent should have _type: 'popupContent'"
        )

    def test_popupcontent_has_required_title(self):
        """PopupContent should have required title field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        popup_section = _extract_interface_content(content, "PopupContent")
        title_lines = [l for l in popup_section.split('\n') if re.match(r'\s+title\s*[?:]', l)]
        assert len(title_lines) > 0, "PopupContent should have title field"
        assert "title?" not in title_lines[0], "PopupContent.title should be required"

    def test_popupcontent_has_optional_fields(self):
        """PopupContent should have optional fields."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        popup_section = _extract_interface_content(content, "PopupContent")

        optional_fields = ["description", "link", "linkText", "tags"]

        for field in optional_fields:
            assert f"{field}?" in popup_section, (
                f"PopupContent.{field} should be optional"
            )


class TestAboutPageInterface:
    """Test AboutPage interface matches Sanity schema."""

    def test_aboutpage_interface_exists(self):
        """AboutPage interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface AboutPage" in content, "AboutPage interface not found"

    def test_aboutpage_extends_sanity_document(self):
        """AboutPage should extend SanityDocument."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "AboutPage extends SanityDocument" in content, (
            "AboutPage should extend SanityDocument"
        )

    def test_aboutpage_has_type_field(self):
        """AboutPage should have _type: 'aboutPage' field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        about_section = _extract_interface_content(content, "AboutPage")
        assert "_type: 'aboutPage'" in about_section or '_type: "aboutPage"' in about_section, (
            "AboutPage should have _type: 'aboutPage'"
        )

    def test_aboutpage_has_credentials_array(self):
        """AboutPage should have optional credentials array."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        about_section = _extract_interface_content(content, "AboutPage")
        assert "credentials?:" in about_section and "Credential[]" in about_section, (
            "AboutPage.credentials should be Credential[]"
        )

    def test_aboutpage_has_clients_array(self):
        """AboutPage should have optional clients string array."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        about_section = _extract_interface_content(content, "AboutPage")
        assert "clients?:" in about_section and "string[]" in about_section, (
            "AboutPage.clients should be string[]"
        )

    def test_credential_type_exists(self):
        """Credential type should be defined for AboutPage."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface Credential" in content, "Credential interface not found"
        assert "title:" in content and "organization?" in content and "period?" in content, (
            "Credential should have title, organization, period fields"
        )


class TestContactPageInterface:
    """Test ContactPage interface matches Sanity schema."""

    def test_contactpage_interface_exists(self):
        """ContactPage interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface ContactPage" in content, "ContactPage interface not found"

    def test_contactpage_extends_sanity_document(self):
        """ContactPage should extend SanityDocument."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "ContactPage extends SanityDocument" in content, (
            "ContactPage should extend SanityDocument"
        )

    def test_contactpage_has_type_field(self):
        """ContactPage should have _type: 'contactPage' field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        contact_section = _extract_interface_content(content, "ContactPage")
        assert "_type: 'contactPage'" in contact_section or '_type: "contactPage"' in contact_section, (
            "ContactPage should have _type: 'contactPage'"
        )

    def test_contactpage_has_form_enabled(self):
        """ContactPage should have formEnabled boolean field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        contact_section = _extract_interface_content(content, "ContactPage")
        assert "formEnabled?:" in contact_section and "boolean" in contact_section, (
            "ContactPage.formEnabled should be optional boolean"
        )

    def test_contactpage_has_social_links(self):
        """ContactPage should have socialLinks array."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        contact_section = _extract_interface_content(content, "ContactPage")
        assert "socialLinks?:" in contact_section and "SocialLink[]" in contact_section, (
            "ContactPage.socialLinks should be SocialLink[]"
        )


class TestSiteSettingsInterface:
    """Test SiteSettings interface matches Sanity schema."""

    def test_sitesettings_interface_exists(self):
        """SiteSettings interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface SiteSettings" in content, "SiteSettings interface not found"

    def test_sitesettings_extends_sanity_document(self):
        """SiteSettings should extend SanityDocument."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "SiteSettings extends SanityDocument" in content, (
            "SiteSettings should extend SanityDocument"
        )

    def test_sitesettings_has_type_field(self):
        """SiteSettings should have _type: 'siteSettings' field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        settings_section = _extract_interface_content(content, "SiteSettings")
        assert "_type: 'siteSettings'" in settings_section or '_type: "siteSettings"' in settings_section, (
            "SiteSettings should have _type: 'siteSettings'"
        )

    def test_sitesettings_has_required_sitename(self):
        """SiteSettings should have required siteName field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        settings_section = _extract_interface_content(content, "SiteSettings")
        sitename_lines = [l for l in settings_section.split('\n') if 'siteName' in l]
        assert len(sitename_lines) > 0, "SiteSettings should have siteName field"
        assert "siteName?" not in sitename_lines[0], (
            "SiteSettings.siteName should be required"
        )

    def test_sitesettings_has_google_analytics_id(self):
        """SiteSettings should have optional googleAnalyticsId."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        settings_section = _extract_interface_content(content, "SiteSettings")
        assert "googleAnalyticsId?:" in settings_section, (
            "SiteSettings.googleAnalyticsId should be optional"
        )


class TestNavigationInterface:
    """Test Navigation interface matches Sanity schema."""

    def test_navigation_interface_exists(self):
        """Navigation interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface Navigation" in content, "Navigation interface not found"

    def test_navigation_extends_sanity_document(self):
        """Navigation should extend SanityDocument."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "Navigation extends SanityDocument" in content, (
            "Navigation should extend SanityDocument"
        )

    def test_navigation_has_type_field(self):
        """Navigation should have _type: 'navigation' field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        nav_section = _extract_interface_content(content, "Navigation")
        assert "_type: 'navigation'" in nav_section or '_type: "navigation"' in nav_section, (
            "Navigation should have _type: 'navigation'"
        )

    def test_navigation_has_main_menu(self):
        """Navigation should have mainMenu array of MenuItems."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        nav_section = _extract_interface_content(content, "Navigation")
        assert "mainMenu?:" in nav_section and "MenuItem[]" in nav_section, (
            "Navigation.mainMenu should be MenuItem[]"
        )

    def test_menuitem_type_exists(self):
        """MenuItem type should be defined for Navigation."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface MenuItem" in content, "MenuItem interface not found"
        menuitem_section = _extract_interface_content(content, "MenuItem")
        assert "label:" in menuitem_section, "MenuItem should have label field"
        assert "link:" in menuitem_section, "MenuItem should have link field"
        assert "openInNewTab?" in menuitem_section, "MenuItem should have optional openInNewTab"


class TestPortableTextBlockType:
    """Test PortableTextBlock type is properly defined."""

    def test_portable_text_block_interface_exists(self):
        """PortableTextBlock interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface PortableTextBlock" in content, (
            "PortableTextBlock interface not found"
        )

    def test_portable_text_block_has_type_field(self):
        """PortableTextBlock should have _type: 'block' field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        block_section = _extract_interface_content(content, "PortableTextBlock")
        assert "_type: 'block'" in block_section or '_type: "block"' in block_section, (
            "PortableTextBlock should have _type: 'block'"
        )

    def test_portable_text_block_has_key(self):
        """PortableTextBlock should have _key field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        block_section = _extract_interface_content(content, "PortableTextBlock")
        assert "_key:" in block_section, "PortableTextBlock should have _key field"

    def test_portable_text_block_has_style(self):
        """PortableTextBlock should have style field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        block_section = _extract_interface_content(content, "PortableTextBlock")
        assert "style:" in block_section, "PortableTextBlock should have style field"

    def test_portable_text_block_style_type_exists(self):
        """PortableTextBlockStyle type should include all styles from schema."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "PortableTextBlockStyle" in content, (
            "PortableTextBlockStyle type should be defined"
        )
        # Check for all style values from portableText schema
        assert "'normal'" in content, "PortableTextBlockStyle should include 'normal'"
        assert "'h2'" in content, "PortableTextBlockStyle should include 'h2'"
        assert "'h3'" in content, "PortableTextBlockStyle should include 'h3'"
        assert "'h4'" in content, "PortableTextBlockStyle should include 'h4'"
        assert "'blockquote'" in content, "PortableTextBlockStyle should include 'blockquote'"

    def test_portable_text_block_has_children(self):
        """PortableTextBlock should have children array."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        block_section = _extract_interface_content(content, "PortableTextBlock")
        assert "children:" in block_section, "PortableTextBlock should have children field"

    def test_portable_text_block_has_mark_defs(self):
        """PortableTextBlock should have markDefs array."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        block_section = _extract_interface_content(content, "PortableTextBlock")
        assert "markDefs:" in block_section, "PortableTextBlock should have markDefs field"

    def test_portable_text_list_item_type_exists(self):
        """PortableTextListItemType should include list types from schema."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "PortableTextListItemType" in content, (
            "PortableTextListItemType should be defined"
        )
        assert "'bullet'" in content, "PortableTextListItemType should include 'bullet'"
        assert "'number'" in content, "PortableTextListItemType should include 'number'"

    def test_portable_text_array_type_exists(self):
        """PortableText array type should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        # Should have PortableText type as array of content
        assert "type PortableText" in content or "PortableText = " in content, (
            "PortableText type should be defined"
        )


class TestSanityImageInterface:
    """Test SanityImage interface includes all required fields."""

    def test_sanity_image_interface_exists(self):
        """SanityImage interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface SanityImage" in content, "SanityImage interface not found"

    def test_sanity_image_has_alt_field(self):
        """SanityImage should have alt field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        image_section = _extract_interface_content(content, "SanityImage")
        assert "alt:" in image_section or "alt" in image_section, (
            "SanityImage should have alt field"
        )

    def test_sanity_image_base_has_asset(self):
        """SanityImageBase should have asset field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "SanityImageBase" in content, "SanityImageBase should exist"
        base_section = _extract_interface_content(content, "SanityImageBase")
        assert "asset:" in base_section, "SanityImageBase should have asset field"

    def test_sanity_image_base_has_hotspot(self):
        """SanityImageBase should have optional hotspot field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        base_section = _extract_interface_content(content, "SanityImageBase")
        assert "hotspot?" in base_section, "SanityImageBase should have optional hotspot"

    def test_sanity_image_base_has_crop(self):
        """SanityImageBase should have optional crop field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        base_section = _extract_interface_content(content, "SanityImageBase")
        assert "crop?" in base_section, "SanityImageBase should have optional crop"

    def test_sanity_image_expanded_exists(self):
        """SanityImageExpanded should be defined for expanded image data."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface SanityImageExpanded" in content, (
            "SanityImageExpanded interface not found"
        )

    def test_sanity_image_expanded_has_url(self):
        """SanityImageExpanded asset should have url field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        expanded_section = _extract_interface_content(content, "SanityImageExpanded")
        assert "url:" in expanded_section, (
            "SanityImageExpanded.asset should have url field"
        )

    def test_sanity_image_metadata_has_dimensions(self):
        """SanityImageMetadata should have dimensions field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "SanityImageMetadata" in content, "SanityImageMetadata should exist"
        metadata_section = _extract_interface_content(content, "SanityImageMetadata")
        assert "dimensions:" in metadata_section, (
            "SanityImageMetadata should have dimensions"
        )
        assert "width:" in content, "dimensions should have width"
        assert "height:" in content, "dimensions should have height"


class TestSEOObjectType:
    """Test SEO object type matches schema."""

    def test_seo_interface_exists(self):
        """SEO interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface SEO" in content, "SEO interface not found"

    def test_seo_has_meta_title(self):
        """SEO should have optional metaTitle field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        seo_section = _extract_interface_content(content, "SEO")
        assert "metaTitle?" in seo_section, "SEO.metaTitle should be optional"

    def test_seo_has_meta_description(self):
        """SEO should have optional metaDescription field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        seo_section = _extract_interface_content(content, "SEO")
        assert "metaDescription?" in seo_section, "SEO.metaDescription should be optional"

    def test_seo_has_og_image(self):
        """SEO should have optional ogImage field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        seo_section = _extract_interface_content(content, "SEO")
        assert "ogImage?" in seo_section, "SEO.ogImage should be optional"


class TestSocialLinkType:
    """Test SocialLink type matches schema."""

    def test_social_link_interface_exists(self):
        """SocialLink interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface SocialLink" in content, "SocialLink interface not found"

    def test_social_link_has_platform(self):
        """SocialLink should have platform field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        social_section = _extract_interface_content(content, "SocialLink")
        assert "platform:" in social_section, "SocialLink should have platform field"

    def test_social_link_has_url(self):
        """SocialLink should have url field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        social_section = _extract_interface_content(content, "SocialLink")
        assert "url:" in social_section, "SocialLink should have url field"

    def test_social_platform_type_has_all_values(self):
        """SocialPlatform type should include all platform options."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "SocialPlatform" in content, "SocialPlatform type should exist"

        platforms = ["instagram", "twitter", "linkedin", "tiktok", "pinterest", "youtube", "facebook", "email"]
        for platform in platforms:
            assert f"'{platform}'" in content or f'"{platform}"' in content, (
                f"SocialPlatform should include '{platform}'"
            )


class TestImageWithPopupType:
    """Test ImageWithPopup type matches schema."""

    def test_image_with_popup_interface_exists(self):
        """ImageWithPopup interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface ImageWithPopup" in content, "ImageWithPopup interface not found"

    def test_image_with_popup_has_image(self):
        """ImageWithPopup should have image field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        iwp_section = _extract_interface_content(content, "ImageWithPopup")
        assert "image:" in iwp_section, "ImageWithPopup should have image field"

    def test_image_with_popup_has_alt(self):
        """ImageWithPopup should have alt field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        iwp_section = _extract_interface_content(content, "ImageWithPopup")
        assert "alt:" in iwp_section, "ImageWithPopup should have alt field"

    def test_image_with_popup_has_popup_reference(self):
        """ImageWithPopup should have optional popup reference."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        iwp_section = _extract_interface_content(content, "ImageWithPopup")
        assert "popup?" in iwp_section, "ImageWithPopup should have optional popup"

    def test_image_with_popup_has_size_options(self):
        """ImageWithPopup should have size field with correct options."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        iwp_section = _extract_interface_content(content, "ImageWithPopup")
        assert "size?" in iwp_section, "ImageWithPopup should have optional size"
        # Check for size values
        assert "'small'" in content, "Size should include 'small'"
        assert "'medium'" in content, "Size should include 'medium'"
        assert "'large'" in content, "Size should include 'large'"
        assert "'full'" in content, "Size should include 'full'"


class TestSanityBaseTypes:
    """Test Sanity base types are properly defined."""

    def test_sanity_document_interface_exists(self):
        """SanityDocument interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface SanityDocument" in content, "SanityDocument interface not found"

    def test_sanity_document_has_required_fields(self):
        """SanityDocument should have all required base fields."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        doc_section = _extract_interface_content(content, "SanityDocument")

        required_fields = ["_id:", "_type:", "_createdAt:", "_updatedAt:", "_rev:"]
        for field in required_fields:
            assert field in doc_section, f"SanityDocument should have {field} field"

    def test_sanity_reference_interface_exists(self):
        """SanityReference interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface SanityReference" in content, "SanityReference interface not found"

    def test_sanity_slug_interface_exists(self):
        """SanitySlug interface should be defined."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        assert "interface SanitySlug" in content, "SanitySlug interface not found"

    def test_sanity_slug_has_current(self):
        """SanitySlug should have current field."""
        sanity_path = TYPES_DIR / "sanity.ts"
        content = sanity_path.read_text()
        slug_section = _extract_interface_content(content, "SanitySlug")
        assert "current:" in slug_section, "SanitySlug should have current field"


# Helper function to extract interface content
def _extract_interface_content(content: str, interface_name: str) -> str:
    """
    Extract the content of an interface definition from TypeScript code.
    Returns the portion from 'interface Name' through the closing brace.
    """
    # Find the start of the interface
    patterns = [
        f"export interface {interface_name} extends",
        f"export interface {interface_name} {{",
        f"interface {interface_name} extends",
        f"interface {interface_name} {{",
    ]

    start_idx = -1
    for pattern in patterns:
        idx = content.find(pattern)
        if idx != -1:
            start_idx = idx
            break

    if start_idx == -1:
        return ""

    # Find the matching closing brace
    brace_count = 0
    started = False
    end_idx = start_idx

    for i, char in enumerate(content[start_idx:], start_idx):
        if char == '{':
            brace_count += 1
            started = True
        elif char == '}':
            brace_count -= 1
            if started and brace_count == 0:
                end_idx = i + 1
                break

    return content[start_idx:end_idx]
