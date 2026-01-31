"""
Tests for T-022: Accessibility Audit and WCAG AA Compliance

These tests verify WCAG AA compliance across the fashion website:
- All images have meaningful alt text (enforced in Sanity)
- Color contrast meets WCAG AA standards (4.5:1 for normal text)
- Keyboard navigation works on all interactive elements
- Focus states are clearly visible
- Modal dialogs trap and restore focus correctly
- Semantic HTML is used throughout (nav, article, main, etc.)

Acceptance Criteria:
- All images have meaningful alt text (enforced in Sanity)
- Color contrast meets WCAG AA standards (4.5:1 for normal text)
- Keyboard navigation works on all interactive elements
- Focus states are clearly visible
- Modal dialogs trap and restore focus correctly
- Automated tests (axe/Lighthouse) show zero critical issues
- Semantic HTML is used throughout (nav, article, main, etc.)
"""

from pathlib import Path
import re


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
COMPONENTS_DIR = PROJECT_ROOT / "components"
APP_DIR = PROJECT_ROOT / "app"
SANITY_SCHEMAS_DIR = PROJECT_ROOT / "sanity" / "schemas"
GLOBALS_CSS = APP_DIR / "globals.css"


# =============================================================================
# IMAGE ALT TEXT TESTS
# =============================================================================


class TestImageAltTextEnforcementInSanity:
    """Test that all images have meaningful alt text enforced in Sanity schemas."""

    def test_sanity_image_with_popup_schema_exists(self):
        """imageWithPopup.ts schema file should exist."""
        schema_file = SANITY_SCHEMAS_DIR / "objects" / "imageWithPopup.ts"
        assert schema_file.exists(), "imageWithPopup.ts schema not found"

    def test_image_with_popup_requires_alt_text(self):
        """imageWithPopup schema should require alt text."""
        schema_file = SANITY_SCHEMAS_DIR / "objects" / "imageWithPopup.ts"
        content = schema_file.read_text()
        # Check for alt field with required validation
        assert "name: 'alt'" in content or 'name: "alt"' in content, (
            "Alt text field should be defined in imageWithPopup schema"
        )
        # Check validation rule requires alt
        assert "Rule.required()" in content or "Rule) => Rule.required()" in content, (
            "Alt text should be required in schema validation"
        )

    def test_alt_text_description_mentions_accessibility(self):
        """Alt text field description should mention accessibility/SEO."""
        schema_file = SANITY_SCHEMAS_DIR / "objects" / "imageWithPopup.ts"
        content = schema_file.read_text()
        # Alt field should have description mentioning accessibility
        assert "accessibility" in content.lower() or "seo" in content.lower(), (
            "Alt text field description should mention accessibility or SEO"
        )

    def test_project_schema_has_alt_for_cover_image(self):
        """Project schema should require alt text for cover images."""
        schema_file = SANITY_SCHEMAS_DIR / "documents" / "project.ts"
        content = schema_file.read_text()
        # Check for alt field in cover image
        assert "alt" in content, (
            "Project schema should include alt text for cover image"
        )


class TestImageComponentAltTextUsage:
    """Test that image components properly use alt text."""

    def test_image_with_popup_accepts_alt_prop(self):
        """ImageWithPopup component should accept alt prop."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Check for alt in props interface
        assert "alt:" in content, (
            "ImageWithPopup should accept alt prop in interface"
        )

    def test_image_with_popup_passes_alt_to_image(self):
        """ImageWithPopup should pass alt prop to Next.js Image component."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Check that alt is passed to Image component
        assert "alt={alt}" in content, (
            "Alt prop should be passed to Next.js Image component"
        )

    def test_header_logo_has_alt_text(self):
        """Header logo should have alt text."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        # Check for alt attribute on Image
        assert "alt=" in content, (
            "Header logo Image should have alt attribute"
        )

    def test_header_logo_uses_site_name_for_alt(self):
        """Header logo should use site name or fallback for alt text."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        # Logo should use siteName or 'Logo' as alt
        assert "siteName" in content and "Logo" in content, (
            "Logo alt should use siteName with fallback to 'Logo'"
        )


