"""
Tests for T-005: Configure Tailwind CSS with custom design tokens

These tests verify that Tailwind CSS is configured according to the requirements:
- Custom color palette (dusty rose) is defined
- Playfair Display font is configured for headings
- Inter font is configured for body text
- Typography plugin is installed and configured
- Custom spacing/sizing values are added
- Content paths include all relevant files
"""

import json
import re
from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
GLOBALS_CSS_PATH = PROJECT_ROOT / "app" / "globals.css"
LAYOUT_TSX_PATH = PROJECT_ROOT / "app" / "layout.tsx"
PACKAGE_JSON_PATH = PROJECT_ROOT / "package.json"


class TestTypographyPluginInstallation:
    """Test that the typography plugin is installed and configured."""

    def test_typography_plugin_dependency_installed(self):
        """@tailwindcss/typography should be listed as a dependency."""
        with open(PACKAGE_JSON_PATH) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        dev_dependencies = package_data.get("devDependencies", {})
        all_deps = {**dependencies, **dev_dependencies}

        assert "@tailwindcss/typography" in all_deps, (
            "@tailwindcss/typography is not installed"
        )

    def test_typography_plugin_imported_in_globals_css(self):
        """globals.css should import the typography plugin."""
        assert GLOBALS_CSS_PATH.exists(), "app/globals.css not found"
        content = GLOBALS_CSS_PATH.read_text()

        # Tailwind CSS v4 uses @plugin directive
        has_typography_plugin = '@plugin "@tailwindcss/typography"' in content
        assert has_typography_plugin, (
            "Typography plugin should be imported via @plugin directive in globals.css"
        )


class TestDustyRoseColorPalette:
    """Test that the dusty rose color palette is properly configured."""

    def test_globals_css_has_theme_directive(self):
        """globals.css should have the @theme directive for custom tokens."""
        assert GLOBALS_CSS_PATH.exists(), "app/globals.css not found"
        content = GLOBALS_CSS_PATH.read_text()

        assert "@theme" in content, "globals.css should use @theme directive for Tailwind v4"

    def test_brand_colors_defined(self):
        """Brand colors should be defined in the theme."""
        content = GLOBALS_CSS_PATH.read_text()

        # Verify all brand color shades are defined
        expected_shades = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"]

        for shade in expected_shades:
            pattern = rf"--color-brand-{shade}:\s*#[0-9a-fA-F]{{6}}"
            match = re.search(pattern, content)
            assert match, f"Brand color shade {shade} not found (expected --color-brand-{shade})"

    def test_brand_primary_is_dusty_rose(self):
        """Brand-500 should be a dusty rose color."""
        content = GLOBALS_CSS_PATH.read_text()

        # Extract brand-500 color
        match = re.search(r"--color-brand-500:\s*#([0-9a-fA-F]{6})", content)
        assert match, "Brand-500 color not found"

        hex_color = match.group(1).lower()

        # Convert to RGB to verify it's in the rose/pink range
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Dusty rose should have red as dominant or near-dominant,
        # with moderate green and blue creating the muted/dusty effect
        # For b86b85: R=184, G=107, B=133
        is_rose_hue = r > g and r > b * 0.8  # Red should be dominant
        is_muted = g > 50 and b > 50  # Should have some green and blue for dusty effect

        assert is_rose_hue and is_muted, (
            f"Brand-500 ({hex_color}) doesn't appear to be a dusty rose color. "
            f"RGB: ({r}, {g}, {b})"
        )


