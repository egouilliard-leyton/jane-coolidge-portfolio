"""
Tests for T-001: Review technical documentation structure

These tests verify that all 8 technical documentation files exist and contain
the required information about architecture, tech stack, file structure, and
data flow between Next.js and Sanity CMS.
"""

import os
import re
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "fashion-website-docs"

# Expected documentation files
EXPECTED_DOCS = [
    "01-PROJECT-OVERVIEW.md",
    "02-ENVIRONMENT-SETUP.md",
    "03-SANITY-SETUP.md",
    "04-CONTENT-SCHEMAS.md",
    "05-NEXTJS-SETUP.md",
    "06-FRONTEND-COMPONENTS.md",
    "07-STYLING-ANIMATIONS.md",
    "08-DEPLOYMENT.md",
]


class TestDocumentationFilesExist:
    """Test that all 8 required documentation files exist."""

    def test_docs_directory_exists(self):
        """Documentation directory should exist."""
        assert DOCS_DIR.exists(), f"Documentation directory not found at {DOCS_DIR}"
        assert DOCS_DIR.is_dir(), f"{DOCS_DIR} should be a directory"

    def test_all_eight_docs_exist(self):
        """All 8 documentation files should exist."""
        missing_docs = []
        for doc in EXPECTED_DOCS:
            doc_path = DOCS_DIR / doc
            if not doc_path.exists():
                missing_docs.append(doc)

        assert len(missing_docs) == 0, f"Missing documentation files: {missing_docs}"

    def test_docs_are_not_empty(self):
        """Each documentation file should have content."""
        for doc in EXPECTED_DOCS:
            doc_path = DOCS_DIR / doc
            if doc_path.exists():
                content = doc_path.read_text()
                assert len(content) > 100, f"{doc} appears to be empty or too short"


class TestProjectOverviewDoc:
    """Test that 01-PROJECT-OVERVIEW.md contains required architecture information."""

    def setup_method(self):
        """Load the project overview document."""
        doc_path = DOCS_DIR / "01-PROJECT-OVERVIEW.md"
        self.content = doc_path.read_text() if doc_path.exists() else ""

    def test_contains_tech_stack_decisions(self):
        """Should document tech stack decisions (Next.js, Sanity, Vercel)."""
        assert "Next.js" in self.content, "Should mention Next.js"
        assert "Sanity" in self.content, "Should mention Sanity CMS"
        assert "Vercel" in self.content, "Should mention Vercel deployment"

    def test_contains_architecture_overview(self):
        """Should contain architecture overview section."""
        assert "Architecture" in self.content or "architecture" in self.content, \
            "Should contain architecture overview"

    def test_contains_file_structure(self):
        """Should document file structure patterns."""
        # Check for common file structure indicators
        has_structure = (
            "File Structure" in self.content or
            "file structure" in self.content or
            "Directory" in self.content or
            "components/" in self.content or
            "app/" in self.content
        )
        assert has_structure, "Should document file structure patterns"

    def test_contains_content_model(self):
        """Should document content model for Sanity."""
        has_content_model = (
            "Content Model" in self.content or
            "content model" in self.content or
            "blogPost" in self.content or
            "Document Type" in self.content
        )
        assert has_content_model, "Should document content model"

    def test_contains_feature_descriptions(self):
        """Should describe main features (blog, portfolio, popups)."""
        assert "Blog" in self.content or "blog" in self.content, \
            "Should describe blog feature"
        assert "Popup" in self.content or "popup" in self.content, \
            "Should describe popup feature"


class TestEnvironmentSetupDoc:
    """Test that 02-ENVIRONMENT-SETUP.md contains setup instructions."""

    def setup_method(self):
        """Load the environment setup document."""
        doc_path = DOCS_DIR / "02-ENVIRONMENT-SETUP.md"
        self.content = doc_path.read_text() if doc_path.exists() else ""

    def test_contains_node_instructions(self):
        """Should contain Node.js installation instructions."""
        assert "Node" in self.content or "node" in self.content, \
            "Should mention Node.js"

    def test_contains_npm_instructions(self):
        """Should contain npm or package manager instructions."""
        has_package_manager = "npm" in self.content or "pnpm" in self.content
        assert has_package_manager, "Should mention package manager"

    def test_contains_env_variables(self):
        """Should document environment variables."""
        has_env_vars = (
            "env" in self.content or
            "ENV" in self.content or
            "environment variable" in self.content.lower()
        )
        assert has_env_vars, "Should document environment variables"


