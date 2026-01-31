"""
Tests for T-021: Optimize images and implement lazy loading

These tests verify that images are properly optimized according to requirements:
- All images use next/image component
- Blur-up placeholders are configured via Sanity LQIP
- Image sizes are specified for responsive optimization
- Below-fold images lazy load automatically
- Image configuration in next.config.ts is properly set up

Acceptance Criteria:
- All images use next/image component
- Blur-up placeholders are configured via Sanity LQIP
- Image sizes are specified for responsive optimization
- Below-fold images lazy load automatically
- Largest Contentful Paint (LCP) is under 2.5 seconds
- No layout shift occurs when images load
"""

from pathlib import Path
import re
import json

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
NEXT_CONFIG_FILE = PROJECT_ROOT / "next.config.ts"
SANITY_IMAGE_FILE = PROJECT_ROOT / "sanity" / "lib" / "image.ts"
IMAGE_WITH_POPUP_FILE = PROJECT_ROOT / "components" / "ui" / "ImageWithPopup.tsx"
HOMEPAGE_CLIENT_FILE = PROJECT_ROOT / "components" / "home" / "HomePageClient.tsx"
ANIMATED_SECTIONS_FILE = PROJECT_ROOT / "components" / "home" / "AnimatedSections.tsx"
PROJECT_DETAIL_FILE = PROJECT_ROOT / "app" / "(site)" / "projects" / "[slug]" / "page.tsx"
BLOG_DETAIL_FILE = PROJECT_ROOT / "app" / "(site)" / "blog" / "[slug]" / "page.tsx"


