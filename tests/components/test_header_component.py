"""
Tests for T-008: Build reusable Header component with navigation

These tests verify that the Header component is properly implemented according to requirements:
- Header component fetches navigation and site settings from Sanity
- Logo displays correctly (image or text based on settings)
- Desktop navigation renders horizontally
- Mobile hamburger menu works on small screens
- Active link states are indicated
- Component uses Tailwind for styling

Acceptance Criteria:
- Header component fetches navigation and site settings from Sanity
- Logo displays correctly (image or text based on settings)
- Desktop navigation renders horizontally
- Mobile hamburger menu works on small screens
- Active link states are indicated
- Component uses Tailwind for styling
"""

from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
HEADER_FILE = PROJECT_ROOT / "components" / "layout" / "Header.tsx"
HEADER_CLIENT_FILE = PROJECT_ROOT / "components" / "layout" / "HeaderClient.tsx"


class TestHeaderFileExists:
    """Test that Header component files exist and have proper structure."""

    def test_header_server_component_exists(self):
        """components/layout/Header.tsx should exist."""
        assert HEADER_FILE.exists(), "components/layout/Header.tsx not found"

    def test_header_client_component_exists(self):
        """components/layout/HeaderClient.tsx should exist."""
        assert HEADER_CLIENT_FILE.exists(), "components/layout/HeaderClient.tsx not found"

    def test_header_server_component_is_async(self):
        """Header.tsx should be an async Server Component."""
        content = HEADER_FILE.read_text()
        assert "async function Header" in content or "export default async function Header" in content, (
            "Header should be an async function (Server Component)"
        )

    def test_header_client_component_has_use_client(self):
        """HeaderClient.tsx should have 'use client' directive."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "HeaderClient should have 'use client' directive"
        )


class TestHeaderFetchesFromSanity:
    """Test that Header component fetches navigation and site settings from Sanity."""

    def test_header_imports_sanity_fetch(self):
        """Header.tsx should import sanityFetch from Sanity client."""
        content = HEADER_FILE.read_text()
        assert "sanityFetch" in content, "Header should import sanityFetch"
        assert "@/sanity/lib/client" in content, (
            "Header should import from @/sanity/lib/client"
        )

    def test_header_imports_site_settings_query(self):
        """Header.tsx should import siteSettingsQuery."""
        content = HEADER_FILE.read_text()
        assert "siteSettingsQuery" in content, "Header should import siteSettingsQuery"

    def test_header_imports_navigation_query(self):
        """Header.tsx should import navigationQuery."""
        content = HEADER_FILE.read_text()
        assert "navigationQuery" in content, "Header should import navigationQuery"

    def test_header_fetches_settings(self):
        """Header.tsx should fetch site settings."""
        content = HEADER_FILE.read_text()
        # Check for Promise.all fetching both or individual fetches
        assert "siteSettingsQuery" in content and "sanityFetch" in content, (
            "Header should fetch site settings using sanityFetch"
        )

    def test_header_fetches_navigation(self):
        """Header.tsx should fetch navigation data."""
        content = HEADER_FILE.read_text()
        assert "navigationQuery" in content and "sanityFetch" in content, (
            "Header should fetch navigation using sanityFetch"
        )

    def test_header_uses_parallel_fetching(self):
        """Header.tsx should fetch settings and navigation in parallel."""
        content = HEADER_FILE.read_text()
        # Check for Promise.all pattern for parallel fetching
        assert "Promise.all" in content, (
            "Header should use Promise.all for parallel data fetching"
        )

    def test_header_uses_cache_tags(self):
        """Header.tsx should use cache tags for revalidation."""
        content = HEADER_FILE.read_text()
        assert "tags:" in content or "tags :" in content, (
            "Header should specify tags for cache revalidation"
        )

    def test_header_imports_result_types(self):
        """Header.tsx should import proper TypeScript result types."""
        content = HEADER_FILE.read_text()
        assert "SiteSettingsResult" in content, (
            "Header should import SiteSettingsResult type"
        )
        assert "NavigationResult" in content, (
            "Header should import NavigationResult type"
        )


class TestHeaderClientPropsInterface:
    """Test that HeaderClient receives proper props from server component."""

    def test_header_client_has_props_interface(self):
        """HeaderClient should define a props interface."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "HeaderClientProps" in content or "interface" in content, (
            "HeaderClient should define a props interface"
        )

    def test_header_client_receives_settings_prop(self):
        """HeaderClient should receive settings prop."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "settings" in content, "HeaderClient should receive settings prop"

    def test_header_client_receives_navigation_prop(self):
        """HeaderClient should receive navigation prop."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "navigation" in content, "HeaderClient should receive navigation prop"

    def test_header_passes_props_to_client(self):
        """Header.tsx should pass fetched data to HeaderClient."""
        content = HEADER_FILE.read_text()
        assert "HeaderClient" in content, "Header should render HeaderClient"
        assert "settings=" in content or "settings =" in content, (
            "Header should pass settings to HeaderClient"
        )
        assert "navigation=" in content or "navigation =" in content, (
            "Header should pass navigation to HeaderClient"
        )