class TestSanitySetupDoc:
    """Test that 03-SANITY-SETUP.md contains Sanity configuration."""

    def setup_method(self):
        """Load the Sanity setup document."""
        doc_path = DOCS_DIR / "03-SANITY-SETUP.md"
        self.content = doc_path.read_text() if doc_path.exists() else ""

    def test_contains_sanity_client_setup(self):
        """Should document Sanity client configuration."""
        has_client = (
            "client" in self.content or
            "createClient" in self.content
        )
        assert has_client, "Should document Sanity client setup"

    def test_contains_studio_configuration(self):
        """Should document Sanity Studio configuration."""
        assert "Studio" in self.content or "studio" in self.content, \
            "Should document Sanity Studio"

    def test_contains_groq_info(self):
        """Should mention GROQ query language."""
        has_groq = "GROQ" in self.content or "groq" in self.content
        assert has_groq, "Should mention GROQ queries"


class TestContentSchemasDoc:
    """Test that 04-CONTENT-SCHEMAS.md contains schema definitions."""

    def setup_method(self):
        """Load the content schemas document."""
        doc_path = DOCS_DIR / "04-CONTENT-SCHEMAS.md"
        self.content = doc_path.read_text() if doc_path.exists() else ""

    def test_contains_document_schemas(self):
        """Should define document schemas."""
        has_schemas = (
            "defineType" in self.content or
            "schema" in self.content.lower() or
            "Document" in self.content
        )
        assert has_schemas, "Should contain schema definitions"

    def test_contains_blog_post_schema(self):
        """Should define blog post schema."""
        has_blog = "blogPost" in self.content or "blog" in self.content.lower()
        assert has_blog, "Should define blog post schema"

    def test_contains_popup_content_schema(self):
        """Should define popup content schema."""
        has_popup = "popupContent" in self.content or "popup" in self.content.lower()
        assert has_popup, "Should define popup content schema"


class TestNextjsSetupDoc:
    """Test that 05-NEXTJS-SETUP.md contains data fetching patterns."""

    def setup_method(self):
        """Load the Next.js setup document."""
        doc_path = DOCS_DIR / "05-NEXTJS-SETUP.md"
        self.content = doc_path.read_text() if doc_path.exists() else ""

    def test_contains_groq_queries(self):
        """Should contain GROQ query definitions."""
        has_queries = (
            "groq`" in self.content or
            "Query" in self.content or
            "query" in self.content.lower()
        )
        assert has_queries, "Should contain GROQ query definitions"

    def test_contains_data_fetching(self):
        """Should document data fetching patterns."""
        has_fetching = (
            "fetch" in self.content.lower() or
            "sanityFetch" in self.content
        )
        assert has_fetching, "Should document data fetching"

    def test_contains_page_examples(self):
        """Should contain page component examples."""
        has_pages = (
            "page.tsx" in self.content or
            "export default" in self.content or
            "HomePage" in self.content
        )
        assert has_pages, "Should contain page examples"

    def test_documents_nextjs_sanity_data_flow(self):
        """Should document data flow between Next.js and Sanity."""
        # Check for indicators of data flow documentation
        has_data_flow = (
            ("Next.js" in self.content and "Sanity" in self.content) or
            "fetch" in self.content.lower() or
            "API" in self.content
        )
        assert has_data_flow, "Should document Next.js <-> Sanity data flow"


class TestFrontendComponentsDoc:
    """Test that 06-FRONTEND-COMPONENTS.md contains component documentation."""

    def setup_method(self):
        """Load the frontend components document."""
        doc_path = DOCS_DIR / "06-FRONTEND-COMPONENTS.md"
        self.content = doc_path.read_text() if doc_path.exists() else ""

    def test_contains_react_components(self):
        """Should document React components."""
        has_components = (
            "component" in self.content.lower() or
            "export default" in self.content or
            "function" in self.content
        )
        assert has_components, "Should document React components"

    def test_contains_layout_components(self):
        """Should document layout components (Header, Footer)."""
        has_layout = (
            "Header" in self.content or
            "Footer" in self.content or
            "Layout" in self.content
        )
        assert has_layout, "Should document layout components"

    def test_contains_popup_component(self):
        """Should document image popup component."""
        has_popup = (
            "ImageWithPopup" in self.content or
            "Popup" in self.content or
            "popup" in self.content.lower()
        )
        assert has_popup, "Should document popup component"