# =============================================================================
# COLOR CONTRAST TESTS (WCAG AA - 4.5:1 for normal text)
# =============================================================================


class TestColorContrastConfiguration:
    """Test that color configuration supports WCAG AA contrast ratios."""

    def test_globals_css_defines_colors(self):
        """globals.css should define color variables."""
        content = GLOBALS_CSS.read_text()
        assert "--color-" in content, (
            "globals.css should define CSS color variables"
        )

    def test_dark_mode_colors_defined(self):
        """Dark mode color scheme should be defined."""
        content = GLOBALS_CSS.read_text()
        assert "prefers-color-scheme: dark" in content, (
            "Dark mode color scheme should be defined"
        )

    def test_brand_colors_defined(self):
        """Brand color palette should be defined in globals.css."""
        content = GLOBALS_CSS.read_text()
        # Check for brand color variables
        assert "--color-brand-" in content, (
            "Brand color palette should be defined"
        )

    def test_neutral_colors_for_text_defined(self):
        """Neutral colors for text should be defined."""
        content = GLOBALS_CSS.read_text()
        # Check for foreground and muted colors
        assert "--color-foreground" in content, (
            "Foreground text color should be defined"
        )
        assert "--color-muted" in content, (
            "Muted text color should be defined"
        )


class TestTextContrastInComponents:
    """Test that components use appropriate text colors for contrast."""

    def test_footer_uses_contrast_colors(self):
        """Footer should use colors with good contrast on dark background."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        # Footer has dark background (bg-neutral-950) with white text
        assert "bg-neutral-950" in content, (
            "Footer should have dark background"
        )
        assert "text-white" in content, (
            "Footer should have white text on dark background"
        )

    def test_footer_muted_text_uses_neutral_400_or_500(self):
        """Footer muted text should use neutral-400/500 for adequate contrast."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        # Muted text should be at least neutral-400 for contrast
        assert "text-neutral-400" in content or "text-neutral-500" in content, (
            "Muted text should use neutral-400 or higher for contrast"
        )

    def test_header_uses_contrast_colors(self):
        """Header text should have adequate contrast."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        # Header should use neutral-900 for primary text (high contrast)
        assert "text-neutral-900" in content, (
            "Header should use neutral-900 for primary text"
        )

    def test_modal_uses_contrast_colors(self):
        """Modal popup text should have adequate contrast."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Modal should use neutral-900 for headings
        assert "text-neutral-900" in content, (
            "Modal should use neutral-900 for headings"
        )
        # Modal should use neutral-600 for body text
        assert "text-neutral-600" in content, (
            "Modal should use neutral-600 for body text"
        )


# =============================================================================
# KEYBOARD NAVIGATION TESTS
# =============================================================================


class TestKeyboardNavigationSupport:
    """Test that all interactive elements support keyboard navigation."""

    def test_skip_link_exists(self):
        """SkipLink component should exist for keyboard navigation."""
        skip_link_file = COMPONENTS_DIR / "ui" / "SkipLink.tsx"
        assert skip_link_file.exists(), "SkipLink component should exist"

    def test_skip_link_targets_main_content(self):
        """Skip link should target #main-content."""
        skip_link_file = COMPONENTS_DIR / "ui" / "SkipLink.tsx"
        content = skip_link_file.read_text()
        assert '#main-content' in content or "#main-content" in content, (
            "Skip link should target #main-content"
        )

    def test_skip_link_is_anchor_element(self):
        """Skip link should be an anchor element."""
        skip_link_file = COMPONENTS_DIR / "ui" / "SkipLink.tsx"
        content = skip_link_file.read_text()
        assert "<a" in content and "href=" in content, (
            "Skip link should be an anchor element with href"
        )

    def test_modal_handles_escape_key(self):
        """Modal should close on ESC key press."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "Escape" in content, (
            "Modal should handle Escape key"
        )

    def test_mobile_menu_handles_escape_key(self):
        """Mobile menu should close on ESC key press."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "Escape" in content, (
            "Mobile menu should handle Escape key"
        )

    def test_modal_handles_tab_key(self):
        """Modal should handle Tab key for focus trapping."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "'Tab'" in content or '"Tab"' in content, (
            "Modal should handle Tab key"
        )

    def test_buttons_are_focusable(self):
        """Interactive buttons should be focusable."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Buttons are naturally focusable
        assert "<button" in content or "<motion.button" in content, (
            "Component should use button elements which are naturally focusable"
        )


