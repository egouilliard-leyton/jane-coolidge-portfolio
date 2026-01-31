"""
Tests for T-018: Contact page implementation

These tests verify that the Contact page is properly implemented according to requirements:
- Contact page fetches singleton document from Sanity
- Introduction text renders
- Email is clickable with mailto: link
- Phone number is clickable (if provided)
- Location displays correctly
- Social media links have proper icons and open in new tabs
- Layout is centered and visually clean
- All content editable via CMS

Acceptance Criteria:
- Contact page fetches singleton document from Sanity
- Introduction text renders as rich text
- Email is clickable with mailto: link
- Phone number is clickable (if provided)
- Location displays correctly
- Social media links have proper icons and open in new tabs
- Layout is centered and visually clean
- All content editable via CMS
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONTACT_PAGE_FILE = PROJECT_ROOT / "app" / "(site)" / "contact" / "page.tsx"
QUERIES_FILE = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
TYPES_FILE = PROJECT_ROOT / "types" / "sanity.ts"


class TestContactPageFileExists:
    """Test that contact page file exists and has proper structure."""

    def test_contact_page_file_exists(self):
        """app/(site)/contact/page.tsx should exist."""
        assert CONTACT_PAGE_FILE.exists(), "app/(site)/contact/page.tsx not found"

    def test_contact_page_is_server_component(self):
        """Contact page should be an async Server Component."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "async function ContactPage" in content or "export default async function ContactPage" in content, (
            "Contact page should be an async function (Server Component)"
        )

    def test_contact_page_no_use_client_directive(self):
        """Contact page should NOT have 'use client' directive (Server Component)."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "'use client'" not in content and '"use client"' not in content, (
            "Contact page should be a Server Component without 'use client' directive"
        )

    def test_contact_page_exports_default(self):
        """Contact page should have a default export."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "export default" in content, (
            "Contact page should have a default export"
        )


class TestContactPageSingletonFetch:
    """Test that contact page fetches singleton document from Sanity."""

    def test_contact_page_imports_sanity_fetch(self):
        """Contact page should import sanityFetch from Sanity client."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "sanityFetch" in content, "Contact page should import sanityFetch"
        assert "@/sanity/lib/client" in content, (
            "Contact page should import from @/sanity/lib/client"
        )

    def test_contact_page_imports_contact_page_query(self):
        """Contact page should import contactPageQuery."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "contactPageQuery" in content, "Contact page should import contactPageQuery"

    def test_contact_page_imports_contact_page_result_type(self):
        """Contact page should import ContactPageResult type."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "ContactPageResult" in content, (
            "Contact page should import ContactPageResult type"
        )

    def test_contact_page_fetches_with_tags(self):
        """Contact page should use cache tags for revalidation."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "tags:" in content and "contactPage" in content, (
            "Contact page should use 'contactPage' tag for cache revalidation"
        )

    def test_contact_page_query_is_singleton(self):
        """contactPageQuery should fetch singleton document (index [0])."""
        content = QUERIES_FILE.read_text()
        assert '*[_type == "contactPage"][0]' in content, (
            "contactPageQuery should fetch singleton document with [0]"
        )


