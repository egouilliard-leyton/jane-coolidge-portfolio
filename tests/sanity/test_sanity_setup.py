"""
Tests for T-003: Initialize Sanity CMS and create Studio project

These tests verify that the Sanity CMS is properly configured according to the requirements:
- sanity.config.ts is properly configured with project ID and dataset
- Sanity client is configured for server and client components
- Studio is accessible at /studio route
- API tokens are stored securely in environment variables

Acceptance Criteria:
- Sanity account is created and project is initialized
- sanity.config.ts is properly configured with project ID and dataset
- Sanity client is configured for server and client components
- Studio is accessible at localhost:3000/studio
- API tokens are stored securely in environment variables
"""

import json
from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestSanityConfigurationFile:
    """Test that sanity.config.ts is properly configured."""

    def test_sanity_config_exists(self):
        """sanity.config.ts should exist in project root."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        assert sanity_config_path.exists(), "sanity.config.ts not found in project root"

    def test_sanity_config_imports_define_config(self):
        """sanity.config.ts should import defineConfig from sanity."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        assert "import { defineConfig }" in content or "import {defineConfig}" in content, (
            "sanity.config.ts should import defineConfig from 'sanity'"
        )

    def test_sanity_config_uses_project_id_env_variable(self):
        """sanity.config.ts should use environment variable for project ID."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        assert "NEXT_PUBLIC_SANITY_PROJECT_ID" in content, (
            "sanity.config.ts should reference NEXT_PUBLIC_SANITY_PROJECT_ID environment variable"
        )

    def test_sanity_config_uses_dataset_env_variable(self):
        """sanity.config.ts should use environment variable for dataset."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        assert "NEXT_PUBLIC_SANITY_DATASET" in content, (
            "sanity.config.ts should reference NEXT_PUBLIC_SANITY_DATASET environment variable"
        )

    def test_sanity_config_has_base_path_studio(self):
        """sanity.config.ts should have basePath set to /studio."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        assert "basePath" in content and "/studio" in content, (
            "sanity.config.ts should configure basePath: '/studio'"
        )

    def test_sanity_config_exports_default_config(self):
        """sanity.config.ts should export a default configuration."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        assert "export default" in content, (
            "sanity.config.ts should export default configuration"
        )

    def test_sanity_config_has_project_name(self):
        """sanity.config.ts should define a project name."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        # Check for name property in config
        has_name = "name:" in content or "name :" in content
        assert has_name, "sanity.config.ts should define a 'name' property"

    def test_sanity_config_has_title(self):
        """sanity.config.ts should define a project title."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        has_title = "title:" in content or "title :" in content
        assert has_title, "sanity.config.ts should define a 'title' property"

    def test_sanity_config_has_plugins(self):
        """sanity.config.ts should configure plugins."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        assert "plugins" in content, "sanity.config.ts should configure plugins"

    def test_sanity_config_has_structure_tool(self):
        """sanity.config.ts should include structureTool plugin."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        assert "structureTool" in content, (
            "sanity.config.ts should include structureTool for custom desk structure"
        )

    def test_sanity_config_has_schema_types(self):
        """sanity.config.ts should configure schema types."""
        sanity_config_path = PROJECT_ROOT / "sanity.config.ts"
        content = sanity_config_path.read_text()
        assert "schema" in content and "types" in content, (
            "sanity.config.ts should configure schema.types"
        )


class TestSanityClientConfiguration:
    """Test that Sanity client is properly configured."""

    def test_sanity_client_file_exists(self):
        """Sanity client configuration file should exist."""
        client_path = PROJECT_ROOT / "sanity" / "lib" / "client.ts"
        assert client_path.exists(), "sanity/lib/client.ts not found"

    def test_sanity_client_imports_create_client(self):
        """Sanity client should import createClient from next-sanity."""
        client_path = PROJECT_ROOT / "sanity" / "lib" / "client.ts"
        content = client_path.read_text()
        assert "createClient" in content and "next-sanity" in content, (
            "sanity/lib/client.ts should import createClient from 'next-sanity'"
        )

    def test_sanity_client_uses_project_id_env_variable(self):
        """Sanity client should use environment variable for project ID."""
        client_path = PROJECT_ROOT / "sanity" / "lib" / "client.ts"
        content = client_path.read_text()
        assert "NEXT_PUBLIC_SANITY_PROJECT_ID" in content, (
            "Sanity client should reference NEXT_PUBLIC_SANITY_PROJECT_ID environment variable"
        )

    def test_sanity_client_uses_dataset_env_variable(self):
        """Sanity client should use environment variable for dataset."""
        client_path = PROJECT_ROOT / "sanity" / "lib" / "client.ts"
        content = client_path.read_text()
        assert "NEXT_PUBLIC_SANITY_DATASET" in content, (
            "Sanity client should reference NEXT_PUBLIC_SANITY_DATASET environment variable"
        )

    def test_sanity_client_uses_api_version(self):
        """Sanity client should configure API version."""
        client_path = PROJECT_ROOT / "sanity" / "lib" / "client.ts"
        content = client_path.read_text()
        assert "apiVersion" in content, (
            "Sanity client should configure apiVersion"
        )

    def test_sanity_client_exports_client(self):
        """Sanity client should export a client instance."""
        client_path = PROJECT_ROOT / "sanity" / "lib" / "client.ts"
        content = client_path.read_text()
        assert "export const client" in content or "export { client" in content, (
            "sanity/lib/client.ts should export a client instance"
        )

    def test_sanity_client_has_fetch_helper(self):
        """Sanity client should provide a fetch helper function."""
        client_path = PROJECT_ROOT / "sanity" / "lib" / "client.ts"
        content = client_path.read_text()
        assert "sanityFetch" in content or "fetch" in content, (
            "sanity/lib/client.ts should provide a fetch helper function"
        )

    def test_sanity_client_configures_cdn(self):
        """Sanity client should configure CDN usage."""
        client_path = PROJECT_ROOT / "sanity" / "lib" / "client.ts"
        content = client_path.read_text()
        assert "useCdn" in content, (
            "Sanity client should configure useCdn option"
        )

    def test_sanity_client_has_perspective(self):
        """Sanity client should configure perspective for content access."""
        client_path = PROJECT_ROOT / "sanity" / "lib" / "client.ts"
        content = client_path.read_text()
        assert "perspective" in content, (
            "Sanity client should configure perspective for content access"
        )