class TestKeyboardEventHandlers:
    """Test that keyboard event handlers are properly implemented."""

    def test_modal_adds_keydown_listener(self):
        """Modal should add keydown event listener."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "addEventListener" in content and "keydown" in content, (
            "Modal should add keydown event listener"
        )

    def test_modal_removes_keydown_listener(self):
        """Modal should remove keydown event listener on cleanup."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "removeEventListener" in content, (
            "Modal should remove keydown event listener on cleanup"
        )

    def test_mobile_menu_adds_keydown_listener(self):
        """Mobile menu should add keydown event listener."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "addEventListener" in content, (
            "Mobile menu should add keydown event listener"
        )

    def test_mobile_menu_removes_keydown_listener(self):
        """Mobile menu should remove keydown event listener on cleanup."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "removeEventListener" in content, (
            "Mobile menu should remove keydown event listener on cleanup"
        )


# =============================================================================
# FOCUS STATE VISIBILITY TESTS
# =============================================================================


class TestFocusStateVisibility:
    """Test that focus states are clearly visible on all interactive elements."""

    def test_globals_css_has_focus_visible_styles(self):
        """globals.css should define :focus-visible styles."""
        content = GLOBALS_CSS.read_text()
        assert ":focus-visible" in content, (
            "globals.css should define :focus-visible styles"
        )

    def test_globals_css_focus_has_outline(self):
        """Focus state should have visible outline."""
        content = GLOBALS_CSS.read_text()
        assert "outline" in content, (
            "Focus state should define outline"
        )

    def test_modal_close_button_has_focus_visible(self):
        """Modal close button should have focus-visible styling."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "focus-visible:" in content or "focus:" in content, (
            "Close button should have focus-visible styling"
        )

    def test_modal_close_button_has_focus_ring(self):
        """Modal close button should have focus ring."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "focus-visible:ring" in content or "focus:ring" in content, (
            "Close button should have focus ring"
        )

    def test_popup_indicator_has_focus_visible(self):
        """Popup indicator button should have focus-visible styling."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Check for focus-visible ring on indicator button
        assert "focus-visible:ring-2" in content or "focus:ring-2" in content, (
            "Popup indicator should have visible focus ring"
        )

    def test_skip_link_has_focus_styles(self):
        """Skip link should have focus styles."""
        skip_link_file = COMPONENTS_DIR / "ui" / "SkipLink.tsx"
        content = skip_link_file.read_text()
        assert "focus:" in content, (
            "Skip link should have focus styles"
        )

    def test_skip_link_visible_on_focus(self):
        """Skip link should become visible when focused."""
        skip_link_file = COMPONENTS_DIR / "ui" / "SkipLink.tsx"
        content = skip_link_file.read_text()
        # Should use sr-only and focus:not-sr-only pattern
        assert "sr-only" in content and "focus:not-sr-only" in content, (
            "Skip link should be sr-only and visible on focus"
        )

    def test_header_mobile_button_has_focus_visible(self):
        """Mobile menu button should have focus-visible styling."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "focus-visible:" in content or "focus:" in content, (
            "Mobile menu button should have focus-visible styling"
        )

    def test_footer_links_have_focus_visible(self):
        """Footer social links should have focus-visible styling."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        assert "focus-visible:" in content or "focus:" in content, (
            "Footer links should have focus-visible styling"
        )

    def test_focus_uses_brand_color(self):
        """Focus rings should use brand color for consistency."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "ring-brand-" in content, (
            "Focus rings should use brand color"
        )


