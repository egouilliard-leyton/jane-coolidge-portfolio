"""
Tests for T-019: Reduced motion preference support

These tests verify that all animations respect the prefers-reduced-motion media query:
- All animation components check useReducedMotion hook
- CSS animations have reduced motion fallbacks
- Page transitions adapt to reduced motion preference
- Modal animations are simplified for reduced motion users
- Scroll animations are disabled for reduced motion
"""

from pathlib import Path
import re


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
ANIMATIONS_FILE = PROJECT_ROOT / "components" / "ui" / "animations.tsx"
PAGE_TRANSITION_FILE = PROJECT_ROOT / "components" / "ui" / "PageTransition.tsx"
ANIMATED_SECTIONS_FILE = PROJECT_ROOT / "components" / "home" / "AnimatedSections.tsx"
SITE_LAYOUT_CLIENT_FILE = PROJECT_ROOT / "app" / "(site)" / "SiteLayoutClient.tsx"
IMAGE_WITH_POPUP_FILE = PROJECT_ROOT / "components" / "ui" / "ImageWithPopup.tsx"
GLOBALS_CSS_FILE = PROJECT_ROOT / "app" / "globals.css"


class TestAnimationsReducedMotion:
    """Test reduced motion support in animations.tsx."""

    def test_imports_use_reduced_motion(self):
        """animations.tsx should import useReducedMotion."""
        content = ANIMATIONS_FILE.read_text()
        assert "useReducedMotion" in content, (
            "animations.tsx should import useReducedMotion hook"
        )

    def test_scroll_reveal_checks_reduced_motion(self):
        """ScrollReveal should check reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        scroll_reveal_match = re.search(
            r"export function ScrollReveal\([^)]*\)\s*\{([\s\S]*?)(?=\nexport)",
            content
        )
        assert scroll_reveal_match, "ScrollReveal function should exist"
        func_content = scroll_reveal_match.group(1)
        assert "useReducedMotion" in func_content or "shouldReduceMotion" in func_content, (
            "ScrollReveal should use useReducedMotion hook"
        )

    def test_scroll_reveal_returns_static_for_reduced_motion(self):
        """ScrollReveal should return static element for reduced motion users."""
        content = ANIMATIONS_FILE.read_text()
        scroll_reveal_match = re.search(
            r"export function ScrollReveal\([^)]*\)\s*\{([\s\S]*?)(?=\nexport)",
            content
        )
        assert scroll_reveal_match, "ScrollReveal function should exist"
        func_content = scroll_reveal_match.group(1)
        # Should have conditional return for reduced motion
        assert "if (shouldReduceMotion)" in func_content, (
            "ScrollReveal should have conditional return for reduced motion"
        )

    def test_stagger_reveal_checks_reduced_motion(self):
        """StaggerReveal should check reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        stagger_match = re.search(
            r"export function StaggerReveal\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function StaggerItem)",
            content
        )
        assert stagger_match, "StaggerReveal function should exist"
        func_content = stagger_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "StaggerReveal should check reduced motion"
        )

    def test_stagger_item_checks_reduced_motion(self):
        """StaggerItem should check reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        stagger_item_match = re.search(
            r"export function StaggerItem\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function HoverCard)",
            content
        )
        assert stagger_item_match, "StaggerItem function should exist"
        func_content = stagger_item_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "StaggerItem should check reduced motion"
        )

    def test_hover_card_checks_reduced_motion(self):
        """HoverCard should check reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        hover_match = re.search(
            r"export function HoverCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function|\/\*\*\n \* Parallax)",
            content
        )
        assert hover_match, "HoverCard function should exist"
        func_content = hover_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "HoverCard should check reduced motion"
        )

    def test_parallax_reveal_checks_reduced_motion(self):
        """ParallaxReveal should check reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        parallax_match = re.search(
            r"export function ParallaxReveal\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function TextReveal)",
            content
        )
        assert parallax_match, "ParallaxReveal function should exist"
        func_content = parallax_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "ParallaxReveal should check reduced motion"
        )

    def test_text_reveal_checks_reduced_motion(self):
        """TextReveal should check reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        text_match = re.search(
            r"export function TextReveal\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function FloatingElement)",
            content
        )
        assert text_match, "TextReveal function should exist"
        func_content = text_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "TextReveal should check reduced motion"
        )

    def test_floating_element_checks_reduced_motion(self):
        """FloatingElement should check reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        floating_match = re.search(
            r"export function FloatingElement\([^)]*\)\s*\{([\s\S]*?)(?=\Z)",
            content
        )
        assert floating_match, "FloatingElement function should exist"
        func_content = floating_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "FloatingElement should check reduced motion"
        )


class TestPageTransitionReducedMotion:
    """Test reduced motion support in PageTransition components."""

    def test_page_transition_imports_use_reduced_motion(self):
        """PageTransition.tsx should import useReducedMotion."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "useReducedMotion" in content, (
            "PageTransition.tsx should import useReducedMotion"
        )

    def test_page_transition_defines_reduced_motion_variants(self):
        """PageTransition should define reduced motion variants."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "reducedMotionVariants" in content, (
            "PageTransition should define reducedMotionVariants"
        )

    def test_page_transition_selects_correct_variants(self):
        """PageTransition should select variants based on preference."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "shouldReduceMotion" in content, (
            "PageTransition should use shouldReduceMotion variable"
        )

    def test_page_transition_has_shorter_duration_for_reduced_motion(self):
        """PageTransition should have shorter duration for reduced motion."""
        content = PAGE_TRANSITION_FILE.read_text()
        # Look for conditional duration
        pattern = r"shouldReduceMotion\s*\?\s*([\d.]+)\s*:\s*([\d.]+)"
        match = re.search(pattern, content)
        assert match, "Should have conditional duration"
        reduced_duration = float(match.group(1))
        normal_duration = float(match.group(2))
        assert reduced_duration < normal_duration, (
            f"Reduced motion duration ({reduced_duration}) should be less than normal ({normal_duration})"
        )

    def test_slide_transition_respects_reduced_motion(self):
        """SlideTransition should respect reduced motion preference."""
        content = PAGE_TRANSITION_FILE.read_text()
        slide_match = re.search(
            r"export function SlideTransition\([^)]*\)\s*\{([\s\S]*?)(?=\Z)",
            content
        )
        assert slide_match, "SlideTransition should exist"
        func_content = slide_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "SlideTransition should check reduced motion"
        )

    def test_fade_transition_respects_reduced_motion(self):
        """FadeTransition should respect reduced motion preference."""
        content = PAGE_TRANSITION_FILE.read_text()
        fade_match = re.search(
            r"export function FadeTransition\([^)]*\)\s*\{([\s\S]*?)(?=\nexport|\n\/\*\*)",
            content
        )
        assert fade_match, "FadeTransition should exist"
        func_content = fade_match.group(1)
        assert "shouldReduceMotion" in func_content or "useReducedMotion" in func_content, (
            "FadeTransition should check reduced motion"
        )