class TestContactPageQueryStructure:
    """Test that contactPageQuery is properly defined in queries.ts."""

    def test_queries_file_exists(self):
        """sanity/lib/queries.ts should exist."""
        assert QUERIES_FILE.exists(), "sanity/lib/queries.ts not found"

    def test_contact_page_query_exported(self):
        """contactPageQuery should be exported."""
        content = QUERIES_FILE.read_text()
        assert "export const contactPageQuery" in content, (
            "contactPageQuery should be exported from queries.ts"
        )

    def test_contact_page_query_includes_id(self):
        """contactPageQuery should include _id field."""
        content = QUERIES_FILE.read_text()
        assert "_id" in content, "contactPageQuery should include _id field"

    def test_contact_page_query_includes_heading(self):
        """contactPageQuery should include heading field."""
        content = QUERIES_FILE.read_text()
        assert "heading" in content, "contactPageQuery should include heading field"

    def test_contact_page_query_includes_intro_text(self):
        """contactPageQuery should include introText field."""
        content = QUERIES_FILE.read_text()
        assert "introText" in content, (
            "contactPageQuery should include introText field"
        )

    def test_contact_page_query_includes_email(self):
        """contactPageQuery should include email field."""
        content = QUERIES_FILE.read_text()
        assert "email" in content, "contactPageQuery should include email field"

    def test_contact_page_query_includes_phone(self):
        """contactPageQuery should include phone field."""
        content = QUERIES_FILE.read_text()
        assert "phone" in content, "contactPageQuery should include phone field"

    def test_contact_page_query_includes_location(self):
        """contactPageQuery should include location field."""
        content = QUERIES_FILE.read_text()
        assert "location" in content, "contactPageQuery should include location field"

    def test_contact_page_query_includes_social_links(self):
        """contactPageQuery should include socialLinks field."""
        content = QUERIES_FILE.read_text()
        assert "socialLinks" in content, (
            "contactPageQuery should include socialLinks field"
        )

    def test_contact_page_query_includes_seo(self):
        """contactPageQuery should include seo field."""
        content = QUERIES_FILE.read_text()
        assert "seo" in content, "contactPageQuery should include seo field"


class TestContactPageResultType:
    """Test that ContactPageResult type is properly defined."""

    def test_contact_page_result_type_exported(self):
        """ContactPageResult type should be exported from queries.ts."""
        content = QUERIES_FILE.read_text()
        assert "export interface ContactPageResult" in content, (
            "ContactPageResult should be exported from queries.ts"
        )

    def test_contact_page_result_has_id(self):
        """ContactPageResult should have _id field."""
        content = QUERIES_FILE.read_text()
        assert "_id: string" in content, "ContactPageResult should have _id: string"

    def test_contact_page_result_has_optional_fields(self):
        """ContactPageResult should have optional fields marked with ?."""
        content = QUERIES_FILE.read_text()
        # Most fields in ContactPageResult should be optional
        assert "email?" in content or "email?: string" in content, (
            "ContactPageResult should have optional email field"
        )


