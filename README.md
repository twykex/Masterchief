# Master Chief PC Stats Monitor

This project is a custom, real-time hardware statistics monitor designed for a vertical PC case touch screen. It features a fully textured, 3D model of Master Chief from the Halo series, displayed against a dynamic, panoramic environment. The interface is styled with a "holographic" Halo-themed UI, presenting key system metrics such as CPU/GPU temperature and utilization, and RAM usage.

The application is built with a Python backend using the Bottle web framework and a Three.js frontend for 3D rendering. It is designed to be cross-platform, allowing for development on macOS and final deployment on a Windows 11 machine.

 <!-- Replace with a screenshot of your finished project! -->

## Features

- **High-Fidelity 3D Model:** Renders a detailed, fully textured 3D model of Master Chief.
- **Real-Time System Stats:** Displays live data for CPU, GPU, and RAM.
-   - **CPU:** Load (%) and Temperature (°C)
-   - **GPU:** Load (%), and Temperature (°C)
-   - **RAM:** Usage (%)
- **Halo-Themed UI:** A custom, futuristic user interface with glowing holographic elements, hexagonal stat boxes, and UNSC-style typography.
- **Dynamic Environment:** Features an animated 360-degree panoramic background with realistic lighting and reflections on the model's armor.
- **Advanced Graphics:** Utilizes a post-processing pipeline with Bloom (for glows) and Bokeh (for depth-of-field background blur) to create a visually stunning image.
- **Cross-Platform:** The Python backend intelligently detects the operating system to provide real hardware data on Windows and mock data for development on macOS.
- **Touch-Enabled:** The 3D model can be rotated via touch or mouse drag.

---

## Project Structure

The project is organized into a simple web server structure.
masterchief_display/
├── app.py # The main Python backend (Bottle web server)
├── README.md # This file
│
├── static/ # All public assets served to the browser
│ ├── assets/
│ │ └── kiara_9d_dawn_4k.hdr # The panoramic environment file
│ ├── main.js # The core Three.js rendering and logic
│ ├── style.css # All styling for the Halo-themed UI
│ └── halo-infinite-master-chief-remastered/
│ ├── source/
│ │ └── master_chief.fbx # The 3D model file
│ └── textures/
│ └── ... (all .png texture files)
│
└── templates/ # HTML file
└── index.html # The main structure of the web page
code
Code
---

## Installation and Setup

Follow the instructions specific to your operating system.

### A) For Development (macOS)

These instructions allow you to run the project on your Mac. It will use mock data for hardware statistics, but the visuals will be identical to the final product.

1.  **Prerequisites:**
    -   Ensure you have Python 3 installed. You can check by running `python3 --version` in the Terminal.

2.  **Clone the Project:**
    -   If you haven't already, place the `masterchief_display` folder in a convenient location.

3.  **Navigate to Project Directory:**
    -   Open a Terminal and navigate into the project folder:
      ```bash
      cd path/to/your/masterchief_display
      ```

4.  **Create a Virtual Environment:**
    -   It's best practice to create a virtual environment to manage dependencies.
      ```bash
      python3 -m venv .venv
      ```

5.  **Activate the Virtual Environment:**
    -   You must activate the environment in each new terminal session before running the app.
      ```bash
      source .venv/bin/activate
      ```
    -   Your terminal prompt should now be prefixed with `(.venv)`.

6.  **Install Python Libraries:**
    -   Install the required libraries for the web server and system monitoring.
      ```bash
      pip install bottle psutil
      ```

7.  **Run the Application:**
    -   Launch the server with the following command:
      ```bash
      python app.py
      ```
    -   The script will automatically open a new tab in your default web browser at `http://127.0.0.1:5050`. You can use the browser's developer tools to simulate the vertical display for accurate layout development.

### B) For Production (Windows 11)

These instructions are for setting up the display to run 24/7 on your final Windows PC with real hardware data.

1.  **Prerequisites:**
    -   **Python:** Install the latest version of Python for Windows from [python.org](https://www.python.org/downloads/windows/). **Important:** During installation, make sure to check the box that says **"Add Python to PATH"**.
    -   **NVIDIA Drivers:** Ensure you have the latest NVIDIA Game Ready drivers installed for your 4090.

2.  **Install Open Hardware Monitor (for CPU Temp):**
    -   Go to [openhardwaremonitor.org/downloads/](https://openhardwaremonitor.org/downloads/).
    -   Download, unzip, and run `OpenHardwareMonitor.exe`.
    -   In the program's menu, go to **`Options -> Remote Web Server -> Run`**. This is crucial for the script to read your CPU temperature.
    -   You can minimize Open Hardware Monitor, but it must be running in the background.

3.  **Copy Project Files:**
    -   Transfer the entire `masterchief_display` folder to your Windows PC (e.g., to your `Documents` folder).

4.  **Install Python Libraries:**
    -   Open the Command Prompt (type `cmd` in the Start Menu).
    -   Navigate to the project directory:
      ```cmd
      cd C:\Users\YourUsername\Documents\masterchief_display
      ```
    -   Install all required libraries for Windows:
      ```cmd
      pip install bottle psutil py-nvml-win requests
      ```

5.  **Run the Application:**
    -   In the same Command Prompt window, run the script:
      ```cmd
      python app.py
      ```
    -   The display will open in your default browser. Drag this window to your vertical PC case screen and press **F11** to make it full-screen.

---

## Automating Startup on Windows

To make the display launch automatically every time your PC boots up:

1.  **Create a Startup Script:**
    -   Open Notepad and paste the following two lines. **Make sure to change the path** to where you saved your project.
      ```batch
      @echo off
      start "" "C:\Program Files\OpenHardwareMonitor\OpenHardwareMonitor.exe"
      timeout /t 5 /nobreak
      python "C:\Users\YourUsername\Documents\masterchief_display\app.py"
      ```
    -   Save this file as `start_monitor.bat` inside your `masterchief_display` folder.

2.  **Create a Shortcut:**
    -   Right-click on the `start_monitor.bat` file and select "Create shortcut".

3.  **Open the Startup Folder:**
    -   Press `Win + R` to open the Run dialog.
    -   Type `shell:startup` and press Enter. This will open the user's Startup folder.

4.  **Move the Shortcut:**
    -   Drag and drop the shortcut you created in step 2 into the Startup folder.

Now, every time you log into Windows, Open Hardware Monitor will start first, followed by the Master Chief display script, which will then launch the browser window automatically.