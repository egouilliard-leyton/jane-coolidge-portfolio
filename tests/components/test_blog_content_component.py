"""
Tests for T-010: Create Portable Text renderer component

These tests verify that the BlogContent component is properly implemented according to requirements:
- Component accepts Portable Text array as prop
- All standard block types render correctly (paragraphs, headings, lists)
- Custom image blocks render with proper optimization and captions
- Links have proper styling and external link handling
- Block quotes are visually distinct
- Typography plugin classes are applied for optimal readability

Acceptance Criteria:
- Component accepts Portable Text array as prop
- All standard block types render correctly (paragraphs, headings, lists)
- Custom image blocks render with proper optimization and captions
- Links have proper styling and external link handling
- Block quotes are visually distinct
- Typography plugin classes are applied for optimal readability
"""

from pathlib import Path
import re


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
BLOG_CONTENT_FILE = PROJECT_ROOT / "components" / "content" / "BlogContent.tsx"
IMAGE_WITH_POPUP_FILE = PROJECT_ROOT / "components" / "ui" / "ImageWithPopup.tsx"


class TestBlogContentFileExists:
    """Test that BlogContent component file exists and has proper structure."""

    def test_blog_content_component_exists(self):
        """components/content/BlogContent.tsx should exist."""
        assert BLOG_CONTENT_FILE.exists(), "components/content/BlogContent.tsx not found"

    def test_blog_content_is_client_component(self):
        """BlogContent.tsx should have 'use client' directive."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "BlogContent should have 'use client' directive"
        )

    def test_blog_content_exports_default(self):
        """BlogContent.tsx should export default component."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "export default" in content, (
            "BlogContent.tsx should have default export"
        )


