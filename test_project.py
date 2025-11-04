# test_project.py

import os
import sys
import time
import json
import threading
import subprocess
import importlib.util

try:
    import requests
except ImportError:
    print("\n[ERROR] The 'requests' library is not installed.")
    print("Please run 'pip install requests' and try again.")
    sys.exit(1)

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_FILENAME_CORRECT = "master_chief.fbx"
MODEL_FILENAME_OLD = "master_chief.fbx"
BASE_URL = "http://127.0.0.1:5000"


# --- ANSI Colors for Readability ---
class colors:
    OK = '\033[92m'  # GREEN
    WARN = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


# --- Global State ---
all_tests_passed = True


def print_test(message, passed):
    global all_tests_passed
    if passed:
        print(f"  {colors.OK}[PASS]{colors.RESET} {message}")
    else:
        print(f"  {colors.FAIL}[FAIL]{colors.RESET} {message}")
        all_tests_passed = False


def check_structure():
    """Validates that the directory and file structure is correct."""
    print("\n--- 1. Checking File & Directory Structure ---")

    # Define required paths relative to the project root
    required_paths = [
        "app.py",
        "templates",
        "templates/index.html",
        "static",
        "static/main.js",
        "static/style.css",
        "static/halo-infinite-master-chief-remastered",
        "static/halo-infinite-master-chief-remastered/source",
        "static/halo-infinite-master-chief-remastered/textures"
    ]

    for path in required_paths:
        full_path = os.path.join(PROJECT_ROOT, path)
        print_test(f"'{path}' exists", os.path.exists(full_path))

    # Specific check for the 3D model file
    model_path_correct = os.path.join(PROJECT_ROOT, "static/halo-infinite-master-chief-remastered/source",
                                      MODEL_FILENAME_CORRECT)
    model_path_old = os.path.join(PROJECT_ROOT, "static/halo-infinite-master-chief-remastered/source",
                                  MODEL_FILENAME_OLD)

    correct_exists = os.path.exists(model_path_correct)
    old_exists = os.path.exists(model_path_old)

    print_test(f"Model file '{MODEL_FILENAME_CORRECT}' exists", correct_exists)
    if not correct_exists and old_exists:
        print(f"  {colors.WARN}[WARN]{colors.RESET} Found '{MODEL_FILENAME_OLD}' but not the renamed version.")
        print(f"         Please rename the file to '{MODEL_FILENAME_CORRECT}' and update main.js.")
        global all_tests_passed
        all_tests_passed = False  # Consider this a failure


def check_environment():
    """Checks if required Python packages are installed."""
    print("\n--- 2. Checking Python Environment ---")

    required_packages = ["flask", "psutil"]
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        print_test(f"Library '{package}' is installed", spec is not None)


def check_server():
    """Starts the server in a background process and tests its endpoints."""
    print("\n--- 3. Checking Server Functionality ---")

    server_process = None
    try:
        # Start the Flask app as a separate process
        # Using sys.executable ensures we use the same Python interpreter
        server_process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("  Attempting to start the Flask server... (waiting 3 seconds)")
        time.sleep(3)

        # Check if the process is still running
        if server_process.poll() is not None:
            print_test("Server started successfully", False)
            print(f"  {colors.FAIL}Server failed to start. Error output:{colors.RESET}")
            print(server_process.stderr.read())
            return

        print_test("Server started successfully", True)

        # Test endpoints
        test_endpoint("/", "Main HTML page", expected_content="<title>PC Stats Display</title>")
        test_endpoint("/static/main.js", "JavaScript file", expected_content="FBXLoader")
        test_endpoint("/static/style.css", "CSS file", expected_content="canvas-container")
        test_endpoint(f"/static/halo-infinite-master-chief-remastered/source/{MODEL_FILENAME_CORRECT}",
                      "FBX model file")
        test_stats_endpoint()

    finally:
        if server_process:
            print("  Shutting down the test server...")
            server_process.terminate()
            server_process.wait()  # Wait for the process to fully close


def test_endpoint(path, description, expected_content=None):
    """Helper function to test a single URL endpoint."""
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url, timeout=5)
        passed = response.status_code == 200
        print_test(f"'{path}' ({description}) is served correctly (HTTP 200)", passed)
        if passed and expected_content:
            content_passed = expected_content in response.text
            print_test(f"'{path}' content is valid", content_passed)

    except requests.exceptions.RequestException as e:
        print_test(f"'{path}' ({description}) is served correctly", False)
        print(f"    {colors.FAIL}Error making request: {e}{colors.RESET}")


def test_stats_endpoint():
    """Specific test for the /stats API endpoint."""
    url = f"{BASE_URL}/stats"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print_test("'/stats' endpoint is served correctly (HTTP 200)", True)
            try:
                data = response.json()
                # Check for expected keys in the JSON response
                keys = ["time", "date", "cpu", "gpu", "ram"]
                keys_present = all(key in data for key in keys)
                print_test("'/stats' returns valid JSON with correct keys", keys_present)
            except json.JSONDecodeError:
                print_test("'/stats' returns valid JSON", False)
        else:
            print_test("'/stats' endpoint is served correctly (HTTP 200)", False)
    except requests.exceptions.RequestException as e:
        print_test("'/stats' endpoint is served correctly", False)
        print(f"    {colors.FAIL}Error making request: {e}{colors.RESET}")


if __name__ == "__main__":
    print("==============================================")
    print("  Running Project Sanity Check...")
    print("==============================================")

    check_structure()
    check_environment()
    check_server()

    print("\n----------------------------------------------")
    if all_tests_passed:
        print(f"{colors.OK}✅ All tests passed! Your project setup looks correct.{colors.RESET}")
        print("If the model is still not showing, the issue is likely within 'main.js' logic")
        print("(e.g., camera position, model scale, or a Three.js error).")
        print("Check the browser's Developer Console for JavaScript errors.")
    else:
        print(f"{colors.FAIL}❌ Some tests failed. Please review the errors above.{colors.RESET}")
    print("----------------------------------------------")