class TestSiteLayoutReducedMotion:
    """Test reduced motion support in SiteLayoutClient."""

    def test_site_layout_imports_use_reduced_motion(self):
        """SiteLayoutClient should import useReducedMotion."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "useReducedMotion" in content, (
            "SiteLayoutClient should import useReducedMotion"
        )

    def test_site_layout_checks_reduced_motion(self):
        """SiteLayoutClient should check reduced motion preference."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "shouldReduceMotion" in content, (
            "SiteLayoutClient should use shouldReduceMotion variable"
        )

    def test_site_layout_removes_y_translation_for_reduced_motion(self):
        """SiteLayoutClient should not have y translation for reduced motion."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        # Check for conditional initial state
        assert "shouldReduceMotion" in content and "opacity" in content, (
            "SiteLayoutClient should have conditional animation based on reduced motion"
        )


class TestModalReducedMotion:
    """Test reduced motion support in ImageWithPopup modal."""

    def test_modal_imports_use_reduced_motion(self):
        """ImageWithPopup should import useReducedMotion."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "useReducedMotion" in content, (
            "ImageWithPopup should import useReducedMotion"
        )

    def test_modal_checks_reduced_motion(self):
        """ImageWithPopup should check reduced motion preference."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "shouldReduceMotion" in content, (
            "ImageWithPopup should use shouldReduceMotion"
        )

    def test_modal_scale_disabled_for_reduced_motion(self):
        """Modal scale should be disabled for reduced motion."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Should have conditional scale
        pattern = r"shouldReduceMotion\s*\?\s*1\s*:"
        assert re.search(pattern, content), (
            "Modal scale should be 1 (disabled) for reduced motion"
        )

    def test_modal_y_disabled_for_reduced_motion(self):
        """Modal y translation should be disabled for reduced motion."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Should have conditional y
        pattern = r"shouldReduceMotion\s*\?\s*0\s*:"
        assert re.search(pattern, content), (
            "Modal y should be 0 (disabled) for reduced motion"
        )

    def test_modal_bounce_disabled_for_reduced_motion(self):
        """Modal spring bounce should be disabled for reduced motion."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Should have conditional bounce
        pattern = r"bounce:\s*shouldReduceMotion\s*\?\s*0"
        assert re.search(pattern, content), (
            "Modal bounce should be 0 for reduced motion"
        )