class TestComponentPropsInterface:
    """Test that BlogContent accepts Portable Text array as prop."""

    def test_has_props_interface(self):
        """BlogContent should define a BlogContentProps interface."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "BlogContentProps" in content, (
            "BlogContent should define BlogContentProps interface"
        )

    def test_accepts_content_prop(self):
        """BlogContent should accept 'content' prop of type PortableText."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for content prop in interface
        assert "content:" in content or "content :" in content, (
            "BlogContent should accept content prop"
        )

    def test_content_prop_type_is_portable_text(self):
        """content prop should be typed as PortableText."""
        content = BLOG_CONTENT_FILE.read_text()
        # Should import and use PortableText type
        assert "PortableText" in content, (
            "BlogContent should use PortableText type"
        )

    def test_accepts_optional_classname_prop(self):
        """BlogContent should accept optional className prop."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "className?" in content or "className ?" in content, (
            "BlogContent should accept optional className prop"
        )

    def test_imports_portable_text_from_sanity(self):
        """BlogContent should import PortableText component from @portabletext/react."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "@portabletext/react" in content, (
            "BlogContent should import from @portabletext/react"
        )

    def test_imports_types_from_types_module(self):
        """BlogContent should import types from @/types module."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "@/types" in content, (
            "BlogContent should import types from @/types"
        )


class TestPortableTextRenderer:
    """Test that PortableText is properly configured with custom components."""

    def test_uses_portable_text_component(self):
        """BlogContent should render PortableText component."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "<PortableText" in content, (
            "BlogContent should render PortableText component"
        )

    def test_passes_value_prop(self):
        """BlogContent should pass content as value prop to PortableText."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "value={content}" in content or "value={ content }" in content, (
            "BlogContent should pass content as value prop"
        )

    def test_passes_custom_components(self):
        """BlogContent should pass custom components to PortableText."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "components=" in content or "components =" in content, (
            "BlogContent should pass components prop to PortableText"
        )

    def test_defines_portable_text_components(self):
        """BlogContent should define PortableTextComponents object."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "PortableTextComponents" in content, (
            "BlogContent should define PortableTextComponents"
        )


class TestStandardBlockTypes:
    """Test that all standard block types render correctly."""

    def test_renders_normal_paragraph(self):
        """BlogContent should handle 'normal' block style for paragraphs."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for block.normal definition
        assert "normal:" in content, (
            "BlogContent should define 'normal' block renderer for paragraphs"
        )
        assert "<p" in content, "BlogContent should render p elements for paragraphs"

    def test_renders_h2_headings(self):
        """BlogContent should handle 'h2' block style."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "h2:" in content, (
            "BlogContent should define 'h2' block renderer"
        )
        assert "<h2" in content, "BlogContent should render h2 elements"

    def test_renders_h3_headings(self):
        """BlogContent should handle 'h3' block style."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "h3:" in content, (
            "BlogContent should define 'h3' block renderer"
        )
        assert "<h3" in content, "BlogContent should render h3 elements"

    def test_renders_h4_headings(self):
        """BlogContent should handle 'h4' block style."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "h4:" in content, (
            "BlogContent should define 'h4' block renderer"
        )
        assert "<h4" in content, "BlogContent should render h4 elements"

    def test_headings_have_id_attribute(self):
        """Headings should have id attribute for anchor links."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check that h2, h3, h4 have id attribute
        assert "id=" in content, "Headings should have id attribute for anchor links"

    def test_has_generate_slug_function(self):
        """BlogContent should have generateSlug function for heading IDs."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "generateSlug" in content, (
            "BlogContent should have generateSlug function"
        )


class TestListRendering:
    """Test that list types render correctly."""

    def test_renders_bullet_list(self):
        """BlogContent should handle bullet list type."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "bullet:" in content, (
            "BlogContent should define 'bullet' list renderer"
        )
        assert "<ul" in content, "BlogContent should render ul elements"

    def test_renders_number_list(self):
        """BlogContent should handle number list type."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "number:" in content, (
            "BlogContent should define 'number' list renderer"
        )
        assert "<ol" in content, "BlogContent should render ol elements"

    def test_defines_list_item_components(self):
        """BlogContent should define listItem components."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "listItem:" in content or "listItem :" in content, (
            "BlogContent should define listItem components"
        )

    def test_renders_list_items(self):
        """BlogContent should render li elements for list items."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "<li" in content, "BlogContent should render li elements"


class TestBlockQuoteStyling:
    """Test that block quotes are visually distinct."""

    def test_renders_blockquote(self):
        """BlogContent should handle blockquote block style."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "blockquote:" in content, (
            "BlogContent should define 'blockquote' block renderer"
        )
        assert "<blockquote" in content, "BlogContent should render blockquote elements"

    def test_blockquote_has_distinct_styling(self):
        """Blockquote should have visually distinct styling."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for border-left styling which is common for blockquotes
        assert "border-l" in content, (
            "Blockquote should have left border styling"
        )

    def test_blockquote_has_background(self):
        """Blockquote should have background styling."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for background class in blockquote section
        blockquote_pattern = r"blockquote:.*?<blockquote[^>]*className[^>]*>"
        if re.search(blockquote_pattern, content, re.DOTALL):
            # Found blockquote, check for bg- class
            assert "bg-" in content, "Blockquote should have background color"

    def test_blockquote_has_padding(self):
        """Blockquote should have padding."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for padding classes
        has_padding = "pl-" in content or "px-" in content or "py-" in content or "p-" in content
        assert has_padding, "Blockquote should have padding"


class TestLinkHandling:
    """Test that links have proper styling and external link handling."""

    def test_defines_link_mark(self):
        """BlogContent should define 'link' mark renderer."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "link:" in content, (
            "BlogContent should define 'link' mark renderer"
        )

    def test_renders_anchor_elements(self):
        """BlogContent should render anchor elements for links."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "<a" in content, "BlogContent should render anchor elements"

    def test_external_links_open_in_new_tab(self):
        """External links should open in new tab."""
        content = BLOG_CONTENT_FILE.read_text()
        assert 'target="_blank"' in content or "target='_blank'" in content, (
            "External links should have target=_blank"
        )

    def test_external_links_have_security_attributes(self):
        """External links should have noopener noreferrer for security."""
        content = BLOG_CONTENT_FILE.read_text()
        assert 'rel="noopener noreferrer"' in content or "rel='noopener noreferrer'" in content, (
            "External links should have rel=noopener noreferrer"
        )

    def test_checks_for_external_link(self):
        """BlogContent should check if link is external (starts with http)."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for external link detection logic
        assert "http" in content, (
            "BlogContent should check if link starts with http"
        )

    def test_handles_open_in_new_tab_property(self):
        """BlogContent should respect openInNewTab property."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "openInNewTab" in content, (
            "BlogContent should handle openInNewTab property"
        )

    def test_links_have_styling(self):
        """Links should have proper styling classes."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for text color and underline styling
        assert "underline" in content, "Links should have underline styling"

    def test_links_have_hover_styling(self):
        """Links should have hover state styling."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "hover:" in content, "Links should have hover state styling"

    def test_external_link_has_screen_reader_text(self):
        """External links should have screen reader text."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "sr-only" in content, (
            "External links should have screen reader text (sr-only)"
        )


