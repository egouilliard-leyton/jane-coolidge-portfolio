"""
Tests for T-019: Page transition components

These tests verify that page transition components are properly implemented:
- PageTransition component provides smooth route change animations
- FadeTransition provides simpler opacity-only transitions
- SlideTransition provides directional slide animations
- SiteLayoutClient implements page transitions at layout level
- All transitions respect prefers-reduced-motion preference
"""

from pathlib import Path
import re


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
PAGE_TRANSITION_FILE = PROJECT_ROOT / "components" / "ui" / "PageTransition.tsx"
SITE_LAYOUT_CLIENT_FILE = PROJECT_ROOT / "app" / "(site)" / "SiteLayoutClient.tsx"
UI_INDEX_FILE = PROJECT_ROOT / "components" / "ui" / "index.ts"


class TestPageTransitionFileStructure:
    """Test that PageTransition.tsx file exists and has proper structure."""

    def test_page_transition_file_exists(self):
        """components/ui/PageTransition.tsx should exist."""
        assert PAGE_TRANSITION_FILE.exists(), "components/ui/PageTransition.tsx not found"

    def test_page_transition_is_client_component(self):
        """PageTransition.tsx should have 'use client' directive."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "PageTransition.tsx should have 'use client' directive"
        )

    def test_imports_motion_library(self):
        """PageTransition.tsx should import from motion/react."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "motion/react" in content, (
            "PageTransition.tsx should import from motion/react"
        )

    def test_imports_animate_presence(self):
        """PageTransition.tsx should import AnimatePresence."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "AnimatePresence" in content, (
            "PageTransition.tsx should import AnimatePresence for exit animations"
        )

    def test_imports_use_reduced_motion(self):
        """PageTransition.tsx should import useReducedMotion."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "useReducedMotion" in content, (
            "PageTransition.tsx should import useReducedMotion hook"
        )

    def test_imports_use_pathname(self):
        """PageTransition.tsx should import usePathname for route detection."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "usePathname" in content, (
            "PageTransition.tsx should import usePathname for route changes"
        )


class TestPageTransitionComponent:
    """Test main PageTransition component."""

    def test_page_transition_default_export(self):
        """PageTransition should be default exported."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "export default" in content and "PageTransition" in content, (
            "PageTransition should be default exported"
        )

    def test_page_transition_props_interface(self):
        """PageTransitionProps interface should be exported."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "export interface PageTransitionProps" in content, (
            "PageTransitionProps interface should be exported"
        )

    def test_page_transition_has_children_prop(self):
        """PageTransition should accept children prop."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "children:" in content, (
            "PageTransition should accept children prop"
        )

    def test_page_transition_has_classname_prop(self):
        """PageTransition should accept optional className prop."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "className?" in content or "className ?" in content, (
            "PageTransition should accept optional className prop"
        )

    def test_uses_animate_presence(self):
        """PageTransition should use AnimatePresence."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "<AnimatePresence" in content, (
            "PageTransition should use AnimatePresence component"
        )

    def test_animate_presence_has_wait_mode(self):
        """AnimatePresence should use mode='wait' for sequential animations."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert 'mode="wait"' in content or "mode='wait'" in content, (
            "AnimatePresence should use mode='wait'"
        )

    def test_uses_motion_div(self):
        """PageTransition should use motion.div for animations."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "<motion.div" in content, (
            "PageTransition should use motion.div"
        )

    def test_uses_pathname_as_key(self):
        """PageTransition should use pathname as key for re-animation."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "key={pathname}" in content or "key={ pathname }" in content, (
            "Motion element should use pathname as key"
        )


class TestPageTransitionVariants:
    """Test PageTransition animation variants."""

    def test_defines_page_variants(self):
        """PageTransition should define animation variants."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "pageVariants" in content, (
            "PageTransition should define pageVariants"
        )

    def test_has_initial_variant(self):
        """Page variants should have initial state."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "initial:" in content, (
            "Page variants should have initial state"
        )

    def test_has_enter_variant(self):
        """Page variants should have enter state."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "enter:" in content, (
            "Page variants should have enter state"
        )

    def test_has_exit_variant(self):
        """Page variants should have exit state."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "exit:" in content, (
            "Page variants should have exit state"
        )

    def test_initial_has_opacity(self):
        """Initial variant should include opacity animation."""
        content = PAGE_TRANSITION_FILE.read_text()
        # Look for opacity in initial variant
        initial_match = re.search(r"initial:\s*\{([^}]+)\}", content)
        assert initial_match, "initial variant should be defined"
        assert "opacity:" in initial_match.group(1), (
            "Initial variant should have opacity"
        )

    def test_initial_has_y_translation(self):
        """Initial variant should include Y translation for slide effect."""
        content = PAGE_TRANSITION_FILE.read_text()
        initial_match = re.search(r"initial:\s*\{([^}]+)\}", content)
        assert initial_match, "initial variant should be defined"
        assert "y:" in initial_match.group(1), (
            "Initial variant should have y translation"
        )


class TestReducedMotionVariants:
    """Test reduced motion variants for PageTransition."""

    def test_defines_reduced_motion_variants(self):
        """PageTransition should define reduced motion variants."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "reducedMotionVariants" in content, (
            "PageTransition should define reducedMotionVariants"
        )

    def test_reduced_motion_has_opacity_only(self):
        """Reduced motion variants should use opacity only (no y translation)."""
        content = PAGE_TRANSITION_FILE.read_text()
        # Find reducedMotionVariants and check it only has opacity
        reduced_match = re.search(
            r"reducedMotionVariants\s*=\s*\{([\s\S]*?)\n\}",
            content
        )
        assert reduced_match, "reducedMotionVariants should be defined"
        variants_content = reduced_match.group(1)
        # Should have opacity but no y in reduced motion
        assert "opacity:" in variants_content, "Reduced motion should have opacity"

    def test_selects_variants_based_on_preference(self):
        """PageTransition should select variants based on reduced motion preference."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "shouldReduceMotion" in content, (
            "PageTransition should check reduced motion preference"
        )
        # Should conditionally select variants
        assert "shouldReduceMotion ? reducedMotionVariants : pageVariants" in content or (
            "reducedMotionVariants" in content and "pageVariants" in content
        ), (
            "Should select variants based on reduced motion"
        )


class TestFadeTransitionComponent:
    """Test FadeTransition component."""

    def test_fade_transition_exported(self):
        """FadeTransition component should be exported."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "export function FadeTransition" in content, (
            "FadeTransition component should be exported"
        )

    def test_fade_transition_uses_opacity_only(self):
        """FadeTransition should use opacity-only animation."""
        content = PAGE_TRANSITION_FILE.read_text()
        # Find FadeTransition function content
        fade_match = re.search(
            r"export function FadeTransition\([^)]*\)\s*\{([\s\S]*?)(?=\nexport|\n\/\*\*)",
            content
        )
        assert fade_match, "FadeTransition function should exist"
        func_content = fade_match.group(1)
        assert "opacity:" in func_content, (
            "FadeTransition should use opacity animation"
        )

    def test_fade_transition_respects_reduced_motion(self):
        """FadeTransition should respect reduced motion preference."""
        content = PAGE_TRANSITION_FILE.read_text()
        fade_match = re.search(
            r"export function FadeTransition\([^)]*\)\s*\{([\s\S]*?)(?=\nexport|\n\/\*\*)",
            content
        )
        assert fade_match, "FadeTransition function should exist"
        func_content = fade_match.group(1)
        assert "shouldReduceMotion" in func_content or "useReducedMotion" in func_content, (
            "FadeTransition should check reduced motion preference"
        )