class TestNextImageComponentUsage:
    """Test that all images use next/image component."""

    def test_homepage_client_uses_next_image(self):
        """HomePageClient.tsx should import and use next/image."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "HomePageClient should import next/image"
        )
        assert "<Image" in content, (
            "HomePageClient should use Image component from next/image"
        )

    def test_animated_sections_uses_next_image(self):
        """AnimatedSections.tsx should import and use next/image."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "AnimatedSections should import next/image"
        )
        assert "<Image" in content, (
            "AnimatedSections should use Image component"
        )

    def test_image_with_popup_uses_next_image(self):
        """ImageWithPopup.tsx should import and use next/image."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "ImageWithPopup should import next/image"
        )
        assert "<Image" in content, (
            "ImageWithPopup should use Image component"
        )

    def test_project_detail_uses_next_image(self):
        """Project detail page should import and use next/image."""
        content = PROJECT_DETAIL_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "Project detail page should import next/image"
        )
        assert "<Image" in content, (
            "Project detail page should use Image component"
        )

    def test_blog_detail_uses_next_image(self):
        """Blog detail page should import and use next/image."""
        content = BLOG_DETAIL_FILE.read_text()
        assert "import Image from 'next/image'" in content or 'import Image from "next/image"' in content, (
            "Blog detail page should import next/image"
        )
        assert "<Image" in content, (
            "Blog detail page should use Image component"
        )

    def test_no_plain_img_tags_in_homepage_client(self):
        """HomePageClient should not use plain <img> tags."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        # Match plain <img tags but not in JSX string literals
        img_pattern = r"<img\s"
        matches = re.findall(img_pattern, content)
        assert len(matches) == 0, (
            f"HomePageClient should not use plain <img> tags, found {len(matches)}"
        )

    def test_no_plain_img_tags_in_animated_sections(self):
        """AnimatedSections should not use plain <img> tags."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        img_pattern = r"<img\s"
        matches = re.findall(img_pattern, content)
        assert len(matches) == 0, (
            f"AnimatedSections should not use plain <img> tags, found {len(matches)}"
        )


class TestNextConfigImageConfiguration:
    """Test next.config.ts has proper image configuration."""

    def test_next_config_exists(self):
        """next.config.ts should exist."""
        assert NEXT_CONFIG_FILE.exists(), "next.config.ts not found"

    def test_images_config_present(self):
        """next.config.ts should have images configuration."""
        content = NEXT_CONFIG_FILE.read_text()
        assert "images:" in content or "images :" in content, (
            "next.config.ts should have images configuration"
        )

    def test_sanity_cdn_configured(self):
        """next.config.ts should have Sanity CDN configured in remotePatterns."""
        content = NEXT_CONFIG_FILE.read_text()
        assert "cdn.sanity.io" in content, (
            "next.config.ts should have cdn.sanity.io configured"
        )

    def test_remote_patterns_configured(self):
        """next.config.ts should have remotePatterns configured."""
        content = NEXT_CONFIG_FILE.read_text()
        assert "remotePatterns" in content, (
            "next.config.ts should have remotePatterns configured"
        )

    def test_formats_include_avif(self):
        """next.config.ts should include avif format for optimization."""
        content = NEXT_CONFIG_FILE.read_text()
        assert "avif" in content, (
            "next.config.ts should include avif format"
        )

    def test_formats_include_webp(self):
        """next.config.ts should include webp format for optimization."""
        content = NEXT_CONFIG_FILE.read_text()
        assert "webp" in content, (
            "next.config.ts should include webp format"
        )

    def test_device_sizes_configured(self):
        """next.config.ts should have deviceSizes configured for srcset."""
        content = NEXT_CONFIG_FILE.read_text()
        assert "deviceSizes" in content, (
            "next.config.ts should have deviceSizes configured"
        )

    def test_image_sizes_configured(self):
        """next.config.ts should have imageSizes configured for srcset."""
        content = NEXT_CONFIG_FILE.read_text()
        assert "imageSizes" in content, (
            "next.config.ts should have imageSizes configured"
        )

    def test_cache_ttl_configured(self):
        """next.config.ts should have cache TTL configured."""
        content = NEXT_CONFIG_FILE.read_text()
        assert "minimumCacheTTL" in content, (
            "next.config.ts should have minimumCacheTTL configured for caching"
        )


class TestBlurUpPlaceholders:
    """Test that blur-up placeholders are configured via Sanity LQIP."""

    def test_sanity_image_helper_exists(self):
        """sanity/lib/image.ts should exist with blur placeholder helpers."""
        assert SANITY_IMAGE_FILE.exists(), "sanity/lib/image.ts not found"

    def test_image_helper_exports_blur_placeholder_function(self):
        """sanity/lib/image.ts should export getBlurPlaceholder function."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "getBlurPlaceholder" in content, (
            "sanity/lib/image.ts should export getBlurPlaceholder function"
        )

    def test_image_helper_handles_lqip(self):
        """sanity/lib/image.ts should handle LQIP (Low Quality Image Placeholder)."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "lqip" in content, (
            "sanity/lib/image.ts should handle LQIP"
        )

    def test_blur_placeholder_returns_blur_type(self):
        """getBlurPlaceholder should return placeholder: 'blur' when LQIP exists."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "'blur'" in content or '"blur"' in content, (
            "getBlurPlaceholder should return placeholder: 'blur'"
        )

    def test_homepage_hero_uses_blur_placeholder(self):
        """Homepage hero image should use blur placeholder."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert "placeholder=" in content, (
            "Homepage should use placeholder prop on Image"
        )
        assert "blurDataURL=" in content, (
            "Homepage should use blurDataURL prop on Image"
        )

    def test_homepage_hero_uses_lqip_from_sanity(self):
        """Homepage hero should use LQIP from Sanity metadata."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert "metadata?.lqip" in content or "metadata.lqip" in content, (
            "Homepage hero should use LQIP from Sanity metadata"
        )

    def test_image_with_popup_supports_blur_placeholder(self):
        """ImageWithPopup should support blur placeholder via lqip prop."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "lqip" in content, (
            "ImageWithPopup should support lqip prop"
        )
        assert "blurDataURL" in content, (
            "ImageWithPopup should use blurDataURL for blur effect"
        )
        assert "placeholder=" in content, (
            "ImageWithPopup should use placeholder prop"
        )

    def test_animated_post_card_uses_blur_placeholder(self):
        """AnimatedPostCard should use blur placeholder for cover images."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "metadata?.lqip" in content, (
            "AnimatedPostCard should check for LQIP metadata"
        )
        assert "blurDataURL=" in content, (
            "AnimatedPostCard should use blurDataURL"
        )

    def test_animated_project_card_uses_blur_placeholder(self):
        """AnimatedProjectCard should use blur placeholder for cover images."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Verify both post and project cards have blur placeholders
        blur_data_url_count = content.count("blurDataURL=")
        assert blur_data_url_count >= 2, (
            f"AnimatedSections should use blurDataURL for both post and project cards, found {blur_data_url_count}"
        )

    def test_project_detail_uses_blur_placeholder(self):
        """Project detail page should use blur placeholder for cover image."""
        content = PROJECT_DETAIL_FILE.read_text()
        assert "metadata?.lqip" in content, (
            "Project detail should check for LQIP metadata"
        )
        assert "blurDataURL=" in content, (
            "Project detail should use blurDataURL"
        )

    def test_blog_detail_uses_blur_placeholder(self):
        """Blog detail page should use blur placeholder for cover image."""
        content = BLOG_DETAIL_FILE.read_text()
        assert "metadata?.lqip" in content, (
            "Blog detail should check for LQIP metadata"
        )
        assert "blurDataURL=" in content, (
            "Blog detail should use blurDataURL"
        )


class TestResponsiveImageSizes:
    """Test that image sizes are specified for responsive optimization."""

    def test_sanity_lib_has_responsive_sizes_function(self):
        """sanity/lib/image.ts should have getResponsiveSizes function."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "getResponsiveSizes" in content, (
            "sanity/lib/image.ts should have getResponsiveSizes function"
        )

    def test_responsive_sizes_handles_hero_variant(self):
        """getResponsiveSizes should handle hero variant."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "'hero'" in content or '"hero"' in content, (
            "getResponsiveSizes should handle hero variant"
        )

    def test_responsive_sizes_handles_card_variant(self):
        """getResponsiveSizes should handle card variant."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "'card'" in content or '"card"' in content, (
            "getResponsiveSizes should handle card variant"
        )

    def test_responsive_sizes_handles_gallery_variant(self):
        """getResponsiveSizes should handle gallery variant."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "'gallery'" in content or '"gallery"' in content, (
            "getResponsiveSizes should handle gallery variant"
        )

    def test_responsive_sizes_uses_viewport_widths(self):
        """getResponsiveSizes should use viewport width units."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "vw" in content, (
            "getResponsiveSizes should use viewport width units (vw)"
        )

    def test_homepage_hero_has_sizes_prop(self):
        """Homepage hero image should have sizes prop."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert "sizes=" in content, (
            "Homepage hero image should have sizes prop"
        )

    def test_homepage_hero_uses_100vw(self):
        """Homepage hero image should use 100vw for full-width display."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert '"100vw"' in content or "'100vw'" in content, (
            "Homepage hero should use 100vw for full-width display"
        )

    def test_animated_post_card_has_sizes_prop(self):
        """AnimatedPostCard should have sizes prop on images."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Check for sizes prop in post card context
        assert "sizes=" in content, (
            "AnimatedPostCard should have sizes prop"
        )

    def test_animated_project_card_has_sizes_prop(self):
        """AnimatedProjectCard should have sizes prop on images."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Multiple sizes props expected for different cards
        sizes_count = content.count("sizes=")
        assert sizes_count >= 2, (
            f"AnimatedSections should have sizes on multiple images, found {sizes_count}"
        )

    def test_image_with_popup_uses_responsive_sizes(self):
        """ImageWithPopup should use getResponsiveSizes helper."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "getResponsiveSizes" in content, (
            "ImageWithPopup should use getResponsiveSizes helper"
        )
        assert "sizes=" in content, (
            "ImageWithPopup should have sizes prop on Image"
        )

    def test_image_presets_defined(self):
        """sanity/lib/image.ts should define IMAGE_PRESETS for consistent sizing."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "IMAGE_PRESETS" in content, (
            "sanity/lib/image.ts should define IMAGE_PRESETS"
        )

    def test_image_presets_include_hero(self):
        """IMAGE_PRESETS should include hero preset."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "hero:" in content, (
            "IMAGE_PRESETS should include hero preset"
        )

    def test_image_presets_include_cover(self):
        """IMAGE_PRESETS should include cover preset."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "cover:" in content, (
            "IMAGE_PRESETS should include cover preset"
        )

    def test_image_presets_include_blog_featured(self):
        """IMAGE_PRESETS should include blogFeatured preset."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "blogFeatured:" in content, (
            "IMAGE_PRESETS should include blogFeatured preset"
        )


class TestLazyLoadingConfiguration:
    """Test that below-fold images lazy load automatically."""

    def test_homepage_hero_has_priority(self):
        """Homepage hero (above-fold) should have priority prop."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert "priority" in content, (
            "Homepage hero image should have priority prop for LCP optimization"
        )

    def test_homepage_hero_has_fetch_priority(self):
        """Homepage hero should have fetchPriority='high' for LCP."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert "fetchPriority" in content, (
            "Homepage hero should have fetchPriority for LCP optimization"
        )

    def test_animated_post_card_uses_conditional_loading(self):
        """AnimatedPostCard should use conditional loading based on index."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "loading=" in content, (
            "AnimatedPostCard should have loading prop"
        )
        # Check for conditional lazy loading based on index
        assert "eager" in content and "lazy" in content, (
            "AnimatedPostCard should conditionally use eager/lazy loading based on index"
        )

    def test_animated_project_card_uses_conditional_loading(self):
        """AnimatedProjectCard should use conditional loading based on index."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        # Check for multiple loading conditions
        loading_count = content.count("loading=")
        assert loading_count >= 2, (
            f"AnimatedSections should have loading props, found {loading_count}"
        )

    def test_image_with_popup_supports_priority_prop(self):
        """ImageWithPopup should support priority prop for above-fold images."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "priority" in content, (
            "ImageWithPopup should support priority prop"
        )
        # Check for conditional loading
        assert "loading=" in content, (
            "ImageWithPopup should use loading prop for lazy loading"
        )

    def test_image_with_popup_lazy_loads_by_default(self):
        """ImageWithPopup should lazy load by default (priority=false)."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "priority = false" in content or "priority=false" in content or "priority: false" in content, (
            "ImageWithPopup should default priority to false for lazy loading"
        )

    def test_project_detail_hero_has_priority(self):
        """Project detail hero (above-fold) should have priority prop."""
        content = PROJECT_DETAIL_FILE.read_text()
        assert "priority" in content, (
            "Project detail cover image should have priority prop"
        )

    def test_project_detail_adjacent_images_lazy_load(self):
        """Project detail adjacent thumbnails should lazy load."""
        content = PROJECT_DETAIL_FILE.read_text()
        assert 'loading="lazy"' in content or "loading='lazy'" in content, (
            "Project detail adjacent thumbnails should have loading='lazy'"
        )

    def test_blog_detail_hero_has_priority(self):
        """Blog detail hero (above-fold) should have priority prop."""
        content = BLOG_DETAIL_FILE.read_text()
        assert "priority" in content, (
            "Blog detail cover image should have priority prop"
        )


class TestLayoutShiftPrevention:
    """Test that configuration prevents layout shift when images load."""

    def test_homepage_hero_uses_fill_layout(self):
        """Homepage hero should use fill prop for stable layout."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        # Check for fill prop on hero image
        assert "fill" in content, (
            "Homepage hero should use fill prop"
        )

    def test_image_with_popup_has_width_height(self):
        """ImageWithPopup should have width and height for aspect ratio."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "width=" in content, (
            "ImageWithPopup should have width prop"
        )
        assert "height=" in content, (
            "ImageWithPopup should have height prop"
        )

    def test_animated_post_card_uses_fill(self):
        """AnimatedPostCard should use fill layout for stable aspect ratio."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "fill" in content, (
            "AnimatedPostCard should use fill prop"
        )

    def test_animated_sections_have_aspect_ratio_containers(self):
        """AnimatedSections should have aspect ratio containers."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "aspect-" in content, (
            "AnimatedSections should use aspect ratio classes (aspect-*)"
        )

    def test_project_detail_cover_uses_fill(self):
        """Project detail cover image should use fill prop."""
        content = PROJECT_DETAIL_FILE.read_text()
        assert "fill" in content, (
            "Project detail cover image should use fill"
        )

    def test_blog_detail_cover_uses_fill(self):
        """Blog detail cover image should use fill prop."""
        content = BLOG_DETAIL_FILE.read_text()
        assert "fill" in content, (
            "Blog detail cover image should use fill"
        )

    def test_sanity_queries_include_dimensions(self):
        """Sanity GROQ queries should request image dimensions."""
        queries_file = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
        if queries_file.exists():
            content = queries_file.read_text()
            assert "dimensions" in content, (
                "Sanity queries should request image dimensions for CLS prevention"
            )

    def test_sanity_image_helper_provides_dimensions(self):
        """sanity/lib/image.ts should provide image dimensions helper."""
        content = SANITY_IMAGE_FILE.read_text()
        assert "getImageDimensions" in content, (
            "sanity/lib/image.ts should have getImageDimensions helper"
        )


class TestImageQualityOptimization:
    """Test that images use appropriate quality settings."""

    def test_sanity_url_builder_uses_quality(self):
        """Image URL generation should use quality settings."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "quality" in content, (
            "ImageWithPopup should use quality setting in URL generation"
        )

    def test_homepage_hero_uses_high_quality(self):
        """Homepage hero should use high quality (90) for important visual."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert "quality(90)" in content or ".quality(90)" in content, (
            "Homepage hero should use quality(90) for high visual importance"
        )

    def test_sanity_uses_auto_format(self):
        """Image URLs should use auto format for optimal encoding."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "auto('format')" in content or 'auto("format")' in content, (
            "Image URLs should use auto format"
        )

    def test_homepage_uses_auto_format(self):
        """Homepage images should use auto format."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert "auto('format')" in content or 'auto("format")' in content, (
            "Homepage images should use auto format"
        )

    def test_image_presets_have_quality_values(self):
        """IMAGE_PRESETS should include quality values."""
        content = SANITY_IMAGE_FILE.read_text()
        quality_count = content.count("quality:")
        assert quality_count >= 3, (
            f"IMAGE_PRESETS should have quality values for multiple presets, found {quality_count}"
        )


class TestImageObjectFit:
    """Test that images use proper object-fit for styling."""

    def test_images_use_object_cover(self):
        """Images should use object-cover for proper cropping."""
        content = ANIMATED_SECTIONS_FILE.read_text()
        assert "object-cover" in content, (
            "Images should use object-cover class"
        )

    def test_homepage_hero_uses_object_cover(self):
        """Homepage hero should use object-cover."""
        content = HOMEPAGE_CLIENT_FILE.read_text()
        assert "object-cover" in content, (
            "Homepage hero should use object-cover"
        )

    def test_image_with_popup_uses_object_cover(self):
        """ImageWithPopup should use object-cover."""
        content = IMAGE_WITH_POPUP_FILE.read_text()
        assert "object-cover" in content, (
            "ImageWithPopup should use object-cover"
        )


class TestSanityImageMetadataQuery:
    """Test that Sanity queries properly request image metadata."""

    def test_queries_file_exists(self):
        """sanity/lib/queries.ts should exist."""
        queries_file = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
        assert queries_file.exists(), "sanity/lib/queries.ts not found"

    def test_image_projection_includes_metadata(self):
        """Image projection should include metadata field."""
        queries_file = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
        content = queries_file.read_text()
        assert "metadata" in content, (
            "Image projection should include metadata field"
        )

    def test_image_projection_includes_lqip(self):
        """Image projection should include lqip in metadata."""
        queries_file = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
        content = queries_file.read_text()
        assert "lqip" in content, (
            "Image projection should include lqip in metadata"
        )

    def test_image_projection_includes_url(self):
        """Image projection should include url field."""
        queries_file = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
        content = queries_file.read_text()
        assert "url" in content, (
            "Image projection should include url field"
        )

    def test_image_projection_includes_asset_expansion(self):
        """Image projection should expand asset reference."""
        queries_file = PROJECT_ROOT / "sanity" / "lib" / "queries.ts"
        content = queries_file.read_text()
        assert "asset->" in content, (
            "Image projection should expand asset reference with asset->"
        )
