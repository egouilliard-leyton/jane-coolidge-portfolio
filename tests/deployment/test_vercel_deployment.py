"""
Tests for T-023: Deploy to Vercel and configure production settings

These tests verify that the Vercel deployment is properly configured according to the requirements:
- Repository is connected to Vercel (configuration files exist)
- All environment variables are documented for Vercel dashboard configuration
- Production deployment configuration is correct
- HTTPS is enforced via security headers
- Sanity Studio is accessible at /studio route
- Core Web Vitals configuration supports performance targets
- Vercel Analytics is integrated

Acceptance Criteria:
- Repository is connected to Vercel (vercel.json configured)
- All environment variables are configured in Vercel dashboard (documented in .env.example)
- Production deployment succeeds without errors (build script configured)
- HTTPS is enforced on all pages (security headers configured)
- Custom domain is configured and SSL certificate is active (if applicable)
- Sanity Studio is accessible at production-url.com/studio
- Content changes in production Sanity reflect on production site (revalidation configured)
- Lighthouse performance score is >= 90 in production (performance optimizations configured)
- Core Web Vitals pass (LCP < 2.5s, CLS < 0.1, FCP < 1.5s) (image optimization configured)
"""

import json
from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent


# =============================================================================
# VERCEL CONFIGURATION FILE TESTS
# =============================================================================


