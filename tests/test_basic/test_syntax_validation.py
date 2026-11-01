# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for Python syntax validation - ensuring all Python files are syntactically correct."""

import ast
import py_compile
from pathlib import Path

import pytest


def get_python_files():
    """Get all Python files in the goerp_payroll package."""
    coati_dir = Path(__file__).parent.parent.parent / "goerp_payroll"
    python_files = list(coati_dir.rglob("*.py"))
    return python_files


def test_all_python_files_have_valid_syntax():
    """
    Test that all Python files in goerp_payroll have valid syntax.

    Setup:
        - Find all .py files in goerp_payroll directory

    Action:
        - Attempt to compile each file

    Verification:
        - All files compile without syntax errors
    """
    python_files = get_python_files()

    # Ensure we found Python files
    assert len(python_files) > 0, "No Python files found in goerp_payroll"

    syntax_errors = []

    for py_file in python_files:
        try:
            # Compile the file to check syntax
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            syntax_errors.append((str(py_file), str(e)))

    if syntax_errors:
        error_msg = "Syntax errors found in the following files:\n"
        for file_path, error in syntax_errors:
            error_msg += f"  {file_path}: {error}\n"
        pytest.fail(error_msg)


def test_all_python_files_can_be_parsed():
    """
    Test that all Python files can be parsed into AST.

    Setup:
        - Find all .py files in goerp_payroll directory

    Action:
        - Parse each file into an Abstract Syntax Tree

    Verification:
        - All files parse successfully
    """
    python_files = get_python_files()

    # Ensure we found Python files
    assert len(python_files) > 0, "No Python files found in goerp_payroll"

    parse_errors = []

    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                source = f.read()
            ast.parse(source, filename=str(py_file))
        except SyntaxError as e:
            parse_errors.append((str(py_file), str(e)))

    if parse_errors:
        error_msg = "Parse errors found in the following files:\n"
        for file_path, error in parse_errors:
            error_msg += f"  {file_path}: {error}\n"
        pytest.fail(error_msg)


def test_main_module_files_exist():
    """
    Test that essential module files exist.

    Setup:
        - Define list of essential files

    Action:
        - Check if each file exists

    Verification:
        - All essential files exist
    """
    coati_dir = Path(__file__).parent.parent.parent / "goerp_payroll"

    essential_files = [
        "__init__.py",
        "model.py",
        "nomina_engine/__init__.py",
        "formula_engine/__init__.py",
        "auth.py",
        "forms.py",
        "config.py",
        "cli.py",
    ]

    missing_files = []

    for filename in essential_files:
        file_path = coati_dir / filename
        if not file_path.exists():
            missing_files.append(filename)

    if missing_files:
        pytest.fail(f"Essential files missing: {', '.join(missing_files)}")


def test_no_empty_python_files():
    """
    Test that Python files are not empty (except __init__.py).

    Setup:
        - Find all .py files in goerp_payroll directory

    Action:
        - Check file size for each file

    Verification:
        - No non-init files are empty
    """
    python_files = get_python_files()

    empty_files = []

    for py_file in python_files:
        # Allow __init__.py files to be empty
        if py_file.name == "__init__.py":
            continue

        if py_file.stat().st_size == 0:
            empty_files.append(str(py_file))

    if empty_files:
        pytest.fail(f"Empty Python files found: {', '.join(empty_files)}")


def test_main_app_file_exists():
    """
    Test that the main application entry point exists.

    Setup:
        - Define path to app.py

    Action:
        - Check if file exists

    Verification:
        - app.py exists
    """
    app_file = Path(__file__).parent.parent.parent / "app.py"
    assert app_file.exists(), "Main application file app.py not found"

    # Also verify it has valid syntax
    with open(app_file, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        ast.parse(source, filename=str(app_file))
    except SyntaxError as e:
        pytest.fail(f"Syntax error in app.py: {e}")