class TestStylingAnimationsDoc:
    """Test that 07-STYLING-ANIMATIONS.md contains styling documentation."""

    def setup_method(self):
        """Load the styling/animations document."""
        doc_path = DOCS_DIR / "07-STYLING-ANIMATIONS.md"
        self.content = doc_path.read_text() if doc_path.exists() else ""

    def test_contains_tailwind_config(self):
        """Should document Tailwind CSS configuration."""
        has_tailwind = (
            "Tailwind" in self.content or
            "tailwind" in self.content.lower()
        )
        assert has_tailwind, "Should document Tailwind CSS"

    def test_contains_animation_patterns(self):
        """Should document animation patterns (Motion/Framer Motion)."""
        has_animation = (
            "Motion" in self.content or
            "motion" in self.content.lower() or
            "animation" in self.content.lower() or
            "Framer" in self.content
        )
        assert has_animation, "Should document animations"


class TestDeploymentDoc:
    """Test that 08-DEPLOYMENT.md contains deployment instructions."""

    def setup_method(self):
        """Load the deployment document."""
        doc_path = DOCS_DIR / "08-DEPLOYMENT.md"
        self.content = doc_path.read_text() if doc_path.exists() else ""

    def test_contains_vercel_deployment(self):
        """Should document Vercel deployment."""
        assert "Vercel" in self.content or "vercel" in self.content.lower(), \
            "Should document Vercel deployment"

    def test_contains_env_configuration(self):
        """Should document production environment configuration."""
        has_env = (
            "environment" in self.content.lower() or
            "ENV" in self.content or
            "env" in self.content
        )
        assert has_env, "Should document environment configuration"

    def test_contains_domain_setup(self):
        """Should document custom domain setup."""
        has_domain = (
            "domain" in self.content.lower() or
            "DNS" in self.content or
            "HTTPS" in self.content
        )
        assert has_domain, "Should document domain setup"

    def test_contains_webhook_setup(self):
        """Should document webhook configuration for revalidation."""
        has_webhook = (
            "webhook" in self.content.lower() or
            "revalidat" in self.content.lower()
        )
        assert has_webhook, "Should document webhook setup"


class TestDocumentationCompleteness:
    """Test overall documentation completeness for acceptance criteria."""

    def test_architecture_decisions_documented(self):
        """Architecture decisions should be clear (Next.js 15, Sanity CMS, Vercel)."""
        overview_path = DOCS_DIR / "01-PROJECT-OVERVIEW.md"
        content = overview_path.read_text() if overview_path.exists() else ""

        assert "Next.js" in content, "Should document Next.js decision"
        assert "Sanity" in content, "Should document Sanity CMS decision"
        assert "Vercel" in content, "Should document Vercel deployment decision"

    def test_file_structure_documented(self):
        """File structure and organization patterns should be documented."""
        overview_path = DOCS_DIR / "01-PROJECT-OVERVIEW.md"
        content = overview_path.read_text() if overview_path.exists() else ""

        # Check for file structure indicators
        has_structure = (
            "app/" in content or
            "components/" in content or
            "sanity/" in content or
            "File Structure" in content
        )
        assert has_structure, "File structure should be documented"

    def test_data_flow_documented(self):
        """Data flow between Next.js and Sanity should be documented."""
        nextjs_path = DOCS_DIR / "05-NEXTJS-SETUP.md"
        sanity_path = DOCS_DIR / "03-SANITY-SETUP.md"

        nextjs_content = nextjs_path.read_text() if nextjs_path.exists() else ""
        sanity_content = sanity_path.read_text() if sanity_path.exists() else ""

        # Check that data fetching from Sanity is documented
        has_fetch = "sanityFetch" in nextjs_content or "fetch" in nextjs_content.lower()
        has_client = "client" in sanity_content.lower()

        assert has_fetch, "Data fetching should be documented in Next.js setup"
        assert has_client, "Sanity client should be documented"

    def test_all_docs_have_headings(self):
        """Each documentation file should have proper heading structure."""
        for doc in EXPECTED_DOCS:
            doc_path = DOCS_DIR / doc
            if doc_path.exists():
                content = doc_path.read_text()
                # Check for markdown headings
                has_headings = re.search(r'^#+ ', content, re.MULTILINE)
                assert has_headings, f"{doc} should have markdown headings"