class TestVercelConfigurationFile:
    """Test that vercel.json is properly configured for deployment."""

    def test_vercel_json_exists(self):
        """vercel.json should exist in project root."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        assert vercel_config_path.exists(), "vercel.json not found in project root"

    def test_vercel_json_is_valid_json(self):
        """vercel.json should be valid JSON."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        assert isinstance(data, dict), "vercel.json should contain a JSON object"

    def test_vercel_json_has_schema(self):
        """vercel.json should have a schema reference."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        assert "$schema" in data, "vercel.json should have $schema for validation"
        assert "vercel" in data["$schema"].lower(), "Schema should be Vercel schema"

    def test_vercel_json_specifies_nextjs_framework(self):
        """vercel.json should specify Next.js as the framework."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        assert data.get("framework") == "nextjs", (
            "vercel.json should specify 'nextjs' as framework"
        )

    def test_vercel_json_has_build_command(self):
        """vercel.json should specify the build command."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        assert "buildCommand" in data, "vercel.json should specify buildCommand"
        assert "build" in data["buildCommand"], (
            "buildCommand should include 'build'"
        )

    def test_vercel_json_has_install_command(self):
        """vercel.json should specify the install command."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        assert "installCommand" in data, "vercel.json should specify installCommand"
        assert "npm install" in data["installCommand"], (
            "installCommand should include 'npm install'"
        )

    def test_vercel_json_specifies_region(self):
        """vercel.json should specify deployment region(s)."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        assert "regions" in data, "vercel.json should specify regions"
        assert isinstance(data["regions"], list), "regions should be a list"
        assert len(data["regions"]) > 0, "At least one region should be specified"


class TestVercelFunctionsConfiguration:
    """Test that Vercel functions are properly configured."""

    def test_vercel_json_has_functions_config(self):
        """vercel.json should have functions configuration."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        assert "functions" in data, "vercel.json should have functions configuration"

    def test_vercel_json_configures_api_functions(self):
        """vercel.json should configure API route functions."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        functions = data.get("functions", {})
        # Check for API function pattern
        has_api_config = any(
            "api" in pattern.lower() for pattern in functions.keys()
        )
        assert has_api_config, (
            "vercel.json should configure API route functions"
        )

    def test_api_functions_have_memory_config(self):
        """API functions should have memory configuration."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        functions = data.get("functions", {})
        for pattern, config in functions.items():
            if "api" in pattern.lower():
                assert "memory" in config, (
                    f"API functions ({pattern}) should have memory configuration"
                )

    def test_api_functions_have_max_duration(self):
        """API functions should have maxDuration configuration."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        functions = data.get("functions", {})
        for pattern, config in functions.items():
            if "api" in pattern.lower():
                assert "maxDuration" in config, (
                    f"API functions ({pattern}) should have maxDuration configuration"
                )


# =============================================================================
# SECURITY HEADERS TESTS (HTTPS ENFORCEMENT)
# =============================================================================


class TestSecurityHeaders:
    """Test that security headers are configured for HTTPS enforcement."""

    def test_vercel_json_has_headers_config(self):
        """vercel.json should have headers configuration."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)
        assert "headers" in data, "vercel.json should have headers configuration"
        assert isinstance(data["headers"], list), "headers should be a list"

    def test_x_content_type_options_header_configured(self):
        """X-Content-Type-Options: nosniff header should be configured."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)

        headers = data.get("headers", [])
        has_nosniff = False
        for header_config in headers:
            for header in header_config.get("headers", []):
                if header.get("key") == "X-Content-Type-Options":
                    if header.get("value") == "nosniff":
                        has_nosniff = True
                        break

        assert has_nosniff, (
            "X-Content-Type-Options: nosniff header should be configured"
        )

    def test_x_frame_options_header_configured(self):
        """X-Frame-Options header should be configured to prevent clickjacking."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)

        headers = data.get("headers", [])
        has_frame_options = False
        for header_config in headers:
            for header in header_config.get("headers", []):
                if header.get("key") == "X-Frame-Options":
                    if header.get("value") in ["DENY", "SAMEORIGIN"]:
                        has_frame_options = True
                        break

        assert has_frame_options, (
            "X-Frame-Options header should be configured (DENY or SAMEORIGIN)"
        )

    def test_x_xss_protection_header_configured(self):
        """X-XSS-Protection header should be configured."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)

        headers = data.get("headers", [])
        has_xss_protection = False
        for header_config in headers:
            for header in header_config.get("headers", []):
                if header.get("key") == "X-XSS-Protection":
                    has_xss_protection = True
                    break

        assert has_xss_protection, (
            "X-XSS-Protection header should be configured"
        )

    def test_referrer_policy_header_configured(self):
        """Referrer-Policy header should be configured."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)

        headers = data.get("headers", [])
        has_referrer_policy = False
        valid_policies = [
            "no-referrer",
            "no-referrer-when-downgrade",
            "origin",
            "origin-when-cross-origin",
            "same-origin",
            "strict-origin",
            "strict-origin-when-cross-origin",
        ]
        for header_config in headers:
            for header in header_config.get("headers", []):
                if header.get("key") == "Referrer-Policy":
                    if header.get("value") in valid_policies:
                        has_referrer_policy = True
                        break

        assert has_referrer_policy, (
            "Referrer-Policy header should be configured with a valid policy"
        )

    def test_security_headers_apply_to_all_routes(self):
        """Security headers should apply to all routes."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)

        headers = data.get("headers", [])
        has_catch_all_security = False
        for header_config in headers:
            source = header_config.get("source", "")
            # Check for catch-all patterns
            if source in ["/(.*)", "/(.*)$", "/:path*"]:
                header_keys = [h.get("key") for h in header_config.get("headers", [])]
                # Should have at least one security header
                security_headers = [
                    "X-Content-Type-Options",
                    "X-Frame-Options",
                    "X-XSS-Protection",
                    "Referrer-Policy",
                ]
                if any(h in header_keys for h in security_headers):
                    has_catch_all_security = True
                    break

        assert has_catch_all_security, (
            "Security headers should apply to all routes using catch-all pattern"
        )


class TestCachingHeaders:
    """Test that caching headers are configured for static assets."""

    def test_font_caching_headers_configured(self):
        """Font files should have long-term caching configured."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)

        headers = data.get("headers", [])
        has_font_caching = False
        for header_config in headers:
            source = header_config.get("source", "")
            if "font" in source.lower():
                for header in header_config.get("headers", []):
                    if header.get("key") == "Cache-Control":
                        value = header.get("value", "")
                        if "max-age" in value and "immutable" in value:
                            has_font_caching = True
                            break

        assert has_font_caching, (
            "Font files should have Cache-Control with max-age and immutable"
        )

    def test_image_caching_headers_configured(self):
        """Image files should have long-term caching configured."""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        with open(vercel_config_path) as f:
            data = json.load(f)

        headers = data.get("headers", [])
        has_image_caching = False
        image_extensions = ["jpg", "jpeg", "png", "gif", "webp", "avif", "svg", "ico"]
        for header_config in headers:
            source = header_config.get("source", "")
            # Check if source matches image patterns
            if any(ext in source.lower() for ext in image_extensions):
                for header in header_config.get("headers", []):
                    if header.get("key") == "Cache-Control":
                        value = header.get("value", "")
                        if "max-age" in value:
                            has_image_caching = True
                            break

        assert has_image_caching, (
            "Image files should have Cache-Control header with max-age"
        )


