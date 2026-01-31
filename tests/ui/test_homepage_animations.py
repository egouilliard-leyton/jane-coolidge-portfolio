"""
Tests for T-019: Homepage section animations

These tests verify that homepage sections properly animate:
- Hero content has staggered reveal animations
- Blog post cards have scroll-triggered animations and hover effects
- Project cards have scroll-triggered animations and hover effects
- Section headers animate on scroll
- CTA section animates on scroll
- All homepage animations respect prefers-reduced-motion preference
"""

from pathlib import Path
import re


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
ANIMATED_SECTIONS_FILE = PROJECT_ROOT / "components" / "home" / "AnimatedSections.tsx"


class TestAnimatedSectionsFileStructure:
    """Test that AnimatedSections.tsx file exists and has proper structure."""

    def test_animated_sections_file_exists(self):
        """components/home/AnimatedSections.tsx should exist."""
        assert ANIMATED_SECTIONS_FILE.exists(), (
            "components/home/AnimatedSections.tsx not found"
        )

    def test_animated_sections_is_client_component(self):
        """AnimatedSections.tsx should have 'use client' directive."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "AnimatedSections.tsx should have 'use client' directive"
        )

    def test_imports_motion_library(self):
        """AnimatedSections.tsx should import from motion/react."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "motion/react" in content, (
            "AnimatedSections.tsx should import from motion/react"
        )

    def test_imports_use_reduced_motion(self):
        """AnimatedSections.tsx should import useReducedMotion."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "useReducedMotion" in content, (
            "AnimatedSections.tsx should import useReducedMotion"
        )

    def test_imports_scroll_reveal_components(self):
        """AnimatedSections.tsx should import ScrollReveal components."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "ScrollReveal" in content, (
            "AnimatedSections.tsx should import ScrollReveal"
        )


class TestAnimatedHeroContent:
    """Test AnimatedHeroContent component."""

    def test_animated_hero_content_exported(self):
        """AnimatedHeroContent should be exported."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "export function AnimatedHeroContent" in content, (
            "AnimatedHeroContent should be exported"
        )

    def test_hero_uses_motion_h1(self):
        """Hero heading should use motion.h1."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "<motion.h1" in content, (
            "Hero should use motion.h1 for animated heading"
        )

    def test_hero_uses_motion_p(self):
        """Hero subheading should use motion.p."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "<motion.p" in content, (
            "Hero should use motion.p for animated subheading"
        )

    def test_hero_has_staggered_delays(self):
        """Hero elements should have staggered animation delays."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Look for multiple delay values
        delays = re.findall(r'delay:\s*([\d.]+)', content)
        assert len(delays) >= 2, (
            f"Hero should have staggered delays. Found {len(delays)} delay values"
        )

    def test_hero_heading_initial_animation(self):
        """Hero heading should have initial animation state."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Look for motion.h1 with initial prop
        h1_match = re.search(r"<motion\.h1[^>]*initial=", content)
        assert h1_match, (
            "Hero h1 should have initial animation state"
        )

    def test_hero_heading_animate_state(self):
        """Hero heading should have animate state."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        h1_match = re.search(r"<motion\.h1[^>]*animate=", content)
        assert h1_match, (
            "Hero h1 should have animate state"
        )

    def test_hero_has_opacity_animation(self):
        """Hero elements should animate opacity."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Find AnimatedHeroContent function content
        hero_match = re.search(
            r"export function AnimatedHeroContent\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert hero_match, "AnimatedHeroContent should exist"
        func_content = hero_match.group(1)
        assert "opacity:" in func_content, (
            "Hero should have opacity animation"
        )

    def test_hero_has_y_translation(self):
        """Hero elements should have Y translation animation."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        hero_match = re.search(
            r"export function AnimatedHeroContent\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert hero_match, "AnimatedHeroContent should exist"
        func_content = hero_match.group(1)
        assert "y:" in func_content, (
            "Hero should have y translation animation"
        )

    def test_hero_respects_reduced_motion(self):
        """AnimatedHeroContent should respect reduced motion preference."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        hero_match = re.search(
            r"export function AnimatedHeroContent\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert hero_match, "AnimatedHeroContent should exist"
        func_content = hero_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "AnimatedHeroContent should check reduced motion preference"
        )

    def test_hero_has_reduced_motion_fallback(self):
        """Hero should have fallback for reduced motion users."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        hero_match = re.search(
            r"export function AnimatedHeroContent\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert hero_match, "AnimatedHeroContent should exist"
        func_content = hero_match.group(1)
        # Should have conditional return for reduced motion
        assert "if (shouldReduceMotion)" in func_content, (
            "Hero should have conditional return for reduced motion"
        )


