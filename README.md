# Master Chief PC Stats Monitor v1.0

A high-fidelity, real-time hardware statistics monitor designed for vertical PC case touch screens. This application renders a fully textured, animated 3D model of Master Chief against a dynamic, panoramic environment, complemented by a futuristic, Halo-themed holographic UI.

 <!-- **Action Required:** Replace this with a real screenshot of your final project! -->

---

## Feature Gallery

-   **High-Fidelity 3D Rendering:** Utilizes Three.js to render a detailed 3D model with full PBR (Physically-Based Rendering) textures, capturing realistic material properties like metalness and roughness.
-   **Real-Time System Statistics:** A Python backend provides live hardware data, including:
    -   **CPU:** Utilization (%) and Temperature (°C)
    -   **GPU:** Utilization (%) and Temperature (°C)
    -   **RAM:** Usage (%)
-   **Halo-Themed Holographic UI:** The user interface is inspired by the Halo universe, featuring glowing cyan text, iconic hexagonal stat boxes, and UNSC-style typography.
-   **Dynamic Environment & Lighting:** A high-dynamic-range (HDRI) panoramic image serves as a 360-degree background and provides image-based lighting, casting realistic reflections and highlights onto the model's armor.
-   **Advanced Graphics Pipeline:** A post-processing chain powered by a 4090-ready effects composer adds:
    -   **Bloom:** Creates a soft, emissive glow on bright UI elements and highlights.
    -   **Bokeh (Depth of Field):** Applies a subtle, camera-like blur to the background, making the 3D model "pop".
-   **"Living" Interface:** The 3D model features a subtle idle animation, and the UI animates into view with professional fade-in and slide-up effects. The stat boxes include a sweeping scanline effect, enhancing the holographic feel.
-   **Cross-Platform Compatibility:** The Python backend intelligently detects the operating system. It provides real hardware data on Windows (leveraging NVIDIA's NVML and Open Hardware Monitor) and uses mock data for seamless development and testing on macOS.
-   **Touch-Enabled Interaction:** While locked by default for a clean presentation, the 3D model supports touch/mouse rotation via `OrbitControls`.

---

## Technology Stack

This project is a modern web application served locally.

-   **Backend:**
    -   **Python 3:** The core programming language.
    -   **Bottle:** A fast, simple, and lightweight WSGI micro web framework used to serve files and the stats API.
    -   **psutil:** A cross-platform library for retrieving system utilization information (CPU load, RAM usage).
    -   **py-nvml-win:** (Windows Only) Python bindings for the NVIDIA Management Library, used to get GPU temperature and utilization directly.
    -   **requests:** (Windows Only) Used to fetch detailed CPU temperature data from the Open Hardware Monitor web server.

-   **Frontend:**
    -   **HTML5 / CSS3:** Provides the structure and extensive styling for the holographic UI, including animations and the hexagonal `clip-path` effect.
    -   **JavaScript (ES6 Modules):** The heart of the visual experience.
    -   **Three.js:** A powerful 3D graphics library for rendering the model, environment, and post-processing effects in WebGL.

---

## Project Structure
masterchief_display/
├── app.py # The main Python backend (Bottle web server)
├── README.md # This project manual
├── verify_project.py # A script to test the project setup
│
├── static/ # Public assets served to the browser
│ ├── assets/
│ │ └── kiara_9d_dawn_4k.hdr # The panoramic environment file
│ ├── main.js # The core Three.js rendering and UI logic
│ ├── style.css # All styling for the Halo-themed UI
│ └── halo-infinite-master-chief-remastered/
│ ├── source/
│ │ └── master_chief.fbx # The 3D model file
│ └── textures/
│ └── ... (all .png texture files)
│
└── templates/ # HTML file served by the backend
└── index.html # The main structure of the web page
code
Code
---

## Installation & Setup

Follow the instructions for your specific operating system. Before starting, ensure all project files are in the structure outlined above.

### A) Production Environment (Windows 11)

These instructions are for setting up the display to run 24/7 on the final PC with real hardware data.

1.  **Install Python:**
    -   Download and install the latest version of Python for Windows from [python.org](https://www.python.org/downloads/windows/).
    -   **CRITICAL:** During installation, on the first screen, check the box that says **"Add Python to PATH"**.

2.  **Install Open Hardware Monitor (for CPU Temperature):**
    -   Go to [openhardwaremonitor.org/downloads/](https://openhardwaremonitor.org/downloads/).
    -   Download, unzip to a permanent location (e.g., `C:\Program Files\OpenHardwareMonitor`), and run `OpenHardwareMonitor.exe`.
    -   In the program's menu, go to **`Options -> Remote Web Server -> Run`**.
    -   The application must be running in the background for CPU temperature to be displayed.

3.  **Install Project Dependencies:**
    -   Open a Command Prompt (`cmd.exe`).
    -   Navigate to the project directory (e.g., `cd C:\Users\YourName\Documents\masterchief_display`).
    -   Install all required Python libraries with this single command:
      ```cmd
      pip install bottle psutil py-nvml-win requests
      ```

4.  **Verify the Setup (Recommended):**
    -   Run the verification script to ensure everything is configured correctly:
      ```cmd
      python verify_project.py
      ```
    -   If all tests pass, you are ready to proceed.

5.  **Launch the Application:**
    -   In the same Command Prompt window, run the main script:
      ```cmd
      python app.py
      ```
    -   A browser window will open. Drag it to your vertical PC case screen and press **F11** for a seamless, full-screen experience.

### B) Development Environment (macOS)

These instructions allow you to run the project on a Mac for development. The visuals will be identical, but hardware stats will be mocked.

1.  **Prerequisites:**
    -   Ensure you have Python 3 and Homebrew installed.

2.  **Create a Virtual Environment:**
    -   Open a Terminal and navigate into the `masterchief_display` folder.
    -   Create and activate a virtual environment:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```

3.  **Install Project Dependencies:**
    -   Install the required libraries:
      ```bash
      pip install bottle psutil requests
      ```

4.  **Verify the Setup (Recommended):**
    -   Run the verification script:
      ```bash
      python verify_project.py
      ```

5.  **Launch the Application:**
    -   Run the main script:
      ```bash
      python app.py
      ```
    -   The project will open in your browser. Use the browser's Developer Tools (Device Simulator) to preview the vertical aspect ratio.

---

## Customization

The project is designed to be easily customizable.

-   **Model Position & Scale:** To change the model's position or zoom, edit the coordinate values in `static/main.js` inside the `fbxLoader.load()` function.
-   **Background Blur:** The background blur is controlled by the `BokehPass` settings in `static/main.js`. Adjust the `aperture` value (a smaller number means more blur).
-   **UI Colors & Fonts:** The primary colors and font are defined as CSS variables at the top of the `static/style.css` file. Changing them there will update the entire UI theme.
-   **Environment:** To use a different background, download a `.hdr` file from a source like [Poly Haven](https://polyhaven.com/hdris) and place it in the `static/assets/` folder. Then, update the filename in the `rgbeLoader.load()` function in `static/main.js`.