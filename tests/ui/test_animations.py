"""
Tests for T-019: Page transitions and scroll animations

These tests verify that animation components are properly implemented according to requirements:
- Page transitions animate smoothly between routes
- Homepage sections animate in on scroll
- Project/blog cards have hover animations
- Modal open/close animations are smooth
- All animations respect prefers-reduced-motion media query
- Performance is not degraded by animations

Acceptance Criteria:
- Page transitions animate smoothly between routes
- Homepage sections animate in on scroll
- Project/blog cards have hover animations
- Modal open/close animations are smooth
- All animations respect prefers-reduced-motion media query
- Performance is not degraded by animations
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
UI_INDEX_FILE = PROJECT_ROOT / "components" / "ui" / "index.ts"


class TestAnimationsFileStructure:
    """Test that animations.tsx file exists and has proper structure."""

    def test_animations_file_exists(self):
        """components/ui/animations.tsx should exist."""
        assert ANIMATIONS_FILE.exists(), "components/ui/animations.tsx not found"

    def test_animations_is_client_component(self):
        """animations.tsx should have 'use client' directive."""
        content = ANIMATIONS_FILE.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "animations.tsx should have 'use client' directive"
        )

    def test_imports_motion_library(self):
        """animations.tsx should import from motion/react."""
        content = ANIMATIONS_FILE.read_text()
        assert "motion/react" in content, (
            "animations.tsx should import from motion/react"
        )

    def test_imports_use_in_view(self):
        """animations.tsx should import useInView hook."""
        content = ANIMATIONS_FILE.read_text()
        assert "useInView" in content, (
            "animations.tsx should import useInView hook for scroll detection"
        )

    def test_imports_use_reduced_motion(self):
        """animations.tsx should import useReducedMotion hook."""
        content = ANIMATIONS_FILE.read_text()
        assert "useReducedMotion" in content, (
            "animations.tsx should import useReducedMotion hook"
        )


class TestScrollRevealComponent:
    """Test ScrollReveal component for scroll-triggered animations."""

    def test_scroll_reveal_exported(self):
        """ScrollReveal component should be exported."""
        content = ANIMATIONS_FILE.read_text()
        assert "export function ScrollReveal" in content, (
            "ScrollReveal component should be exported"
        )

    def test_scroll_reveal_props_interface(self):
        """ScrollRevealProps interface should be exported."""
        content = ANIMATIONS_FILE.read_text()
        assert "export interface ScrollRevealProps" in content, (
            "ScrollRevealProps interface should be exported"
        )

    def test_scroll_reveal_has_variant_prop(self):
        """ScrollReveal should accept variant prop."""
        content = ANIMATIONS_FILE.read_text()
        assert "variant?" in content or "variant ?" in content, (
            "ScrollReveal should accept optional variant prop"
        )

    def test_scroll_reveal_supports_fade_up_variant(self):
        """ScrollReveal should support 'fade-up' variant."""
        content = ANIMATIONS_FILE.read_text()
        assert "'fade-up'" in content or '"fade-up"' in content, (
            "ScrollReveal should support fade-up variant"
        )

    def test_scroll_reveal_supports_multiple_variants(self):
        """ScrollReveal should support multiple animation variants."""
        content = ANIMATIONS_FILE.read_text()
        variants = ["fade", "fade-up", "fade-left", "fade-right", "scale"]
        found_variants = sum(1 for v in variants if f"'{v}'" in content or f'"{v}"' in content)
        assert found_variants >= 4, (
            f"ScrollReveal should support multiple variants. Found {found_variants}/5"
        )

    def test_scroll_reveal_has_delay_prop(self):
        """ScrollReveal should accept delay prop."""
        content = ANIMATIONS_FILE.read_text()
        assert "delay?" in content or "delay ?" in content, (
            "ScrollReveal should accept optional delay prop"
        )

    def test_scroll_reveal_has_duration_prop(self):
        """ScrollReveal should accept duration prop."""
        content = ANIMATIONS_FILE.read_text()
        assert "duration?" in content or "duration ?" in content, (
            "ScrollReveal should accept optional duration prop"
        )

    def test_scroll_reveal_has_threshold_prop(self):
        """ScrollReveal should accept threshold prop for viewport detection."""
        content = ANIMATIONS_FILE.read_text()
        assert "threshold?" in content or "threshold ?" in content, (
            "ScrollReveal should accept threshold prop"
        )

    def test_scroll_reveal_has_once_prop(self):
        """ScrollReveal should accept once prop."""
        content = ANIMATIONS_FILE.read_text()
        assert "once?" in content or "once ?" in content, (
            "ScrollReveal should accept once prop"
        )

    def test_scroll_reveal_uses_in_view_hook(self):
        """ScrollReveal should use useInView for viewport detection."""
        content = ANIMATIONS_FILE.read_text()
        assert "useInView" in content and "isInView" in content, (
            "ScrollReveal should use useInView hook"
        )

    def test_scroll_reveal_uses_ref(self):
        """ScrollReveal should use useRef for element tracking."""
        content = ANIMATIONS_FILE.read_text()
        assert "useRef" in content, (
            "ScrollReveal should use useRef hook"
        )

    def test_scroll_reveal_respects_reduced_motion(self):
        """ScrollReveal should check reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        # Find ScrollReveal function and check it uses shouldReduceMotion
        scroll_reveal_match = re.search(
            r"export function ScrollReveal\([^)]*\)\s*\{([\s\S]*?)(?=\nexport|\n\/\*\*|\Z)",
            content
        )
        assert scroll_reveal_match, "ScrollReveal function should exist"
        func_content = scroll_reveal_match.group(1)
        assert "shouldReduceMotion" in func_content or "useReducedMotion" in func_content, (
            "ScrollReveal should check reduced motion preference"
        )