class TestAnimatedSectionsReducedMotion:
    """Test reduced motion support in AnimatedSections."""

    def test_imports_use_reduced_motion(self):
        """AnimatedSections should import useReducedMotion."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "useReducedMotion" in content, (
            "AnimatedSections should import useReducedMotion"
        )

    def test_hero_content_checks_reduced_motion(self):
        """AnimatedHeroContent should check reduced motion."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        hero_match = re.search(
            r"export function AnimatedHeroContent\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert hero_match, "AnimatedHeroContent should exist"
        func_content = hero_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "AnimatedHeroContent should check reduced motion"
        )

    def test_post_card_checks_reduced_motion(self):
        """AnimatedPostCard should check reduced motion."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        post_match = re.search(
            r"export function AnimatedPostCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert post_match, "AnimatedPostCard should exist"
        func_content = post_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "AnimatedPostCard should check reduced motion"
        )

    def test_project_card_checks_reduced_motion(self):
        """AnimatedProjectCard should check reduced motion."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        project_match = re.search(
            r"export function AnimatedProjectCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert project_match, "AnimatedProjectCard should exist"
        func_content = project_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "AnimatedProjectCard should check reduced motion"
        )

    def test_cta_checks_reduced_motion(self):
        """AnimatedCTA should check reduced motion."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        cta_match = re.search(
            r"export function AnimatedCTA\([^)]*\)\s*\{([\s\S]*?)$",
            content
        )
        assert cta_match, "AnimatedCTA should exist"
        func_content = cta_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "AnimatedCTA should check reduced motion"
        )


class TestCSSReducedMotion:
    """Test CSS-level reduced motion support in globals.css."""

    def test_has_reduced_motion_media_query(self):
        """globals.css should have prefers-reduced-motion media query."""
        content = GLOBALS_CSS_FILE.read_text()
        assert "@media (prefers-reduced-motion: reduce)" in content, (
            "globals.css should have reduced motion media query"
        )

    def test_disables_animations_for_reduced_motion(self):
        """Reduced motion styles should disable animations."""
        content = GLOBALS_CSS_FILE.read_text()
        # Look within reduced motion media query
        reduced_match = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{([\s\S]*?)\n\}",
            content
        )
        assert reduced_match, "Should have reduced motion media query"
        reduced_content = reduced_match.group(1)
        assert "animation-duration: 0.01ms" in reduced_content or "animation: none" in reduced_content, (
            "Should disable animations in reduced motion"
        )

    def test_disables_transitions_for_reduced_motion(self):
        """Reduced motion styles should minimize transitions."""
        content = GLOBALS_CSS_FILE.read_text()
        reduced_match = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{([\s\S]*?)\n\}",
            content
        )
        assert reduced_match, "Should have reduced motion media query"
        reduced_content = reduced_match.group(1)
        assert "transition-duration: 0.01ms" in reduced_content, (
            "Should minimize transitions in reduced motion"
        )

    def test_disables_smooth_scroll_for_reduced_motion(self):
        """Reduced motion should disable smooth scrolling."""
        content = GLOBALS_CSS_FILE.read_text()
        reduced_match = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{([\s\S]*?)\n\}",
            content
        )
        assert reduced_match, "Should have reduced motion media query"
        reduced_content = reduced_match.group(1)
        assert "scroll-behavior: auto" in reduced_content, (
            "Should disable smooth scroll in reduced motion"
        )

    def test_disables_parallax_for_reduced_motion(self):
        """Reduced motion should disable parallax effects."""
        content = GLOBALS_CSS_FILE.read_text()
        reduced_match = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{([\s\S]*?)\n\}",
            content
        )
        assert reduced_match, "Should have reduced motion media query"
        reduced_content = reduced_match.group(1)
        assert ".parallax" in reduced_content, (
            "Should disable parallax in reduced motion"
        )

    def test_disables_image_zoom_for_reduced_motion(self):
        """Reduced motion should disable image zoom on hover."""
        content = GLOBALS_CSS_FILE.read_text()
        reduced_match = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{([\s\S]*?)\n\}",
            content
        )
        assert reduced_match, "Should have reduced motion media query"
        reduced_content = reduced_match.group(1)
        assert ".img-zoom" in reduced_content or "img" in reduced_content, (
            "Should disable image zoom in reduced motion"
        )

    def test_disables_skeleton_animation_for_reduced_motion(self):
        """Reduced motion should disable skeleton loading animation."""
        content = GLOBALS_CSS_FILE.read_text()
        reduced_match = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{([\s\S]*?)\n\}",
            content
        )
        assert reduced_match, "Should have reduced motion media query"
        reduced_content = reduced_match.group(1)
        assert ".skeleton" in reduced_content, (
            "Should disable skeleton animation in reduced motion"
        )

    def test_ensures_content_visibility_for_reduced_motion(self):
        """Reduced motion should ensure content is immediately visible."""
        content = GLOBALS_CSS_FILE.read_text()
        reduced_match = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{([\s\S]*?)\n\}",
            content
        )
        assert reduced_match, "Should have reduced motion media query"
        reduced_content = reduced_match.group(1)
        assert "opacity: 1" in reduced_content, (
            "Should ensure content is visible in reduced motion"
        )


class TestSmoothScrollForNoPreference:
    """Test smooth scroll is enabled for users without reduced motion preference."""

    def test_has_no_preference_media_query(self):
        """globals.css should have no-preference media query."""
        content = GLOBALS_CSS_FILE.read_text()
        assert "@media (prefers-reduced-motion: no-preference)" in content, (
            "globals.css should have no-preference media query"
        )

    def test_enables_smooth_scroll_for_no_preference(self):
        """Smooth scroll should be enabled for no-preference users."""
        content = GLOBALS_CSS_FILE.read_text()
        no_pref_match = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*no-preference\)\s*\{([\s\S]*?)\n\}",
            content
        )
        assert no_pref_match, "Should have no-preference media query"
        no_pref_content = no_pref_match.group(1)
        assert "scroll-behavior: smooth" in no_pref_content, (
            "Should enable smooth scroll for no-preference users"
        )


class TestReducedMotionFallbackBehavior:
    """Test that reduced motion fallbacks provide equivalent functionality."""

    def test_scroll_reveal_fallback_renders_children(self):
        """ScrollReveal fallback should render children."""
        content = ANIMATIONS_FILE.read_text()
        # Look for fallback return with children
        # The pattern has if (shouldReduceMotion) { ... return <div ...>{children}</div> }
        fallback_pattern = r"if \(shouldReduceMotion\)[\s\S]*?return[\s\S]*?\{children\}"
        assert re.search(fallback_pattern, content), (
            "ScrollReveal fallback should render children"
        )

    def test_hover_card_fallback_renders_children(self):
        """HoverCard fallback should render children."""
        content = ANIMATIONS_FILE.read_text()
        hover_match = re.search(
            r"export function HoverCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function|\/\*\*\n \* Parallax)",
            content
        )
        assert hover_match, "HoverCard should exist"
        func_content = hover_match.group(1)
        # Should have return with children in reduced motion block
        assert "{children}" in func_content and "shouldReduceMotion" in func_content, (
            "HoverCard fallback should render children"
        )

    def test_animated_components_return_static_elements(self):
        """Animated components should return static elements for reduced motion."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Check that there are conditional returns for reduced motion
        returns_count = len(re.findall(r"if \(shouldReduceMotion\)\s*\{\s*return", content))
        assert returns_count >= 3, (
            f"Should have multiple conditional returns for reduced motion. Found {returns_count}"
        )