class TestIntroductionTextDisplay:
    """Test that introduction text renders correctly."""

    def test_intro_text_accesses_page_intro(self):
        """Contact page should access page.introText."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.introText" in content or "page?.introText" in content, (
            "Contact page should access page.introText"
        )

    def test_intro_text_displays_in_paragraph(self):
        """Introduction text should be displayed in a paragraph or text element."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "<p" in content, "Introduction text should be displayed in paragraph"

    def test_intro_text_conditionally_renders(self):
        """Introduction text should only render when data exists."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page?.introText" in content or "page.introText &&" in content, (
            "Introduction text should conditionally render"
        )


class TestEmailClickable:
    """Test that email is clickable with mailto: link."""

    def test_email_uses_mailto_link(self):
        """Email should use mailto: protocol."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "mailto:" in content, "Email should use mailto: protocol"

    def test_email_is_anchor_element(self):
        """Email should be rendered as anchor element."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "<a" in content and "mailto:" in content, (
            "Email should be rendered as clickable anchor with mailto:"
        )

    def test_email_accesses_page_email(self):
        """Email link should use page.email."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.email" in content or "page?.email" in content, (
            "Email link should use page.email"
        )

    def test_email_displays_address(self):
        """Email address should be displayed as text."""
        content = CONTACT_PAGE_FILE.read_text()
        # Check that email is displayed (not just in href)
        assert "{page.email}" in content or "{page?.email}" in content, (
            "Email address should be displayed as visible text"
        )

    def test_email_conditionally_renders(self):
        """Email section should only render when email exists."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page?.email" in content or "page.email &&" in content, (
            "Email should conditionally render when data exists"
        )


class TestPhoneClickable:
    """Test that phone number is clickable (if provided)."""

    def test_phone_uses_tel_link(self):
        """Phone should use tel: protocol."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "tel:" in content, "Phone should use tel: protocol"

    def test_phone_is_anchor_element(self):
        """Phone should be rendered as anchor element."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "<a" in content and "tel:" in content, (
            "Phone should be rendered as clickable anchor with tel:"
        )

    def test_phone_accesses_page_phone(self):
        """Phone link should use page.phone."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.phone" in content or "page?.phone" in content, (
            "Phone link should use page.phone"
        )

    def test_phone_conditionally_renders(self):
        """Phone section should only render when phone exists."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page?.phone" in content or "page.phone &&" in content, (
            "Phone should conditionally render when data exists"
        )

    def test_phone_strips_spaces_for_tel_link(self):
        """Phone tel: link should strip spaces."""
        content = CONTACT_PAGE_FILE.read_text()
        # Check for space removal in tel link
        assert "replace(" in content and "tel:" in content, (
            "Phone tel: link should strip spaces from number"
        )


class TestLocationDisplay:
    """Test that location displays correctly."""

    def test_location_accesses_page_location(self):
        """Contact page should access page.location."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.location" in content or "page?.location" in content, (
            "Contact page should access page.location"
        )

    def test_location_displays_as_text(self):
        """Location should be displayed as text (not a link)."""
        content = CONTACT_PAGE_FILE.read_text()
        # Location is rendered in a span, not as a link
        assert "{page.location}" in content or "{page?.location}" in content, (
            "Location should be displayed as text"
        )

    def test_location_conditionally_renders(self):
        """Location should only render when data exists."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page?.location" in content or "page.location &&" in content, (
            "Location should conditionally render when data exists"
        )

    def test_location_has_icon(self):
        """Location should have a location/pin icon."""
        content = CONTACT_PAGE_FILE.read_text()
        # Check for SVG with location-related path
        assert "svg" in content.lower() and "location" in content.lower(), (
            "Location should have an icon"
        )


class TestSocialMediaLinks:
    """Test that social media links have proper icons and open in new tabs."""

    def test_social_links_iterate_with_map(self):
        """Social links should iterate using map."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "socialLinks.map" in content or "socialLinks?.map" in content, (
            "Social links should iterate using map"
        )

    def test_social_links_have_href(self):
        """Social links should have href attribute."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "href={social.url}" in content or 'href={social.url}' in content, (
            "Social links should use social.url for href"
        )

    def test_social_links_open_in_new_tab(self):
        """Social links should open in new tab."""
        content = CONTACT_PAGE_FILE.read_text()
        assert 'target="_blank"' in content, (
            "Social links should open in new tab"
        )

    def test_social_links_have_noopener_noreferrer(self):
        """Social links should have rel='noopener noreferrer' for security."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "noopener" in content and "noreferrer" in content, (
            "Social links should have rel='noopener noreferrer'"
        )

    def test_social_links_have_aria_label(self):
        """Social links should have aria-label for accessibility."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "aria-label" in content, (
            "Social links should have aria-label"
        )

    def test_social_links_have_icons(self):
        """Social links should have platform-specific icons."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "socialIcons" in content or "<svg" in content, (
            "Social links should have icons"
        )

    def test_social_links_use_platform_key(self):
        """Social links should use platform to select icon."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "social.platform" in content, (
            "Social links should use social.platform"
        )

    def test_social_links_conditionally_render(self):
        """Social links section should only render when data exists."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "socialLinks && page.socialLinks.length" in content or "page?.socialLinks && page.socialLinks.length" in content, (
            "Social links should conditionally render when data exists"
        )

    def test_social_links_have_key(self):
        """Social links items should have unique key."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "key=" in content, "Social links items should have unique key"


class TestSocialIconsMapping:
    """Test that social icons are properly mapped."""

    def test_social_icons_object_exists(self):
        """socialIcons mapping object should exist."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "socialIcons" in content, "socialIcons mapping should exist"

    def test_social_icons_includes_instagram(self):
        """socialIcons should include instagram."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "instagram:" in content or "instagram" in content.lower(), (
            "socialIcons should include instagram"
        )

    def test_social_icons_includes_twitter(self):
        """socialIcons should include twitter."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "twitter:" in content or "twitter" in content.lower(), (
            "socialIcons should include twitter"
        )

    def test_social_icons_includes_linkedin(self):
        """socialIcons should include linkedin."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "linkedin:" in content or "linkedin" in content.lower(), (
            "socialIcons should include linkedin"
        )

    def test_social_icons_includes_tiktok(self):
        """socialIcons should include tiktok."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "tiktok:" in content or "tiktok" in content.lower(), (
            "socialIcons should include tiktok"
        )

    def test_platform_label_function_exists(self):
        """getPlatformLabel function should exist."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "getPlatformLabel" in content, (
            "getPlatformLabel function should exist"
        )


class TestCenteredLayout:
    """Test that layout is centered and visually clean."""

    def test_uses_mx_auto_for_centering(self):
        """Layout should use mx-auto for horizontal centering."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "mx-auto" in content, "Layout should use mx-auto for centering"

    def test_uses_max_width_constraint(self):
        """Layout should use max-width constraint."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "max-w-" in content, "Layout should use max-width constraint"

    def test_uses_text_center_for_content(self):
        """Content should use text-center for alignment."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "text-center" in content, "Content should use text-center"

    def test_uses_flex_for_layout(self):
        """Layout should use flexbox."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "flex" in content, "Layout should use flexbox"

    def test_has_appropriate_padding(self):
        """Layout should have appropriate padding."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "py-" in content and "px-" in content, (
            "Layout should have padding"
        )


