"""
Tests for T-004: Define Sanity content schemas for all document types

These tests verify that all Sanity CMS schemas are properly defined according to the requirements:
- All 8 document type schemas are created in schemas/ directory
- Portable Text configuration is set up for rich content
- Image fields include alt text requirements
- Slug fields have auto-generation enabled
- SEO metadata objects are defined and reusable
- All schemas appear correctly in Sanity Studio sidebar (via schema index)

Acceptance Criteria:
- All 8 document type schemas are created in schemas/ directory
- Portable Text configuration is set up for rich content
- Image fields include alt text requirements
- Slug fields have auto-generation enabled
- SEO metadata objects are defined and reusable
- All schemas appear correctly in Sanity Studio sidebar
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCHEMAS_DIR = PROJECT_ROOT / "sanity" / "schemas"
DOCUMENTS_DIR = SCHEMAS_DIR / "documents"
OBJECTS_DIR = SCHEMAS_DIR / "objects"


class TestSchemaDirectoryStructure:
    """Test that schema directory structure is properly organized."""

    def test_schemas_directory_exists(self):
        """sanity/schemas/ directory should exist."""
        assert SCHEMAS_DIR.exists(), "sanity/schemas/ directory not found"
        assert SCHEMAS_DIR.is_dir(), "sanity/schemas/ should be a directory"

    def test_documents_directory_exists(self):
        """sanity/schemas/documents/ directory should exist."""
        assert DOCUMENTS_DIR.exists(), "sanity/schemas/documents/ directory not found"
        assert DOCUMENTS_DIR.is_dir(), "sanity/schemas/documents/ should be a directory"

    def test_objects_directory_exists(self):
        """sanity/schemas/objects/ directory should exist."""
        assert OBJECTS_DIR.exists(), "sanity/schemas/objects/ directory not found"
        assert OBJECTS_DIR.is_dir(), "sanity/schemas/objects/ should be a directory"

    def test_schema_index_exists(self):
        """sanity/schemas/index.ts should exist."""
        index_path = SCHEMAS_DIR / "index.ts"
        assert index_path.exists(), "sanity/schemas/index.ts not found"


class TestDocumentTypeSchemas:
    """Test that all 8 required document type schemas exist."""

    def test_blog_post_schema_exists(self):
        """blogPost schema file should exist."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        assert path.exists(), "sanity/schemas/documents/blogPost.ts not found"

    def test_project_schema_exists(self):
        """project schema file should exist."""
        path = DOCUMENTS_DIR / "project.ts"
        assert path.exists(), "sanity/schemas/documents/project.ts not found"

    def test_popup_content_schema_exists(self):
        """popupContent schema file should exist."""
        path = DOCUMENTS_DIR / "popupContent.ts"
        assert path.exists(), "sanity/schemas/documents/popupContent.ts not found"

    def test_homepage_schema_exists(self):
        """homepage (singleton) schema file should exist."""
        path = DOCUMENTS_DIR / "homepage.ts"
        assert path.exists(), "sanity/schemas/documents/homepage.ts not found"

    def test_about_page_schema_exists(self):
        """aboutPage (singleton) schema file should exist."""
        path = DOCUMENTS_DIR / "aboutPage.ts"
        assert path.exists(), "sanity/schemas/documents/aboutPage.ts not found"

    def test_contact_page_schema_exists(self):
        """contactPage (singleton) schema file should exist."""
        path = DOCUMENTS_DIR / "contactPage.ts"
        assert path.exists(), "sanity/schemas/documents/contactPage.ts not found"

    def test_site_settings_schema_exists(self):
        """siteSettings (singleton) schema file should exist."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        assert path.exists(), "sanity/schemas/documents/siteSettings.ts not found"

    def test_navigation_schema_exists(self):
        """navigation (singleton) schema file should exist."""
        path = DOCUMENTS_DIR / "navigation.ts"
        assert path.exists(), "sanity/schemas/documents/navigation.ts not found"


class TestObjectTypeSchemas:
    """Test that required object type schemas exist."""

    def test_portable_text_schema_exists(self):
        """portableText object schema should exist."""
        path = OBJECTS_DIR / "portableText.ts"
        assert path.exists(), "sanity/schemas/objects/portableText.ts not found"

    def test_seo_schema_exists(self):
        """seo object schema should exist."""
        path = OBJECTS_DIR / "seo.ts"
        assert path.exists(), "sanity/schemas/objects/seo.ts not found"

    def test_image_with_popup_schema_exists(self):
        """imageWithPopup object schema should exist."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        assert path.exists(), "sanity/schemas/objects/imageWithPopup.ts not found"

    def test_social_link_schema_exists(self):
        """socialLink object schema should exist."""
        path = OBJECTS_DIR / "socialLink.ts"
        assert path.exists(), "sanity/schemas/objects/socialLink.ts not found"


