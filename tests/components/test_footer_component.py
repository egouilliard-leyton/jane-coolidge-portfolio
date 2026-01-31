"""
Tests for T-009: Build reusable Footer component

These tests verify that the Footer component is properly implemented according to requirements:
- Footer component fetches site settings from Sanity
- Footer text and copyright display correctly
- Social media links open in new tabs with proper icons
- Footer is styled with Tailwind and matches design system
- Component is responsive across all screen sizes

Acceptance Criteria:
- Footer component fetches site settings from Sanity
- Footer text and copyright display correctly
- Social media links open in new tabs with proper icons
- Footer is styled with Tailwind and matches design system
- Component is responsive across all screen sizes
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
FOOTER_FILE = PROJECT_ROOT / "components" / "layout" / "Footer.tsx"
FOOTER_CLIENT_FILE = PROJECT_ROOT / "components" / "layout" / "FooterClient.tsx"


class TestFooterFileExists:
    """Test that Footer component files exist and have proper structure."""

    def test_footer_server_component_exists(self):
        """components/layout/Footer.tsx should exist."""
        assert FOOTER_FILE.exists(), "components/layout/Footer.tsx not found"

    def test_footer_client_component_exists(self):
        """components/layout/FooterClient.tsx should exist."""
        assert FOOTER_CLIENT_FILE.exists(), "components/layout/FooterClient.tsx not found"

    def test_footer_server_component_is_async(self):
        """Footer.tsx should be an async Server Component."""
        content = FOOTER_FILE.read_text()
        assert "async function Footer" in content or "export default async function Footer" in content, (
            "Footer should be an async function (Server Component)"
        )

    def test_footer_client_component_has_use_client(self):
        """FooterClient.tsx should have 'use client' directive."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "FooterClient should have 'use client' directive"
        )


class TestFooterFetchesSiteSettings:
    """Test that Footer component fetches site settings from Sanity."""

    def test_footer_imports_sanity_fetch(self):
        """Footer.tsx should import sanityFetch from Sanity client."""
        content = FOOTER_FILE.read_text()
        assert "sanityFetch" in content, "Footer should import sanityFetch"
        assert "@/sanity/lib/client" in content, (
            "Footer should import from @/sanity/lib/client"
        )

    def test_footer_imports_site_settings_query(self):
        """Footer.tsx should import siteSettingsQuery."""
        content = FOOTER_FILE.read_text()
        assert "siteSettingsQuery" in content, "Footer should import siteSettingsQuery"

    def test_footer_fetches_settings(self):
        """Footer.tsx should fetch site settings."""
        content = FOOTER_FILE.read_text()
        assert "siteSettingsQuery" in content and "sanityFetch" in content, (
            "Footer should fetch site settings using sanityFetch"
        )

    def test_footer_uses_cache_tags(self):
        """Footer.tsx should use cache tags for revalidation."""
        content = FOOTER_FILE.read_text()
        assert "tags:" in content or "tags :" in content, (
            "Footer should specify tags for cache revalidation"
        )

    def test_footer_imports_site_settings_result_type(self):
        """Footer.tsx should import SiteSettingsResult type."""
        content = FOOTER_FILE.read_text()
        assert "SiteSettingsResult" in content, (
            "Footer should import SiteSettingsResult type"
        )


class TestFooterClientPropsInterface:
    """Test that FooterClient receives proper props from server component."""

    def test_footer_client_has_props_interface(self):
        """FooterClient should define a props interface."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "FooterClientProps" in content or "interface" in content, (
            "FooterClient should define a props interface"
        )

    def test_footer_client_receives_settings_prop(self):
        """FooterClient should receive settings prop."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "settings" in content, "FooterClient should receive settings prop"

    def test_footer_passes_props_to_client(self):
        """Footer.tsx should pass fetched data to FooterClient."""
        content = FOOTER_FILE.read_text()
        assert "FooterClient" in content, "Footer should render FooterClient"
        assert "settings=" in content or "settings =" in content, (
            "Footer should pass settings to FooterClient"
        )


