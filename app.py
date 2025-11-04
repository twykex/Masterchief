# app.py (Final Version with Correct Bottle Template Path)

import sys
import platform
import random
import datetime
import webbrowser
import os
import time
from threading import Timer
import psutil

# --- NEW: Import TEMPLATE_PATH ---
from bottle import Bottle, run, template, static_file, TEMPLATE_PATH

# --- 1. CONFIGURATION ---
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5050

# --- 2. ROBUST PORT CONFLICT RESOLUTION (Unchanged) ---
def check_and_free_port(port):
    print(f"Checking for conflicts on port {port}...")
    try:
        my_pid = os.getpid()
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN' and conn.laddr.port == port:
                if conn.pid and conn.pid != my_pid:
                    p = psutil.Process(conn.pid)
                    print(f"  - CONFLICT: Port {port} is in use by PID {p.pid} ({p.name()}).")
                    print(f"  - Attempting to terminate the conflicting process...")
                    p.kill(); p.wait(timeout=3)
                    print(f"  - SUCCESS: Process {p.pid} terminated.")
                    time.sleep(1); break
        print("  - No conflicts found on accessible processes.")
    except psutil.AccessDenied:
        print(f"  - WARNING: Could not check all processes for port conflicts due to macOS security.")
        print(f"  - The script will attempt to start. If it fails with 'Address already in use',")
        print(f"  - please close the other program using port {port} and restart.")
    except Exception as e:
        print(f"  - An unexpected error occurred during port check: {e}")
    print("  - Port check complete.")

# --- OS Detection and Initialization (Unchanged) ---
IS_WINDOWS = platform.system() == "Windows"
# ... (rest of OS detection logic) ...
gpu_handle = None
if IS_WINDOWS:
    try:
        import pynvml
        pynvml.nvmlInit()
        gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        print("✅ Successfully initialized NVIDIA GPU monitoring for Windows.")
    except Exception as e:
        print(f"⚠️ Could not initialize NVIDIA monitoring on Windows: {e}")
        print("   GPU stats will be mocked.")
        IS_WINDOWS = False
else:
    print("✅ Running on non-Windows OS. GPU stats will be mocked.")

# --- Bottle Application Setup (Updated) ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, 'templates')

# --- NEW: Tell Bottle where to find the templates folder ---
TEMPLATE_PATH.insert(0, TEMPLATE_ROOT)

app = Bottle()

# --- Route definitions (Updated) ---
@app.route('/')
def index():
    # --- NEW: Use the simpler, relative path name ---
    return template('index.html')

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=STATIC_ROOT)

# ... (get_stats function is unchanged) ...
@app.route('/stats')
def get_stats():
    now = datetime.datetime.now()
    cpu_percent = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    if IS_WINDOWS and gpu_handle:
        gpu_temp = pynvml.nvmlDeviceGetTemperature(gpu_handle, pynvml.NVML_TEMPERATURE_GPU)
        gpu_util = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle)
        gpu_load_percent = gpu_util.gpu
        cpu_temp = "N/A"
    else:
        cpu_temp = f"{random.uniform(45.0, 65.0):.1f}"
        gpu_temp = int(random.uniform(50.0, 75.0))
        gpu_load_percent = random.randint(5, 40)
    data = {
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%A, %B %d"),
        "cpu": {"load": cpu_percent, "temp": cpu_temp},
        "gpu": {"load": gpu_load_percent, "temp": gpu_temp},
        "ram": {"used_percent": ram_percent}
    }
    return data

# --- Browser Opening and Server Start (Unchanged) ---
def open_browser():
    webbrowser.open_new(f'http://127.0.0.1:{SERVER_PORT}/')

if __name__ == '__main__':
    check_and_free_port(SERVER_PORT)
    Timer(1, open_browser).start()
    print("\n🚀 Server starting...")
    print("   Listening on all network interfaces. To access from another device, use:")
    print(f"   http://<YOUR_PC_IP_ADDRESS>:{SERVER_PORT}\n")
    run(app, host=SERVER_HOST, port=SERVER_PORT, debug=True, reloader=False)