class TestSchemaIndexExports:
    """Test that schema index properly exports all schemas."""

    def test_schema_index_exports_schema_types(self):
        """Schema index should export schemaTypes array."""
        index_path = SCHEMAS_DIR / "index.ts"
        content = index_path.read_text()
        assert "export const schemaTypes" in content, (
            "Schema index should export schemaTypes"
        )

    def test_schema_index_imports_all_documents(self):
        """Schema index should import all document schemas."""
        index_path = SCHEMAS_DIR / "index.ts"
        content = index_path.read_text()

        document_schemas = [
            "blogPost",
            "project",
            "popupContent",
            "homepage",
            "aboutPage",
            "contactPage",
            "siteSettings",
            "navigation",
        ]

        for schema in document_schemas:
            assert schema in content, (
                f"Schema index should import {schema} document schema"
            )

    def test_schema_index_imports_all_objects(self):
        """Schema index should import all object schemas."""
        index_path = SCHEMAS_DIR / "index.ts"
        content = index_path.read_text()

        object_schemas = ["portableText", "seo", "imageWithPopup", "socialLink"]

        for schema in object_schemas:
            assert schema in content, (
                f"Schema index should import {schema} object schema"
            )

    def test_schema_index_includes_documents_in_export(self):
        """Schema index schemaTypes array should include document schemas."""
        index_path = SCHEMAS_DIR / "index.ts"
        content = index_path.read_text()

        # Find the schemaTypes array content
        assert "blogPost," in content or "blogPost]" in content, (
            "schemaTypes should include blogPost"
        )
        assert "homepage," in content or "homepage]" in content, (
            "schemaTypes should include homepage"
        )
        assert "siteSettings," in content or "siteSettings]" in content, (
            "schemaTypes should include siteSettings"
        )

    def test_schema_index_includes_objects_in_export(self):
        """Schema index schemaTypes array should include object schemas."""
        index_path = SCHEMAS_DIR / "index.ts"
        content = index_path.read_text()

        assert "portableText," in content or "portableText]" in content, (
            "schemaTypes should include portableText"
        )
        assert "seo," in content or "seo]" in content, (
            "schemaTypes should include seo"
        )


class TestBlogPostSchema:
    """Test blogPost document schema structure."""

    def test_blog_post_uses_define_type(self):
        """blogPost should use defineType from sanity."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "defineType" in content, "blogPost should use defineType"

    def test_blog_post_has_name_field(self):
        """blogPost should define name as 'blogPost'."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "name: 'blogPost'" in content or 'name: "blogPost"' in content, (
            "blogPost should have name: 'blogPost'"
        )

    def test_blog_post_is_document_type(self):
        """blogPost should be of type 'document'."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "type: 'document'" in content or 'type: "document"' in content, (
            "blogPost should be of type 'document'"
        )

    def test_blog_post_has_title_field(self):
        """blogPost should have a title field with validation."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "name: 'title'" in content or 'name: "title"' in content, (
            "blogPost should have a title field"
        )

    def test_blog_post_has_slug_field(self):
        """blogPost should have a slug field."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "name: 'slug'" in content or 'name: "slug"' in content, (
            "blogPost should have a slug field"
        )

    def test_blog_post_slug_has_source_title(self):
        """blogPost slug should auto-generate from title."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "source: 'title'" in content or 'source: "title"' in content, (
            "blogPost slug should have source: 'title' for auto-generation"
        )

    def test_blog_post_has_cover_image(self):
        """blogPost should have a coverImage field."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "name: 'coverImage'" in content or 'name: "coverImage"' in content, (
            "blogPost should have a coverImage field"
        )

    def test_blog_post_has_content_field(self):
        """blogPost should have a content field using portableText."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "name: 'content'" in content or 'name: "content"' in content, (
            "blogPost should have a content field"
        )
        assert "type: 'portableText'" in content or 'type: "portableText"' in content, (
            "blogPost content should use portableText type"
        )

    def test_blog_post_has_seo_field(self):
        """blogPost should have an seo field."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "name: 'seo'" in content or 'name: "seo"' in content, (
            "blogPost should have an seo field"
        )
        assert "type: 'seo'" in content or 'type: "seo"' in content, (
            "blogPost seo should use seo object type"
        )

    def test_blog_post_has_published_at_field(self):
        """blogPost should have a publishedAt datetime field."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "name: 'publishedAt'" in content or 'name: "publishedAt"' in content, (
            "blogPost should have a publishedAt field"
        )
        assert "type: 'datetime'" in content or 'type: "datetime"' in content, (
            "blogPost publishedAt should be of type datetime"
        )

    def test_blog_post_has_icon(self):
        """blogPost should have an icon configured."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "icon:" in content, "blogPost should have an icon configured"

    def test_blog_post_exports_schema(self):
        """blogPost should export the schema."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "export const blogPost" in content or "export { blogPost" in content, (
            "blogPost should export the schema"
        )


