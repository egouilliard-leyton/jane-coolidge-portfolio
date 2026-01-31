"""
Tests for T-011: Build ImageWithPopup component with modal interaction

These tests verify that the ImageWithPopup component is properly implemented according to requirements:
- Component accepts image data and popup content reference
- Visual indicator (icon/badge) shows image has popup
- Modal opens with smooth scale/fade animation on click
- Modal displays title, description, tags, and optional link
- Click outside or ESC key closes modal
- Close button is visible and functional
- Works with both mouse and touch events
- Focus is trapped within modal when open

Acceptance Criteria:
- Component accepts image data and popup content reference
- Visual indicator (icon/badge) shows image has popup
- Modal opens with smooth scale/fade animation on click
- Modal displays title, description, tags, and optional link
- Click outside or ESC key closes modal
- Close button is visible and functional
- Works with both mouse and touch events
- Focus is trapped within modal when open
"""

from pathlib import Path
import re


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
IMAGE_WITH_POPUP_FILE = PROJECT_ROOT / "components" / "ui" / "ImageWithPopup.tsx"


class TestImageWithPopupFileExists:
    """Test that ImageWithPopup component file exists and has proper structure."""

    def test_image_with_popup_component_exists(self):
        """components/ui/ImageWithPopup.tsx should exist."""
        assert IMAGE_WITH_POPUP_FILE.exists(), "components/ui/ImageWithPopup.tsx not found"

    def test_image_with_popup_is_client_component(self):
        """ImageWithPopup.tsx should have 'use client' directive."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "ImageWithPopup should have 'use client' directive"
        )

    def test_image_with_popup_exports_default(self):
        """ImageWithPopup.tsx should export default component."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "export default" in content, (
            "ImageWithPopup.tsx should have default export"
        )


class TestComponentPropsInterface:
    """Test that ImageWithPopup accepts image data and popup content reference."""

    def test_has_props_interface(self):
        """ImageWithPopup should define an ImageWithPopupProps interface."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "ImageWithPopupProps" in content, (
            "ImageWithPopup should define ImageWithPopupProps interface"
        )

    def test_exports_props_interface(self):
        """ImageWithPopupProps interface should be exported."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "export interface ImageWithPopupProps" in content, (
            "ImageWithPopupProps should be exported"
        )

    def test_accepts_image_prop(self):
        """ImageWithPopup should accept 'image' prop."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "image:" in content, (
            "ImageWithPopup should accept image prop"
        )

    def test_accepts_alt_prop(self):
        """ImageWithPopup should accept 'alt' prop for accessibility."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "alt:" in content, (
            "ImageWithPopup should accept alt prop"
        )

    def test_accepts_caption_prop(self):
        """ImageWithPopup should accept optional 'caption' prop."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "caption?" in content or "caption ?" in content, (
            "ImageWithPopup should accept optional caption prop"
        )

    def test_accepts_popup_prop(self):
        """ImageWithPopup should accept 'popup' prop for popup content."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "popup?" in content or "popup ?" in content, (
            "ImageWithPopup should accept optional popup prop"
        )

    def test_accepts_size_prop(self):
        """ImageWithPopup should accept optional 'size' prop."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "size?" in content or "size ?" in content, (
            "ImageWithPopup should accept optional size prop"
        )

    def test_accepts_classname_prop(self):
        """ImageWithPopup should accept optional className prop."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "className?" in content or "className ?" in content, (
            "ImageWithPopup should accept optional className prop"
        )

    def test_imports_types(self):
        """ImageWithPopup should import types from @/types."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "@/types" in content, (
            "ImageWithPopup should import types from @/types"
        )

    def test_imports_popup_content_type(self):
        """ImageWithPopup should import PopupContent type."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "PopupContent" in content, (
            "ImageWithPopup should import PopupContent type"
        )