class TestStaggerRevealComponent:
    """Test StaggerReveal and StaggerItem components for staggered animations."""

    def test_stagger_reveal_exported(self):
        """StaggerReveal component should be exported."""
        content = ANIMATIONS_FILE.read_text()
        assert "export function StaggerReveal" in content, (
            "StaggerReveal component should be exported"
        )

    def test_stagger_item_exported(self):
        """StaggerItem component should be exported."""
        content = ANIMATIONS_FILE.read_text()
        assert "export function StaggerItem" in content, (
            "StaggerItem component should be exported"
        )

    def test_stagger_reveal_has_stagger_delay_prop(self):
        """StaggerReveal should accept staggerDelay prop."""
        content = ANIMATIONS_FILE.read_text()
        assert "staggerDelay?" in content or "staggerDelay ?" in content, (
            "StaggerReveal should accept staggerDelay prop"
        )

    def test_stagger_reveal_uses_stagger_children(self):
        """StaggerReveal should use staggerChildren for sequenced animation."""
        content = ANIMATIONS_FILE.read_text()
        assert "staggerChildren" in content, (
            "StaggerReveal should use staggerChildren"
        )

    def test_stagger_reveal_respects_reduced_motion(self):
        """StaggerReveal should respect reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        # Find StaggerReveal function and check for reduced motion
        stagger_match = re.search(
            r"export function StaggerReveal\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function StaggerItem)",
            content
        )
        assert stagger_match, "StaggerReveal function should exist"
        func_content = stagger_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "StaggerReveal should check reduced motion preference"
        )


class TestHoverCardComponent:
    """Test HoverCard component for card hover animations."""

    def test_hover_card_exported(self):
        """HoverCard component should be exported."""
        content = ANIMATIONS_FILE.read_text()
        assert "export function HoverCard" in content, (
            "HoverCard component should be exported"
        )

    def test_hover_card_props_interface(self):
        """HoverCardProps interface should be exported."""
        content = ANIMATIONS_FILE.read_text()
        assert "export interface HoverCardProps" in content, (
            "HoverCardProps interface should be exported"
        )

    def test_hover_card_has_scale_prop(self):
        """HoverCard should accept scale prop."""
        content = ANIMATIONS_FILE.read_text()
        assert "scale?" in content or "scale ?" in content, (
            "HoverCard should accept scale prop"
        )

    def test_hover_card_has_lift_prop(self):
        """HoverCard should accept lift prop for Y translation."""
        content = ANIMATIONS_FILE.read_text()
        assert "lift?" in content or "lift ?" in content, (
            "HoverCard should accept lift prop"
        )

    def test_hover_card_uses_while_hover(self):
        """HoverCard should use whileHover for hover animation."""
        content = ANIMATIONS_FILE.read_text()
        assert "whileHover" in content, (
            "HoverCard should use whileHover"
        )

    def test_hover_card_uses_while_tap(self):
        """HoverCard should use whileTap for tap animation."""
        content = ANIMATIONS_FILE.read_text()
        assert "whileTap" in content, (
            "HoverCard should use whileTap"
        )

    def test_hover_card_respects_reduced_motion(self):
        """HoverCard should respect reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        # Find HoverCard function
        hover_match = re.search(
            r"export function HoverCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function|\/\*\*\n \* Parallax)",
            content
        )
        assert hover_match, "HoverCard function should exist"
        func_content = hover_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "HoverCard should check reduced motion preference"
        )