class TestSEOMetadata:
    """Test that SEO metadata is properly configured."""

    def test_exports_generate_metadata(self):
        """Contact page should export generateMetadata function."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "generateMetadata" in content, (
            "Contact page should export generateMetadata"
        )

    def test_generate_metadata_is_async(self):
        """generateMetadata should be async function."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "async function generateMetadata" in content or "export async function generateMetadata" in content, (
            "generateMetadata should be async"
        )

    def test_metadata_fetches_page_data(self):
        """generateMetadata should fetch page data."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "sanityFetch" in content and "contactPageQuery" in content, (
            "generateMetadata should fetch page data"
        )

    def test_metadata_returns_metadata_type(self):
        """generateMetadata should return Metadata type."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "Metadata" in content, (
            "generateMetadata should return Metadata type"
        )

    def test_metadata_includes_title(self):
        """Metadata should include title."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "title:" in content, "Metadata should include title"

    def test_metadata_includes_description(self):
        """Metadata should include description."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "description:" in content, "Metadata should include description"

    def test_metadata_includes_open_graph(self):
        """Metadata should include Open Graph config."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "openGraph" in content, (
            "Metadata should include Open Graph configuration"
        )

    def test_metadata_uses_seo_fields(self):
        """Metadata should use SEO fields from CMS."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "seo?.metaTitle" in content or "seo.metaTitle" in content, (
            "Metadata should use SEO metaTitle from CMS"
        )

    def test_metadata_has_fallbacks(self):
        """Metadata should have fallback values."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "||" in content or "??" in content, (
            "Metadata should have fallback values"
        )


class TestSemanticHTML:
    """Test that contact page uses proper semantic HTML."""

    def test_uses_article_wrapper(self):
        """Contact page should use article element as wrapper."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "<article" in content, "Contact page should use article element"

    def test_uses_section_elements(self):
        """Contact page should use section elements for content areas."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "<section" in content, "Contact page should use section elements"

    def test_uses_header_element(self):
        """Contact page should use header element for header content."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "<header" in content, (
            "Contact page should use header element"
        )

    def test_uses_h1_heading(self):
        """Contact page should have h1 heading."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "<h1" in content, "Contact page should have h1 heading"

    def test_sections_have_aria_labels(self):
        """Sections should have aria-label or aria-labelledby."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "aria-label" in content, (
            "Sections should have aria-label for accessibility"
        )

    def test_decorative_elements_hidden(self):
        """Decorative elements should be hidden from accessibility."""
        content = CONTACT_PAGE_FILE.read_text()
        assert 'aria-hidden="true"' in content, (
            "Decorative elements should have aria-hidden"
        )