class TestProjectSchema:
    """Test project document schema structure."""

    def test_project_uses_define_type(self):
        """project should use defineType from sanity."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "defineType" in content, "project should use defineType"

    def test_project_has_name_field(self):
        """project should define name as 'project'."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "name: 'project'" in content or 'name: "project"' in content, (
            "project should have name: 'project'"
        )

    def test_project_is_document_type(self):
        """project should be of type 'document'."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "type: 'document'" in content or 'type: "document"' in content, (
            "project should be of type 'document'"
        )

    def test_project_has_slug_with_auto_generation(self):
        """project should have a slug field with auto-generation from title."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "name: 'slug'" in content or 'name: "slug"' in content, (
            "project should have a slug field"
        )
        assert "source: 'title'" in content or 'source: "title"' in content, (
            "project slug should auto-generate from title"
        )

    def test_project_has_images_gallery(self):
        """project should have an images array for gallery."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "name: 'images'" in content or 'name: "images"' in content, (
            "project should have an images field for gallery"
        )

    def test_project_images_use_image_with_popup(self):
        """project images should use imageWithPopup type."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "imageWithPopup" in content, (
            "project images should use imageWithPopup type for popup feature"
        )

    def test_project_has_category_field(self):
        """project should have a category field with predefined options."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "name: 'category'" in content or 'name: "category"' in content, (
            "project should have a category field"
        )
        # Check for fashion-related categories
        assert "editorial" in content.lower() or "campaign" in content.lower(), (
            "project category should include fashion categories like editorial, campaign"
        )

    def test_project_has_seo_field(self):
        """project should have an seo field."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "name: 'seo'" in content or 'name: "seo"' in content, (
            "project should have an seo field"
        )

    def test_project_exports_schema(self):
        """project should export the schema."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "export const project" in content or "export { project" in content, (
            "project should export the schema"
        )


class TestPopupContentSchema:
    """Test popupContent document schema structure."""

    def test_popup_content_uses_define_type(self):
        """popupContent should use defineType from sanity."""
        path = DOCUMENTS_DIR / "popupContent.ts"
        content = path.read_text()
        assert "defineType" in content, "popupContent should use defineType"

    def test_popup_content_has_name(self):
        """popupContent should define name as 'popupContent'."""
        path = DOCUMENTS_DIR / "popupContent.ts"
        content = path.read_text()
        assert "name: 'popupContent'" in content or 'name: "popupContent"' in content, (
            "popupContent should have name: 'popupContent'"
        )

    def test_popup_content_is_document_type(self):
        """popupContent should be of type 'document'."""
        path = DOCUMENTS_DIR / "popupContent.ts"
        content = path.read_text()
        assert "type: 'document'" in content or 'type: "document"' in content, (
            "popupContent should be of type 'document'"
        )

    def test_popup_content_has_title_field(self):
        """popupContent should have a title field."""
        path = DOCUMENTS_DIR / "popupContent.ts"
        content = path.read_text()
        assert "name: 'title'" in content or 'name: "title"' in content, (
            "popupContent should have a title field"
        )

    def test_popup_content_has_description_field(self):
        """popupContent should have a description field for styling notes."""
        path = DOCUMENTS_DIR / "popupContent.ts"
        content = path.read_text()
        assert "name: 'description'" in content or 'name: "description"' in content, (
            "popupContent should have a description field"
        )

    def test_popup_content_has_link_field(self):
        """popupContent should have a link field for product info."""
        path = DOCUMENTS_DIR / "popupContent.ts"
        content = path.read_text()
        assert "name: 'link'" in content or 'name: "link"' in content, (
            "popupContent should have a link field"
        )

    def test_popup_content_exports_schema(self):
        """popupContent should export the schema."""
        path = DOCUMENTS_DIR / "popupContent.ts"
        content = path.read_text()
        assert "export const popupContent" in content or "export { popupContent" in content, (
            "popupContent should export the schema"
        )


class TestHomepageSchema:
    """Test homepage singleton document schema structure."""

    def test_homepage_uses_define_type(self):
        """homepage should use defineType from sanity."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "defineType" in content, "homepage should use defineType"

    def test_homepage_has_name(self):
        """homepage should define name as 'homepage'."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "name: 'homepage'" in content or 'name: "homepage"' in content, (
            "homepage should have name: 'homepage'"
        )

    def test_homepage_is_document_type(self):
        """homepage should be of type 'document'."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "type: 'document'" in content or 'type: "document"' in content, (
            "homepage should be of type 'document'"
        )

    def test_homepage_has_hero_heading(self):
        """homepage should have heroHeading field."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "heroHeading" in content, (
            "homepage should have heroHeading field"
        )

    def test_homepage_has_hero_image(self):
        """homepage should have heroImage field."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "heroImage" in content, (
            "homepage should have heroImage field"
        )

    def test_homepage_has_intro_text(self):
        """homepage should have introText field using portableText."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "introText" in content, (
            "homepage should have introText field"
        )

    def test_homepage_has_seo_field(self):
        """homepage should have an seo field."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "name: 'seo'" in content or 'name: "seo"' in content, (
            "homepage should have an seo field"
        )

    def test_homepage_has_static_preview(self):
        """homepage singleton should have static preview title."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "preview" in content, (
            "homepage should have preview configuration"
        )

    def test_homepage_exports_schema(self):
        """homepage should export the schema."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "export const homepage" in content or "export { homepage" in content, (
            "homepage should export the schema"
        )


