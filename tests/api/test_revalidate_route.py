"""
Tests for T-020: Configure revalidation and webhook endpoints

These tests verify that the revalidation API route is properly configured according to the requirements:
- API route /api/revalidate is created with authentication
- Webhook authenticates using secret token
- Content changes trigger revalidation of affected paths
- Proper logging is configured for debugging

Acceptance Criteria:
- API route /api/revalidate is created with authentication
- Sanity webhook is configured to call revalidation endpoint
- Webhook authenticates using secret token
- Content changes trigger revalidation of affected paths
- Published content appears on site within 60 seconds
- Webhook logs are available for debugging
"""

import re
from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestRevalidateRouteExists:
    """Test that the revalidate API route exists and has proper structure."""

    def test_revalidate_route_directory_exists(self):
        """app/api/revalidate directory should exist."""
        route_dir = PROJECT_ROOT / "app" / "api" / "revalidate"
        assert route_dir.exists(), "app/api/revalidate directory not found"
        assert route_dir.is_dir(), "app/api/revalidate should be a directory"

    def test_revalidate_route_file_exists(self):
        """app/api/revalidate/route.ts should exist."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        assert route_path.exists(), "app/api/revalidate/route.ts not found"

    def test_route_exports_post_handler(self):
        """Revalidate route should export a POST handler."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "export async function POST" in content, (
            "Revalidate route should export an async POST handler"
        )

    def test_route_exports_get_handler(self):
        """Revalidate route should export a GET handler for health checks."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "export async function GET" in content, (
            "Revalidate route should export a GET handler for health checks"
        )


class TestRevalidateAuthentication:
    """Test that the revalidate route has proper authentication."""

    def test_route_uses_sanity_revalidate_secret(self):
        """Revalidate route should use SANITY_REVALIDATE_SECRET environment variable."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "SANITY_REVALIDATE_SECRET" in content, (
            "Revalidate route should use SANITY_REVALIDATE_SECRET for authentication"
        )

    def test_route_checks_for_missing_secret(self):
        """Revalidate route should check if the secret is missing."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # Check for conditional that verifies secret exists
        assert "!process.env.SANITY_REVALIDATE_SECRET" in content, (
            "Revalidate route should check for missing SANITY_REVALIDATE_SECRET"
        )

    def test_route_returns_500_for_missing_secret(self):
        """Revalidate route should return 500 when secret is missing."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # Check that 500 status is returned for missing config
        assert "status: 500" in content, (
            "Revalidate route should return 500 status for missing secret"
        )

    def test_route_validates_signature(self):
        """Revalidate route should validate webhook signature."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "isValidSignature" in content, (
            "Revalidate route should validate webhook signature using isValidSignature"
        )

    def test_route_returns_401_for_invalid_signature(self):
        """Revalidate route should return 401 for invalid signature."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "status: 401" in content, (
            "Revalidate route should return 401 status for invalid signature"
        )

    def test_route_uses_parse_body_from_next_sanity(self):
        """Revalidate route should use parseBody from next-sanity/webhook."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "parseBody" in content and "next-sanity/webhook" in content, (
            "Revalidate route should import parseBody from 'next-sanity/webhook'"
        )


class TestRevalidatePayloadValidation:
    """Test that the revalidate route properly validates webhook payloads."""

    def test_route_validates_type_field(self):
        """Revalidate route should validate _type field in payload."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "_type" in content, (
            "Revalidate route should check for _type field in payload"
        )

    def test_route_returns_400_for_bad_request(self):
        """Revalidate route should return 400 for malformed requests."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "status: 400" in content, (
            "Revalidate route should return 400 status for bad requests"
        )

    def test_route_has_webhook_payload_type(self):
        """Revalidate route should define a WebhookPayload type."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "type WebhookPayload" in content or "interface WebhookPayload" in content, (
            "Revalidate route should define WebhookPayload type"
        )