class TestTailwindStyling:
    """Test that contact page uses Tailwind CSS properly."""

    def test_uses_tailwind_layout_classes(self):
        """Contact page should use Tailwind layout classes."""
        content = CONTACT_PAGE_FILE.read_text()
        tailwind_indicators = ["flex", "grid", "items-", "justify-", "mx-auto", "max-w-"]
        found = [cls for cls in tailwind_indicators if cls in content]
        assert len(found) >= 3, f"Contact page should use Tailwind layout classes, found: {found}"

    def test_uses_tailwind_spacing_classes(self):
        """Contact page should use Tailwind spacing classes."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "px-" in content and "py-" in content, (
            "Contact page should use Tailwind padding classes"
        )

    def test_uses_responsive_classes(self):
        """Contact page should use responsive Tailwind classes."""
        content = CONTACT_PAGE_FILE.read_text()
        responsive_prefixes = ["sm:", "md:", "lg:", "xl:"]
        found = [prefix for prefix in responsive_prefixes if prefix in content]
        assert len(found) >= 2, (
            "Contact page should use responsive Tailwind classes"
        )

    def test_uses_dark_mode_classes(self):
        """Contact page should support dark mode."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "dark:" in content, "Contact page should have dark mode support"

    def test_uses_brand_colors(self):
        """Contact page should use brand color classes."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "brand-" in content, "Contact page should use brand color utilities"


class TestAnimations:
    """Test that contact page has appropriate animations."""

    def test_uses_animation_classes(self):
        """Contact page should use animation classes."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "animate-" in content, "Contact page should use animation classes"

    def test_uses_transitions(self):
        """Contact page should use transition effects."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "transition" in content, (
            "Contact page should use transition effects"
        )


class TestHoverEffects:
    """Test that contact page elements have hover effects."""

    def test_has_hover_effects(self):
        """Contact page should have hover effects."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "hover:" in content, "Contact page should have hover effects"

    def test_has_group_hover(self):
        """Contact page should use group hover for coordinated effects."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "group" in content and "group-hover:" in content, (
            "Contact page should use group hover for coordinated effects"
        )


class TestContactPageTypes:
    """Test that ContactPage type is properly defined in types/sanity.ts."""

    def test_types_file_exists(self):
        """types/sanity.ts should exist."""
        assert TYPES_FILE.exists(), "types/sanity.ts not found"

    def test_contact_page_type_exported(self):
        """ContactPage type should be exported."""
        content = TYPES_FILE.read_text()
        assert "export interface ContactPage" in content, (
            "ContactPage type should be exported"
        )

    def test_social_platform_type_exported(self):
        """SocialPlatform type should be exported."""
        content = TYPES_FILE.read_text()
        assert "export type SocialPlatform" in content, (
            "SocialPlatform type should be exported"
        )

    def test_social_link_type_exported(self):
        """SocialLink type should be exported."""
        content = TYPES_FILE.read_text()
        assert "export interface SocialLink" in content, (
            "SocialLink type should be exported"
        )

    def test_contact_page_has_heading_field(self):
        """ContactPage type should have heading field."""
        content = TYPES_FILE.read_text()
        assert "heading" in content, "ContactPage should have heading field"

    def test_contact_page_has_intro_text_field(self):
        """ContactPage type should have introText field."""
        content = TYPES_FILE.read_text()
        assert "introText" in content, (
            "ContactPage should have introText field"
        )

    def test_contact_page_has_email_field(self):
        """ContactPage type should have email field."""
        content = TYPES_FILE.read_text()
        assert "email" in content, "ContactPage should have email field"

    def test_contact_page_has_phone_field(self):
        """ContactPage type should have phone field."""
        content = TYPES_FILE.read_text()
        assert "phone" in content, "ContactPage should have phone field"

    def test_contact_page_has_location_field(self):
        """ContactPage type should have location field."""
        content = TYPES_FILE.read_text()
        assert "location" in content, "ContactPage should have location field"

    def test_contact_page_has_social_links_field(self):
        """ContactPage type should have socialLinks field."""
        content = TYPES_FILE.read_text()
        assert "socialLinks" in content, "ContactPage should have socialLinks field"

    def test_contact_page_has_seo_field(self):
        """ContactPage type should have seo field."""
        content = TYPES_FILE.read_text()
        assert "seo" in content, "ContactPage should have seo field"


class TestCMSEditability:
    """Test that all content is editable via CMS (fetched from Sanity)."""

    def test_heading_from_cms(self):
        """Heading should come from CMS."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.heading" in content or "page?.heading" in content, (
            "Heading should be fetched from CMS"
        )

    def test_intro_text_from_cms(self):
        """Introduction text should come from CMS."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.introText" in content or "page?.introText" in content, (
            "Introduction text should be fetched from CMS"
        )

    def test_email_from_cms(self):
        """Email should come from CMS."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.email" in content or "page?.email" in content, (
            "Email should be fetched from CMS"
        )

    def test_phone_from_cms(self):
        """Phone should come from CMS."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.phone" in content or "page?.phone" in content, (
            "Phone should be fetched from CMS"
        )

    def test_location_from_cms(self):
        """Location should come from CMS."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.location" in content or "page?.location" in content, (
            "Location should be fetched from CMS"
        )

    def test_social_links_from_cms(self):
        """Social links should come from CMS."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "page.socialLinks" in content or "page?.socialLinks" in content, (
            "Social links should be fetched from CMS"
        )

    def test_no_hardcoded_content(self):
        """Main content should not be hardcoded (except labels)."""
        content = CONTACT_PAGE_FILE.read_text()
        # Count references to page data
        page_refs = content.count('page.')
        assert page_refs >= 8, (
            "Contact page should reference CMS data frequently (found {} refs)".format(page_refs)
        )


class TestResponsiveLayout:
    """Test that contact page has responsive layout."""

    def test_uses_lg_breakpoint(self):
        """Contact page should use lg: breakpoint for desktop."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "lg:" in content, "Contact page should use lg: breakpoint"

    def test_uses_md_breakpoint(self):
        """Contact page should use md: breakpoint for tablet."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "md:" in content, "Contact page should use md: breakpoint"


class TestBackNavigation:
    """Test that contact page has back to home navigation."""

    def test_has_back_link(self):
        """Contact page should have back to home link."""
        content = CONTACT_PAGE_FILE.read_text()
        assert 'href="/"' in content or "href='/'" in content, (
            "Contact page should have link back to home"
        )

    def test_imports_next_link(self):
        """Contact page should import Next.js Link component."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "import Link from 'next/link'" in content or 'import Link from "next/link"' in content, (
            "Contact page should import Next.js Link"
        )

    def test_back_link_has_arrow_icon(self):
        """Back link should have arrow icon."""
        content = CONTACT_PAGE_FILE.read_text()
        # Check for arrow in SVG path near "Back" text
        assert "Back" in content and "<svg" in content, (
            "Back link should have arrow icon"
        )


class TestFocusStyles:
    """Test that contact page has proper focus styles for accessibility."""

    def test_links_have_focus_styles(self):
        """Links should have focus styles."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "focus:" in content or "focus-visible:" in content, (
            "Links should have focus styles for accessibility"
        )

    def test_social_links_have_focus_ring(self):
        """Social links should have focus ring."""
        content = CONTACT_PAGE_FILE.read_text()
        assert "focus-visible:ring" in content or "focus:ring" in content, (
            "Social links should have focus ring"
        )