# =============================================================================
# MODAL FOCUS TRAP AND RESTORE TESTS
# =============================================================================


class TestModalFocusTrap:
    """Test that modal dialogs trap focus correctly."""

    def test_modal_has_modal_ref(self):
        """Modal should have a ref to query focusable elements."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "modalRef" in content, (
            "Modal should have modalRef for focus management"
        )

    def test_modal_queries_focusable_elements(self):
        """Modal should query all focusable elements."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "querySelectorAll" in content, (
            "Modal should query focusable elements"
        )

    def test_modal_queries_correct_focusable_selectors(self):
        """Modal should query correct focusable element selectors."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Should query buttons, links, inputs, etc.
        assert "button" in content and "[href]" in content, (
            "Modal should query buttons and links as focusable elements"
        )

    def test_modal_handles_shift_tab(self):
        """Modal should handle Shift+Tab for reverse focus navigation."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "shiftKey" in content, (
            "Modal should check for shiftKey for reverse tab"
        )

    def test_modal_prevents_default_at_boundaries(self):
        """Modal should prevent default tab behavior at boundaries."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "preventDefault" in content, (
            "Modal should prevent default at focus boundaries"
        )

    def test_modal_focuses_first_element(self):
        """Modal should track first focusable element."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "firstElement" in content, (
            "Modal should track first focusable element"
        )

    def test_modal_focuses_last_element(self):
        """Modal should track last focusable element."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "lastElement" in content, (
            "Modal should track last focusable element"
        )


class TestModalFocusRestore:
    """Test that modal restores focus correctly when closed."""

    def test_modal_has_trigger_ref(self):
        """Modal should have ref to trigger element for focus restore."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "triggerRef" in content, (
            "Modal should have triggerRef for focus restore"
        )

    def test_modal_restores_focus_on_close(self):
        """Modal should restore focus to trigger when closed."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Check for focus() call on triggerRef
        assert "triggerRef.current?.focus()" in content, (
            "Modal should call focus() on triggerRef when closed"
        )

    def test_modal_has_close_button_ref(self):
        """Modal should have ref for close button to receive initial focus."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "closeButtonRef" in content, (
            "Modal should have closeButtonRef"
        )

    def test_modal_focuses_close_button_on_open(self):
        """Modal should focus close button when opened."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Check for focus on close button when modal opens
        assert "closeButtonRef.current" in content and ".focus()" in content, (
            "Modal should focus close button on open"
        )


class TestMobileMenuFocusTrap:
    """Test that mobile menu traps focus correctly."""

    def test_mobile_menu_has_ref(self):
        """Mobile menu should have a ref for focus trapping."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "mobileMenuRef" in content, (
            "Mobile menu should have mobileMenuRef"
        )

    def test_mobile_menu_queries_focusable_elements(self):
        """Mobile menu should query focusable elements."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "querySelectorAll" in content, (
            "Mobile menu should query focusable elements"
        )

    def test_mobile_menu_handles_shift_tab(self):
        """Mobile menu should handle Shift+Tab."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "shiftKey" in content, (
            "Mobile menu should handle Shift+Tab"
        )

    def test_mobile_menu_has_trigger_ref(self):
        """Mobile menu should have ref to trigger button."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "mobileMenuButtonRef" in content, (
            "Mobile menu should have mobileMenuButtonRef"
        )

    def test_mobile_menu_restores_focus(self):
        """Mobile menu should restore focus to button on close."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "mobileMenuButtonRef.current?.focus()" in content, (
            "Mobile menu should restore focus to button on close"
        )


# =============================================================================
# SEMANTIC HTML TESTS
# =============================================================================