class TestAboutPageSchema:
    """Test aboutPage singleton document schema structure."""

    def test_about_page_uses_define_type(self):
        """aboutPage should use defineType from sanity."""
        path = DOCUMENTS_DIR / "aboutPage.ts"
        content = path.read_text()
        assert "defineType" in content, "aboutPage should use defineType"

    def test_about_page_has_name(self):
        """aboutPage should define name as 'aboutPage'."""
        path = DOCUMENTS_DIR / "aboutPage.ts"
        content = path.read_text()
        assert "name: 'aboutPage'" in content or 'name: "aboutPage"' in content, (
            "aboutPage should have name: 'aboutPage'"
        )

    def test_about_page_is_document_type(self):
        """aboutPage should be of type 'document'."""
        path = DOCUMENTS_DIR / "aboutPage.ts"
        content = path.read_text()
        assert "type: 'document'" in content or 'type: "document"' in content, (
            "aboutPage should be of type 'document'"
        )

    def test_about_page_has_profile_image(self):
        """aboutPage should have profileImage field."""
        path = DOCUMENTS_DIR / "aboutPage.ts"
        content = path.read_text()
        assert "profileImage" in content, (
            "aboutPage should have profileImage field"
        )

    def test_about_page_has_bio_field(self):
        """aboutPage should have bio field using portableText."""
        path = DOCUMENTS_DIR / "aboutPage.ts"
        content = path.read_text()
        assert "name: 'bio'" in content or 'name: "bio"' in content, (
            "aboutPage should have bio field"
        )

    def test_about_page_has_seo_field(self):
        """aboutPage should have an seo field."""
        path = DOCUMENTS_DIR / "aboutPage.ts"
        content = path.read_text()
        assert "name: 'seo'" in content or 'name: "seo"' in content, (
            "aboutPage should have an seo field"
        )

    def test_about_page_exports_schema(self):
        """aboutPage should export the schema."""
        path = DOCUMENTS_DIR / "aboutPage.ts"
        content = path.read_text()
        assert "export const aboutPage" in content or "export { aboutPage" in content, (
            "aboutPage should export the schema"
        )


class TestContactPageSchema:
    """Test contactPage singleton document schema structure."""

    def test_contact_page_uses_define_type(self):
        """contactPage should use defineType from sanity."""
        path = DOCUMENTS_DIR / "contactPage.ts"
        content = path.read_text()
        assert "defineType" in content, "contactPage should use defineType"

    def test_contact_page_has_name(self):
        """contactPage should define name as 'contactPage'."""
        path = DOCUMENTS_DIR / "contactPage.ts"
        content = path.read_text()
        assert "name: 'contactPage'" in content or 'name: "contactPage"' in content, (
            "contactPage should have name: 'contactPage'"
        )

    def test_contact_page_is_document_type(self):
        """contactPage should be of type 'document'."""
        path = DOCUMENTS_DIR / "contactPage.ts"
        content = path.read_text()
        assert "type: 'document'" in content or 'type: "document"' in content, (
            "contactPage should be of type 'document'"
        )

    def test_contact_page_has_email_field(self):
        """contactPage should have email field."""
        path = DOCUMENTS_DIR / "contactPage.ts"
        content = path.read_text()
        assert "name: 'email'" in content or 'name: "email"' in content, (
            "contactPage should have email field"
        )

    def test_contact_page_has_social_links(self):
        """contactPage should have socialLinks field."""
        path = DOCUMENTS_DIR / "contactPage.ts"
        content = path.read_text()
        assert "socialLinks" in content, (
            "contactPage should have socialLinks field"
        )

    def test_contact_page_has_seo_field(self):
        """contactPage should have an seo field."""
        path = DOCUMENTS_DIR / "contactPage.ts"
        content = path.read_text()
        assert "name: 'seo'" in content or 'name: "seo"' in content, (
            "contactPage should have an seo field"
        )

    def test_contact_page_exports_schema(self):
        """contactPage should export the schema."""
        path = DOCUMENTS_DIR / "contactPage.ts"
        content = path.read_text()
        assert "export const contactPage" in content or "export { contactPage" in content, (
            "contactPage should export the schema"
        )