class TestImageRendering:
    """Test that the image is properly rendered."""

    def test_uses_next_image_component(self):
        """ImageWithPopup should use Next.js Image for optimization."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "ImageWithPopup should import Next.js Image component"
        )
        assert "<Image" in content, "ImageWithPopup should use Image component"

    def test_image_has_width_and_height(self):
        """Image should have width and height props for optimization."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "width=" in content, "Image should have width prop"
        assert "height=" in content, "Image should have height prop"

    def test_image_has_alt_text(self):
        """Image should have alt text."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "alt={alt}" in content or "alt={ alt }" in content, (
            "Image should use alt prop"
        )

    def test_uses_url_for_helper(self):
        """ImageWithPopup should use urlFor helper for Sanity images."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "urlFor" in content, (
            "ImageWithPopup should use urlFor helper for image URLs"
        )
        assert "@/sanity/lib/image" in content, (
            "ImageWithPopup should import urlFor from @/sanity/lib/image"
        )

    def test_renders_figure_element(self):
        """Image should be wrapped in figure element."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<figure" in content, "Image should be wrapped in figure element"

    def test_renders_figcaption_for_caption(self):
        """ImageWithPopup should render figcaption when caption is provided."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<figcaption" in content, (
            "ImageWithPopup should render figcaption for image captions"
        )

    def test_caption_is_conditional(self):
        """Caption should only render when provided."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "caption &&" in content, (
            "Caption should be conditionally rendered"
        )

    def test_handles_size_variations(self):
        """ImageWithPopup should handle different image size options."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "sizeClasses" in content or "size" in content, (
            "ImageWithPopup should handle image size property"
        )


class TestVisualIndicator:
    """Test that visual indicator shows image has popup."""

    def test_has_popup_indicator_button(self):
        """ImageWithPopup should have an indicator button when popup exists."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for button element that serves as indicator
        assert "<motion.button" in content or "<button" in content, (
            "ImageWithPopup should have indicator button"
        )

    def test_indicator_has_aria_label(self):
        """Popup indicator should have aria-label for accessibility."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "aria-label=" in content, (
            "Popup indicator should have aria-label"
        )

    def test_indicator_has_icon(self):
        """Popup indicator should have an icon (svg)."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<svg" in content, (
            "Popup indicator should have an icon"
        )

    def test_indicator_conditional_on_popup(self):
        """Indicator should only show when popup content exists."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "hasPopup" in content, (
            "ImageWithPopup should check if popup exists (hasPopup)"
        )

    def test_indicator_has_styling(self):
        """Popup indicator should have styling classes."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for button styling
        assert "rounded-" in content, (
            "Indicator should have rounded styling"
        )

    def test_indicator_is_focusable(self):
        """Popup indicator should be focusable."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Focus visible ring for accessibility
        assert "focus-visible:" in content or "focus:" in content, (
            "Indicator should have focus styling"
        )


class TestModalInteraction:
    """Test that modal opens and closes properly."""

    def test_has_open_state(self):
        """ImageWithPopup should manage isOpen state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "isOpen" in content, (
            "ImageWithPopup should have isOpen state"
        )

    def test_uses_use_state(self):
        """ImageWithPopup should use useState hook."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "useState" in content, (
            "ImageWithPopup should use useState hook"
        )

    def test_has_open_modal_handler(self):
        """ImageWithPopup should have handler to open modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "openModal" in content or "setIsOpen(true)" in content, (
            "ImageWithPopup should have open modal handler"
        )

    def test_has_close_modal_handler(self):
        """ImageWithPopup should have handler to close modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "closeModal" in content, (
            "ImageWithPopup should have closeModal handler"
        )

    def test_image_click_opens_modal(self):
        """Clicking on image should open modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "onClick" in content, (
            "ImageWithPopup should have onClick handler"
        )

    def test_indicator_click_opens_modal(self):
        """Clicking on indicator button should open modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Indicator button should have onClick
        button_pattern = r"<motion\.button[^>]*onClick"
        assert re.search(button_pattern, content) or "onClick={openModal}" in content, (
            "Indicator button should have onClick handler"
        )