class TestLogoDisplay:
    """Test that logo displays correctly based on settings."""

    def test_logo_conditional_rendering(self):
        """HeaderClient should conditionally render logo image or site name."""
        content = HEADER_CLIENT_FILE.read_text()
        # Should check for logo.asset existence
        assert "logo" in content, "HeaderClient should reference logo"

    def test_logo_image_rendering(self):
        """HeaderClient should render Image component when logo asset exists."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "HeaderClient should import Next.js Image component"
        )
        assert "<Image" in content, "HeaderClient should render Image component for logo"

    def test_logo_uses_urlfor_helper(self):
        """HeaderClient should use urlFor helper for logo image URL."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "urlFor" in content, "HeaderClient should use urlFor helper for images"

    def test_logo_fallback_to_site_name(self):
        """HeaderClient should fall back to site name when no logo."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "siteName" in content, (
            "HeaderClient should reference siteName for text fallback"
        )

    def test_logo_links_to_home(self):
        """Logo should link to homepage."""
        content = HEADER_CLIENT_FILE.read_text()
        assert 'href="/"' in content or "href='/'" in content, (
            "Logo should link to homepage"
        )

    def test_logo_has_alt_text(self):
        """Logo image should have alt text."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "alt=" in content or "alt =" in content, (
            "Logo image should have alt attribute"
        )


class TestDesktopNavigation:
    """Test that desktop navigation renders horizontally."""

    def test_navigation_uses_nav_element(self):
        """HeaderClient should use semantic nav element."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "<nav" in content, "HeaderClient should use nav element"

    def test_navigation_renders_menu_items(self):
        """HeaderClient should render navigation menu items."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "mainMenu" in content, (
            "HeaderClient should reference mainMenu from navigation"
        )

    def test_navigation_maps_over_items(self):
        """HeaderClient should map over navigation items."""
        content = HEADER_CLIENT_FILE.read_text()
        assert ".map(" in content, "HeaderClient should map over menu items"

    def test_navigation_renders_links(self):
        """HeaderClient should render Link components for navigation."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "import Link from 'next/link'" in content or 'import Link from "next/link"' in content, (
            "HeaderClient should import Next.js Link component"
        )
        assert "<Link" in content, "HeaderClient should render Link components"

    def test_navigation_items_have_labels(self):
        """Navigation items should display labels."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "label" in content, "Navigation items should reference label property"

    def test_navigation_items_have_hrefs(self):
        """Navigation items should have href from link property."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "href=" in content, "Navigation links should have href attribute"
        assert "link" in content.lower(), "Navigation should reference link property"

    def test_desktop_nav_hidden_on_mobile(self):
        """Desktop navigation should be hidden on mobile screens."""
        content = HEADER_CLIENT_FILE.read_text()
        # Check for Tailwind responsive hiding
        assert "hidden md:" in content or "hidden lg:" in content, (
            "Desktop navigation should be hidden on mobile (hidden md:block or similar)"
        )

    def test_navigation_supports_external_links(self):
        """Navigation should support openInNewTab for external links."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "openInNewTab" in content, (
            "Navigation should check openInNewTab property"
        )
        assert 'target="_blank"' in content or "target='_blank'" in content, (
            "Navigation should support target=_blank for external links"
        )