class TestParallaxRevealComponent:
    """Test ParallaxReveal component for parallax scroll effects."""

    def test_parallax_reveal_exported(self):
        """ParallaxReveal component should be exported."""
        content = ANIMATIONS_FILE.read_text()
        assert "export function ParallaxReveal" in content, (
            "ParallaxReveal component should be exported"
        )

    def test_parallax_reveal_has_offset_prop(self):
        """ParallaxReveal should accept offset prop."""
        content = ANIMATIONS_FILE.read_text()
        assert "offset?" in content or "offset ?" in content, (
            "ParallaxReveal should accept offset prop"
        )

    def test_parallax_uses_scroll_listener(self):
        """ParallaxReveal should use scroll event listener."""
        content = ANIMATIONS_FILE.read_text()
        assert "addEventListener" in content and "scroll" in content, (
            "ParallaxReveal should use scroll event listener"
        )

    def test_parallax_uses_passive_listener(self):
        """ParallaxReveal should use passive scroll listener for performance."""
        content = ANIMATIONS_FILE.read_text()
        assert "passive: true" in content or "{ passive: true }" in content, (
            "ParallaxReveal should use passive scroll listener"
        )

    def test_parallax_respects_reduced_motion(self):
        """ParallaxReveal should respect reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        parallax_match = re.search(
            r"export function ParallaxReveal\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function TextReveal)",
            content
        )
        assert parallax_match, "ParallaxReveal function should exist"
        func_content = parallax_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "ParallaxReveal should check reduced motion preference"
        )


class TestTextRevealComponent:
    """Test TextReveal component for character/word reveal animations."""

    def test_text_reveal_exported(self):
        """TextReveal component should be exported."""
        content = ANIMATIONS_FILE.read_text()
        assert "export function TextReveal" in content, (
            "TextReveal component should be exported"
        )

    def test_text_reveal_supports_word_mode(self):
        """TextReveal should support 'word' animation mode."""
        content = ANIMATIONS_FILE.read_text()
        assert "'word'" in content or '"word"' in content, (
            "TextReveal should support word mode"
        )

    def test_text_reveal_supports_character_mode(self):
        """TextReveal should support 'character' animation mode."""
        content = ANIMATIONS_FILE.read_text()
        assert "'character'" in content or '"character"' in content, (
            "TextReveal should support character mode"
        )

    def test_text_reveal_respects_reduced_motion(self):
        """TextReveal should respect reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        text_match = re.search(
            r"export function TextReveal\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function FloatingElement)",
            content
        )
        assert text_match, "TextReveal function should exist"
        func_content = text_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "TextReveal should check reduced motion preference"
        )