class TestFooterTextAndCopyrightDisplay:
    """Test that footer text and copyright display correctly."""

    def test_footer_displays_footer_text(self):
        """FooterClient should display footerText from settings."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "footerText" in content, (
            "FooterClient should reference footerText from settings"
        )

    def test_footer_displays_copyright(self):
        """FooterClient should display copyright symbol."""
        content = FOOTER_CLIENT_FILE.read_text()
        # Check for copyright symbol (HTML entity or unicode)
        assert "©" in content or "&copy;" in content, (
            "FooterClient should display copyright symbol"
        )

    def test_footer_displays_current_year(self):
        """FooterClient should display current year."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "getFullYear()" in content, (
            "FooterClient should get current year using getFullYear()"
        )

    def test_footer_displays_site_name(self):
        """FooterClient should display site name."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "siteName" in content, (
            "FooterClient should reference siteName"
        )

    def test_footer_has_fallback_for_empty_footer_text(self):
        """FooterClient should have fallback when footerText is not set."""
        content = FOOTER_CLIENT_FILE.read_text()
        # Should have conditional rendering for footerText
        assert "||" in content or "?" in content, (
            "FooterClient should have fallback for missing footerText"
        )


class TestSocialMediaLinks:
    """Test that social media links work correctly."""

    def test_footer_displays_social_links(self):
        """FooterClient should display social links."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "socialLinks" in content, (
            "FooterClient should reference socialLinks"
        )

    def test_social_links_map_over_items(self):
        """FooterClient should map over social link items."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert ".map(" in content, "FooterClient should map over social links"

    def test_social_links_open_in_new_tab(self):
        """Social links should open in new tabs."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert 'target="_blank"' in content or "target='_blank'" in content, (
            "Social links should have target=_blank"
        )

    def test_social_links_have_security_attributes(self):
        """Social links should have noopener noreferrer for security."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert 'rel="noopener noreferrer"' in content or "rel='noopener noreferrer'" in content, (
            "Social links should have rel=noopener noreferrer"
        )

    def test_social_links_have_href(self):
        """Social links should have href attribute with URL."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "href=" in content, "Social links should have href attribute"
        # Check that url from socialLinks is used
        assert "url" in content.lower(), "Social links should use url property"

    def test_social_links_have_aria_labels(self):
        """Social links should have aria-label for accessibility."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "aria-label" in content, (
            "Social links should have aria-label for accessibility"
        )


class TestSocialMediaIcons:
    """Test that social media icons are properly rendered."""

    def test_footer_has_social_icon_component(self):
        """FooterClient should have SocialIcon component or inline icons."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "SocialIcon" in content or "<svg" in content, (
            "FooterClient should render social icons"
        )

    def test_footer_renders_svg_icons(self):
        """FooterClient should render SVG icons for social platforms."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "<svg" in content, "FooterClient should have SVG icons"

    def test_footer_supports_instagram_icon(self):
        """FooterClient should support Instagram icon."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "instagram" in content.lower(), (
            "FooterClient should support Instagram platform"
        )

    def test_footer_supports_twitter_icon(self):
        """FooterClient should support Twitter/X icon."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "twitter" in content.lower(), (
            "FooterClient should support Twitter platform"
        )

    def test_footer_supports_linkedin_icon(self):
        """FooterClient should support LinkedIn icon."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "linkedin" in content.lower(), (
            "FooterClient should support LinkedIn platform"
        )

    def test_footer_has_platform_switch(self):
        """FooterClient should have switch/conditional for platform icons."""
        content = FOOTER_CLIENT_FILE.read_text()
        # Should have switch statement or conditional for different platforms
        assert "switch" in content or "case" in content, (
            "FooterClient should have switch statement for platform icons"
        )


class TestTailwindStyling:
    """Test that component uses Tailwind for styling."""

    def test_uses_tailwind_classes(self):
        """FooterClient should use Tailwind CSS classes."""
        content = FOOTER_CLIENT_FILE.read_text()
        tailwind_indicators = [
            "flex",
            "items-center",
            "justify-",
            "px-",
            "py-",
            "bg-",
            "text-",
        ]
        found_classes = [cls for cls in tailwind_indicators if cls in content]
        assert len(found_classes) >= 4, (
            f"FooterClient should use Tailwind classes, found: {found_classes}"
        )

    def test_uses_responsive_classes(self):
        """FooterClient should use Tailwind responsive classes."""
        content = FOOTER_CLIENT_FILE.read_text()
        responsive_prefixes = ["sm:", "md:", "lg:", "xl:"]
        found_responsive = [prefix for prefix in responsive_prefixes if prefix in content]
        assert len(found_responsive) >= 1, (
            "FooterClient should use Tailwind responsive classes"
        )

    def test_uses_tailwind_transitions(self):
        """FooterClient should use Tailwind transition classes."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "transition" in content, (
            "FooterClient should use Tailwind transition classes"
        )

    def test_uses_tailwind_colors(self):
        """FooterClient should use Tailwind color utilities."""
        content = FOOTER_CLIENT_FILE.read_text()
        color_found = any(
            pattern in content
            for pattern in ["text-neutral", "bg-neutral", "text-white", "bg-black"]
        )
        assert color_found, "FooterClient should use Tailwind color utilities"

    def test_uses_tailwind_spacing(self):
        """FooterClient should use Tailwind spacing utilities."""
        content = FOOTER_CLIENT_FILE.read_text()
        spacing_found = any(
            pattern in content
            for pattern in ["p-", "m-", "gap-", "space-"]
        )
        assert spacing_found, "FooterClient should use Tailwind spacing utilities"


class TestResponsiveDesign:
    """Test that footer is responsive across all screen sizes."""

    def test_footer_has_responsive_layout(self):
        """Footer should have responsive layout classes."""
        content = FOOTER_CLIENT_FILE.read_text()
        # Check for flex direction changes on different screen sizes
        assert "flex-col" in content or "md:flex-row" in content, (
            "Footer should have responsive flex layout"
        )

    def test_footer_has_max_width_constraint(self):
        """Footer content should have max-width constraint."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "max-w-" in content, "Footer should have max-width class"

    def test_footer_is_centered(self):
        """Footer content should be centered."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "mx-auto" in content, "Footer content should be centered with mx-auto"

    def test_footer_has_responsive_padding(self):
        """Footer should have responsive padding."""
        content = FOOTER_CLIENT_FILE.read_text()
        # Check for padding classes with responsive prefixes
        has_responsive_padding = (
            "px-" in content and ("md:px-" in content or "lg:px-" in content)
        ) or "py-" in content
        assert has_responsive_padding, "Footer should have responsive padding"

    def test_footer_has_responsive_gap(self):
        """Footer should have responsive gap between elements."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "gap-" in content, "Footer should use gap for spacing"