class TestSiteSettingsSchema:
    """Test siteSettings singleton document schema structure."""

    def test_site_settings_uses_define_type(self):
        """siteSettings should use defineType from sanity."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "defineType" in content, "siteSettings should use defineType"

    def test_site_settings_has_name(self):
        """siteSettings should define name as 'siteSettings'."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "name: 'siteSettings'" in content or 'name: "siteSettings"' in content, (
            "siteSettings should have name: 'siteSettings'"
        )

    def test_site_settings_is_document_type(self):
        """siteSettings should be of type 'document'."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "type: 'document'" in content or 'type: "document"' in content, (
            "siteSettings should be of type 'document'"
        )

    def test_site_settings_has_site_name(self):
        """siteSettings should have siteName field."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "siteName" in content, (
            "siteSettings should have siteName field"
        )

    def test_site_settings_has_logo(self):
        """siteSettings should have logo field."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "name: 'logo'" in content or 'name: "logo"' in content, (
            "siteSettings should have logo field"
        )

    def test_site_settings_has_default_seo(self):
        """siteSettings should have defaultSeo field for fallback SEO."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "defaultSeo" in content, (
            "siteSettings should have defaultSeo field"
        )

    def test_site_settings_has_social_links(self):
        """siteSettings should have socialLinks field."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "socialLinks" in content, (
            "siteSettings should have socialLinks field"
        )

    def test_site_settings_exports_schema(self):
        """siteSettings should export the schema."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "export const siteSettings" in content or "export { siteSettings" in content, (
            "siteSettings should export the schema"
        )


class TestNavigationSchema:
    """Test navigation singleton document schema structure."""

    def test_navigation_uses_define_type(self):
        """navigation should use defineType from sanity."""
        path = DOCUMENTS_DIR / "navigation.ts"
        content = path.read_text()
        assert "defineType" in content, "navigation should use defineType"

    def test_navigation_has_name(self):
        """navigation should define name as 'navigation'."""
        path = DOCUMENTS_DIR / "navigation.ts"
        content = path.read_text()
        assert "name: 'navigation'" in content or 'name: "navigation"' in content, (
            "navigation should have name: 'navigation'"
        )

    def test_navigation_is_document_type(self):
        """navigation should be of type 'document'."""
        path = DOCUMENTS_DIR / "navigation.ts"
        content = path.read_text()
        assert "type: 'document'" in content or 'type: "document"' in content, (
            "navigation should be of type 'document'"
        )

    def test_navigation_has_main_menu(self):
        """navigation should have mainMenu array field."""
        path = DOCUMENTS_DIR / "navigation.ts"
        content = path.read_text()
        assert "mainMenu" in content, (
            "navigation should have mainMenu field"
        )

    def test_navigation_menu_has_label_field(self):
        """navigation menu items should have label field."""
        path = DOCUMENTS_DIR / "navigation.ts"
        content = path.read_text()
        assert "name: 'label'" in content or 'name: "label"' in content, (
            "navigation menu items should have label field"
        )

    def test_navigation_menu_has_link_field(self):
        """navigation menu items should have link field."""
        path = DOCUMENTS_DIR / "navigation.ts"
        content = path.read_text()
        assert "name: 'link'" in content or 'name: "link"' in content, (
            "navigation menu items should have link field"
        )

    def test_navigation_exports_schema(self):
        """navigation should export the schema."""
        path = DOCUMENTS_DIR / "navigation.ts"
        content = path.read_text()
        assert "export const navigation" in content or "export { navigation" in content, (
            "navigation should export the schema"
        )


