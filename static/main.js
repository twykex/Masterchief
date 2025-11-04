// static/main.js (FINAL POLISHED PRODUCTION - "Living" Interface)

import * as THREE from 'three';
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { BokehPass } from 'three/addons/postprocessing/BokehPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

let chiefModel = null; // We need a global reference to the model for animation

// --- 1. Scene Setup ---
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, 682 / 2560, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.outputColorSpace = THREE.SRGBColorSpace;
const container = document.getElementById('canvas-container');
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

// --- 2. Lighting ---
const fillLight = new THREE.PointLight(0xffffff, 0.8);
camera.add(fillLight);
scene.add(camera);

// --- 3. Controls ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enablePan = false;
controls.enableZoom = false;
// Add a small amount of auto-rotation for a dynamic feel when idle
controls.autoRotate = true;
controls.autoRotateSpeed = 0.2; // Adjust speed here (positive/negative for direction)

// --- 4. Post-Processing ---
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloomPass = new UnrealBloomPass(new THREE.Vector2(container.clientWidth, container.clientHeight), 0.5, 0.5, 0.85);
composer.addPass(bloomPass);
const bokehPass = new BokehPass(scene, camera, { focus: 2.3, aperture: 0.005, maxblur: 0.005 });
composer.addPass(bokehPass);

// --- 5. Environment ---
const rgbeLoader = new RGBELoader();
rgbeLoader.load('/static/assets/kiara_9d_dawn_4k.hdr', (texture) => {
    texture.mapping = THREE.EquirectangularReflectionMapping;
    scene.background = texture;
    scene.environment = texture;
});

// --- 6. Load Model ---
const modelPath = '/static/halo-infinite-master-chief-remastered/source/master_chief.fbx';
const texturePath = '/static/halo-infinite-master-chief-remastered/textures/';
const fbxLoader = new FBXLoader();
const textureLoader = new THREE.TextureLoader();

fbxLoader.load(modelPath, (object) => {
    // --- THIS LOCATION AND SIZE CODE IS LOCKED ---
    object.scale.set(0.025, 0.025, 0.025);
    const targetX = 0.00, targetY = 0.8, cameraZ = 2.6;
    controls.target.set(targetX, targetY, 0);
    camera.position.set(targetX, targetY, cameraZ);
    // --- END OF LOCKED CODE ---

    object.traverse((child) => {
        if (child.isMesh && Array.isArray(child.material)) {
            const newMaterials = [];
            child.material.forEach((material) => {
                const matName = material.name.toLowerCase();
                const newMaterial = new THREE.MeshStandardMaterial({ name: material.name });
                if (matName.includes('arms')) {
                    newMaterial.map = textureLoader.load(texturePath + 'Arms_Base_color.png');
                    newMaterial.metalnessMap = textureLoader.load(texturePath + 'Arms_Metallic.png');
                    newMaterial.roughnessMap = textureLoader.load(texturePath + 'Arms_Roughness.png');
                    newMaterial.normalMap = textureLoader.load(texturePath + 'Arms_Normal_OpenGL.png');
                } else if (matName.includes('chest')) {
                    newMaterial.map = textureLoader.load(texturePath + 'Chest_Base_color.png');
                    newMaterial.metalnessMap = textureLoader.load(texturePath + 'Chest_Metallic.png');
                    newMaterial.roughnessMap = textureLoader.load(texturePath + 'Chest_Roughness.png');
                    newMaterial.normalMap = textureLoader.load(texturePath + 'Chest_Normal_OpenGL.png');
                } else if (matName.includes('helmet')) {
                    newMaterial.map = textureLoader.load(texturePath + 'Helmet_Base_color.png');
                    newMaterial.metalnessMap = textureLoader.load(texturePath + 'Helmet_Metallic.png');
                    newMaterial.roughnessMap = textureLoader.load(texturePath + 'Helmet_Roughness.png');
                    newMaterial.normalMap = textureLoader.load(texturePath + 'Helmet_Normal_OpenGL.png');
                } else if (matName.includes('legs')) {
                    newMaterial.map = textureLoader.load(texturePath + 'Legs_Base_color.png');
                    newMaterial.metalnessMap = textureLoader.load(texturePath + 'Legs_Metallic.png');
                    newMaterial.roughnessMap = textureLoader.load(texturePath + 'Legs_Roughness.png');
                    newMaterial.normalMap = textureLoader.load(texturePath + 'Legs_Normal_OpenGL.png');
                }
                if (newMaterial.map) newMaterial.map.colorSpace = THREE.SRGBColorSpace;
                newMaterials.push(newMaterial);
            });
            child.material = newMaterials;
        }
    });
    scene.add(object);
    chiefModel = object; // Assign to our global variable
});

// --- 7. Animation & Stats ---
function animate() {
    requestAnimationFrame(animate);
    controls.update(); // This is needed for auto-rotate and damping
    composer.render();
}
animate();

async function updateStats() { try { const response = await fetch('/stats'); const data = await response.json(); document.getElementById('time').innerText = data.time; document.getElementById('date').innerText = data.date; document.getElementById('cpu-load').innerText = data.cpu.load.toFixed(1); document.getElementById('cpu-temp').innerText = data.cpu.temp; document.getElementById('gpu-load').innerText = data.gpu.load; document.getElementById('gpu-temp').innerText = data.gpu.temp; document.getElementById('ram-usage').innerText = data.ram.used_percent.toFixed(1); } catch (error) {} }
setInterval(updateStats, 2000); updateStats();