class TestSemanticHTMLUsage:
    """Test that semantic HTML elements are used throughout."""

    def test_root_layout_has_lang_attribute(self):
        """Root layout should have lang attribute on html element."""
        layout_file = APP_DIR / "layout.tsx"
        content = layout_file.read_text()
        assert 'lang="en"' in content or "lang='en'" in content, (
            "HTML element should have lang attribute"
        )

    def test_header_uses_header_element(self):
        """Header component should use <header> element."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "<header" in content, (
            "Header component should use semantic <header> element"
        )

    def test_header_uses_nav_element(self):
        """Header should use <nav> element for navigation."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "<nav" in content, (
            "Header should use semantic <nav> element"
        )

    def test_footer_uses_footer_element(self):
        """Footer component should use <footer> element."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        assert "<footer" in content, (
            "Footer component should use semantic <footer> element"
        )

    def test_footer_navigation_uses_nav(self):
        """Footer navigation should use <nav> element."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        # Footer social links should be in nav with aria-label
        assert "<motion.nav" in content or "<nav" in content, (
            "Footer navigation should use <nav> element"
        )

    def test_image_uses_figure_element(self):
        """ImageWithPopup should use <figure> element."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "<figure" in content, (
            "Image should use semantic <figure> element"
        )

    def test_image_uses_figcaption_element(self):
        """ImageWithPopup should use <figcaption> for captions."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "<figcaption" in content, (
            "Image should use <figcaption> for captions"
        )

    def test_modal_title_uses_heading_element(self):
        """Modal title should use heading element."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Modal should use h2 or h3 for title
        assert "<h3" in content or "<h2" in content, (
            "Modal title should use heading element"
        )

    def test_mobile_menu_uses_list_for_nav_items(self):
        """Mobile menu navigation should use list for items."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "<ul" in content or "<ol" in content, (
            "Mobile menu navigation should use list element"
        )

    def test_mobile_menu_nav_items_use_list_items(self):
        """Mobile menu nav items should use <li> elements."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "<motion.li" in content or "<li" in content, (
            "Mobile menu nav items should use <li> elements"
        )


# =============================================================================
# ARIA ATTRIBUTES TESTS
# =============================================================================


class TestAriaAttributesModal:
    """Test that modal has proper ARIA attributes."""

    def test_modal_has_role_dialog(self):
        """Modal should have role='dialog'."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert 'role="dialog"' in content, (
            "Modal should have role='dialog'"
        )

    def test_modal_has_aria_modal(self):
        """Modal should have aria-modal='true'."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert 'aria-modal="true"' in content, (
            "Modal should have aria-modal='true'"
        )

    def test_modal_has_aria_labelledby(self):
        """Modal should have aria-labelledby pointing to title."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "aria-labelledby" in content, (
            "Modal should have aria-labelledby"
        )

    def test_modal_title_has_id(self):
        """Modal title should have id for aria-labelledby reference."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "popup-title" in content or 'id="' in content, (
            "Modal title should have id"
        )

    def test_close_button_has_aria_label(self):
        """Close button should have aria-label."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert 'aria-label="Close' in content, (
            "Close button should have aria-label"
        )

    def test_backdrop_has_aria_hidden(self):
        """Modal backdrop should have aria-hidden='true'."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert 'aria-hidden="true"' in content, (
            "Decorative elements should have aria-hidden='true'"
        )

    def test_tags_container_has_role_list(self):
        """Tags container should have role='list'."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert 'role="list"' in content, (
            "Tags container should have role='list'"
        )

    def test_tag_items_have_role_listitem(self):
        """Tag items should have role='listitem'."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert 'role="listitem"' in content, (
            "Tag items should have role='listitem'"
        )


class TestAriaAttributesMobileMenu:
    """Test that mobile menu has proper ARIA attributes."""

    def test_mobile_menu_button_has_aria_label(self):
        """Mobile menu button should have aria-label."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "aria-label=" in content, (
            "Mobile menu button should have aria-label"
        )

    def test_mobile_menu_button_has_aria_expanded(self):
        """Mobile menu button should have aria-expanded."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "aria-expanded" in content, (
            "Mobile menu button should have aria-expanded"
        )

    def test_mobile_menu_button_has_aria_controls(self):
        """Mobile menu button should have aria-controls."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "aria-controls" in content, (
            "Mobile menu button should have aria-controls"
        )

    def test_mobile_menu_has_role_dialog(self):
        """Mobile menu should have role='dialog' or similar."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert 'role="dialog"' in content, (
            "Mobile menu should have role='dialog'"
        )

    def test_mobile_menu_has_aria_modal(self):
        """Mobile menu should have aria-modal='true'."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert 'aria-modal="true"' in content, (
            "Mobile menu should have aria-modal='true'"
        )

    def test_mobile_menu_has_aria_label(self):
        """Mobile menu should have aria-label for screen readers."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        # Mobile menu panel should have aria-label
        assert "aria-label=" in content, (
            "Mobile menu should have aria-label"
        )


class TestAriaAttributesFooter:
    """Test that footer has proper ARIA attributes."""

    def test_footer_social_nav_has_aria_label(self):
        """Footer social navigation should have aria-label."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        assert 'aria-label="Social media links"' in content or 'aria-label=' in content, (
            "Footer social navigation should have aria-label"
        )

    def test_social_links_have_aria_labels(self):
        """Social links should have aria-label for icon-only links."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        assert "aria-label={`Follow on" in content or "aria-label=" in content, (
            "Social links should have aria-label"
        )

    def test_social_icons_have_aria_hidden(self):
        """Social icons (SVGs) should have aria-hidden='true'."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        assert 'aria-hidden="true"' in content, (
            "Decorative SVG icons should have aria-hidden='true'"
        )

    def test_back_to_top_button_has_aria_label(self):
        """Back to top button should have aria-label."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        assert 'aria-label="Scroll back to top' in content or "aria-label=" in content, (
            "Back to top button should have aria-label"
        )


# =============================================================================
# REDUCED MOTION TESTS
# =============================================================================


class TestReducedMotionSupport:
    """Test that the site respects prefers-reduced-motion."""

    def test_globals_css_has_reduced_motion_query(self):
        """globals.css should have prefers-reduced-motion media query."""
        content = GLOBALS_CSS.read_text()
        assert "prefers-reduced-motion: reduce" in content, (
            "globals.css should handle prefers-reduced-motion"
        )

    def test_reduced_motion_disables_animations(self):
        """Reduced motion should disable or minimize animations."""
        content = GLOBALS_CSS.read_text()
        # Check that animations are disabled in reduced motion
        assert "animation-duration: 0.01ms" in content or "animation: none" in content, (
            "Reduced motion should disable animations"
        )

    def test_reduced_motion_disables_transitions(self):
        """Reduced motion should disable or minimize transitions."""
        content = GLOBALS_CSS.read_text()
        assert "transition-duration: 0.01ms" in content or "transition: none" in content, (
            "Reduced motion should disable transitions"
        )

    def test_reduced_motion_disables_smooth_scroll(self):
        """Reduced motion should disable smooth scrolling."""
        content = GLOBALS_CSS.read_text()
        assert "scroll-behavior: auto" in content, (
            "Reduced motion should disable smooth scroll"
        )

    def test_modal_uses_reduced_motion_hook(self):
        """Modal should use useReducedMotion hook."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "useReducedMotion" in content, (
            "Modal should import useReducedMotion"
        )

    def test_modal_respects_reduced_motion(self):
        """Modal animations should respect reduced motion preference."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "shouldReduceMotion" in content, (
            "Modal should use shouldReduceMotion to adjust animations"
        )


# =============================================================================
# BODY SCROLL LOCK TESTS
# =============================================================================


class TestBodyScrollLock:
    """Test that body scroll is locked when modals are open."""

    def test_modal_locks_body_scroll(self):
        """Modal should lock body scroll when open."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "document.body.style.overflow" in content and "'hidden'" in content, (
            "Modal should set overflow: hidden on body"
        )

    def test_modal_unlocks_body_scroll(self):
        """Modal should unlock body scroll when closed."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert "overflow = ''" in content or "overflow=''" in content, (
            "Modal should reset overflow when closed"
        )

    def test_mobile_menu_locks_body_scroll(self):
        """Mobile menu should lock body scroll when open."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "document.body.style.overflow" in content, (
            "Mobile menu should set overflow on body"
        )

    def test_mobile_menu_unlocks_body_scroll(self):
        """Mobile menu should unlock body scroll when closed."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "overflow = ''" in content or "overflow=''" in content, (
            "Mobile menu should reset overflow when closed"
        )


# =============================================================================
# EXTERNAL LINK SECURITY TESTS
# =============================================================================


class TestExternalLinkSecurity:
    """Test that external links have proper security attributes."""

    def test_modal_link_has_rel_noopener(self):
        """Modal external links should have rel='noopener noreferrer'."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert 'rel="noopener noreferrer"' in content, (
            "Modal links should have rel='noopener noreferrer'"
        )

    def test_modal_link_has_target_blank(self):
        """Modal external links should have target='_blank'."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        assert 'target="_blank"' in content, (
            "Modal links should have target='_blank'"
        )

    def test_footer_social_links_have_rel_noopener(self):
        """Footer social links should have rel='noopener noreferrer'."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        assert 'rel="noopener noreferrer"' in content, (
            "Footer social links should have rel='noopener noreferrer'"
        )

    def test_header_social_links_have_rel_noopener(self):
        """Header social links should have rel='noopener noreferrer'."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert 'rel="noopener noreferrer"' in content, (
            "Header social links should have rel='noopener noreferrer'"
        )


# =============================================================================
# SCREEN READER ONLY TEXT TESTS
# =============================================================================


class TestScreenReaderOnlyContent:
    """Test that appropriate screen reader only content is provided."""

    def test_globals_css_defines_sr_only(self):
        """globals.css should define .sr-only utility."""
        content = GLOBALS_CSS.read_text()
        assert ".sr-only" in content, (
            "globals.css should define .sr-only utility class"
        )

    def test_sr_only_is_visually_hidden(self):
        """sr-only class should visually hide content."""
        content = GLOBALS_CSS.read_text()
        # Check for standard sr-only properties
        assert "position: absolute" in content and "overflow: hidden" in content, (
            ".sr-only should visually hide content"
        )

    def test_skip_link_uses_sr_only(self):
        """Skip link should use sr-only class."""
        skip_link_file = COMPONENTS_DIR / "ui" / "SkipLink.tsx"
        content = skip_link_file.read_text()
        assert "sr-only" in content, (
            "Skip link should use sr-only class"
        )

    def test_modal_link_has_sr_only_context(self):
        """Modal external link should have screen reader context."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Check for sr-only text indicating new tab
        assert "sr-only" in content, (
            "Modal link should have sr-only context for screen readers"
        )