class TestPortableTextConfiguration:
    """Test Portable Text configuration for rich content."""

    def test_portable_text_uses_define_type(self):
        """portableText should use defineType from sanity."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "defineType" in content, "portableText should use defineType"

    def test_portable_text_has_name(self):
        """portableText should define name as 'portableText'."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "name: 'portableText'" in content or 'name: "portableText"' in content, (
            "portableText should have name: 'portableText'"
        )

    def test_portable_text_is_array_type(self):
        """portableText should be of type 'array'."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "type: 'array'" in content or 'type: "array"' in content, (
            "portableText should be of type 'array'"
        )

    def test_portable_text_has_block_type(self):
        """portableText should include block type."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "type: 'block'" in content or 'type: "block"' in content, (
            "portableText should include block type"
        )

    def test_portable_text_has_heading_styles(self):
        """portableText should have heading styles (h2, h3, etc.)."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "'h2'" in content or '"h2"' in content, (
            "portableText should support h2 heading style"
        )
        assert "'h3'" in content or '"h3"' in content, (
            "portableText should support h3 heading style"
        )

    def test_portable_text_has_list_types(self):
        """portableText should have list types (bullet, number)."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "'bullet'" in content or '"bullet"' in content, (
            "portableText should support bullet list"
        )

    def test_portable_text_has_decorators(self):
        """portableText should have text decorators (strong, em)."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "'strong'" in content or '"strong"' in content, (
            "portableText should support strong decorator"
        )
        assert "'em'" in content or '"em"' in content, (
            "portableText should support emphasis decorator"
        )

    def test_portable_text_has_link_annotation(self):
        """portableText should have link annotation for external links."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "'link'" in content or '"link"' in content, (
            "portableText should support link annotation"
        )

    def test_portable_text_has_internal_link_annotation(self):
        """portableText should have internal link annotation."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "internalLink" in content, (
            "portableText should support internalLink annotation"
        )

    def test_portable_text_supports_embedded_images(self):
        """portableText should support embedded images with popup."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "imageWithPopup" in content, (
            "portableText should support embedded imageWithPopup"
        )

    def test_portable_text_exports_schema(self):
        """portableText should export the schema."""
        path = OBJECTS_DIR / "portableText.ts"
        content = path.read_text()
        assert "export const portableText" in content or "export { portableText" in content, (
            "portableText should export the schema"
        )


class TestSEOMetadataObject:
    """Test SEO metadata object schema."""

    def test_seo_uses_define_type(self):
        """seo should use defineType from sanity."""
        path = OBJECTS_DIR / "seo.ts"
        content = path.read_text()
        assert "defineType" in content, "seo should use defineType"

    def test_seo_has_name(self):
        """seo should define name as 'seo'."""
        path = OBJECTS_DIR / "seo.ts"
        content = path.read_text()
        assert "name: 'seo'" in content or 'name: "seo"' in content, (
            "seo should have name: 'seo'"
        )

    def test_seo_is_object_type(self):
        """seo should be of type 'object'."""
        path = OBJECTS_DIR / "seo.ts"
        content = path.read_text()
        assert "type: 'object'" in content or 'type: "object"' in content, (
            "seo should be of type 'object'"
        )

    def test_seo_has_meta_title(self):
        """seo should have metaTitle field."""
        path = OBJECTS_DIR / "seo.ts"
        content = path.read_text()
        assert "metaTitle" in content, (
            "seo should have metaTitle field"
        )

    def test_seo_meta_title_has_max_validation(self):
        """seo metaTitle should have max length validation (around 60 chars)."""
        path = OBJECTS_DIR / "seo.ts"
        content = path.read_text()
        # Check for max validation - usually max(60) for SEO titles
        assert "max(60)" in content or "max(70)" in content, (
            "seo metaTitle should have max length validation"
        )

    def test_seo_has_meta_description(self):
        """seo should have metaDescription field."""
        path = OBJECTS_DIR / "seo.ts"
        content = path.read_text()
        assert "metaDescription" in content, (
            "seo should have metaDescription field"
        )

    def test_seo_meta_description_has_max_validation(self):
        """seo metaDescription should have max length validation (around 160 chars)."""
        path = OBJECTS_DIR / "seo.ts"
        content = path.read_text()
        # Check for max validation - usually max(160) for SEO descriptions
        assert "max(160)" in content or "max(155)" in content, (
            "seo metaDescription should have max length validation"
        )

    def test_seo_has_og_image(self):
        """seo should have ogImage field for social sharing."""
        path = OBJECTS_DIR / "seo.ts"
        content = path.read_text()
        assert "ogImage" in content, (
            "seo should have ogImage field for social sharing"
        )

    def test_seo_exports_schema(self):
        """seo should export the schema."""
        path = OBJECTS_DIR / "seo.ts"
        content = path.read_text()
        assert "export const seo" in content or "export { seo" in content, (
            "seo should export the schema"
        )