class TestSanityStudioRoute:
    """Test that Studio route is properly configured."""

    def test_studio_route_directory_exists(self):
        """Studio route directory should exist at app/studio/[[...tool]]."""
        studio_dir = PROJECT_ROOT / "app" / "studio" / "[[...tool]]"
        assert studio_dir.exists(), "app/studio/[[...tool]] directory not found"
        assert studio_dir.is_dir(), "app/studio/[[...tool]] should be a directory"

    def test_studio_page_exists(self):
        """Studio page.tsx should exist."""
        page_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "page.tsx"
        assert page_path.exists(), "app/studio/[[...tool]]/page.tsx not found"

    def test_studio_page_is_client_component(self):
        """Studio page should be a client component."""
        page_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "page.tsx"
        content = page_path.read_text()
        assert "'use client'" in content or '"use client"' in content, (
            "Studio page should be a client component with 'use client' directive"
        )

    def test_studio_page_imports_next_studio(self):
        """Studio page should import NextStudio from next-sanity/studio."""
        page_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "page.tsx"
        content = page_path.read_text()
        assert "NextStudio" in content and "next-sanity/studio" in content, (
            "Studio page should import NextStudio from 'next-sanity/studio'"
        )

    def test_studio_page_imports_config(self):
        """Studio page should import sanity config."""
        page_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "page.tsx"
        content = page_path.read_text()
        assert "sanity.config" in content, (
            "Studio page should import config from sanity.config"
        )

    def test_studio_page_exports_default_component(self):
        """Studio page should export a default component."""
        page_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "page.tsx"
        content = page_path.read_text()
        assert "export default" in content, (
            "Studio page should export a default component"
        )

    def test_studio_page_renders_next_studio(self):
        """Studio page should render NextStudio component."""
        page_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "page.tsx"
        content = page_path.read_text()
        assert "<NextStudio" in content, (
            "Studio page should render <NextStudio /> component"
        )

    def test_studio_layout_exists(self):
        """Studio layout.tsx should exist."""
        layout_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "layout.tsx"
        assert layout_path.exists(), "app/studio/[[...tool]]/layout.tsx not found"

    def test_studio_layout_has_metadata(self):
        """Studio layout should define metadata."""
        layout_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "layout.tsx"
        content = layout_path.read_text()
        assert "metadata" in content, (
            "Studio layout should define metadata for the admin page"
        )

    def test_studio_layout_exports_default(self):
        """Studio layout should export a default function."""
        layout_path = PROJECT_ROOT / "app" / "studio" / "[[...tool]]" / "layout.tsx"
        content = layout_path.read_text()
        assert "export default" in content, (
            "Studio layout should export a default function"
        )


