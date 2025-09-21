#!/usr/bin/env python3
"""
Test runner for IT Support System
"""

import os
import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run all tests in the test suite"""

    # Get the test directory
    test_dir = Path(__file__).parent
    backend_dir = test_dir.parent

    print("🧪 IT Support System - Test Runner")
    print("=" * 50)

    # Change to backend directory
    os.chdir(backend_dir)

    # Test categories
    test_categories = {
        "Authentication Tests": "tests/auth",
        "API Tests": "tests/api",
        "Integration Tests": "tests/integration"
    }

    results = {}

    for category, test_path in test_categories.items():
        print(f"\n📋 Running {category}...")
        print("-" * 30)

        test_files = list(Path(test_path).glob("test_*.py"))

        if not test_files:
            print(f"   No test files found in {test_path}")
            continue

        category_results = []

        for test_file in test_files:
            print(f"\n   Running {test_file.name}...")
            try:
                result = subprocess.run(
                    [sys.executable, str(test_file)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    print(f"   ✅ {test_file.name} - PASSED")
                    category_results.append(("PASSED", test_file.name))
                else:
                    print(f"   ❌ {test_file.name} - FAILED")
                    print(f"      Error: {result.stderr.strip()}")
                    category_results.append(("FAILED", test_file.name))

            except subprocess.TimeoutExpired:
                print(f"   ⏰ {test_file.name} - TIMEOUT")
                category_results.append(("TIMEOUT", test_file.name))
            except Exception as e:
                print(f"   💥 {test_file.name} - ERROR: {e}")
                category_results.append(("ERROR", test_file.name))

        results[category] = category_results

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)

    total_tests = 0
    passed_tests = 0

    for category, category_results in results.items():
        print(f"\n{category}:")
        for status, test_name in category_results:
            total_tests += 1
            if status == "PASSED":
                passed_tests += 1
            print(f"   {status:8} - {test_name}")

    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
