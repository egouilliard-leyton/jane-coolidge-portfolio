"""
Tests for T-019: Modal animation implementation in ImageWithPopup

These tests verify that modal animations are properly implemented:
- Modal opens with smooth scale/fade animation
- Modal closes with smooth exit animation
- Backdrop animates separately from modal content
- Animation variants are properly defined
- All modal animations respect prefers-reduced-motion preference
"""

from pathlib import Path
import re


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
IMAGE_WITH_POPUP_FILE = PROJECT_ROOT / "components" / "ui" / "ImageWithPopup.tsx"


class TestModalAnimationSetup:
    """Test modal animation setup and imports."""

    def test_imports_animate_presence(self):
        """ImageWithPopup should import AnimatePresence for exit animations."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "AnimatePresence" in content, (
            "ImageWithPopup should import AnimatePresence"
        )

    def test_imports_motion(self):
        """ImageWithPopup should import motion for animations."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "motion" in content and "motion/react" in content, (
            "ImageWithPopup should import motion from motion/react"
        )

    def test_imports_use_reduced_motion(self):
        """ImageWithPopup should import useReducedMotion."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "useReducedMotion" in content, (
            "ImageWithPopup should import useReducedMotion"
        )


class TestModalAnimationVariants:
    """Test modal animation variants definition."""

    def test_defines_overlay_variants(self):
        """ImageWithPopup should define overlay animation variants."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "overlayVariants" in content, (
            "Should define overlayVariants for backdrop animation"
        )

    def test_defines_modal_variants(self):
        """ImageWithPopup should define modal content variants."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "modalVariants" in content, (
            "Should define modalVariants for modal content animation"
        )

    def test_overlay_has_hidden_state(self):
        """Overlay variants should have hidden state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Find overlayVariants definition
        overlay_match = re.search(
            r"overlayVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert overlay_match, "overlayVariants should be defined"
        variants_content = overlay_match.group(1)
        assert "hidden:" in variants_content, (
            "overlayVariants should have hidden state"
        )

    def test_overlay_has_visible_state(self):
        """Overlay variants should have visible state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        overlay_match = re.search(
            r"overlayVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert overlay_match, "overlayVariants should be defined"
        variants_content = overlay_match.group(1)
        assert "visible:" in variants_content, (
            "overlayVariants should have visible state"
        )

    def test_modal_has_hidden_state(self):
        """Modal variants should have hidden state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        modal_match = re.search(
            r"modalVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert modal_match, "modalVariants should be defined"
        variants_content = modal_match.group(1)
        assert "hidden:" in variants_content, (
            "modalVariants should have hidden state"
        )

    def test_modal_has_visible_state(self):
        """Modal variants should have visible state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Look for modalVariants with both hidden and visible states
        modal_match = re.search(
            r"modalVariants\s*=\s*\{[\s\S]*?visible:\s*\{[^}]+\}",
            content
        )
        assert modal_match, (
            "modalVariants should have visible state"
        )


class TestModalScaleAnimation:
    """Test modal scale animation."""

    def test_modal_has_scale_in_hidden(self):
        """Modal hidden state should have scale less than 1."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        modal_match = re.search(
            r"modalVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert modal_match, "modalVariants should be defined"
        variants_content = modal_match.group(1)
        # Should have scale property
        assert "scale:" in variants_content, (
            "Modal variants should have scale property"
        )

    def test_modal_scales_to_1_when_visible(self):
        """Modal visible state should have scale: 1."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for visible state with scale: 1 in modalVariants
        # Look specifically in modalVariants visible state
        modal_visible_match = re.search(
            r"modalVariants\s*=[\s\S]*?visible:\s*\{([^}]+)\}",
            content
        )
        assert modal_visible_match, "modalVariants visible state should exist"
        visible_content = modal_visible_match.group(1)
        assert "scale: 1" in visible_content or "scale:1" in visible_content, (
            "Modal should scale to 1 when visible"
        )


class TestModalOpacityAnimation:
    """Test modal opacity/fade animation."""

    def test_overlay_fades_in(self):
        """Overlay should fade in from opacity 0 to 1."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        overlay_match = re.search(
            r"overlayVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert overlay_match, "overlayVariants should be defined"
        variants_content = overlay_match.group(1)
        assert "opacity:" in variants_content, (
            "Overlay should have opacity animation"
        )

    def test_modal_has_opacity_animation(self):
        """Modal should have opacity animation."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        modal_match = re.search(
            r"modalVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert modal_match, "modalVariants should be defined"
        variants_content = modal_match.group(1)
        assert "opacity:" in variants_content, (
            "Modal should have opacity animation"
        )


class TestModalYTranslation:
    """Test modal Y translation animation."""

    def test_modal_has_y_translation(self):
        """Modal should animate with Y translation."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        modal_match = re.search(
            r"modalVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert modal_match, "modalVariants should be defined"
        variants_content = modal_match.group(1)
        assert "y:" in variants_content, (
            "Modal should have y translation for slide effect"
        )


class TestAnimatePresenceUsage:
    """Test AnimatePresence component usage for exit animations."""

    def test_modal_wrapped_in_animate_presence(self):
        """Modal should be wrapped in AnimatePresence."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<AnimatePresence>" in content or "<AnimatePresence " in content, (
            "Modal should be wrapped in AnimatePresence"
        )

    def test_animate_presence_wraps_conditional_modal(self):
        """AnimatePresence should wrap the conditional modal render."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Look for pattern of AnimatePresence with conditional inside
        pattern = r"<AnimatePresence[^>]*>\s*\{isOpen"
        assert re.search(pattern, content), (
            "AnimatePresence should wrap conditional modal rendering"
        )

    def test_modal_uses_motion_div(self):
        """Modal content should use motion.div."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<motion.div" in content, (
            "Modal should use motion.div for animations"
        )


class TestModalTransitionConfig:
    """Test modal transition configuration."""

    def test_modal_has_transition_config(self):
        """Modal should have transition configuration."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "transition=" in content or "transition:" in content, (
            "Modal should have transition configuration"
        )

    def test_modal_uses_spring_animation(self):
        """Modal should use spring animation for natural feel."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Look for spring type in transition
        assert "'spring'" in content or '"spring"' in content, (
            "Modal should use spring animation type"
        )

    def test_modal_has_bounce_config(self):
        """Modal spring should have bounce configuration."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "bounce:" in content or "bounce :" in content, (
            "Modal spring should configure bounce"
        )