class TestRevalidateTagMapping:
    """Test that the revalidate route properly maps document types to cache tags."""

    def test_route_has_document_type_to_tags_mapping(self):
        """Revalidate route should have document type to tags mapping."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "documentTypeToTags" in content, (
            "Revalidate route should have documentTypeToTags mapping"
        )

    def test_route_maps_homepage_type(self):
        """Revalidate route should map homepage document type."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "homepage:" in content or "'homepage'" in content, (
            "Revalidate route should map homepage document type"
        )

    def test_route_maps_blog_post_type(self):
        """Revalidate route should map blogPost document type."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "blogPost:" in content or "'blogPost'" in content, (
            "Revalidate route should map blogPost document type"
        )

    def test_route_maps_project_type(self):
        """Revalidate route should map project document type."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "project:" in content or "'project'" in content, (
            "Revalidate route should map project document type"
        )

    def test_route_maps_about_page_type(self):
        """Revalidate route should map aboutPage document type."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "aboutPage:" in content or "'aboutPage'" in content, (
            "Revalidate route should map aboutPage document type"
        )

    def test_route_maps_contact_page_type(self):
        """Revalidate route should map contactPage document type."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "contactPage:" in content or "'contactPage'" in content, (
            "Revalidate route should map contactPage document type"
        )

    def test_route_maps_site_settings_type(self):
        """Revalidate route should map siteSettings document type."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "siteSettings:" in content or "'siteSettings'" in content, (
            "Revalidate route should map siteSettings document type"
        )

    def test_route_maps_navigation_type(self):
        """Revalidate route should map navigation document type."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "navigation:" in content or "'navigation'" in content, (
            "Revalidate route should map navigation document type"
        )

    def test_route_maps_popup_content_type(self):
        """Revalidate route should map popupContent document type."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "popupContent:" in content or "'popupContent'" in content, (
            "Revalidate route should map popupContent document type"
        )


class TestRevalidatePathHandling:
    """Test that the revalidate route properly handles path revalidation."""

    def test_route_imports_revalidate_tag(self):
        """Revalidate route should import revalidateTag from next/cache."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "revalidateTag" in content and "next/cache" in content, (
            "Revalidate route should import revalidateTag from 'next/cache'"
        )

    def test_route_imports_revalidate_path(self):
        """Revalidate route should import revalidatePath from next/cache."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "revalidatePath" in content and "next/cache" in content, (
            "Revalidate route should import revalidatePath from 'next/cache'"
        )

    def test_route_has_document_type_to_path_mapping(self):
        """Revalidate route should have document type to path mapping."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "documentTypeToPath" in content, (
            "Revalidate route should have documentTypeToPath mapping for slug-based content"
        )

    def test_route_handles_slug_based_paths(self):
        """Revalidate route should handle slug-based path revalidation."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # Check for slug handling
        assert "slug?.current" in content or "slug.current" in content, (
            "Revalidate route should handle slug-based path revalidation"
        )

    def test_route_revalidates_blog_path(self):
        """Revalidate route should revalidate /blog path for blog posts."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "'/blog'" in content or '"/blog"' in content, (
            "Revalidate route should revalidate /blog path"
        )

    def test_route_revalidates_projects_path(self):
        """Revalidate route should revalidate /projects path for projects."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "'/projects'" in content or '"/projects"' in content, (
            "Revalidate route should revalidate /projects path"
        )

    def test_route_revalidates_homepage_path(self):
        """Revalidate route should revalidate homepage path."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # Homepage should be revalidated for certain content types
        assert "'/'" in content or "'/ (layout)'" in content, (
            "Revalidate route should revalidate homepage path"
        )

    def test_route_revalidates_about_path(self):
        """Revalidate route should revalidate /about path for about page changes."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "'/about'" in content or '"/about"' in content, (
            "Revalidate route should revalidate /about path"
        )

    def test_route_revalidates_contact_path(self):
        """Revalidate route should revalidate /contact path for contact page changes."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "'/contact'" in content or '"/contact"' in content, (
            "Revalidate route should revalidate /contact path"
        )

    def test_route_revalidates_layout_for_settings(self):
        """Revalidate route should revalidate layout for siteSettings and navigation."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # Check for layout revalidation
        assert "'layout'" in content or '"layout"' in content, (
            "Revalidate route should revalidate layout for site-wide settings changes"
        )


class TestRevalidateLogging:
    """Test that the revalidate route has proper logging for debugging."""

    def test_route_logs_incoming_webhooks(self):
        """Revalidate route should log incoming webhook requests."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "console.log" in content and "Revalidate" in content, (
            "Revalidate route should log incoming webhook requests"
        )

    def test_route_logs_validation_signature(self):
        """Revalidate route should log signature validation status."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # Check that signature validation is logged
        assert "isValidSignature" in content, (
            "Revalidate route should log signature validation status"
        )

    def test_route_logs_document_type(self):
        """Revalidate route should log the document type being revalidated."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # Check for type logging in both incoming and success logs
        has_type_logging = "type:" in content or "type: _type" in content
        assert has_type_logging, (
            "Revalidate route should log the document type being revalidated"
        )

    def test_route_logs_timestamps(self):
        """Revalidate route should log timestamps for debugging."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "timestamp" in content and "toISOString" in content, (
            "Revalidate route should log timestamps for debugging"
        )

    def test_route_logs_revalidated_tags(self):
        """Revalidate route should log which tags were revalidated."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "revalidatedTags" in content, (
            "Revalidate route should log which cache tags were revalidated"
        )

    def test_route_logs_revalidated_paths(self):
        """Revalidate route should log which paths were revalidated."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "revalidatedPaths" in content, (
            "Revalidate route should log which paths were revalidated"
        )

    def test_route_warns_on_invalid_signature(self):
        """Revalidate route should warn when invalid signature is received."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "console.warn" in content, (
            "Revalidate route should use console.warn for invalid signatures"
        )

    def test_route_logs_errors(self):
        """Revalidate route should log errors."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "console.error" in content, (
            "Revalidate route should log errors for debugging"
        )


class TestRevalidateErrorHandling:
    """Test that the revalidate route has proper error handling."""

    def test_route_has_try_catch(self):
        """Revalidate route should have try-catch error handling."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "try {" in content and "catch" in content, (
            "Revalidate route should have try-catch error handling"
        )

    def test_route_returns_500_on_error(self):
        """Revalidate route should return 500 on processing errors."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # Check that 500 is returned in catch block
        # The implementation has status: 500 in multiple places
        assert content.count("status: 500") >= 2, (
            "Revalidate route should return 500 on processing errors"
        )

    def test_route_returns_error_message(self):
        """Revalidate route should return error message in response."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "Error processing webhook" in content or "error:" in content, (
            "Revalidate route should return error message in response"
        )