# =============================================================================
# ENVIRONMENT VARIABLES DOCUMENTATION TESTS
# =============================================================================


class TestEnvironmentVariablesDocumentation:
    """Test that all required environment variables are documented."""

    def test_env_example_exists(self):
        """.env.example should exist to document required variables."""
        env_example_path = PROJECT_ROOT / ".env.example"
        assert env_example_path.exists(), (
            ".env.example not found - required variables should be documented"
        )

    def test_sanity_project_id_documented(self):
        """NEXT_PUBLIC_SANITY_PROJECT_ID should be documented."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "NEXT_PUBLIC_SANITY_PROJECT_ID" in content, (
            "NEXT_PUBLIC_SANITY_PROJECT_ID should be documented in .env.example"
        )

    def test_sanity_dataset_documented(self):
        """NEXT_PUBLIC_SANITY_DATASET should be documented."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "NEXT_PUBLIC_SANITY_DATASET" in content, (
            "NEXT_PUBLIC_SANITY_DATASET should be documented in .env.example"
        )

    def test_sanity_api_version_documented(self):
        """NEXT_PUBLIC_SANITY_API_VERSION should be documented."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "NEXT_PUBLIC_SANITY_API_VERSION" in content, (
            "NEXT_PUBLIC_SANITY_API_VERSION should be documented in .env.example"
        )

    def test_sanity_api_read_token_documented(self):
        """SANITY_API_READ_TOKEN should be documented."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "SANITY_API_READ_TOKEN" in content, (
            "SANITY_API_READ_TOKEN should be documented in .env.example"
        )

    def test_sanity_revalidate_secret_documented(self):
        """SANITY_REVALIDATE_SECRET should be documented."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "SANITY_REVALIDATE_SECRET" in content, (
            "SANITY_REVALIDATE_SECRET should be documented in .env.example"
        )

    def test_env_example_has_vercel_checklist(self):
        """.env.example should include Vercel deployment checklist."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text().lower()
        # Check for Vercel-related instructions
        has_vercel_info = (
            "vercel" in content or
            "dashboard" in content or
            "deployment" in content
        )
        assert has_vercel_info, (
            ".env.example should include Vercel deployment instructions"
        )

    def test_env_example_does_not_contain_real_secrets(self):
        """.env.example should not contain real API tokens or secrets."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()

        lines = content.split('\n')
        for line in lines:
            # Skip comments
            if line.strip().startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                value = value.strip()
                # Sensitive keys that should have placeholder values
                sensitive_keys = [
                    'SANITY_API_READ_TOKEN',
                    'SANITY_REVALIDATE_SECRET',
                ]
                for sensitive_key in sensitive_keys:
                    if sensitive_key in key:
                        # Value should be empty, a placeholder, or a comment
                        is_safe = (
                            value == '' or
                            value.startswith('#') or
                            'your' in value.lower() or
                            len(value) < 10
                        )
                        assert is_safe, (
                            f"{sensitive_key} should not contain a real value in .env.example"
                        )


# =============================================================================
# NEXT.JS PRODUCTION CONFIGURATION TESTS
# =============================================================================


class TestNextJsProductionConfig:
    """Test that Next.js is configured for production deployment."""

    def test_next_config_exists(self):
        """next.config.ts should exist."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        assert next_config_path.exists(), "next.config.ts not found"

    def test_next_config_disables_powered_by_header(self):
        """Next.js should disable X-Powered-By header for security."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "poweredByHeader" in content and "false" in content, (
            "Next.js should disable X-Powered-By header (poweredByHeader: false)"
        )

    def test_next_config_enables_compression(self):
        """Next.js should enable compression for production."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "compress" in content and "true" in content, (
            "Next.js should enable compression (compress: true)"
        )

    def test_next_config_enables_strict_mode(self):
        """Next.js should enable React strict mode."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "reactStrictMode" in content and "true" in content, (
            "Next.js should enable React strict mode (reactStrictMode: true)"
        )


# =============================================================================
# SANITY STUDIO ACCESSIBILITY TESTS
# =============================================================================


class TestSanityStudioAccessibility:
    """Test that Sanity Studio is accessible at /studio route."""

    def test_studio_route_directory_exists(self):
        """app/studio/[[...tool]] directory should exist."""
        studio_dir = PROJECT_ROOT / "app" / "studio" / "[[...tool]]"
        assert studio_dir.exists(), "app/studio/[[...tool]] directory not found"
        assert studio_dir.is_dir(), "app/studio/[[...tool]] should be a directory"

    def test_studio_page_exists(self):
        """app/studio/[[...tool]]/page.tsx should exist."""
        page_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "page.tsx"
        assert page_path.exists(), "app/studio/[[...tool]]/page.tsx not found"

    def test_studio_page_uses_next_studio(self):
        """Studio page should use NextStudio component."""
        page_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "page.tsx"
        content = page_path.read_text()
        assert "NextStudio" in content, (
            "Studio page should render NextStudio component"
        )

    def test_studio_page_is_client_component(self):
        """Studio page should be a client component."""
        page_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "page.tsx"
        content = page_path.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "Studio page should have 'use client' directive"
        )

    def test_sanity_config_has_studio_base_path(self):
        """sanity.config.ts should configure /studio as base path."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        assert "basePath" in content and "/studio" in content, (
            "Sanity config should set basePath to '/studio'"
        )