class TestImageWithPopupObject:
    """Test imageWithPopup object schema."""

    def test_image_with_popup_uses_define_type(self):
        """imageWithPopup should use defineType from sanity."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        assert "defineType" in content, "imageWithPopup should use defineType"

    def test_image_with_popup_has_name(self):
        """imageWithPopup should define name as 'imageWithPopup'."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        assert "name: 'imageWithPopup'" in content or 'name: "imageWithPopup"' in content, (
            "imageWithPopup should have name: 'imageWithPopup'"
        )

    def test_image_with_popup_is_object_type(self):
        """imageWithPopup should be of type 'object'."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        assert "type: 'object'" in content or 'type: "object"' in content, (
            "imageWithPopup should be of type 'object'"
        )

    def test_image_with_popup_has_image_field(self):
        """imageWithPopup should have image field."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        assert "name: 'image'" in content or 'name: "image"' in content, (
            "imageWithPopup should have image field"
        )

    def test_image_with_popup_has_alt_field(self):
        """imageWithPopup should have alt text field."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        assert "name: 'alt'" in content or 'name: "alt"' in content, (
            "imageWithPopup should have alt text field"
        )

    def test_image_with_popup_alt_is_required(self):
        """imageWithPopup alt text should be required for accessibility."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        # Check that alt field has required validation
        assert "Rule.required()" in content or "required()" in content, (
            "imageWithPopup alt text should have required validation"
        )

    def test_image_with_popup_has_popup_reference(self):
        """imageWithPopup should have popup reference field."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        assert "name: 'popup'" in content or 'name: "popup"' in content, (
            "imageWithPopup should have popup field"
        )
        assert "type: 'reference'" in content or 'type: "reference"' in content, (
            "imageWithPopup popup should be a reference type"
        )

    def test_image_with_popup_references_popup_content(self):
        """imageWithPopup popup should reference popupContent document."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        assert "popupContent" in content, (
            "imageWithPopup popup should reference popupContent"
        )

    def test_image_with_popup_has_hotspot(self):
        """imageWithPopup image should have hotspot enabled for cropping."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        assert "hotspot: true" in content or "hotspot:true" in content, (
            "imageWithPopup image should have hotspot enabled"
        )

    def test_image_with_popup_exports_schema(self):
        """imageWithPopup should export the schema."""
        path = OBJECTS_DIR / "imageWithPopup.ts"
        content = path.read_text()
        assert "export const imageWithPopup" in content or "export { imageWithPopup" in content, (
            "imageWithPopup should export the schema"
        )


class TestSocialLinkObject:
    """Test socialLink object schema."""

    def test_social_link_uses_define_type(self):
        """socialLink should use defineType from sanity."""
        path = OBJECTS_DIR / "socialLink.ts"
        content = path.read_text()
        assert "defineType" in content, "socialLink should use defineType"

    def test_social_link_has_name(self):
        """socialLink should define name as 'socialLink'."""
        path = OBJECTS_DIR / "socialLink.ts"
        content = path.read_text()
        assert "name: 'socialLink'" in content or 'name: "socialLink"' in content, (
            "socialLink should have name: 'socialLink'"
        )

    def test_social_link_is_object_type(self):
        """socialLink should be of type 'object'."""
        path = OBJECTS_DIR / "socialLink.ts"
        content = path.read_text()
        assert "type: 'object'" in content or 'type: "object"' in content, (
            "socialLink should be of type 'object'"
        )

    def test_social_link_has_platform_field(self):
        """socialLink should have platform field."""
        path = OBJECTS_DIR / "socialLink.ts"
        content = path.read_text()
        assert "name: 'platform'" in content or 'name: "platform"' in content, (
            "socialLink should have platform field"
        )

    def test_social_link_has_url_field(self):
        """socialLink should have url field."""
        path = OBJECTS_DIR / "socialLink.ts"
        content = path.read_text()
        assert "name: 'url'" in content or 'name: "url"' in content, (
            "socialLink should have url field"
        )

    def test_social_link_has_platform_options(self):
        """socialLink platform should have predefined social media options."""
        path = OBJECTS_DIR / "socialLink.ts"
        content = path.read_text()
        assert "instagram" in content.lower(), (
            "socialLink should include Instagram option"
        )

    def test_social_link_exports_schema(self):
        """socialLink should export the schema."""
        path = OBJECTS_DIR / "socialLink.ts"
        content = path.read_text()
        assert "export const socialLink" in content or "export { socialLink" in content, (
            "socialLink should export the schema"
        )


class TestImageAltTextRequirements:
    """Test that image fields include alt text requirements."""

    def test_blog_post_cover_image_has_alt(self):
        """blogPost coverImage should have nested alt text field."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        # Check that coverImage has alt field
        assert "coverImage" in content and "alt" in content, (
            "blogPost coverImage should have alt text field"
        )

    def test_project_cover_image_has_alt(self):
        """project coverImage should have nested alt text field."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "coverImage" in content and "alt" in content, (
            "project coverImage should have alt text field"
        )

    def test_homepage_hero_image_has_alt(self):
        """homepage heroImage should have nested alt text field."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "heroImage" in content and "alt" in content, (
            "homepage heroImage should have alt text field"
        )

    def test_about_page_profile_image_has_alt(self):
        """aboutPage profileImage should have nested alt text field."""
        path = DOCUMENTS_DIR / "aboutPage.ts"
        content = path.read_text()
        assert "profileImage" in content and "alt" in content, (
            "aboutPage profileImage should have alt text field"
        )


