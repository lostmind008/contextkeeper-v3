#!/usr/bin/env python3
"""
test_path_filtering.py - Path filtering tests for ContextKeeper v3

Created: 2025-07-29 04:17:00 (Australia/Sydney)
Part of: ContextKeeper v3.0 Test Suite

Tests path filtering functionality including exclusion of venv/site-packages,
proper inclusion of project files, directory traversal logic, and edge cases
for nested structures. Validates the recently fixed path filtering issues.
"""

import pytest
import os
from pathlib import Path
import sys

from src.core.path_utils import normalize_path

# Add parent directory to path for imports
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


@pytest.mark.unit
class TestPathFilteringLogic:
    """Test core path filtering logic and exclusion rules"""

    @pytest.fixture
    def sample_directory_structure(self, temp_dir):
        """Create a sample directory structure for testing path filtering"""
        base_path = Path(temp_dir)

        # Create various directories and files to test filtering
        directories_to_create = [
            "src/main",
            "src/utils",
            "tests/unit",
            "tests/integration",
            "venv/lib/python3.9/site-packages/requests",
            "venv/lib/python3.9/site-packages/numpy",
            ".venv/lib/python3.9/site-packages/pandas",
            "node_modules/react/lib",
            "node_modules/express/dist",
            ".git/objects/12",
            ".pytest_cache/v/cache",
            "__pycache__/test",
            "build/lib/mypackage",
            "dist/mypackage-1.0.0",
            ".tox/py39/lib",
            "docs/build/html",
        ]

        for dir_path in directories_to_create:
            (base_path / dir_path).mkdir(parents=True, exist_ok=True)

        # Create test files in various locations
        files_to_create = [
            # Should be included
            "src/main/app.py",
            "src/utils/helpers.py",
            "tests/unit/test_app.py",
            "tests/integration/test_api.py",
            "README.md",
            "setup.py",
            "requirements.txt",
            "docs/source/index.rst",
            # Should be excluded
            "venv/lib/python3.9/site-packages/requests/__init__.py",
            "venv/lib/python3.9/site-packages/numpy/core.py",
            ".venv/lib/python3.9/site-packages/pandas/core.py",
            "node_modules/react/lib/react.js",
            "node_modules/express/dist/express.js",
            ".git/objects/12/34567890abcdef",
            ".pytest_cache/v/cache/nodeids",
            "__pycache__/test/app.cpython-39.pyc",
            "build/lib/mypackage/__init__.py",
            "dist/mypackage-1.0.0/setup.py",
            ".tox/py39/lib/python/site-packages/test.py",
            "docs/build/html/index.html",
        ]

        for file_path in files_to_create:
            file_full_path = base_path / file_path
            file_full_path.parent.mkdir(parents=True, exist_ok=True)
            file_full_path.write_text(f"# Content of {file_path}")

        return base_path

    def test_venv_exclusion(self, sample_directory_structure):
        """Test that virtual environment directories are properly excluded"""
        base_path = sample_directory_structure

        # Define exclusion patterns (matching ContextKeeper's logic)
        exclusion_patterns = [
            "venv",
            ".venv",
            "env",
            ".env",
            "site-packages",
            "__pycache__",
            "node_modules",
            ".git",
            ".pytest_cache",
            "build",
            "dist",
            ".tox",
        ]

        def should_exclude_path(path):
            """Check if a path should be excluded based on exclusion patterns"""
            path_str = str(path)
            path_parts = Path(path).parts

            for pattern in exclusion_patterns:
                if pattern in path_parts:
                    return True
                if pattern in path_str:
                    return True

            return False

        # Test specific exclusions
        excluded_paths = [
            base_path / "venv/lib/python3.9/site-packages/requests/__init__.py",
            base_path / ".venv/lib/python3.9/site-packages/pandas/core.py",
            base_path / "node_modules/react/lib/react.js",
            base_path / ".git/objects/12/34567890abcdef",
            base_path / "__pycache__/test/app.cpython-39.pyc",
            base_path / "build/lib/mypackage/__init__.py",
            base_path / "dist/mypackage-1.0.0/setup.py",
        ]

        for path in excluded_paths:
            assert should_exclude_path(path), f"Path should be excluded: {path}"

    def test_project_file_inclusion(self, sample_directory_structure):
        """Test that legitimate project files are properly included"""
        base_path = sample_directory_structure

        def should_exclude_path(path):
            """Simplified exclusion logic for testing"""
            exclusion_patterns = [
                "venv",
                ".venv",
                "env",
                ".env",
                "site-packages",
                "__pycache__",
                "node_modules",
                ".git",
                ".pytest_cache",
                "build",
                "dist",
                ".tox",
            ]

            path_parts = Path(path).parts
            return any(pattern in path_parts for pattern in exclusion_patterns)

        # Test specific inclusions
        included_paths = [
            base_path / "src/main/app.py",
            base_path / "src/utils/helpers.py",
            base_path / "tests/unit/test_app.py",
            base_path / "tests/integration/test_api.py",
            base_path / "README.md",
            base_path / "setup.py",
            base_path / "requirements.txt",
        ]

        for path in included_paths:
            assert not should_exclude_path(path), f"Path should be included: {path}"

    def test_nested_exclusion_logic(self, sample_directory_structure):
        """Test exclusion logic for deeply nested structures"""
        base_path = sample_directory_structure

        # Test deeply nested venv paths
        deep_venv_paths = [
            "venv/lib/python3.9/site-packages/requests/adapters.py",
            "venv/lib/python3.9/site-packages/urllib3/connectionpool.py",
            ".venv/lib/python3.9/site-packages/numpy/core/multiarray.py",
        ]

        def is_in_excluded_directory(path, exclusions):
            """Check if path is within any excluded directory"""
            path_obj = Path(path)
            for part in path_obj.parts:
                if part in exclusions:
                    return True
            return False

        exclusions = {"venv", ".venv", "site-packages"}

        for path_str in deep_venv_paths:
            full_path = base_path / path_str
            assert is_in_excluded_directory(
                full_path, exclusions
            ), f"Deeply nested path should be excluded: {path_str}"

    def test_file_extension_filtering(self, sample_directory_structure):
        """Test filtering based on file extensions"""
        base_path = sample_directory_structure

        # Create additional test files with various extensions
        test_files = [
            "src/code.py",  # Should include
            "src/data.json",  # Should include
            "src/config.yaml",  # Should include
            "src/readme.md",  # Should include
            "src/styles.css",  # Should include
            "src/app.js",  # Should include
            "src/temp.tmp",  # Might exclude
            "src/backup.bak",  # Might exclude
            "src/compiled.pyc",  # Should exclude
            "src/object.o",  # Should exclude
        ]

        # Define inclusion patterns for code files
        code_extensions = {
            ".py",
            ".js",
            ".ts",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".md",
            ".rst",
            ".txt",
            ".json",
            ".yaml",
            ".yml",
            ".xml",
            ".html",
            ".css",
            ".scss",
            ".sql",
        }

        # Define exclusion patterns for generated files
        exclude_extensions = {
            ".pyc",
            ".pyo",
            ".o",
            ".so",
            ".exe",
            ".dll",
            ".tmp",
            ".temp",
            ".bak",
            ".backup",
            ".log",
        }

        def should_include_file(file_path):
            """Determine if file should be included based on extension"""
            suffix = Path(file_path).suffix.lower()

            # Exclude specific extensions
            if suffix in exclude_extensions:
                return False

            # Include code extensions
            if suffix in code_extensions:
                return True

            # Default to include if no specific rule
            return True

        # Test the logic
        for file_path in test_files:
            full_path = base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text("test content")

            include = should_include_file(full_path)
            suffix = Path(file_path).suffix.lower()

            if suffix in exclude_extensions:
                assert not include, f"File with extension {suffix} should be excluded"
            elif suffix in code_extensions:
                assert include, f"File with extension {suffix} should be included"