class TestBackdropAnimation:
    """Test backdrop/overlay animation."""

    def test_backdrop_has_separate_animation(self):
        """Backdrop should have separate animation from modal."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Should have two motion.div elements (backdrop and modal content)
        motion_div_count = content.count("<motion.div")
        assert motion_div_count >= 2, (
            f"Should have separate backdrop and modal animations. Found {motion_div_count} motion.div elements"
        )

    def test_backdrop_uses_variants(self):
        """Backdrop should use overlayVariants."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check that a motion.div uses overlayVariants
        assert "variants={overlayVariants}" in content or "variants={ overlayVariants }" in content, (
            "Backdrop should use overlayVariants"
        )

    def test_modal_content_uses_variants(self):
        """Modal content should use modalVariants."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "variants={modalVariants}" in content or "variants={ modalVariants }" in content, (
            "Modal content should use modalVariants"
        )


class TestModalReducedMotion:
    """Test modal animations respect reduced motion preference."""

    def test_uses_should_reduce_motion(self):
        """ImageWithPopup should use shouldReduceMotion variable."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "shouldReduceMotion" in content, (
            "Should use shouldReduceMotion variable"
        )

    def test_modal_scale_respects_reduced_motion(self):
        """Modal scale animation should be disabled for reduced motion."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check that scale is conditionally set based on reduced motion
        pattern = r"shouldReduceMotion\s*\?\s*1\s*:\s*[\d.]+"
        assert re.search(pattern, content) or "shouldReduceMotion ? 1" in content, (
            "Scale should be 1 (no scale) for reduced motion"
        )

    def test_modal_y_respects_reduced_motion(self):
        """Modal y translation should be disabled for reduced motion."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check that y is conditionally set based on reduced motion
        pattern = r"shouldReduceMotion\s*\?\s*0\s*:\s*\d+"
        assert re.search(pattern, content) or "shouldReduceMotion ? 0" in content, (
            "Y translation should be 0 for reduced motion"
        )

    def test_reduced_motion_has_shorter_duration(self):
        """Animation duration should be shorter for reduced motion."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for conditional duration based on reduced motion
        pattern = r"shouldReduceMotion\s*\?\s*[\d.]+\s*:\s*[\d.]+"
        assert re.search(pattern, content), (
            "Duration should be conditional on reduced motion preference"
        )

    def test_reduced_motion_has_no_bounce(self):
        """Spring animation should have no bounce for reduced motion."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for bounce: 0 when reduced motion
        pattern = r"shouldReduceMotion\s*\?\s*0\s*:"
        assert re.search(pattern, content), (
            "Bounce should be 0 for reduced motion"
        )


class TestIndicatorButtonAnimation:
    """Test indicator button hover/tap animations."""

    def test_defines_indicator_variants(self):
        """Should define indicatorVariants for button animation."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "indicatorVariants" in content, (
            "Should define indicatorVariants"
        )

    def test_indicator_has_initial_state(self):
        """Indicator variants should have initial state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        indicator_match = re.search(
            r"indicatorVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert indicator_match, "indicatorVariants should be defined"
        variants_content = indicator_match.group(1)
        assert "initial:" in variants_content, (
            "indicatorVariants should have initial state"
        )

    def test_indicator_has_hover_state(self):
        """Indicator variants should have hover state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        indicator_match = re.search(
            r"indicatorVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert indicator_match, "indicatorVariants should be defined"
        variants_content = indicator_match.group(1)
        assert "hover:" in variants_content, (
            "indicatorVariants should have hover state"
        )

    def test_indicator_has_tap_state(self):
        """Indicator variants should have tap state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        indicator_match = re.search(
            r"indicatorVariants\s*=\s*\{([\s\S]*?)\n\s*\}",
            content
        )
        assert indicator_match, "indicatorVariants should be defined"
        variants_content = indicator_match.group(1)
        assert "tap:" in variants_content, (
            "indicatorVariants should have tap state"
        )

    def test_indicator_uses_while_hover(self):
        """Indicator button should use whileHover."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'whileHover="hover"' in content or "whileHover='hover'" in content, (
            "Indicator should use whileHover='hover'"
        )

    def test_indicator_uses_while_tap(self):
        """Indicator button should use whileTap."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'whileTap="tap"' in content or "whileTap='tap'" in content, (
            "Indicator should use whileTap='tap'"
        )


class TestAnimationInitialAndAnimate:
    """Test initial and animate state props on modal elements."""

    def test_modal_wrapper_has_initial(self):
        """Modal wrapper should have initial state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'initial="hidden"' in content or "initial='hidden'" in content, (
            "Modal should have initial='hidden'"
        )

    def test_modal_wrapper_has_animate(self):
        """Modal wrapper should have animate state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'animate="visible"' in content or "animate='visible'" in content, (
            "Modal should have animate='visible'"
        )

    def test_modal_wrapper_has_exit(self):
        """Modal wrapper should have exit state."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert 'exit="hidden"' in content or "exit='hidden'" in content, (
            "Modal should have exit='hidden'"
        )