class TestInternalLinks:
    """Test internal link handling."""

    def test_defines_internal_link_mark(self):
        """BlogContent should define 'internalLink' mark renderer."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "internalLink:" in content or "internalLink :" in content, (
            "BlogContent should define 'internalLink' mark renderer"
        )

    def test_uses_next_link_for_internal_links(self):
        """BlogContent should use Next.js Link for internal links."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "import Link from" in content, (
            "BlogContent should import Next.js Link component"
        )
        assert "<Link" in content, (
            "BlogContent should use Link component for internal links"
        )

    def test_imports_portable_text_internal_link_type(self):
        """BlogContent should import PortableTextInternalLinkMark type."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "PortableTextInternalLinkMark" in content, (
            "BlogContent should import PortableTextInternalLinkMark type"
        )


class TestTextMarks:
    """Test text mark rendering (bold, italic, etc.)."""

    def test_defines_strong_mark(self):
        """BlogContent should define 'strong' mark renderer."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "strong:" in content, (
            "BlogContent should define 'strong' mark renderer"
        )
        assert "<strong" in content, "BlogContent should render strong elements"

    def test_defines_em_mark(self):
        """BlogContent should define 'em' mark renderer."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "em:" in content, (
            "BlogContent should define 'em' mark renderer"
        )
        assert "<em" in content, "BlogContent should render em elements"

    def test_defines_underline_mark(self):
        """BlogContent should define 'underline' mark renderer."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "underline:" in content, (
            "BlogContent should define 'underline' mark renderer"
        )

    def test_defines_strikethrough_mark(self):
        """BlogContent should define strike-through mark renderer."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "strike-through" in content or "strikethrough" in content, (
            "BlogContent should define strike-through mark renderer"
        )


class TestCustomImageBlocks:
    """Test that custom image blocks render with proper optimization and captions."""

    def test_defines_image_type(self):
        """BlogContent should define imageWithPopup custom type."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "imageWithPopup:" in content or "imageWithPopup :" in content, (
            "BlogContent should define 'imageWithPopup' custom type"
        )

    def test_uses_next_image_component(self):
        """Image rendering should use Next.js Image for optimization."""
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
        content = BLOG_CONTENT_FILE.read_text()
        assert "alt=" in content, "Image should have alt attribute"

    def test_image_uses_url_for_helper(self):
        """Image rendering should use urlFor helper for Sanity images."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "urlFor" in content, (
            "ImageWithPopup should use urlFor helper for image URLs"
        )
        assert "@/sanity/lib/image" in content, (
            "ImageWithPopup should import urlFor from @/sanity/lib/image"
        )

    def test_renders_figure_element(self):
        """Images should be wrapped in figure element."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<figure" in content, "Images should be wrapped in figure element"

    def test_renders_figcaption_for_caption(self):
        """Images should render figcaption when caption is provided."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "<figcaption" in content or "figcaption" in content, (
            "ImageWithPopup should render figcaption for image captions"
        )

    def test_caption_is_conditional(self):
        """Caption should only render when provided."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        # Check for conditional caption rendering
        assert "caption &&" in content or "{caption &&" in content, (
            "Caption should be conditionally rendered"
        )

    def test_handles_image_size_variations(self):
        """BlogContent should handle different image size options."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for size prop usage
        assert "size" in content, (
            "BlogContent should handle image size property"
        )

    def test_image_handles_missing_asset(self):
        """BlogContent should handle images with missing asset gracefully."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for null check on image.asset
        assert "asset" in content, "BlogContent should check for image asset"

    def test_imports_image_with_popup_type(self):
        """BlogContent should import PortableTextImageWithPopup type."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "PortableTextImageWithPopup" in content, (
            "BlogContent should import PortableTextImageWithPopup type"
        )


class TestTypographyPluginClasses:
    """Test that typography plugin classes are applied for optimal readability."""

    def test_wrapper_has_prose_class(self):
        """BlogContent wrapper should have 'prose' class from typography plugin."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "prose" in content, (
            "BlogContent should use 'prose' class from typography plugin"
        )

    def test_wrapper_has_prose_lg_for_readability(self):
        """BlogContent should use prose-lg for larger text."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "prose-lg" in content, (
            "BlogContent should use 'prose-lg' for better readability"
        )

    def test_wrapper_has_max_w_none(self):
        """BlogContent should have max-w-none to not constrain width."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "max-w-none" in content, (
            "BlogContent should have 'max-w-none' class"
        )

    def test_paragraphs_have_leading_relaxed(self):
        """Paragraphs should have relaxed line-height for readability."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "leading-relaxed" in content, (
            "Paragraphs should have 'leading-relaxed' class"
        )

    def test_paragraphs_have_margin_bottom(self):
        """Paragraphs should have bottom margin for spacing."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "mb-" in content, (
            "Paragraphs should have margin-bottom for spacing"
        )

    def test_headings_have_tracking(self):
        """Headings should have letter-spacing (tracking) for style."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "tracking-" in content, (
            "Headings should have tracking class for letter-spacing"
        )

    def test_headings_have_scroll_margin(self):
        """Headings should have scroll-margin-top for anchor links."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "scroll-mt-" in content, (
            "Headings should have scroll-mt for proper anchor link positioning"
        )