class TestModalAnimation:
    """Test that modal has smooth scale/fade animations."""

    def test_uses_motion_library(self):
        """ImageWithPopup should use motion/react for animations."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "motion/react" in content, (
            "ImageWithPopup should use motion/react for animations"
        )

    def test_imports_animate_presence(self):
        """ImageWithPopup should import AnimatePresence for exit animations."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "AnimatePresence" in content, (
            "ImageWithPopup should import AnimatePresence"
        )

    def test_uses_animate_presence(self):
        """ImageWithPopup should wrap modal with AnimatePresence."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<AnimatePresence>" in content or "<AnimatePresence " in content, (
            "Modal should be wrapped with AnimatePresence"
        )

    def test_uses_motion_div(self):
        """ImageWithPopup should use motion.div for animated modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<motion.div" in content, (
            "ImageWithPopup should use motion.div for modal"
        )

    def test_has_modal_variants(self):
        """ImageWithPopup should define animation variants for modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "modalVariants" in content or "overlayVariants" in content, (
            "ImageWithPopup should define animation variants"
        )

    def test_modal_has_scale_animation(self):
        """Modal should have scale animation."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "scale:" in content or "scale :" in content, (
            "Modal should have scale animation"
        )

    def test_modal_has_opacity_animation(self):
        """Modal should have opacity/fade animation."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "opacity:" in content or "opacity :" in content, (
            "Modal should have opacity animation"
        )

    def test_respects_reduced_motion(self):
        """Modal should respect user's reduced motion preference."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "useReducedMotion" in content or "shouldReduceMotion" in content, (
            "ImageWithPopup should respect reduced motion preference"
        )


class TestModalContent:
    """Test that modal displays title, description, tags, and optional link."""

    def test_modal_renders_title(self):
        """Modal should render popup title."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "popup.title" in content or "popup?.title" in content, (
            "Modal should render popup title"
        )

    def test_title_has_heading_element(self):
        """Title should be rendered as a heading element."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<h3" in content or "<h2" in content, (
            "Title should be a heading element"
        )

    def test_modal_renders_description(self):
        """Modal should render popup description."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "popup.description" in content or "popup?.description" in content, (
            "Modal should render popup description"
        )

    def test_modal_renders_tags(self):
        """Modal should render popup tags."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "popup.tags" in content or "popup?.tags" in content, (
            "Modal should render popup tags"
        )

    def test_tags_are_iterable(self):
        """Tags should be rendered with map."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert ".map(" in content, (
            "Tags should be rendered using map"
        )

    def test_modal_renders_link(self):
        """Modal should render popup link when provided."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "popup.link" in content or "popup?.link" in content, (
            "Modal should render popup link"
        )

    def test_link_is_anchor_element(self):
        """Link should be an anchor element."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<a" in content, (
            "Link should be an anchor element"
        )

    def test_link_opens_in_new_tab(self):
        """External link should open in new tab."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'target="_blank"' in content or "target='_blank'" in content, (
            "Link should open in new tab"
        )

    def test_link_has_security_attributes(self):
        """Link should have noopener noreferrer for security."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'rel="noopener noreferrer"' in content or "rel='noopener noreferrer'" in content, (
            "Link should have rel=noopener noreferrer"
        )

    def test_link_has_custom_text(self):
        """Link should support custom link text."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "linkText" in content, (
            "Link should support custom link text"
        )


class TestModalClose:
    """Test that clicking outside or ESC key closes modal."""

    def test_backdrop_click_closes_modal(self):
        """Clicking on backdrop should close modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for onClick on backdrop that closes modal
        assert "onClick={closeModal}" in content or "onClick={ closeModal }" in content, (
            "Backdrop should have onClick to close modal"
        )

    def test_modal_content_stops_propagation(self):
        """Click on modal content should not close modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "stopPropagation" in content, (
            "Modal content should stop click propagation"
        )

    def test_handles_escape_key(self):
        """ESC key should close modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "Escape" in content, (
            "ImageWithPopup should handle Escape key"
        )

    def test_uses_use_effect_for_keydown(self):
        """ImageWithPopup should use useEffect for keyboard event listener."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "useEffect" in content, (
            "ImageWithPopup should use useEffect"
        )

    def test_adds_keydown_event_listener(self):
        """ImageWithPopup should add keydown event listener."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "addEventListener" in content, (
            "ImageWithPopup should add event listener"
        )

    def test_removes_keydown_event_listener(self):
        """ImageWithPopup should remove keydown event listener on cleanup."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "removeEventListener" in content, (
            "ImageWithPopup should remove event listener"
        )