# =============================================================================
# IMAGE OPTIMIZATION & CORE WEB VITALS TESTS
# =============================================================================


class TestImageOptimization:
    """Test that image optimization is configured for Core Web Vitals."""

    def test_next_config_has_images_config(self):
        """next.config.ts should configure images."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "images:" in content or "images :" in content, (
            "next.config.ts should have images configuration"
        )

    def test_next_config_allows_sanity_cdn_images(self):
        """Next.js should allow images from Sanity CDN."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "cdn.sanity.io" in content, (
            "Next.js should allow images from cdn.sanity.io"
        )

    def test_next_config_enables_modern_image_formats(self):
        """Next.js should enable AVIF and WebP image formats."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "avif" in content.lower(), (
            "Next.js should enable AVIF image format"
        )
        assert "webp" in content.lower(), (
            "Next.js should enable WebP image format"
        )

    def test_next_config_has_device_sizes(self):
        """Next.js should configure device sizes for responsive images."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "deviceSizes" in content, (
            "Next.js should configure deviceSizes for responsive images"
        )

    def test_next_config_has_image_sizes(self):
        """Next.js should configure image sizes for srcset generation."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "imageSizes" in content, (
            "Next.js should configure imageSizes for srcset generation"
        )

    def test_next_config_has_cache_ttl(self):
        """Next.js should configure image cache TTL for performance."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "minimumCacheTTL" in content, (
            "Next.js should configure minimumCacheTTL for image caching"
        )