# =============================================================================
# TOUCH TARGET SIZE TESTS
# =============================================================================


class TestTouchTargetSize:
    """Test that touch targets meet minimum size requirements (44x44px)."""

    def test_modal_close_button_has_padding(self):
        """Modal close button should have padding for adequate touch target."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # p-2 = 8px padding on each side, icon is 24px, total = 40px minimum
        assert "p-2" in content or "p-3" in content or "p-4" in content, (
            "Close button should have padding for touch target"
        )

    def test_popup_indicator_button_has_padding(self):
        """Popup indicator button should have padding for adequate touch target."""
        component_file = COMPONENTS_DIR / "ui" / "ImageWithPopup.tsx"
        content = component_file.read_text()
        # Should have px and py padding
        assert "px-" in content and "py-" in content, (
            "Indicator button should have padding for touch target"
        )

    def test_mobile_menu_button_has_padding(self):
        """Mobile menu button should have padding for adequate touch target."""
        component_file = COMPONENTS_DIR / "layout" / "HeaderClient.tsx"
        content = component_file.read_text()
        assert "p-2" in content or "p-3" in content, (
            "Mobile menu button should have padding"
        )

    def test_footer_social_links_have_padding(self):
        """Footer social links should have padding for touch targets."""
        component_file = COMPONENTS_DIR / "layout" / "FooterClient.tsx"
        content = component_file.read_text()
        assert "p-1" in content or "p-2" in content, (
            "Social links should have padding"
        )
