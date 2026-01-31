"""
Tests for T-002: Set up development environment and initialize Next.js project

These tests verify that the development environment is properly configured
according to the requirements:
- Node.js version 18.17 or higher
- Next.js 15 project with App Router
- TypeScript configuration
- Tailwind CSS 4 installed and configured
- Motion (Framer Motion) installed
- Development server can start without errors
"""

import json
import subprocess
import re
from pathlib import Path


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestNodeJsVersion:
    """Test that Node.js version 18.17 or higher is installed."""

    def test_node_is_installed(self):
        """Node.js should be installed and accessible."""
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "Node.js is not installed or not accessible"
        assert result.stdout.strip().startswith("v"), "Invalid Node.js version output"

    def test_node_version_meets_minimum(self):
        """Node.js version should be 18.17 or higher."""
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
        )
        version_string = result.stdout.strip()
        # Extract version numbers (e.g., "v20.10.0" -> [20, 10, 0])
        match = re.match(r"v(\d+)\.(\d+)\.(\d+)", version_string)
        assert match, f"Could not parse Node.js version: {version_string}"

        major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))

        # Check minimum version 18.17
        meets_minimum = (major > 18) or (major == 18 and minor >= 17)
        assert meets_minimum, f"Node.js version {major}.{minor}.{patch} is below minimum 18.17"

    def test_npm_is_installed(self):
        """npm should be installed and accessible."""
        result = subprocess.run(
            ["npm", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "npm is not installed or not accessible"


class TestNextJsProjectInitialization:
    """Test that Next.js 15 project is initialized with App Router."""

    def test_package_json_exists(self):
        """package.json should exist in project root."""
        package_json_path = PROJECT_ROOT / "package.json"
        assert package_json_path.exists(), "package.json not found in project root"

    def test_nextjs_dependency_installed(self):
        """Next.js should be listed as a dependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "next" in dependencies, "Next.js is not listed in dependencies"

    def test_nextjs_version_is_15(self):
        """Next.js version should be 15.x."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        next_version = dependencies.get("next", "")

        # Extract major version from semver (e.g., "^15.5.11" -> 15)
        match = re.search(r"(\d+)\.", next_version)
        assert match, f"Could not parse Next.js version: {next_version}"
        major_version = int(match.group(1))
        assert major_version == 15, f"Next.js major version is {major_version}, expected 15"

    def test_app_router_directory_exists(self):
        """App Router directory (app/) should exist."""
        app_dir = PROJECT_ROOT / "app"
        assert app_dir.exists(), "App Router directory (app/) not found"
        assert app_dir.is_dir(), "app/ should be a directory"

    def test_app_router_layout_exists(self):
        """App Router layout.tsx should exist."""
        layout_path = PROJECT_ROOT / "app" / "layout.tsx"
        assert layout_path.exists(), "app/layout.tsx not found (required for App Router)"

    def test_app_router_page_exists(self):
        """App Router page.tsx should exist (either direct or via route group)."""
        page_path = PROJECT_ROOT / "app" / "page.tsx"
        route_group_page = PROJECT_ROOT / "app" / "(site)" / "page.tsx"
        assert page_path.exists() or route_group_page.exists(), (
            "app/page.tsx or app/(site)/page.tsx not found"
        )

    def test_next_config_exists(self):
        """next.config.ts should exist."""
        # Check for both .ts and .js extensions
        next_config_ts = PROJECT_ROOT / "next.config.ts"
        next_config_js = PROJECT_ROOT / "next.config.js"
        next_config_mjs = PROJECT_ROOT / "next.config.mjs"

        config_exists = (
            next_config_ts.exists() or
            next_config_js.exists() or
            next_config_mjs.exists()
        )
        assert config_exists, "next.config.ts (or .js/.mjs) not found"


class TestTypeScriptConfiguration:
    """Test that TypeScript is properly configured."""

    def test_tsconfig_exists(self):
        """tsconfig.json should exist in project root."""
        tsconfig_path = PROJECT_ROOT / "tsconfig.json"
        assert tsconfig_path.exists(), "tsconfig.json not found"

    def test_tsconfig_is_valid_json(self):
        """tsconfig.json should be valid JSON."""
        tsconfig_path = PROJECT_ROOT / "tsconfig.json"
        with open(tsconfig_path) as f:
            data = json.load(f)
        assert isinstance(data, dict), "tsconfig.json should contain a JSON object"

    def test_tsconfig_has_compiler_options(self):
        """tsconfig.json should have compilerOptions."""
        tsconfig_path = PROJECT_ROOT / "tsconfig.json"
        with open(tsconfig_path) as f:
            data = json.load(f)
        assert "compilerOptions" in data, "tsconfig.json should have compilerOptions"

    def test_tsconfig_strict_mode_enabled(self):
        """TypeScript strict mode should be enabled."""
        tsconfig_path = PROJECT_ROOT / "tsconfig.json"
        with open(tsconfig_path) as f:
            data = json.load(f)
        compiler_options = data.get("compilerOptions", {})
        assert compiler_options.get("strict") is True, "TypeScript strict mode should be enabled"

    def test_tsconfig_has_next_plugin(self):
        """tsconfig.json should have Next.js plugin configured."""
        tsconfig_path = PROJECT_ROOT / "tsconfig.json"
        with open(tsconfig_path) as f:
            data = json.load(f)
        compiler_options = data.get("compilerOptions", {})
        plugins = compiler_options.get("plugins", [])

        has_next_plugin = any(
            plugin.get("name") == "next" for plugin in plugins
        )
        assert has_next_plugin, "tsconfig.json should have Next.js plugin configured"

    def test_typescript_dependency_installed(self):
        """TypeScript should be listed as a devDependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dev_dependencies = package_data.get("devDependencies", {})
        assert "typescript" in dev_dependencies, "TypeScript is not listed in devDependencies"

    def test_react_types_installed(self):
        """React type definitions should be installed."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dev_dependencies = package_data.get("devDependencies", {})
        assert "@types/react" in dev_dependencies, "@types/react is not listed in devDependencies"
        assert "@types/react-dom" in dev_dependencies, "@types/react-dom is not listed in devDependencies"


class TestTailwindCSSInstallation:
    """Test that Tailwind CSS 4 is installed and configured."""

    def test_tailwindcss_dependency_installed(self):
        """Tailwind CSS should be listed as a dependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "tailwindcss" in dependencies, "Tailwind CSS is not listed in dependencies"

    def test_tailwindcss_version_is_4(self):
        """Tailwind CSS version should be 4.x."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        tailwind_version = dependencies.get("tailwindcss", "")

        # Extract major version from semver
        match = re.search(r"(\d+)\.", tailwind_version)
        assert match, f"Could not parse Tailwind CSS version: {tailwind_version}"
        major_version = int(match.group(1))
        assert major_version == 4, f"Tailwind CSS major version is {major_version}, expected 4"

    def test_tailwindcss_postcss_plugin_installed(self):
        """Tailwind CSS PostCSS plugin should be installed."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        dev_dependencies = package_data.get("devDependencies", {})
        all_deps = {**dependencies, **dev_dependencies}

        assert "@tailwindcss/postcss" in all_deps, "@tailwindcss/postcss is not installed"

    def test_postcss_config_exists(self):
        """PostCSS configuration file should exist."""
        postcss_mjs = PROJECT_ROOT / "postcss.config.mjs"
        postcss_js = PROJECT_ROOT / "postcss.config.js"
        postcss_cjs = PROJECT_ROOT / "postcss.config.cjs"

        config_exists = postcss_mjs.exists() or postcss_js.exists() or postcss_cjs.exists()
        assert config_exists, "PostCSS configuration file not found"

    def test_postcss_config_has_tailwind_plugin(self):
        """PostCSS config should have Tailwind CSS plugin configured."""
        postcss_mjs = PROJECT_ROOT / "postcss.config.mjs"
        postcss_js = PROJECT_ROOT / "postcss.config.js"

        config_path = postcss_mjs if postcss_mjs.exists() else postcss_js

        if config_path.exists():
            content = config_path.read_text()
            has_tailwind = "@tailwindcss/postcss" in content or "tailwindcss" in content
            assert has_tailwind, "PostCSS config should reference Tailwind CSS"

    def test_globals_css_imports_tailwind(self):
        """globals.css should import Tailwind CSS."""
        globals_css_path = PROJECT_ROOT / "app" / "globals.css"
        assert globals_css_path.exists(), "app/globals.css not found"

        content = globals_css_path.read_text()
        # Tailwind CSS 4 uses @import "tailwindcss"
        has_tailwind_import = (
            '@import "tailwindcss"' in content or
            "@import 'tailwindcss'" in content or
            "@tailwind" in content
        )
        assert has_tailwind_import, "globals.css should import Tailwind CSS"


class TestMotionInstallation:
    """Test that Motion (Framer Motion) is installed."""

    def test_motion_dependency_installed(self):
        """Motion should be listed as a dependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        # Check for 'motion' (new name) or 'framer-motion' (old name)
        has_motion = "motion" in dependencies or "framer-motion" in dependencies
        assert has_motion, "Motion (or framer-motion) is not listed in dependencies"


class TestPackageJsonScripts:
    """Test that package.json has required scripts configured."""

    def test_dev_script_exists(self):
        """package.json should have a dev script."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        scripts = package_data.get("scripts", {})
        assert "dev" in scripts, "package.json should have a 'dev' script"

    def test_dev_script_runs_next(self):
        """dev script should run next dev."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        scripts = package_data.get("scripts", {})
        dev_script = scripts.get("dev", "")
        assert "next dev" in dev_script, "dev script should run 'next dev'"

    def test_build_script_exists(self):
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
        assert "next build" in build_script, "build script should run 'next build'"

    def test_start_script_exists(self):
        """package.json should have a start script."""
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
        assert "next start" in start_script, "start script should run 'next start'"

    def test_lint_script_exists(self):
        """package.json should have a lint script."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        scripts = package_data.get("scripts", {})
        assert "lint" in scripts, "package.json should have a 'lint' script"


class TestReactInstallation:
    """Test that React is properly installed."""

    def test_react_dependency_installed(self):
        """React should be listed as a dependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "react" in dependencies, "React is not listed in dependencies"

    def test_react_dom_dependency_installed(self):
        """React DOM should be listed as a dependency."""
        package_json_path = PROJECT_ROOT / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        assert "react-dom" in dependencies, "react-dom is not listed in dependencies"


class TestNodeModulesInstalled:
    """Test that dependencies are installed."""

    def test_node_modules_exists(self):
        """node_modules directory should exist (dependencies installed)."""
        node_modules_path = PROJECT_ROOT / "node_modules"
        assert node_modules_path.exists(), "node_modules not found - run 'npm install'"
        assert node_modules_path.is_dir(), "node_modules should be a directory"

    def test_next_module_installed(self):
        """Next.js module should be installed."""
        next_module_path = PROJECT_ROOT / "node_modules" / "next"
        assert next_module_path.exists(), "next module not found in node_modules"

    def test_tailwindcss_module_installed(self):
        """Tailwind CSS module should be installed."""
        tailwind_module_path = PROJECT_ROOT / "node_modules" / "tailwindcss"
        assert tailwind_module_path.exists(), "tailwindcss module not found in node_modules"

    def test_motion_module_installed(self):
        """Motion module should be installed."""
        motion_module_path = PROJECT_ROOT / "node_modules" / "motion"
        framer_motion_path = PROJECT_ROOT / "node_modules" / "framer-motion"
        has_motion = motion_module_path.exists() or framer_motion_path.exists()
        assert has_motion, "motion (or framer-motion) module not found in node_modules"