class TestMobileHamburgerMenu:
    """Test that mobile hamburger menu works on small screens."""

    def test_mobile_menu_button_exists(self):
        """HeaderClient should have a mobile menu button."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "<button" in content, "HeaderClient should have a button element"

    def test_mobile_menu_button_has_aria_label(self):
        """Mobile menu button should have aria-label for accessibility."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "aria-label" in content, (
            "Mobile menu button should have aria-label"
        )

    def test_mobile_menu_button_has_aria_expanded(self):
        """Mobile menu button should have aria-expanded state."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "aria-expanded" in content, (
            "Mobile menu button should have aria-expanded attribute"
        )

    def test_mobile_menu_state_management(self):
        """HeaderClient should manage mobile menu open/closed state."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "useState" in content, "HeaderClient should use useState for state"
        assert "mobileMenuOpen" in content or "menuOpen" in content or "isOpen" in content, (
            "HeaderClient should have mobile menu state"
        )

    def test_mobile_menu_toggle_handler(self):
        """HeaderClient should have toggle handler for mobile menu."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "onClick" in content, "HeaderClient should have onClick handler"
        assert "setMobileMenuOpen" in content or "setMenuOpen" in content or "setIsOpen" in content, (
            "HeaderClient should toggle mobile menu state"
        )

    def test_mobile_menu_visible_only_on_mobile(self):
        """Mobile menu button should only be visible on mobile."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "md:hidden" in content or "lg:hidden" in content, (
            "Mobile menu button should be hidden on desktop (md:hidden or lg:hidden)"
        )

    def test_mobile_menu_has_close_mechanism(self):
        """Mobile menu should have a way to close it."""
        content = HEADER_CLIENT_FILE.read_text()
        # Should have close button or backdrop click handler
        assert "Close menu" in content or "close" in content.lower(), (
            "Mobile menu should have close functionality"
        )

    def test_mobile_menu_renders_same_navigation(self):
        """Mobile menu should render the same navigation items."""
        content = HEADER_CLIENT_FILE.read_text()
        # Should map over mainMenu items in mobile section too
        map_count = content.count("mainMenu?.map") + content.count("mainMenu.map")
        assert map_count >= 2, (
            "Both desktop and mobile navigation should iterate over mainMenu"
        )


class TestActiveLinkStates:
    """Test that active link states are indicated."""

    def test_uses_pathname_hook(self):
        """HeaderClient should use usePathname to determine current route."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "usePathname" in content, (
            "HeaderClient should use usePathname from next/navigation"
        )

    def test_imports_pathname_hook(self):
        """HeaderClient should import usePathname from next/navigation."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "from 'next/navigation'" in content or 'from "next/navigation"' in content, (
            "HeaderClient should import from next/navigation"
        )

    def test_has_active_link_check(self):
        """HeaderClient should have logic to check if link is active."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "isActive" in content or "active" in content.lower(), (
            "HeaderClient should have active link checking logic"
        )

    def test_active_link_styling_differs(self):
        """Active links should have different styling than inactive links."""
        content = HEADER_CLIENT_FILE.read_text()
        # Check for conditional class application
        assert "?" in content and ":" in content, (
            "HeaderClient should have conditional styling (ternary for active/inactive)"
        )

    def test_pathname_compared_to_link(self):
        """Current pathname should be compared to link href."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "pathname" in content, "HeaderClient should reference pathname"


