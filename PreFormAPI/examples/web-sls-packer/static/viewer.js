// 3D view of one part with rotation rings for choosing the pose it will be packed in; drag off the part to orbit.
// Loaded on demand by app.js the first time a thumbnail is clicked. Axes are PreForm's: Z up.
import * as THREE from "three";
import { STLLoader } from "three/addons/loaders/STLLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { TransformControls } from "three/addons/controls/TransformControls.js";

// PreForm composes its orient endpoint's x, y, z degrees as Ry * Rx * Rz, which is Three's 'YXZ' Euler order.
const PREFORM_ORDER = "YXZ";
let renderer, scene, camera, orbit, gizmo, mesh, frame, dialog, thumb;

function setup(canvas) {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(40, 1, 0.1, 10000);
  camera.up.set(0, 0, 1);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8899aa, 1.1));
  const key = new THREE.DirectionalLight(0xffffff, 1.2);
  key.position.set(1, -2, 3);
  scene.add(key);
  orbit = new OrbitControls(camera, canvas);
  orbit.enableDamping = true;
  gizmo = new TransformControls(camera, canvas);
  gizmo.setMode("rotate");
  gizmo.addEventListener("dragging-changed", (e) => { orbit.enabled = !e.value; });
  gizmo.addEventListener("objectChange", report);
  scene.add(gizmo);
}

function degrees() {
  const e = new THREE.Euler().setFromQuaternion(mesh.quaternion, PREFORM_ORDER);
  return [e.x, e.y, e.z].map((r) => Math.round(THREE.MathUtils.radToDeg(r) * 100) / 100);
}

function report() {
  if (!mesh) return;
  const box = new THREE.Box3().setFromObject(mesh);
  const s = box.getSize(new THREE.Vector3());
  const [x, y, z] = degrees();
  dialog.querySelector(".viewer-status").textContent =
    `${s.x.toFixed(1)} × ${s.y.toFixed(1)} × ${s.z.toFixed(1)} mm in this pose · rotation x ${x}°, y ${y}°, z ${z}°`;
}

function turn(spec) {
  if (spec === "reset") mesh.quaternion.identity();
  else {
    const [axis, deg] = spec.split(":");
    const q = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(axis === "x" ? 1 : 0, axis === "y" ? 1 : 0, axis === "z" ? 1 : 0), THREE.MathUtils.degToRad(+deg));
    mesh.quaternion.premultiply(q);                   // turn about the world axis, as the buttons promise
  }
  report();
}

async function post(method, url, body) {
  const html = await fetch(url, { method, body }).then((r) => r.text());
  const row = document.getElementById(`part-${thumb.dataset.part}`);
  if (row) htmx.swap(row, html, { swapStyle: "outerHTML" });
}

export async function show(dlg, el) {
  dialog = dlg; thumb = el;
  const canvas = dialog.querySelector("canvas");
  dialog.querySelector(".viewer-title").textContent = thumb.dataset.title;
  dialog.querySelector(".viewer-status").textContent = "Loading…";
  dialog.showModal();
  if (!renderer) {
    setup(canvas);
    dialog.querySelectorAll("[data-turn]").forEach((b) => b.addEventListener("click", () => turn(b.dataset.turn)));
    dialog.querySelector(".viewer-use").addEventListener("click", async () => {
      const [x, y, z] = degrees();
      const body = new FormData(); body.append("x", x); body.append("y", y); body.append("z", z);
      await post("POST", thumb.dataset.orientUrl, body);
      dialog.close();
    });
    dialog.querySelector(".viewer-clear").addEventListener("click", async () => { await post("DELETE", thumb.dataset.orientUrl); dialog.close(); });
  }
  if (mesh) { gizmo.detach(); scene.remove(mesh); mesh.geometry.dispose(); mesh = null; }
  const size = Math.min(window.innerWidth - 120, window.innerHeight - 260, 560);
  renderer.setSize(size, size, true);
  camera.aspect = 1;
  const geometry = await new STLLoader().loadAsync(thumb.dataset.stl);
  geometry.computeVertexNormals();
  geometry.computeBoundingBox();
  const centre = geometry.boundingBox.getCenter(new THREE.Vector3());
  const radius = geometry.boundingBox.getSize(new THREE.Vector3()).length() / 2;
  geometry.translate(-centre.x, -centre.y, -centre.z);
  mesh = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.1, roughness: 0.65 }));
  const [x, y, z] = thumb.dataset.orientation.split(",").map(Number);
  mesh.rotation.set(...[x, y, z].map(THREE.MathUtils.degToRad), PREFORM_ORDER);
  scene.add(mesh);
  camera.position.set(radius * 1.7, -radius * 1.7, radius * 1.2);
  camera.near = radius / 100; camera.far = radius * 100;
  camera.updateProjectionMatrix();
  orbit.target.set(0, 0, 0);
  orbit.update();
  gizmo.attach(mesh);                                  // rotate rings on the part; dragging elsewhere orbits the camera
  report();
  cancelAnimationFrame(frame);
  const loop = () => { orbit.update(); renderer.render(scene, camera); frame = requestAnimationFrame(loop); };
  loop();
}

export function hide() {
  cancelAnimationFrame(frame);
  if (mesh) { gizmo.detach(); scene.remove(mesh); mesh.geometry.dispose(); mesh = null; }
}
