# verify_project.py

import os
import sys
import time
import platform
import subprocess
import importlib.util
import urllib.request

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER_PORT = 5050
BASE_URL = f"http://127.0.0.1:{SERVER_PORT}"


# --- ANSI Colors for Readability ---
class Colors:
    OK = '\033[92m'  # GREEN
    WARN = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    CYAN = '\033[96m'  # CYAN
    BOLD = '\033[1m'
    RESET = '\033[0m'


# --- Global State ---
all_tests_passed = True
IS_WINDOWS = platform.system() == "Windows"


def print_test(message, passed, fatal=False):
    """Prints a formatted test result."""
    global all_tests_passed
    if passed:
        print(f"  {Colors.OK}[PASS]{Colors.RESET} {message}")
    else:
        print(f"  {Colors.FAIL}[FAIL]{Colors.RESET} {message}")
        all_tests_passed = False
        if fatal:
            print(f"\n{Colors.FAIL}Fatal error. Aborting tests.{Colors.RESET}")
            sys.exit(1)


def check_structure():
    """Validates that the directory and file structure is correct."""
    print(f"\n{Colors.CYAN}--- 1. Checking File & Directory Structure ---{Colors.RESET}")

    required_paths = [
        "app.py",
        "templates/index.html",
        "static/main.js",
        "static/style.css",
        "static/assets/kiara_9d_dawn_4k.hdr",
        "static/halo-infinite-master-chief-remastered/source/master_chief.fbx",
    ]

    for path in required_paths:
        full_path = os.path.join(PROJECT_ROOT, path.replace('/', os.sep))
        print_test(f"File exists: '{path}'", os.path.exists(full_path))

    old_model_path = os.path.join(PROJECT_ROOT, "static", "halo-infinite-master-chief-remastered", "source",
                                  "Infinite Master Chief.fbx")
    if os.path.exists(old_model_path):
        print(
            f"  {Colors.WARN}[WARN]{Colors.RESET} Found old model file with spaces. Please delete 'Infinite Master Chief.fbx' to avoid confusion.")


def check_environment():
    """Checks if required Python packages are installed."""
    print(f"\n{Colors.CYAN}--- 2. Checking Python Environment ---{Colors.RESET}")

    required_packages = ["bottle", "psutil", "requests"]
    if IS_WINDOWS:
        required_packages.append("pynvml")

    for package in required_packages:
        spec = importlib.util.find_spec(package)
        print_test(f"Library installed: '{package}'", spec is not None)

    if not all(importlib.util.find_spec(pkg) for pkg in required_packages):
        print(f"\n  {Colors.FAIL}Missing required libraries. Please run:{Colors.RESET}")
        if IS_WINDOWS:
            print("  pip install bottle psutil requests py-nvml-win")
        else:
            print("  pip install bottle psutil requests")
        sys.exit(1)


def check_server():
    """Starts the server in a background process and tests its endpoints."""
    print(f"\n{Colors.CYAN}--- 3. Checking Server Functionality ---{Colors.RESET}")

    server_process = None
    try:
        print("  Attempting to start 'app.py' in the background...")
        # Use sys.executable to ensure we use the same Python interpreter
        # Use CREATE_NO_WINDOW flag on Windows for a cleaner start
        kwargs = {'creationflags': subprocess.CREATE_NO_WINDOW} if IS_WINDOWS else {}
        server_process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            **kwargs
        )

        print("  Waiting up to 10 seconds for server to respond...")
        for i in range(10):
            time.sleep(1)
            try:
                # Check if the server is responding on the main page
                with urllib.request.urlopen(f"{BASE_URL}/", timeout=1) as response:
                    if response.getcode() == 200:
                        print(f"  Server is up and running after {i + 1} seconds.")
                        print_test("Server started successfully", True)
                        break
            except Exception:
                continue
        else:  # This 'else' belongs to the 'for' loop, runs if it completes without breaking
            print_test("Server started successfully", False, fatal=True)
            print(f"  {Colors.FAIL}Server failed to respond after 10 seconds. Error output:{Colors.RESET}")
            print(server_process.stderr.read())
            return

        # Test critical endpoints
        test_endpoint("/", "Main HTML page")
        test_endpoint("/static/main.js", "JavaScript file")
        test_endpoint("/static/assets/kiara_9d_dawn_4k.hdr", "Environment asset")
        test_endpoint("/static/halo-infinite-master-chief-remastered/source/master_chief.fbx", "3D model asset")
        test_endpoint("/stats", "Stats API endpoint")

    finally:
        if server_process:
            print("  Shutting down the test server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()


def test_endpoint(path, description):
    """Helper function to test a single URL endpoint."""
    url = f"{BASE_URL}{path}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            status = response.getcode()
            passed = 200 <= status < 400  # Accept any success or redirect code
            print_test(f"Endpoint is accessible: '{path}' ({description})", passed)
    except Exception as e:
        print_test(f"Endpoint is accessible: '{path}' ({description})", False)
        print(f"    {Colors.FAIL}Error: {e}{Colors.RESET}")


if __name__ == "__main__":
    print(f"{Colors.BOLD}{Colors.CYAN}==============================================")
    print("  Master Chief PC Stats Monitor - Verification")
    print(f"  OS Detected: {platform.system()}")
    print(f"=============================================={Colors.RESET}")

    check_structure()
    check_environment()
    check_server()

    print(f"\n{Colors.BOLD}----------------------------------------------{Colors.RESET}")
    if all_tests_passed:
        print(f"{Colors.OK}✅ All tests passed! Your project is correctly configured.{Colors.RESET}")
        print("You can now run 'python app.py' to launch the display.")
    else:
        print(
            f"{Colors.FAIL}❌ Some tests failed. Please review the errors above and follow the instructions to fix them.{Colors.RESET}")
    print(f"{Colors.BOLD}----------------------------------------------{Colors.RESET}")