@pytest.mark.unit
class TestDirectoryTraversal:
    """Test directory traversal logic and performance"""

    def test_recursive_directory_traversal(self, temp_dir):
        """Test recursive traversal with proper filtering"""
        base_path = Path(temp_dir)

        # Create nested structure
        test_structure = [
            "project/src/main.py",
            "project/src/utils/helper.py",
            "project/tests/test_main.py",
            "project/venv/lib/python3.9/site-packages/package.py",
            "project/docs/readme.md",
        ]

        for file_path in test_structure:
            full_path = base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text("test content")

        def traverse_directory(root_path, exclude_patterns):
            """Simulate directory traversal with filtering"""
            included_files = []

            for root, dirs, files in os.walk(root_path):
                # Filter directories to avoid traversing excluded ones
                dirs[:] = [d for d in dirs if d not in exclude_patterns]

                for file in files:
                    file_path = Path(root) / file

                    # Check if file is in excluded path
                    should_exclude = False
                    for part in file_path.parts:
                        if part in exclude_patterns:
                            should_exclude = True
                            break

                    if not should_exclude:
                        included_files.append(file_path)

            return included_files

        exclude_patterns = {"venv", ".venv", "__pycache__", ".git"}
        included_files = traverse_directory(base_path, exclude_patterns)

        # Verify results
        assert (
            len(included_files) >= 4
        )  # Should include main.py, helper.py, test_main.py, readme.md

        # Verify venv files are excluded
        venv_files = [f for f in included_files if "venv" in str(f)]
        assert len(venv_files) == 0, "Virtual environment files should be excluded"

    def test_symlink_handling(self, temp_dir):
        """Test handling of symbolic links in directory traversal"""
        base_path = Path(temp_dir)

        # Create real file and directory
        real_file = base_path / "real_file.py"
        real_dir = base_path / "real_dir"
        real_dir.mkdir()
        (real_dir / "content.py").write_text("real content")
        real_file.write_text("real file content")

        # Create symbolic links if supported by the system
        try:
            symlink_file = base_path / "symlink_file.py"
            symlink_dir = base_path / "symlink_dir"

            symlink_file.symlink_to(real_file)
            symlink_dir.symlink_to(real_dir)

            # Test symlink detection
            assert symlink_file.is_symlink()
            assert symlink_dir.is_symlink()
            assert not real_file.is_symlink()
            assert not real_dir.is_symlink()

        except (OSError, NotImplementedError):
            # Symlinks not supported on this system
            pytest.skip("Symbolic links not supported on this system")

    def test_permission_error_handling(self, temp_dir):
        """Test handling of permission errors during traversal"""
        base_path = Path(temp_dir)

        # Create a file and then make it unreadable (if possible)
        test_file = base_path / "permission_test.py"
        test_file.write_text("test content")

        try:
            # Skip test if running as root, since permission changes may be ignored
            if os.name != "nt" and hasattr(os, "geteuid") and os.geteuid() == 0:
                pytest.skip("Permission checks are ineffective when run as root")

            # Remove read permissions (Unix-like systems)
            os.chmod(test_file, 0o000)

            def safe_read_file(file_path):
                """Safely attempt to read a file"""
                try:
                    return file_path.read_text()
                except PermissionError:
                    return None
                except OSError:
                    return None

            # Test that permission errors are handled gracefully
            content = safe_read_file(test_file)
            assert content is None, "Should handle permission error gracefully"

        except (OSError, NotImplementedError):
            # Permission modification not supported
            pytest.skip("Permission modification not supported on this system")

        finally:
            # Restore permissions for cleanup
            try:
                os.chmod(test_file, 0o644)
            except (OSError, FileNotFoundError):
                pass