class TestSanityEnvironmentVariables:
    """Test that environment variables are properly configured."""

    def test_env_example_exists(self):
        """.env.example should exist to document required variables."""
        env_example_path = PROJECT_ROOT / ".env.example"
        assert env_example_path.exists(), ".env.example not found - should document required environment variables"

    def test_env_example_has_project_id(self):
        """.env.example should document NEXT_PUBLIC_SANITY_PROJECT_ID."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "NEXT_PUBLIC_SANITY_PROJECT_ID" in content, (
            ".env.example should document NEXT_PUBLIC_SANITY_PROJECT_ID"
        )

    def test_env_example_has_dataset(self):
        """.env.example should document NEXT_PUBLIC_SANITY_DATASET."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "NEXT_PUBLIC_SANITY_DATASET" in content, (
            ".env.example should document NEXT_PUBLIC_SANITY_DATASET"
        )

    def test_env_example_has_api_version(self):
        """.env.example should document NEXT_PUBLIC_SANITY_API_VERSION."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "NEXT_PUBLIC_SANITY_API_VERSION" in content, (
            ".env.example should document NEXT_PUBLIC_SANITY_API_VERSION"
        )

    def test_env_example_has_read_token_placeholder(self):
        """.env.example should document SANITY_API_READ_TOKEN (optional)."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()
        assert "SANITY_API_READ_TOKEN" in content, (
            ".env.example should document SANITY_API_READ_TOKEN for authenticated requests"
        )

    def test_env_example_does_not_contain_real_credentials(self):
        """.env.example should not contain real credentials."""
        env_example_path = PROJECT_ROOT / ".env.example"
        content = env_example_path.read_text()

        # Check that project ID is a placeholder, not a real ID
        # Real Sanity project IDs are typically 8-12 alphanumeric characters
        lines = content.split('\n')
        for line in lines:
            if 'NEXT_PUBLIC_SANITY_PROJECT_ID' in line and '=' in line:
                value = line.split('=', 1)[1].strip()
                # Should be a placeholder like "your-project-id" or empty
                is_placeholder = (
                    value == '' or
                    'your' in value.lower() or
                    value.startswith('#') or
                    len(value) < 5
                )
                assert is_placeholder, (
                    ".env.example should not contain real Sanity project ID"
                )


class TestSanityDependencies:
    """Test that Sanity dependencies are properly installed."""

    def test_sanity_dependency_installed(self):
        """sanity package should be listed as a dependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "sanity" in dependencies, "sanity is not listed in dependencies"

    def test_next_sanity_dependency_installed(self):
        """next-sanity package should be listed as a dependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "next-sanity" in dependencies, "next-sanity is not listed in dependencies"

    def test_sanity_image_url_dependency_installed(self):
        """@sanity/image-url package should be listed as a dependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "@sanity/image-url" in dependencies, (
            "@sanity/image-url is not listed in dependencies"
        )

    def test_sanity_icons_dependency_installed(self):
        """@sanity/icons package should be listed as a dependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "@sanity/icons" in dependencies, "@sanity/icons is not listed in dependencies"

    def test_sanity_modules_installed(self):
        """Sanity modules should be installed in node_modules."""
        sanity_module_path = PROJECT_ROOT / "node_modules" / "sanity"
        assert sanity_module_path.exists(), "sanity module not found in node_modules"

    def test_next_sanity_module_installed(self):
        """next-sanity module should be installed in node_modules."""
        next_sanity_path = PROJECT_ROOT / "node_modules" / "next-sanity"
        assert next_sanity_path.exists(), "next-sanity module not found in node_modules"


class TestSanitySchemaDirectory:
    """Test that Sanity schema directory structure is set up."""

    def test_sanity_directory_exists(self):
        """sanity/ directory should exist."""
        sanity_dir = PROJECT_ROOT / "sanity"
        assert sanity_dir.exists(), "sanity/ directory not found"
        assert sanity_dir.is_dir(), "sanity/ should be a directory"

    def test_sanity_schemas_directory_exists(self):
        """sanity/schemas/ directory should exist."""
        schemas_dir = PROJECT_ROOT / "sanity" / "schemas"
        assert schemas_dir.exists(), "sanity/schemas/ directory not found"
        assert schemas_dir.is_dir(), "sanity/schemas/ should be a directory"

    def test_sanity_schemas_index_exists(self):
        """sanity/schemas/index.ts should exist."""
        schemas_index = PROJECT_ROOT / "sanity" / "schemas" / "index.ts"
        assert schemas_index.exists(), "sanity/schemas/index.ts not found"

    def test_sanity_schemas_index_exports_schema_types(self):
        """sanity/schemas/index.ts should export schemaTypes."""
        schemas_index = PROJECT_ROOT / "sanity" / "schemas" / "index.ts"
        content = schemas_index.read_text()
        assert "schemaTypes" in content and "export" in content, (
            "sanity/schemas/index.ts should export schemaTypes"
        )

    def test_sanity_lib_directory_exists(self):
        """sanity/lib/ directory should exist."""
        lib_dir = PROJECT_ROOT / "sanity" / "lib"
        assert lib_dir.exists(), "sanity/lib/ directory not found"
        assert lib_dir.is_dir(), "sanity/lib/ should be a directory"


class TestSanityStudioStructure:
    """Test that Sanity Studio structure is configured."""

    def test_sanity_structure_file_exists(self):
        """sanity/structure.ts should exist for custom desk structure."""
        structure_path = PROJECT_ROOT / "sanity" / "structure.ts"
        assert structure_path.exists(), "sanity/structure.ts not found"

    def test_sanity_structure_exports_structure(self):
        """sanity/structure.ts should export structure."""
        structure_path = PROJECT_ROOT / "sanity" / "structure.ts"
        content = structure_path.read_text()
        assert "export" in content and "structure" in content, (
            "sanity/structure.ts should export a structure configuration"
        )

    def test_sanity_structure_imports_structure_resolver(self):
        """sanity/structure.ts should use StructureResolver type."""
        structure_path = PROJECT_ROOT / "sanity" / "structure.ts"
        content = structure_path.read_text()
        assert "StructureResolver" in content, (
            "sanity/structure.ts should use StructureResolver type"
        )