class TestCloseButton:
    """Test that close button is visible and functional."""

    def test_has_close_button(self):
        """Modal should have a close button."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for close button with aria-label
        assert 'aria-label="Close' in content or "aria-label='Close" in content, (
            "Modal should have close button with aria-label"
        )

    def test_close_button_has_on_click(self):
        """Close button should have onClick handler."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Close button calls closeModal
        assert "onClick={closeModal}" in content, (
            "Close button should have onClick handler calling closeModal"
        )

    def test_close_button_has_icon(self):
        """Close button should have an X icon."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # X icon SVG path (common X pattern is 6 18 and 18 6)
        assert "M6" in content and "18" in content, (
            "Close button should have X icon"
        )

    def test_close_button_is_focusable(self):
        """Close button should be focusable with visible focus indicator."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "closeButtonRef" in content or "focus:" in content, (
            "Close button should be focusable"
        )


class TestTouchEvents:
    """Test that component works with both mouse and touch events."""

    def test_image_is_tappable(self):
        """Image container should be tappable (has role button when popup exists)."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Role is set conditionally via JSX expression
        assert "role={hasPopup ? 'button' : undefined}" in content or 'role={hasPopup ? "button" : undefined}' in content, (
            "Image should have button role when tappable"
        )

    def test_indicator_button_works_for_touch(self):
        """Indicator is a button element which works with touch."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # button elements work naturally with touch
        assert "<motion.button" in content or "<button" in content, (
            "Indicator should be a button for touch support"
        )

    def test_close_button_is_touch_friendly(self):
        """Close button should have adequate touch target size."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for padding on close button (p-2 or similar)
        assert "p-2" in content or "p-3" in content or "p-4" in content, (
            "Close button should have padding for touch target"
        )


class TestFocusTrap:
    """Test that focus is trapped within modal when open."""

    def test_has_modal_ref(self):
        """ImageWithPopup should have a ref for the modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "modalRef" in content, (
            "ImageWithPopup should have modalRef"
        )

    def test_uses_use_ref(self):
        """ImageWithPopup should use useRef hook."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "useRef" in content, (
            "ImageWithPopup should use useRef hook"
        )

    def test_handles_tab_key(self):
        """ImageWithPopup should handle Tab key for focus trapping."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "Tab" in content, (
            "ImageWithPopup should handle Tab key"
        )

    def test_queries_focusable_elements(self):
        """ImageWithPopup should query focusable elements in modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "querySelectorAll" in content, (
            "ImageWithPopup should query focusable elements"
        )

    def test_finds_button_elements(self):
        """Focus trap should find button elements."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "button" in content.lower(), (
            "Focus trap should find button elements"
        )

    def test_prevents_default_tab_behavior(self):
        """Focus trap should prevent default tab behavior at boundaries."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "preventDefault" in content, (
            "Focus trap should prevent default at boundaries"
        )

    def test_focuses_first_element(self):
        """Focus trap should focus first element at end."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "firstElement" in content or ".focus()" in content, (
            "Focus trap should focus first element"
        )

    def test_focuses_last_element(self):
        """Focus trap should focus last element on shift+tab from first."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "lastElement" in content, (
            "Focus trap should handle last element"
        )

    def test_handles_shift_tab(self):
        """Focus trap should handle shift+tab for reverse navigation."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "shiftKey" in content, (
            "Focus trap should handle shift+tab"
        )


class TestModalAccessibility:
    """Test modal accessibility features."""

    def test_modal_has_role_dialog(self):
        """Modal should have role=dialog."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'role="dialog"' in content or "role='dialog'" in content, (
            "Modal should have role=dialog"
        )

    def test_modal_has_aria_modal(self):
        """Modal should have aria-modal=true."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'aria-modal="true"' in content or "aria-modal='true'" in content, (
            "Modal should have aria-modal=true"
        )

    def test_modal_has_aria_labelledby(self):
        """Modal should have aria-labelledby pointing to title."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "aria-labelledby" in content, (
            "Modal should have aria-labelledby"
        )

    def test_title_has_id(self):
        """Title should have id for aria-labelledby reference."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "popup-title" in content or 'id="' in content, (
            "Title should have id for accessibility"
        )

    def test_returns_focus_to_trigger(self):
        """Focus should return to trigger element after closing."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "triggerRef" in content, (
            "ImageWithPopup should track trigger element for focus return"
        )

    def test_focuses_close_button_on_open(self):
        """Close button should receive focus when modal opens."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "closeButtonRef" in content, (
            "ImageWithPopup should have closeButtonRef for initial focus"
        )