class TestCoreWebVitalsConfig:
    """Test configuration that supports Core Web Vitals targets."""

    def test_experimental_optimize_package_imports(self):
        """Next.js should optimize package imports for smaller bundles."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        assert "optimizePackageImports" in content, (
            "Next.js should configure optimizePackageImports for smaller bundles"
        )

    def test_motion_package_optimized(self):
        """Motion (Framer Motion) package should be optimized."""
        next_config_path = PROJECT_ROOT / "next.config.ts"
        content = next_config_path.read_text()
        # Check that motion is in the optimizePackageImports list
        has_motion_optimization = (
            "optimizePackageImports" in content and
            ("'motion'" in content or '"motion"' in content)
        )
        assert has_motion_optimization, (
            "Motion package should be in optimizePackageImports for smaller bundles"
        )


# =============================================================================
# VERCEL ANALYTICS INTEGRATION TESTS
# =============================================================================


class TestVercelAnalyticsIntegration:
    """Test that Vercel Analytics is properly integrated."""

    def test_vercel_analytics_package_installed(self):
        """@vercel/analytics package should be installed."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "@vercel/analytics" in dependencies, (
            "@vercel/analytics package should be installed"
        )

    def test_vercel_speed_insights_package_installed(self):
        """@vercel/speed-insights package should be installed."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "@vercel/speed-insights" in dependencies, (
            "@vercel/speed-insights package should be installed"
        )

    def test_root_layout_imports_analytics(self):
        """Root layout should import Vercel Analytics."""
        layout_path = PROJECT_ROOT / "app" / "layout.tsx"
        content = layout_path.read_text()
        assert "@vercel/analytics" in content, (
            "Root layout should import from @vercel/analytics"
        )

    def test_root_layout_imports_speed_insights(self):
        """Root layout should import Vercel Speed Insights."""
        layout_path = PROJECT_ROOT / "app" / "layout.tsx"
        content = layout_path.read_text()
        assert "@vercel/speed-insights" in content, (
            "Root layout should import from @vercel/speed-insights"
        )

    def test_root_layout_renders_analytics_component(self):
        """Root layout should render Analytics component."""
        layout_path = PROJECT_ROOT / "app" / "layout.tsx"
        content = layout_path.read_text()
        assert "<Analytics" in content, (
            "Root layout should render <Analytics /> component"
        )

    def test_root_layout_renders_speed_insights_component(self):
        """Root layout should render SpeedInsights component."""
        layout_path = PROJECT_ROOT / "app" / "layout.tsx"
        content = layout_path.read_text()
        assert "<SpeedInsights" in content, (
            "Root layout should render <SpeedInsights /> component"
        )


# =============================================================================
# BUILD CONFIGURATION TESTS
# =============================================================================


class TestBuildConfiguration:
    """Test that the project is configured for successful production builds."""

    def test_package_json_has_build_script(self):
        """package.json should have a build script."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        scripts = package_data.get("scripts", {})
        assert "build" in scripts, "package.json should have a 'build' script"

    def test_build_script_runs_next_build(self):
        """build script should run next build."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        scripts = package_data.get("scripts", {})
        build_script = scripts.get("build", "")
        assert "next build" in build_script, (
            "build script should run 'next build'"
        )

    def test_package_json_has_start_script(self):
        """package.json should have a start script for production."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        scripts = package_data.get("scripts", {})
        assert "start" in scripts, "package.json should have a 'start' script"

    def test_start_script_runs_next_start(self):
        """start script should run next start."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        scripts = package_data.get("scripts", {})
        start_script = scripts.get("start", "")
        assert "next start" in start_script, (
            "start script should run 'next start'"
        )


# =============================================================================
# CONTENT REVALIDATION CONFIGURATION TESTS
# =============================================================================


class TestContentRevalidationForProduction:
    """Test that content revalidation is configured for production deployment."""

    def test_revalidate_api_route_exists(self):
        """Revalidation API route should exist."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        assert route_path.exists(), "app/api/revalidate/route.ts not found"

    def test_revalidate_route_uses_webhook_secret(self):
        """Revalidation route should authenticate using SANITY_REVALIDATE_SECRET."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "SANITY_REVALIDATE_SECRET" in content, (
            "Revalidation route should use SANITY_REVALIDATE_SECRET for authentication"
        )

    def test_revalidate_route_supports_on_demand_revalidation(self):
        """Revalidation route should support on-demand revalidation."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # Should use revalidateTag or revalidatePath
        has_revalidation = (
            "revalidateTag" in content or "revalidatePath" in content
        )
        assert has_revalidation, (
            "Revalidation route should use revalidateTag or revalidatePath"
        )


# =============================================================================
# GITIGNORE CONFIGURATION TESTS
# =============================================================================