class TestResponsiveTypography:
    """Test responsive typography sizing."""

    def test_headings_have_responsive_sizing(self):
        """Headings should have responsive text sizing."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for responsive text sizing (e.g., text-3xl md:text-4xl)
        assert "md:text-" in content, (
            "Headings should have responsive text sizing"
        )


class TestDarkModeSupport:
    """Test dark mode styling support."""

    def test_has_dark_mode_classes(self):
        """BlogContent should have dark mode styling."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "dark:" in content, (
            "BlogContent should have dark mode styling classes"
        )

    def test_text_colors_support_dark_mode(self):
        """Text colors should support dark mode."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for dark mode text colors
        dark_text_pattern = r"dark:text-"
        assert re.search(dark_text_pattern, content), (
            "Text colors should have dark mode variants"
        )


class TestExternalLinkIcon:
    """Test external link icon rendering."""

    def test_has_external_link_icon(self):
        """BlogContent should have ExternalLinkIcon component."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "ExternalLinkIcon" in content, (
            "BlogContent should have ExternalLinkIcon component"
        )

    def test_external_link_icon_is_accessible(self):
        """ExternalLinkIcon should be hidden from assistive technology."""
        content = BLOG_CONTENT_FILE.read_text()
        assert 'aria-hidden="true"' in content or "aria-hidden='true'" in content, (
            "ExternalLinkIcon should have aria-hidden for accessibility"
        )


class TestSlugGeneration:
    """Test heading slug generation for anchor links."""

    def test_generate_slug_function_exists(self):
        """generateSlug function should exist for creating heading IDs."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "function generateSlug" in content, (
            "generateSlug function should be defined"
        )

    def test_generate_slug_handles_block_children(self):
        """generateSlug should extract text from block children."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "children" in content, (
            "generateSlug should handle block children"
        )

    def test_generate_slug_lowercases_text(self):
        """generateSlug should lowercase text."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "toLowerCase" in content, (
            "generateSlug should lowercase text"
        )

    def test_generate_slug_replaces_special_chars(self):
        """generateSlug should replace special characters with hyphens."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "replace" in content, (
            "generateSlug should use replace for special characters"
        )


class TestBrandColors:
    """Test use of brand colors for styling."""

    def test_uses_brand_colors(self):
        """BlogContent should use brand colors for accents."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "brand-" in content, (
            "BlogContent should use brand colors"
        )

    def test_blockquote_uses_brand_border(self):
        """Blockquote should use brand color for border."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "border-brand" in content, (
            "Blockquote should use brand color for border"
        )

    def test_links_use_brand_colors(self):
        """Links should use brand colors."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "text-brand" in content, (
            "Links should use brand text colors"
        )


class TestListStyling:
    """Test custom list styling."""

    def test_bullet_list_has_custom_markers(self):
        """Bullet lists should have custom markers."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for custom bullet styling
        assert "list-none" in content, (
            "Lists should use list-none to hide default markers"
        )

    def test_bullet_list_items_have_visual_markers(self):
        """Bullet list items should have visual marker elements."""
        content = BLOG_CONTENT_FILE.read_text()
        # Check for custom bullet element styling
        assert "rounded-full" in content, (
            "Bullet markers should have rounded-full class"
        )

    def test_number_list_uses_counter(self):
        """Number lists should use CSS counter for numbering."""
        content = BLOG_CONTENT_FILE.read_text()
        assert "counter" in content, (
            "Number lists should use CSS counter"
        )