class TestBodyScrollLock:
    """Test that body scroll is locked when modal is open."""

    def test_locks_body_scroll(self):
        """Body scroll should be locked when modal is open."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "overflow" in content and "hidden" in content, (
            "Body scroll should be locked (overflow: hidden)"
        )

    def test_unlocks_body_scroll(self):
        """Body scroll should be unlocked when modal is closed."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check that overflow is reset
        assert "overflow = ''" in content or 'overflow = ""' in content, (
            "Body scroll should be unlocked on close"
        )


class TestDarkModeSupport:
    """Test dark mode styling support."""

    def test_has_dark_mode_classes(self):
        """ImageWithPopup should have dark mode styling."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "dark:" in content, (
            "ImageWithPopup should have dark mode styling classes"
        )

    def test_modal_has_dark_mode_background(self):
        """Modal should have dark mode background."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "dark:bg-" in content, (
            "Modal should have dark mode background"
        )

    def test_text_colors_support_dark_mode(self):
        """Text colors should support dark mode."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "dark:text-" in content, (
            "Text colors should have dark mode variants"
        )


class TestBackdropStyling:
    """Test backdrop/overlay styling."""

    def test_has_backdrop(self):
        """Modal should have a backdrop overlay."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "backdrop" in content.lower() or "overlay" in content.lower(), (
            "Modal should have backdrop"
        )

    def test_backdrop_has_blur(self):
        """Backdrop should have blur effect."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "backdrop-blur" in content, (
            "Backdrop should have blur effect"
        )

    def test_backdrop_has_opacity(self):
        """Backdrop should have semi-transparent background."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for bg-black/60 or similar
        assert "bg-black/" in content or "bg-opacity" in content, (
            "Backdrop should have semi-transparent background"
        )


class TestTagsStyling:
    """Test tags display styling."""

    def test_tags_have_container(self):
        """Tags should have a flex container."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "flex-wrap" in content or "flex " in content, (
            "Tags should have flex container"
        )

    def test_tags_have_gap(self):
        """Tags should have gap between them."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "gap-" in content, (
            "Tags should have gap between them"
        )

    def test_tags_have_role_list(self):
        """Tags container should have role=list for accessibility."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'role="list"' in content or "role='list'" in content, (
            "Tags container should have role=list"
        )

    def test_tags_have_role_listitem(self):
        """Individual tags should have role=listitem."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'role="listitem"' in content or "role='listitem'" in content, (
            "Tags should have role=listitem"
        )


class TestIndicatorAnimation:
    """Test indicator button animation."""

    def test_indicator_has_animation_variants(self):
        """Indicator should have animation variants."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "indicatorVariants" in content, (
            "Indicator should have animation variants"
        )

    def test_indicator_has_hover_animation(self):
        """Indicator should have hover animation."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "whileHover" in content, (
            "Indicator should have whileHover animation"
        )

    def test_indicator_has_tap_animation(self):
        """Indicator should have tap/press animation."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "whileTap" in content, (
            "Indicator should have whileTap animation"
        )


class TestEmptyStateHandling:
    """Test handling of missing or empty data."""

    def test_returns_null_without_image_url(self):
        """Component should return null if no image URL can be generated."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "return null" in content, (
            "Component should return null for invalid image"
        )

    def test_handles_missing_popup(self):
        """Component should handle missing popup gracefully."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # hasPopup checks for popup existence
        assert "hasPopup" in content, (
            "Component should check for popup existence"
        )

    def test_popup_requires_title_or_description(self):
        """Popup should require at least title or description."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "popup.title || popup.description" in content or (
            "popup.title" in content and "popup.description" in content
        ), (
            "Popup should require title or description"
        )