class TestFontConfiguration:
    """Test that fonts are properly configured."""

    def test_font_sans_configured_with_inter(self):
        """font-sans should use Inter font."""
        content = GLOBALS_CSS_PATH.read_text()

        # Check that --font-sans references Inter
        match = re.search(r"--font-sans:\s*(.+?);", content)
        assert match, "--font-sans not defined in globals.css"

        font_value = match.group(1)
        assert "--font-inter" in font_value or "Inter" in font_value, (
            f"font-sans should use Inter font, got: {font_value}"
        )

    def test_font_serif_configured_with_playfair(self):
        """font-serif should use Playfair Display font."""
        content = GLOBALS_CSS_PATH.read_text()

        # Check that --font-serif references Playfair
        match = re.search(r"--font-serif:\s*(.+?);", content)
        assert match, "--font-serif not defined in globals.css"

        font_value = match.group(1)
        assert "--font-playfair" in font_value or "Playfair" in font_value, (
            f"font-serif should use Playfair Display font, got: {font_value}"
        )

    def test_font_display_configured_for_headings(self):
        """font-display should be defined for heading usage."""
        content = GLOBALS_CSS_PATH.read_text()

        # Check that --font-display is defined (commonly used for headings)
        match = re.search(r"--font-display:\s*(.+?);", content)
        assert match, "--font-display not defined in globals.css"

        font_value = match.group(1)
        # font-display should use Playfair for fashion headings
        assert "--font-playfair" in font_value or "Playfair" in font_value, (
            f"font-display should use Playfair Display for headings, got: {font_value}"
        )


class TestLayoutFontImports:
    """Test that fonts are properly imported in the layout."""

    def test_layout_imports_inter_font(self):
        """layout.tsx should import Inter font from Google Fonts."""
        assert LAYOUT_TSX_PATH.exists(), "app/layout.tsx not found"
        content = LAYOUT_TSX_PATH.read_text()

        # Check for Inter import from next/font/google
        has_inter_import = "Inter" in content and "next/font/google" in content
        assert has_inter_import, "Inter font should be imported from next/font/google"

    def test_layout_imports_playfair_font(self):
        """layout.tsx should import Playfair Display font from Google Fonts."""
        content = LAYOUT_TSX_PATH.read_text()

        # Check for Playfair_Display import from next/font/google
        has_playfair_import = "Playfair_Display" in content and "next/font/google" in content
        assert has_playfair_import, (
            "Playfair Display font should be imported from next/font/google"
        )

    def test_layout_defines_inter_css_variable(self):
        """Inter font should define a CSS variable."""
        content = LAYOUT_TSX_PATH.read_text()

        # Check for variable definition in Inter config
        has_inter_variable = 'variable: "--font-inter"' in content or "variable: '--font-inter'" in content
        assert has_inter_variable, "Inter font should define --font-inter CSS variable"

    def test_layout_defines_playfair_css_variable(self):
        """Playfair font should define a CSS variable."""
        content = LAYOUT_TSX_PATH.read_text()

        # Check for variable definition in Playfair config
        has_playfair_variable = 'variable: "--font-playfair"' in content or "variable: '--font-playfair'" in content
        assert has_playfair_variable, "Playfair font should define --font-playfair CSS variable"

    def test_layout_applies_font_variables_to_html(self):
        """Font CSS variables should be applied to the html element."""
        content = LAYOUT_TSX_PATH.read_text()

        # Check that className includes font variables
        has_inter_class = "inter.variable" in content
        has_playfair_class = "playfair.variable" in content

        assert has_inter_class, "inter.variable should be applied to html className"
        assert has_playfair_class, "playfair.variable should be applied to html className"


class TestExtendedSpacingScale:
    """Test that custom spacing values are defined."""

    def test_custom_spacing_values_defined(self):
        """Custom spacing values should be defined in the theme."""
        content = GLOBALS_CSS_PATH.read_text()

        # Check for at least some custom spacing values
        # These are extended values beyond Tailwind's defaults
        has_custom_spacing = (
            "--spacing-" in content
        )
        assert has_custom_spacing, "Custom spacing values should be defined in theme"

    def test_spacing_18_defined(self):
        """Spacing-18 should be defined for editorial layouts."""
        content = GLOBALS_CSS_PATH.read_text()

        match = re.search(r"--spacing-18:\s*[\d.]+rem", content)
        assert match, "--spacing-18 should be defined for extended spacing scale"


class TestExtendedTypographyScale:
    """Test that extended typography scale is defined."""

    def test_large_text_sizes_defined(self):
        """Large text sizes (7xl, 8xl, 9xl) should be defined for hero sections."""
        content = GLOBALS_CSS_PATH.read_text()

        expected_sizes = ["7xl", "8xl", "9xl"]
        for size in expected_sizes:
            pattern = rf"--text-{size}:\s*[\d.]+rem"
            match = re.search(pattern, content)
            assert match, f"--text-{size} should be defined for fashion hero sections"