class TestRevalidateSuccessResponse:
    """Test that the revalidate route returns proper success responses."""

    def test_route_uses_next_response_json(self):
        """Revalidate route should use NextResponse.json for success responses."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "NextResponse.json" in content and "NextResponse" in content, (
            "Revalidate route should use NextResponse.json for success responses"
        )

    def test_route_returns_revalidated_flag(self):
        """Revalidate route should return revalidated: true on success."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "revalidated: true" in content, (
            "Revalidate route should return revalidated: true on success"
        )

    def test_route_returns_timestamp_on_success(self):
        """Revalidate route should return timestamp on success."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "now: Date.now()" in content or "timestamp" in content, (
            "Revalidate route should return timestamp on success"
        )


class TestRevalidateHealthCheck:
    """Test that the revalidate route has a proper health check endpoint."""

    def test_get_handler_returns_ok_status(self):
        """GET handler should return ok status for health checks."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "status: 'ok'" in content or 'status: "ok"' in content, (
            "GET handler should return status: 'ok' for health checks"
        )

    def test_get_handler_returns_message(self):
        """GET handler should return a descriptive message."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        assert "endpoint is active" in content.lower() or "message:" in content, (
            "GET handler should return a descriptive message"
        )


class TestSanityRevalidateSecretInEnvExample:
    """Test that environment configuration documents the revalidation secret."""

    def test_env_example_has_revalidate_secret(self):
        """.env.example should document SANITY_REVALIDATE_SECRET."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "SANITY_REVALIDATE_SECRET" in content, (
            ".env.example should document SANITY_REVALIDATE_SECRET"
        )

    def test_env_example_revalidate_secret_is_placeholder(self):
        """.env.example should not contain a real revalidation secret."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()

        lines = content.split('\n')
        for line in lines:
            if 'SANITY_REVALIDATE_SECRET' in line and '=' in line:
                value = line.split('=', 1)[1].strip()
                # Should be empty or a placeholder
                is_placeholder = (
                    value == '' or
                    value.startswith('#') or
                    'your' in value.lower() or
                    len(value) < 10
                )
                assert is_placeholder, (
                    ".env.example should not contain a real revalidation secret"
                )


class TestContentLakeConsistency:
    """Test that the revalidate route handles Content Lake eventual consistency."""

    def test_route_waits_for_content_lake_consistency(self):
        """Revalidate route should wait for Content Lake consistency."""
        route_path = PROJECT_ROOT / "app" / "api" / "revalidate" / "route.ts"
        content = route_path.read_text()
        # The third parameter to parseBody (true) enables waiting for Content Lake consistency
        # Check that parseBody is called with true as third argument
        has_consistency_wait = (
            "parseBody" in content and
            "true" in content and
            ("Wait" in content or "consistency" in content.lower())
        )
        assert has_consistency_wait, (
            "Revalidate route should wait for Content Lake consistency (parseBody third param)"
        )


class TestWebhookDocumentation:
    """Test that webhook configuration is documented."""

    def test_sanity_setup_doc_has_webhook_section(self):
        """Documentation should include webhook setup instructions."""
        doc_path = PROJECT_ROOT / "fashion-website-docs" / "03-SANITY-SETUP.md"
        if doc_path.exists():
            content = doc_path.read_text()
            has_webhook_info = (
                "webhook" in content.lower() or
                "revalidat" in content.lower()
            )
            assert has_webhook_info, (
                "03-SANITY-SETUP.md should document webhook configuration"
            )
        # If docs don't exist, we pass silently (docs are optional)

    def test_deployment_doc_exists_for_webhook_config(self):
        """Deployment documentation should exist for production webhook setup."""
        doc_path = PROJECT_ROOT / "fashion-website-docs" / "08-DEPLOYMENT.md"
        # If this doc exists, it should mention webhooks/revalidation
        if doc_path.exists():
            content = doc_path.read_text()
            has_relevant_info = (
                "webhook" in content.lower() or
                "revalidat" in content.lower() or
                "SANITY_REVALIDATE_SECRET" in content
            )
            assert has_relevant_info, (
                "08-DEPLOYMENT.md should document webhook configuration for production"
            )
        # If docs don't exist, we pass silently (docs are optional)