class TestAnimatedIntroSection:
    """Test AnimatedIntroSection component."""

    def test_animated_intro_section_exported(self):
        """AnimatedIntroSection should be exported."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "export function AnimatedIntroSection" in content, (
            "AnimatedIntroSection should be exported"
        )

    def test_intro_uses_scroll_reveal(self):
        """Intro section should use ScrollReveal components."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        intro_match = re.search(
            r"export function AnimatedIntroSection\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert intro_match, "AnimatedIntroSection should exist"
        func_content = intro_match.group(1)
        assert "<ScrollReveal" in func_content, (
            "IntroSection should use ScrollReveal"
        )

    def test_intro_has_fade_up_animation(self):
        """Intro section should use fade-up animation."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        intro_match = re.search(
            r"export function AnimatedIntroSection\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert intro_match, "AnimatedIntroSection should exist"
        func_content = intro_match.group(1)
        assert "'fade-up'" in func_content or '"fade-up"' in func_content, (
            "IntroSection should use fade-up variant"
        )


class TestAnimatedPostCard:
    """Test AnimatedPostCard component for blog post cards."""

    def test_animated_post_card_exported(self):
        """AnimatedPostCard should be exported."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "export function AnimatedPostCard" in content, (
            "AnimatedPostCard should be exported"
        )

    def test_post_card_uses_motion_article(self):
        """Post card should use motion.article."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "<motion.article" in content, (
            "Post card should use motion.article"
        )

    def test_post_card_has_while_in_view(self):
        """Post card should use whileInView for scroll animation."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        post_match = re.search(
            r"export function AnimatedPostCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert post_match, "AnimatedPostCard should exist"
        func_content = post_match.group(1)
        assert "whileInView" in func_content, (
            "Post card should use whileInView for scroll animation"
        )

    def test_post_card_has_viewport_config(self):
        """Post card should have viewport configuration."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        post_match = re.search(
            r"export function AnimatedPostCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert post_match, "AnimatedPostCard should exist"
        func_content = post_match.group(1)
        assert "viewport=" in func_content or "viewport:" in func_content, (
            "Post card should have viewport configuration"
        )

    def test_post_card_animates_once(self):
        """Post card should only animate once."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        post_match = re.search(
            r"export function AnimatedPostCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert post_match, "AnimatedPostCard should exist"
        func_content = post_match.group(1)
        assert "once: true" in func_content, (
            "Post card should animate only once"
        )

    def test_post_card_has_while_hover(self):
        """Post card should have hover animation."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        post_match = re.search(
            r"export function AnimatedPostCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert post_match, "AnimatedPostCard should exist"
        func_content = post_match.group(1)
        assert "whileHover" in func_content, (
            "Post card should have whileHover animation"
        )

    def test_post_card_hover_lifts_card(self):
        """Post card hover should lift the card (negative Y)."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        post_match = re.search(
            r"export function AnimatedPostCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert post_match, "AnimatedPostCard should exist"
        func_content = post_match.group(1)
        # Look for y: -8 or similar negative value in whileHover
        hover_y_match = re.search(r"whileHover=\{\s*\{[^}]*y:\s*(-\d+)", func_content)
        assert hover_y_match, (
            "Post card hover should lift card with negative Y"
        )

    def test_post_card_has_stagger_delay(self):
        """Post card should have index-based stagger delay."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        post_match = re.search(
            r"export function AnimatedPostCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert post_match, "AnimatedPostCard should exist"
        func_content = post_match.group(1)
        assert "index" in func_content and "delay" in func_content, (
            "Post card should have index-based stagger delay"
        )

    def test_post_card_respects_reduced_motion(self):
        """AnimatedPostCard should respect reduced motion preference."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        post_match = re.search(
            r"export function AnimatedPostCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert post_match, "AnimatedPostCard should exist"
        func_content = post_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "AnimatedPostCard should check reduced motion preference"
        )