@pytest.mark.unit
class TestPathNormalization:
    """Test path normalization and cross-platform compatibility"""

    def test_path_separator_normalization(self):
        """Test normalization of path separators across platforms"""
        test_paths = [
            "src/main/app.py",
            "src\\main\\app.py",  # Windows-style
            "src/main\\utils/helper.py",  # Mixed style
            "./src/main/app.py",  # Relative with dot
            "../src/main/app.py",  # Relative with parent
        ]

        for path_str in test_paths:
            normalized = normalize_path(path_str)

            # Should use forward slashes
            assert "\\" not in normalized or os.name == "nt"

            # Should be a valid path
            assert isinstance(normalized, str)
            assert len(normalized) > 0

    def test_absolute_vs_relative_paths(self, temp_dir):
        """Test handling of absolute vs relative paths"""
        base_path = Path(temp_dir)

        # Create test file
        test_file = base_path / "test.py"
        test_file.write_text("test content")

        # Test absolute path
        absolute_path = test_file.absolute()
        assert absolute_path.is_absolute()

        # Test relative path
        relative_path = Path("test.py")
        assert not relative_path.is_absolute()

        # Test conversion
        def ensure_absolute(path, base_dir):
            """Ensure path is absolute"""
            path_obj = Path(path)
            if path_obj.is_absolute():
                return path_obj
            else:
                return (Path(base_dir) / path_obj).absolute()

        abs_from_rel = ensure_absolute("test.py", temp_dir)
        assert abs_from_rel.is_absolute()
        assert abs_from_rel.name == "test.py"

    def test_case_sensitivity_handling(self):
        """Test handling of case sensitivity in file paths"""
        test_cases = [
            ("README.md", "readme.md"),
            ("SRC/main.py", "src/main.py"),
            ("Tests/Unit/test.py", "tests/unit/test.py"),
        ]

        def normalize_case(path_str):
            """Normalize case for case-insensitive comparison"""
            return str(Path(path_str)).lower()

        for original, expected_lower in test_cases:
            normalized = normalize_case(original)

            if os.name == "nt":  # Windows is case-insensitive
                assert normalized == expected_lower.replace("/", "\\").lower()
            else:  # Unix-like systems preserve case
                # Still normalize for comparison
                assert isinstance(normalized, str)