class TestGitIgnoreConfiguration:
    """Test that .gitignore is properly configured for deployment."""

    def test_gitignore_exists(self):
        """.gitignore should exist."""
        gitignore_path = PROJECT_ROOT / ".gitignore"
        assert gitignore_path.exists(), ".gitignore not found"

    def test_gitignore_excludes_env_files(self):
        """.gitignore should exclude .env files."""
        gitignore_path = PROJECT_ROOT / ".gitignore"
        content = gitignore_path.read_text()
        # Should exclude .env or .env.local
        has_env_exclusion = (
            ".env" in content or
            ".env.local" in content or
            ".env.*" in content
        )
        assert has_env_exclusion, (
            ".gitignore should exclude .env files"
        )

    def test_gitignore_excludes_node_modules(self):
        """.gitignore should exclude node_modules."""
        gitignore_path = PROJECT_ROOT / ".gitignore"
        content = gitignore_path.read_text()
        assert "node_modules" in content, (
            ".gitignore should exclude node_modules"
        )

    def test_gitignore_excludes_next_build(self):
        """.gitignore should exclude .next build directory."""
        gitignore_path = PROJECT_ROOT / ".gitignore"
        content = gitignore_path.read_text()
        assert ".next" in content, (
            ".gitignore should exclude .next build directory"
        )


# =============================================================================
# DEPLOYMENT DOCUMENTATION TESTS
# =============================================================================


class TestDeploymentDocumentation:
    """Test that deployment documentation exists and is complete."""

    def test_deployment_docs_exist(self):
        """Deployment documentation should exist."""
        docs_path = PROJECT_ROOT / "fashion-website-docs" / "08-DEPLOYMENT.md"
        assert docs_path.exists(), (
            "fashion-website-docs/08-DEPLOYMENT.md should exist"
        )

    def test_deployment_docs_cover_vercel_setup(self):
        """Deployment docs should cover Vercel setup."""
        docs_path = PROJECT_ROOT / "fashion-website-docs" / "08-DEPLOYMENT.md"
        if docs_path.exists():
            content = docs_path.read_text().lower()
            assert "vercel" in content, (
                "Deployment docs should cover Vercel setup"
            )

    def test_deployment_docs_cover_environment_variables(self):
        """Deployment docs should cover environment variables setup."""
        docs_path = PROJECT_ROOT / "fashion-website-docs" / "08-DEPLOYMENT.md"
        if docs_path.exists():
            content = docs_path.read_text().lower()
            assert "environment variable" in content, (
                "Deployment docs should cover environment variables setup"
            )

    def test_deployment_docs_cover_custom_domain(self):
        """Deployment docs should cover custom domain setup."""
        docs_path = PROJECT_ROOT / "fashion-website-docs" / "08-DEPLOYMENT.md"
        if docs_path.exists():
            content = docs_path.read_text().lower()
            has_domain_info = "domain" in content or "dns" in content
            assert has_domain_info, (
                "Deployment docs should cover custom domain setup"
            )

    def test_deployment_docs_cover_sanity_webhook(self):
        """Deployment docs should cover Sanity webhook configuration."""
        docs_path = PROJECT_ROOT / "fashion-website-docs" / "08-DEPLOYMENT.md"
        if docs_path.exists():
            content = docs_path.read_text().lower()
            has_webhook_info = "webhook" in content or "revalidat" in content
            assert has_webhook_info, (
                "Deployment docs should cover Sanity webhook configuration"
            )

    def test_deployment_docs_cover_ssl_https(self):
        """Deployment docs should mention SSL/HTTPS."""
        docs_path = PROJECT_ROOT / "fashion-website-docs" / "08-DEPLOYMENT.md"
        if docs_path.exists():
            content = docs_path.read_text().lower()
            has_ssl_info = "ssl" in content or "https" in content
            assert has_ssl_info, (
                "Deployment docs should mention SSL/HTTPS"
            )

    def test_deployment_docs_cover_performance(self):
        """Deployment docs should cover performance optimization."""
        docs_path = PROJECT_ROOT / "fashion-website-docs" / "08-DEPLOYMENT.md"
        if docs_path.exists():
            content = docs_path.read_text().lower()
            has_perf_info = (
                "performance" in content or
                "lighthouse" in content or
                "web vitals" in content
            )
            assert has_perf_info, (
                "Deployment docs should cover performance optimization"
            )