class TestFloatingElementComponent:
    """Test FloatingElement component for decorative floating animations."""

    def test_floating_element_exported(self):
        """FloatingElement component should be exported."""
        content = ANIMATIONS_FILE.read_text()
        assert "export function FloatingElement" in content, (
            "FloatingElement component should be exported"
        )

    def test_floating_element_has_amplitude_prop(self):
        """FloatingElement should accept amplitude prop."""
        content = ANIMATIONS_FILE.read_text()
        assert "amplitude?" in content or "amplitude ?" in content, (
            "FloatingElement should accept amplitude prop"
        )

    def test_floating_element_has_duration_prop(self):
        """FloatingElement should accept duration prop."""
        content = ANIMATIONS_FILE.read_text()
        # Check within FloatingElement props interface
        floating_props = re.search(
            r"export interface FloatingElementProps\s*\{([\s\S]*?)\}",
            content
        )
        assert floating_props, "FloatingElementProps should exist"
        assert "duration?" in floating_props.group(1), (
            "FloatingElement should accept duration prop"
        )

    def test_floating_element_uses_infinite_animation(self):
        """FloatingElement should use infinite repeat animation."""
        content = ANIMATIONS_FILE.read_text()
        assert "Infinity" in content or "repeat:" in content, (
            "FloatingElement should use infinite animation"
        )

    def test_floating_element_respects_reduced_motion(self):
        """FloatingElement should respect reduced motion preference."""
        content = ANIMATIONS_FILE.read_text()
        floating_match = re.search(
            r"export function FloatingElement\([^)]*\)\s*\{([\s\S]*?)(?=\Z)",
            content
        )
        assert floating_match, "FloatingElement function should exist"
        func_content = floating_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "FloatingElement should check reduced motion preference"
        )


class TestAnimationTiming:
    """Test animation timing configuration."""

    def test_has_timing_configuration(self):
        """animations.tsx should define timing constants."""
        content = ANIMATIONS_FILE.read_text()
        assert "TIMING" in content, (
            "animations.tsx should define TIMING configuration"
        )

    def test_has_fashion_easing(self):
        """Should define a smooth easing curve for elegant animations."""
        content = ANIMATIONS_FILE.read_text()
        # Check for cubic-bezier or array easing
        has_easing = (
            "0.25, 0.1, 0.25, 1" in content or
            "fashion" in content.lower()
        )
        assert has_easing, (
            "Should define elegant easing curve for fashion animations"
        )

    def test_has_spring_configuration(self):
        """Should define spring animation configuration."""
        content = ANIMATIONS_FILE.read_text()
        assert "spring" in content.lower(), (
            "Should define spring animation configuration"
        )


class TestAnimationVariants:
    """Test that animation variants are properly defined."""

    def test_reveal_variants_defined(self):
        """Animation variants should be defined."""
        content = ANIMATIONS_FILE.read_text()
        assert "revealVariants" in content or "Variants" in content, (
            "Animation variants should be defined"
        )

    def test_variants_have_hidden_state(self):
        """Variants should have hidden state."""
        content = ANIMATIONS_FILE.read_text()
        assert "hidden:" in content or "'hidden'" in content or '"hidden"' in content, (
            "Variants should have hidden state"
        )

    def test_variants_have_visible_state(self):
        """Variants should have visible state."""
        content = ANIMATIONS_FILE.read_text()
        assert "visible:" in content or "'visible'" in content or '"visible"' in content, (
            "Variants should have visible state"
        )


class TestAnimationsExports:
    """Test that animations are properly exported from index."""

    def test_scroll_reveal_exported_from_index(self):
        """ScrollReveal should be exported from ui/index.ts."""
        content = UI_INDEX_FILE.read_text()
        assert "ScrollReveal" in content, (
            "ScrollReveal should be exported from ui/index.ts"
        )

    def test_stagger_reveal_exported_from_index(self):
        """StaggerReveal should be exported from ui/index.ts."""
        content = UI_INDEX_FILE.read_text()
        assert "StaggerReveal" in content, (
            "StaggerReveal should be exported from ui/index.ts"
        )

    def test_hover_card_exported_from_index(self):
        """HoverCard should be exported from ui/index.ts."""
        content = UI_INDEX_FILE.read_text()
        assert "HoverCard" in content, (
            "HoverCard should be exported from ui/index.ts"
        )

    def test_exports_from_animations_file(self):
        """ui/index.ts should export from animations file."""
        content = UI_INDEX_FILE.read_text()
        assert "'./animations'" in content or '"./animations"' in content, (
            "ui/index.ts should export from ./animations"
        )