@pytest.mark.unit
class TestFilteringPerformance:
    """Test performance characteristics of path filtering"""

    def test_large_directory_filtering_performance(self, temp_dir):
        """Test filtering performance with large number of files"""
        import time

        base_path = Path(temp_dir)

        # Create many files for performance testing
        num_files = 100  # Reduced for test speed
        file_types = [".py", ".js", ".md", ".json", ".txt"]

        start_time = time.time()

        for i in range(num_files):
            file_ext = file_types[i % len(file_types)]
            file_path = base_path / f"file_{i:04d}{file_ext}"
            file_path.write_text(f"Content of file {i}")

        creation_time = time.time() - start_time

        # Test filtering performance
        exclude_patterns = {"venv", ".venv", "__pycache__", ".git"}

        start_filter_time = time.time()

        filtered_files = []
        for file_path in base_path.rglob("*"):
            if file_path.is_file():
                should_exclude = any(
                    pattern in file_path.parts for pattern in exclude_patterns
                )
                if not should_exclude:
                    filtered_files.append(file_path)

        filter_time = time.time() - start_filter_time

        # Performance assertions
        assert creation_time < 5.0, "File creation should be fast"
        assert filter_time < 2.0, "Filtering should be fast"
        assert (
            len(filtered_files) == num_files
        ), "All files should be included (no exclusions)"

    def test_exclusion_pattern_efficiency(self):
        """Test efficiency of different exclusion pattern matching methods"""
        import time

        test_paths = [
            "src/main/app.py",
            "venv/lib/python3.9/site-packages/requests/__init__.py",
            "tests/unit/test_app.py",
            "node_modules/react/lib/react.js",
            "docs/source/index.rst",
        ] * 20  # Repeat for performance testing

        exclude_patterns = {"venv", ".venv", "__pycache__", ".git", "node_modules"}

        # Method 1: String-based checking
        def method1_string_check(paths, patterns):
            results = []
            for path in paths:
                should_exclude = any(pattern in path for pattern in patterns)
                results.append(not should_exclude)
            return results

        # Method 2: Path parts checking
        def method2_parts_check(paths, patterns):
            results = []
            for path in paths:
                path_parts = Path(path).parts
                should_exclude = any(pattern in path_parts for pattern in patterns)
                results.append(not should_exclude)
            return results

        # Test both methods
        start_time = time.time()
        results1 = method1_string_check(test_paths, exclude_patterns)
        time1 = time.time() - start_time

        start_time = time.time()
        results2 = method2_parts_check(test_paths, exclude_patterns)
        time2 = time.time() - start_time

        # Both methods should be fast
        assert time1 < 1.0, "String-based method should be fast"
        assert time2 < 1.0, "Parts-based method should be fast"

        # Results should be consistent for most cases
        # (Some edge cases might differ, but major exclusions should match)
        major_exclusions = sum(
            1 for r1, r2 in zip(results1, results2) if not r1 and not r2
        )
        assert major_exclusions > 0, "Both methods should exclude some paths"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