class TestAnimatedProjectCard:
    """Test AnimatedProjectCard component for project cards."""

    def test_animated_project_card_exported(self):
        """AnimatedProjectCard should be exported."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "export function AnimatedProjectCard" in content, (
            "AnimatedProjectCard should be exported"
        )

    def test_project_card_uses_motion_article(self):
        """Project card should use motion.article."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Already checked above for post card, but let's ensure project card also has it
        project_match = re.search(
            r"export function AnimatedProjectCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert project_match, "AnimatedProjectCard should exist"
        func_content = project_match.group(1)
        assert "<motion.article" in func_content, (
            "Project card should use motion.article"
        )

    def test_project_card_has_while_in_view(self):
        """Project card should use whileInView for scroll animation."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        project_match = re.search(
            r"export function AnimatedProjectCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert project_match, "AnimatedProjectCard should exist"
        func_content = project_match.group(1)
        assert "whileInView" in func_content, (
            "Project card should use whileInView"
        )

    def test_project_card_has_while_hover(self):
        """Project card should have hover animation."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        project_match = re.search(
            r"export function AnimatedProjectCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert project_match, "AnimatedProjectCard should exist"
        func_content = project_match.group(1)
        assert "whileHover" in func_content, (
            "Project card should have whileHover animation"
        )

    def test_project_card_hover_scales(self):
        """Project card hover should scale the card."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        project_match = re.search(
            r"export function AnimatedProjectCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert project_match, "AnimatedProjectCard should exist"
        func_content = project_match.group(1)
        # Look for scale in whileHover
        hover_scale_match = re.search(r"whileHover=\{\s*\{[^}]*scale:", func_content)
        assert hover_scale_match, (
            "Project card hover should scale card"
        )

    def test_project_card_has_stagger_delay(self):
        """Project card should have index-based stagger delay."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        project_match = re.search(
            r"export function AnimatedProjectCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert project_match, "AnimatedProjectCard should exist"
        func_content = project_match.group(1)
        assert "index" in func_content and "delay" in func_content, (
            "Project card should have index-based stagger delay"
        )

    def test_project_card_respects_reduced_motion(self):
        """AnimatedProjectCard should respect reduced motion preference."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        project_match = re.search(
            r"export function AnimatedProjectCard\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert project_match, "AnimatedProjectCard should exist"
        func_content = project_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "AnimatedProjectCard should check reduced motion preference"
        )


class TestAnimatedSectionHeader:
    """Test AnimatedSectionHeader component."""

    def test_animated_section_header_exported(self):
        """AnimatedSectionHeader should be exported."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "export function AnimatedSectionHeader" in content, (
            "AnimatedSectionHeader should be exported"
        )

    def test_section_header_uses_scroll_reveal(self):
        """Section header should use ScrollReveal."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        header_match = re.search(
            r"export function AnimatedSectionHeader\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert header_match, "AnimatedSectionHeader should exist"
        func_content = header_match.group(1)
        assert "<ScrollReveal" in func_content, (
            "Section header should use ScrollReveal"
        )

    def test_section_header_has_staggered_delays(self):
        """Section header elements should have staggered delays."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        header_match = re.search(
            r"export function AnimatedSectionHeader\([^)]*\)\s*\{([\s\S]*?)(?=\nexport function)",
            content
        )
        assert header_match, "AnimatedSectionHeader should exist"
        func_content = header_match.group(1)
        # Look for multiple delay values
        delays = re.findall(r'delay=\{([\d.]+)\}', func_content)
        assert len(delays) >= 2, (
            f"Section header should have staggered delays. Found {len(delays)}"
        )


class TestAnimatedCTA:
    """Test AnimatedCTA component."""

    def test_animated_cta_exported(self):
        """AnimatedCTA should be exported."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "export function AnimatedCTA" in content, (
            "AnimatedCTA should be exported"
        )

    def test_cta_uses_motion_div(self):
        """CTA should use motion.div."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        cta_match = re.search(
            r"export function AnimatedCTA\([^)]*\)\s*\{([\s\S]*?)$",
            content
        )
        assert cta_match, "AnimatedCTA should exist"
        func_content = cta_match.group(1)
        assert "<motion.div" in func_content, (
            "CTA should use motion.div"
        )

    def test_cta_has_while_in_view(self):
        """CTA should use whileInView for scroll animation."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        cta_match = re.search(
            r"export function AnimatedCTA\([^)]*\)\s*\{([\s\S]*?)$",
            content
        )
        assert cta_match, "AnimatedCTA should exist"
        func_content = cta_match.group(1)
        assert "whileInView" in func_content, (
            "CTA should use whileInView"
        )

    def test_cta_respects_reduced_motion(self):
        """AnimatedCTA should respect reduced motion preference."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        cta_match = re.search(
            r"export function AnimatedCTA\([^)]*\)\s*\{([\s\S]*?)$",
            content
        )
        assert cta_match, "AnimatedCTA should exist"
        func_content = cta_match.group(1)
        assert "shouldReduceMotion" in func_content, (
            "AnimatedCTA should check reduced motion preference"
        )


class TestAnimationTimingConfiguration:
    """Test animation timing configuration in AnimatedSections."""

    def test_defines_timing_constant(self):
        """AnimatedSections should define TIMING constant."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "TIMING" in content, (
            "AnimatedSections should define TIMING constant"
        )

    def test_timing_is_cubic_bezier(self):
        """TIMING should be a cubic-bezier easing curve."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Look for array with 4 numbers
        timing_match = re.search(r"TIMING[^=]*=\s*\[([^\]]+)\]", content)
        assert timing_match, "TIMING should be defined as array"
        timing_values = timing_match.group(1)
        numbers = [n.strip() for n in timing_values.split(",")]
        assert len(numbers) == 4, (
            "TIMING should have 4 values (cubic-bezier)"
        )

    def test_uses_ease_in_transitions(self):
        """Transitions should use ease configuration."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "ease:" in content or "ease :" in content, (
            "Transitions should use ease configuration"
        )


class TestImageHoverAnimation:
    """Test image hover animations on cards."""

    def test_image_has_hover_scale(self):
        """Card images should scale on hover."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "group-hover:scale-" in content, (
            "Card images should scale on group hover"
        )

    def test_image_has_transition_duration(self):
        """Image scale should have transition duration."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "duration-" in content and "transition-" in content, (
            "Image should have transition duration"
        )