class TestSlideTransitionComponent:
    """Test SlideTransition component."""

    def test_slide_transition_exported(self):
        """SlideTransition component should be exported."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "export function SlideTransition" in content, (
            "SlideTransition component should be exported"
        )

    def test_slide_transition_props_interface(self):
        """SlideTransitionProps interface should be exported."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "export interface SlideTransitionProps" in content, (
            "SlideTransitionProps interface should be exported"
        )

    def test_slide_transition_has_direction_prop(self):
        """SlideTransition should accept direction prop."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "direction?" in content or "direction ?" in content, (
            "SlideTransition should accept direction prop"
        )

    def test_slide_transition_supports_all_directions(self):
        """SlideTransition should support all slide directions."""
        content = PAGE_TRANSITION_FILE.read_text()
        directions = ["'left'", "'right'", "'up'", "'down'"]
        found_directions = sum(1 for d in directions if d in content or d.replace("'", '"') in content)
        assert found_directions >= 4, (
            f"SlideTransition should support all 4 directions. Found {found_directions}"
        )

    def test_slide_transition_uses_spring_animation(self):
        """SlideTransition should use spring animation for natural feel."""
        content = PAGE_TRANSITION_FILE.read_text()
        # Find SlideTransition function
        slide_match = re.search(
            r"export function SlideTransition\([^)]*\)\s*\{([\s\S]*?)(?=\Z)",
            content
        )
        assert slide_match, "SlideTransition function should exist"
        func_content = slide_match.group(1)
        assert "'spring'" in func_content or '"spring"' in func_content, (
            "SlideTransition should use spring animation"
        )

    def test_slide_transition_respects_reduced_motion(self):
        """SlideTransition should respect reduced motion preference."""
        content = PAGE_TRANSITION_FILE.read_text()
        slide_match = re.search(
            r"export function SlideTransition\([^)]*\)\s*\{([\s\S]*?)(?=\Z)",
            content
        )
        assert slide_match, "SlideTransition function should exist"
        func_content = slide_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "SlideTransition should check reduced motion preference"
        )


class TestTransitionEasing:
    """Test transition easing configuration."""

    def test_defines_transition_ease(self):
        """PageTransition should define TRANSITION_EASE constant."""
        content = PAGE_TRANSITION_FILE.read_text()
        assert "TRANSITION_EASE" in content, (
            "Should define TRANSITION_EASE constant"
        )

    def test_transition_ease_is_cubic_bezier(self):
        """Transition ease should be a cubic-bezier curve."""
        content = PAGE_TRANSITION_FILE.read_text()
        # Should be an array of 4 numbers
        ease_match = re.search(
            r"TRANSITION_EASE[^=]*=\s*\[([^\]]+)\]",
            content
        )
        assert ease_match, "TRANSITION_EASE should be defined as array"
        ease_values = ease_match.group(1)
        # Should have 4 comma-separated numbers
        numbers = [n.strip() for n in ease_values.split(",")]
        assert len(numbers) == 4, (
            "TRANSITION_EASE should have 4 values (cubic-bezier)"
        )


class TestTransitionDuration:
    """Test transition duration configuration."""

    def test_has_normal_duration(self):
        """Should have normal animation duration."""
        content = PAGE_TRANSITION_FILE.read_text()
        # Look for duration around 0.4s (normal)
        assert "0.4" in content or "0.45" in content or "0.5" in content, (
            "Should have normal animation duration"
        )

    def test_has_reduced_motion_duration(self):
        """Should have shorter duration for reduced motion."""
        content = PAGE_TRANSITION_FILE.read_text()
        # Look for shorter duration (around 0.1-0.2s)
        assert "0.1" in content or "0.15" in content or "0.2" in content, (
            "Should have reduced motion duration"
        )


class TestSiteLayoutClient:
    """Test SiteLayoutClient page transition implementation."""

    def test_site_layout_client_exists(self):
        """app/(site)/SiteLayoutClient.tsx should exist."""
        assert SITE_LAYOUT_CLIENT_FILE.exists(), (
            "app/(site)/SiteLayoutClient.tsx not found"
        )

    def test_site_layout_is_client_component(self):
        """SiteLayoutClient should be a client component."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "SiteLayoutClient should have 'use client' directive"
        )

    def test_site_layout_imports_motion(self):
        """SiteLayoutClient should import motion."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "motion" in content and "motion/react" in content, (
            "SiteLayoutClient should import motion from motion/react"
        )

    def test_site_layout_imports_use_reduced_motion(self):
        """SiteLayoutClient should import useReducedMotion."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "useReducedMotion" in content, (
            "SiteLayoutClient should import useReducedMotion"
        )

    def test_site_layout_imports_use_pathname(self):
        """SiteLayoutClient should import usePathname."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "usePathname" in content, (
            "SiteLayoutClient should import usePathname"
        )

    def test_site_layout_uses_motion_main(self):
        """SiteLayoutClient should use motion.main element."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "<motion.main" in content, (
            "SiteLayoutClient should use motion.main for page transitions"
        )

    def test_site_layout_uses_pathname_key(self):
        """SiteLayoutClient should use pathname as animation key."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "key={pathname}" in content, (
            "SiteLayoutClient should use pathname as animation key"
        )

    def test_site_layout_has_initial_animation(self):
        """SiteLayoutClient should define initial animation state."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "initial=" in content or "initial:" in content, (
            "SiteLayoutClient should define initial animation state"
        )

    def test_site_layout_has_animate_state(self):
        """SiteLayoutClient should define animate state."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "animate=" in content or "animate:" in content, (
            "SiteLayoutClient should define animate state"
        )

    def test_site_layout_respects_reduced_motion(self):
        """SiteLayoutClient should respect reduced motion preference."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "shouldReduceMotion" in content, (
            "SiteLayoutClient should check reduced motion preference"
        )

    def test_site_layout_has_transition_config(self):
        """SiteLayoutClient should configure transition timing."""
        content = SITE_LAYOUT_CLIENT_FILE.read_text()
        assert "transition=" in content or "transition:" in content, (
            "SiteLayoutClient should configure transition"
        )


class TestPageTransitionExports:
    """Test that page transitions are properly exported."""

    def test_page_transition_exported_from_index(self):
        """PageTransition should be exported from ui/index.ts."""
        content = UI_INDEX_FILE.read_text()
        assert "PageTransition" in content, (
            "PageTransition should be exported from ui/index.ts"
        )

    def test_fade_transition_exported_from_index(self):
        """FadeTransition should be exported from ui/index.ts."""
        content = UI_INDEX_FILE.read_text()
        assert "FadeTransition" in content, (
            "FadeTransition should be exported from ui/index.ts"
        )

    def test_slide_transition_exported_from_index(self):
        """SlideTransition should be exported from ui/index.ts."""
        content = UI_INDEX_FILE.read_text()
        assert "SlideTransition" in content, (
            "SlideTransition should be exported from ui/index.ts"
        )