class TestTailwindStyling:
    """Test that component uses Tailwind for styling."""

    def test_uses_tailwind_classes(self):
        """HeaderClient should use Tailwind CSS classes."""
        content = HEADER_CLIENT_FILE.read_text()
        # Check for common Tailwind utility classes
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
            f"HeaderClient should use Tailwind classes, found: {found_classes}"
        )

    def test_uses_responsive_classes(self):
        """HeaderClient should use Tailwind responsive classes."""
        content = HEADER_CLIENT_FILE.read_text()
        responsive_prefixes = ["sm:", "md:", "lg:", "xl:"]
        found_responsive = [prefix for prefix in responsive_prefixes if prefix in content]
        assert len(found_responsive) >= 1, (
            "HeaderClient should use Tailwind responsive classes"
        )

    def test_uses_tailwind_transitions(self):
        """HeaderClient should use Tailwind transition classes."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "transition" in content, (
            "HeaderClient should use Tailwind transition classes"
        )

    def test_uses_tailwind_spacing(self):
        """HeaderClient should use Tailwind spacing utilities."""
        content = HEADER_CLIENT_FILE.read_text()
        # Check for padding, margin, gap classes
        spacing_found = any(
            pattern in content
            for pattern in ["p-", "m-", "gap-", "space-"]
        )
        assert spacing_found, "HeaderClient should use Tailwind spacing utilities"

    def test_uses_tailwind_typography(self):
        """HeaderClient should use Tailwind typography utilities."""
        content = HEADER_CLIENT_FILE.read_text()
        typography_found = any(
            pattern in content
            for pattern in ["text-", "font-", "tracking-"]
        )
        assert typography_found, "HeaderClient should use Tailwind typography utilities"

    def test_uses_tailwind_colors(self):
        """HeaderClient should use Tailwind color utilities."""
        content = HEADER_CLIENT_FILE.read_text()
        # Check for color classes
        color_found = any(
            pattern in content
            for pattern in ["text-neutral", "bg-white", "bg-black", "text-brand"]
        )
        assert color_found, "HeaderClient should use Tailwind color utilities"


class TestHeaderResponsiveness:
    """Test that header is properly responsive."""

    def test_header_is_fixed(self):
        """Header should have fixed positioning."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "fixed" in content, "Header should use fixed positioning"

    def test_header_has_max_width(self):
        """Header content should have max-width constraint."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "max-w-" in content, "Header should have max-width class"

    def test_header_is_centered(self):
        """Header content should be centered."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "mx-auto" in content, "Header content should be centered with mx-auto"

    def test_header_has_z_index(self):
        """Header should have z-index for proper stacking."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "z-" in content, "Header should have z-index class"


class TestHeaderScrollBehavior:
    """Test header scroll-related behavior."""

    def test_has_scroll_effect_state(self):
        """HeaderClient should track scroll state for visual effects."""
        content = HEADER_CLIENT_FILE.read_text()
        # Check for scroll-related state
        assert "scroll" in content.lower(), (
            "HeaderClient should have scroll-related functionality"
        )

    def test_uses_use_effect_for_scroll(self):
        """HeaderClient should use useEffect for scroll event handling."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "useEffect" in content, (
            "HeaderClient should use useEffect hook"
        )

    def test_adds_scroll_event_listener(self):
        """HeaderClient should add scroll event listener."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "addEventListener" in content and "scroll" in content, (
            "HeaderClient should add scroll event listener"
        )

    def test_removes_scroll_event_listener(self):
        """HeaderClient should clean up scroll event listener."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "removeEventListener" in content, (
            "HeaderClient should remove event listener on cleanup"
        )


class TestMobileMenuAccessibility:
    """Test mobile menu accessibility features."""

    def test_mobile_menu_prevents_body_scroll(self):
        """Mobile menu should prevent body scrolling when open."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "overflow" in content, (
            "Mobile menu should control body overflow when open"
        )

    def test_mobile_menu_closes_on_route_change(self):
        """Mobile menu should close when route changes."""
        content = HEADER_CLIENT_FILE.read_text()
        # Should have useEffect that watches pathname
        assert "pathname" in content and "useEffect" in content, (
            "Mobile menu should close on route change"
        )


class TestAnimations:
    """Test that component uses animations appropriately."""

    def test_uses_motion_library(self):
        """HeaderClient should use motion library for animations."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "motion" in content.lower(), (
            "HeaderClient should use motion for animations"
        )

    def test_imports_animate_presence(self):
        """HeaderClient should import AnimatePresence for exit animations."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "AnimatePresence" in content, (
            "HeaderClient should import AnimatePresence"
        )


class TestSocialLinksInMobile:
    """Test social links display in mobile menu."""

    def test_mobile_menu_shows_social_links(self):
        """Mobile menu should display social links if available."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "socialLinks" in content, (
            "HeaderClient should reference socialLinks"
        )

    def test_social_links_have_proper_attributes(self):
        """Social links should have proper security attributes."""
        content = HEADER_CLIENT_FILE.read_text()
        assert 'rel="noopener noreferrer"' in content or "rel='noopener noreferrer'" in content, (
            "External social links should have rel=noopener noreferrer"
        )


class TestExportAndModuleStructure:
    """Test proper module exports and structure."""

    def test_header_exports_default(self):
        """Header.tsx should export default component."""
        content = HEADER_FILE.read_text()
        assert "export default" in content, (
            "Header.tsx should have default export"
        )

    def test_header_client_exports_default(self):
        """HeaderClient.tsx should export default component."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "export default" in content, (
            "HeaderClient.tsx should have default export"
        )

    def test_header_client_imports_types(self):
        """HeaderClient should import types from queries."""
        content = HEADER_CLIENT_FILE.read_text()
        assert "@/sanity/lib/queries" in content, (
            "HeaderClient should import types from @/sanity/lib/queries"
        )

    def test_header_imports_header_client(self):
        """Header.tsx should import HeaderClient."""
        content = HEADER_FILE.read_text()
        assert "import HeaderClient from" in content, (
            "Header should import HeaderClient"
        )