class TestSemanticHTML:
    """Test that footer uses semantic HTML elements."""

    def test_uses_footer_element(self):
        """FooterClient should use semantic footer element."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "<footer" in content, "FooterClient should use footer element"

    def test_uses_nav_element_for_social(self):
        """FooterClient should use nav element for social links navigation."""
        content = FOOTER_CLIENT_FILE.read_text()
        # May use <nav or motion.nav for animated nav element
        assert "<nav" in content or "motion.nav" in content, (
            "FooterClient should use nav element for social links"
        )

    def test_nav_has_aria_label(self):
        """Navigation should have aria-label for accessibility."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "aria-label" in content, (
            "Social navigation should have aria-label"
        )


class TestAnimations:
    """Test that component uses animations appropriately."""

    def test_uses_motion_library(self):
        """FooterClient should use motion library for animations."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "motion" in content.lower(), (
            "FooterClient should use motion for animations"
        )

    def test_imports_motion_components(self):
        """FooterClient should import motion components."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "from 'motion" in content or 'from "motion' in content, (
            "FooterClient should import from motion library"
        )

    def test_uses_motion_elements(self):
        """FooterClient should use motion elements for animation."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "motion." in content, (
            "FooterClient should use motion elements like motion.div"
        )


class TestDesignSystemConsistency:
    """Test that footer matches the design system."""

    def test_uses_brand_colors(self):
        """FooterClient should use brand color classes."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "brand-" in content, (
            "FooterClient should use brand color classes from design system"
        )

    def test_uses_neutral_colors(self):
        """FooterClient should use neutral color palette."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "neutral-" in content, (
            "FooterClient should use neutral color classes"
        )

    def test_uses_consistent_typography(self):
        """FooterClient should use typography classes from design system."""
        content = FOOTER_CLIENT_FILE.read_text()
        typography_classes = ["text-xs", "text-sm", "uppercase", "tracking-"]
        found_typography = [cls for cls in typography_classes if cls in content]
        assert len(found_typography) >= 2, (
            "FooterClient should use design system typography classes"
        )


class TestLinkToHomepage:
    """Test that site name links to homepage."""

    def test_footer_has_link_component(self):
        """FooterClient should import Next.js Link component."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "import Link from 'next/link'" in content or 'import Link from "next/link"' in content, (
            "FooterClient should import Next.js Link component"
        )

    def test_site_name_links_to_home(self):
        """Site name should link to homepage."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert 'href="/"' in content or "href='/'" in content, (
            "Site name should link to homepage"
        )


class TestBackToTopButton:
    """Test back to top button functionality."""

    def test_footer_has_back_to_top(self):
        """FooterClient should have back to top button."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "back to top" in content.lower() or "Back to top" in content, (
            "FooterClient should have back to top button"
        )

    def test_back_to_top_has_scroll_behavior(self):
        """Back to top button should scroll to top of page."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "scrollTo" in content, (
            "Back to top should use scrollTo for smooth scroll"
        )

    def test_back_to_top_is_button(self):
        """Back to top should be a button element."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "<button" in content, (
            "Back to top should use button element"
        )


class TestExportAndModuleStructure:
    """Test proper module exports and structure."""

    def test_footer_exports_default(self):
        """Footer.tsx should export default component."""
        content = FOOTER_FILE.read_text()
        assert "export default" in content, (
            "Footer.tsx should have default export"
        )

    def test_footer_client_exports_default(self):
        """FooterClient.tsx should export default component."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "export default" in content, (
            "FooterClient.tsx should have default export"
        )

    def test_footer_client_imports_types(self):
        """FooterClient should import types from queries."""
        content = FOOTER_CLIENT_FILE.read_text()
        assert "@/sanity/lib/queries" in content, (
            "FooterClient should import types from @/sanity/lib/queries"
        )

    def test_footer_imports_footer_client(self):
        """Footer.tsx should import FooterClient."""
        content = FOOTER_FILE.read_text()
        assert "import FooterClient from" in content, (
            "Footer should import FooterClient"
        )