class TestSlugAutoGeneration:
    """Test that slug fields have auto-generation enabled."""

    def test_blog_post_slug_has_source(self):
        """blogPost slug should have source option for auto-generation."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        # Check for source option in slug field
        assert "source:" in content and "slug" in content, (
            "blogPost slug should have source option"
        )

    def test_project_slug_has_source(self):
        """project slug should have source option for auto-generation."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "source:" in content and "slug" in content, (
            "project slug should have source option"
        )

    def test_blog_post_slug_has_max_length(self):
        """blogPost slug should have maxLength option."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "maxLength:" in content or "maxLength :" in content, (
            "blogPost slug should have maxLength option"
        )

    def test_project_slug_has_max_length(self):
        """project slug should have maxLength option."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "maxLength:" in content or "maxLength :" in content, (
            "project slug should have maxLength option"
        )


class TestValidationRules:
    """Test that schemas have proper validation rules."""

    def test_blog_post_title_is_required(self):
        """blogPost title should have required validation."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        # Title field should have required validation
        assert "Rule.required()" in content or "required()" in content, (
            "blogPost should have required validation on title"
        )

    def test_blog_post_slug_is_required(self):
        """blogPost slug should have required validation."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        # Should have multiple required validations (title, slug)
        assert content.count("required()") >= 2 or content.count("Rule.required()") >= 2, (
            "blogPost should have required validation on slug"
        )

    def test_project_title_is_required(self):
        """project title should have required validation."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "required()" in content, (
            "project should have required validation on title"
        )

    def test_site_settings_site_name_is_required(self):
        """siteSettings siteName should have required validation."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "required()" in content, (
            "siteSettings should have required validation on siteName"
        )

    def test_popup_content_title_is_required(self):
        """popupContent title should have required validation."""
        path = DOCUMENTS_DIR / "popupContent.ts"
        content = path.read_text()
        assert "required()" in content, (
            "popupContent should have required validation on title"
        )

    def test_social_link_fields_are_required(self):
        """socialLink platform and url should have required validation."""
        path = OBJECTS_DIR / "socialLink.ts"
        content = path.read_text()
        # Should have required on both platform and url
        assert content.count("required()") >= 2 or content.count("Rule.required()") >= 2, (
            "socialLink should have required validation on platform and url"
        )


class TestSchemaIcons:
    """Test that document schemas have icons configured for Sanity Studio sidebar."""

    def test_blog_post_has_icon(self):
        """blogPost should have an icon for Studio sidebar."""
        path = DOCUMENTS_DIR / "blogPost.ts"
        content = path.read_text()
        assert "icon:" in content or "icon :" in content, (
            "blogPost should have an icon configured"
        )

    def test_project_has_icon(self):
        """project should have an icon for Studio sidebar."""
        path = DOCUMENTS_DIR / "project.ts"
        content = path.read_text()
        assert "icon:" in content or "icon :" in content, (
            "project should have an icon configured"
        )

    def test_homepage_has_icon(self):
        """homepage should have an icon for Studio sidebar."""
        path = DOCUMENTS_DIR / "homepage.ts"
        content = path.read_text()
        assert "icon:" in content or "icon :" in content, (
            "homepage should have an icon configured"
        )

    def test_site_settings_has_icon(self):
        """siteSettings should have an icon for Studio sidebar."""
        path = DOCUMENTS_DIR / "siteSettings.ts"
        content = path.read_text()
        assert "icon:" in content or "icon :" in content, (
            "siteSettings should have an icon configured"
        )

    def test_navigation_has_icon(self):
        """navigation should have an icon for Studio sidebar."""
        path = DOCUMENTS_DIR / "navigation.ts"
        content = path.read_text()
        assert "icon:" in content or "icon :" in content, (
            "navigation should have an icon configured"
        )