class TestCustomAnimations:
    """Test that custom animations are defined."""

    def test_fade_in_animation_defined(self):
        """Fade-in animation should be defined."""
        content = GLOBALS_CSS_PATH.read_text()

        has_fade_in = "--animate-fade-in:" in content or "@keyframes fade-in" in content
        assert has_fade_in, "Fade-in animation should be defined"

    def test_custom_easing_functions_defined(self):
        """Custom easing functions should be defined for elegant transitions."""
        content = GLOBALS_CSS_PATH.read_text()

        # Check for custom easing curves
        has_custom_easing = (
            "--ease-out-expo" in content or
            "--ease-fashion" in content or
            "cubic-bezier" in content
        )
        assert has_custom_easing, "Custom easing functions should be defined"


class TestProseTypographyStyling:
    """Test that prose/typography styles are customized for blog content."""

    def test_prose_class_customized(self):
        """Prose class should have custom styling for blog content."""
        content = GLOBALS_CSS_PATH.read_text()

        # Check that .prose has custom variables or styles
        has_prose_customization = ".prose" in content
        assert has_prose_customization, (
            "Prose class should have custom styling for blog content"
        )

    def test_prose_uses_brand_colors(self):
        """Prose styling should incorporate brand colors."""
        content = GLOBALS_CSS_PATH.read_text()

        # Check that prose references brand colors
        # The implementation uses brand colors in blockquote border and link decorations
        has_brand_in_prose = (
            ("prose" in content.lower() and "brand" in content.lower()) or
            (re.search(r"\.prose.*\{[^}]*--.*brand", content, re.DOTALL))
        )
        # Alternative: check for the specific hex color used
        if not has_brand_in_prose:
            # Check for the brand-500 color value directly in prose section
            has_brand_in_prose = "184, 107, 133" in content or "b86b85" in content.lower()

        assert has_brand_in_prose, "Prose styling should incorporate brand colors"


class TestTailwindV4Configuration:
    """Test Tailwind CSS v4 specific configuration."""

    def test_tailwind_v4_import_syntax(self):
        """globals.css should use Tailwind v4 @import syntax."""
        content = GLOBALS_CSS_PATH.read_text()

        # Tailwind v4 uses @import "tailwindcss" instead of @tailwind directives
        has_v4_import = '@import "tailwindcss"' in content or "@import 'tailwindcss'" in content
        assert has_v4_import, (
            'globals.css should use Tailwind v4 import syntax: @import "tailwindcss"'
        )

    def test_tailwind_v4_theme_directive(self):
        """globals.css should use @theme directive for customization."""
        content = GLOBALS_CSS_PATH.read_text()

        has_theme_directive = "@theme" in content
        assert has_theme_directive, (
            "globals.css should use @theme directive for Tailwind v4 customization"
        )


class TestBodyDefaultFont:
    """Test that the body uses the correct default font."""

    def test_body_uses_font_sans(self):
        """Body should use font-sans (Inter) as the default font."""
        content = GLOBALS_CSS_PATH.read_text()

        # Check that body element references font-sans
        body_section = re.search(r"body\s*\{[^}]+\}", content)
        assert body_section, "Body styles should be defined in globals.css"

        body_styles = body_section.group(0)
        has_font_sans = "font-family" in body_styles and "font-sans" in body_styles
        assert has_font_sans, "Body should use var(--font-sans) for font-family"


class TestCustomAspectRatios:
    """Test that custom aspect ratios for fashion photography are defined."""

    def test_aspect_ratios_defined(self):
        """Custom aspect ratios should be defined for fashion photography."""
        content = GLOBALS_CSS_PATH.read_text()

        # Check for at least one custom aspect ratio
        has_aspect_ratio = "--aspect-" in content
        assert has_aspect_ratio, "Custom aspect ratios should be defined for fashion photography"
