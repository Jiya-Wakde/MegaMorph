const scene = new THREE.Scene();
const loader = new GLTFLoader();

let camera, renderer, clock;
let optimus, megatron;

init();
animate();

function init() {
  scene = new THREE.Scene();

  camera = new THREE.PerspectiveCamera(
    50,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(0, 3, 10);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  clock = new THREE.Clock();

  // Lights
  const ambient = new THREE.AmbientLight(0x404040, 2);
  scene.add(ambient);

  const pointLight = new THREE.PointLight(0xffffff, 2, 50);
  pointLight.position.set(0, 10, 10);
  scene.add(pointLight);

  // Loader
  const loader = new GLTFLoader();

  // Load Optimus
  loader.load("static/models/optimus_prime.glb", (gltf) => {
    optimus = gltf.scene;
    optimus.position.set(-3, 0, 0);
    optimus.scale.set(1.5, 1.5, 1.5);

    scene.add(optimus);
  });

  // Load Megatron
  loader.load("static/models/megatron.glb", (gltf) => {
    megatron = gltf.scene;
    megatron.position.set(3, 0, 0);
    megatron.scale.set(1.5, 1.5, 1.5);

    scene.add(megatron);
  });

  window.addEventListener("resize", onWindowResize, false);
}

function animate() {
  requestAnimationFrame(animate);

  const elapsed = clock.getElapsedTime();

  // Camera rotation
  camera.position.x = Math.sin(elapsed * 0.3) * 10;
  camera.position.z = Math.cos(elapsed * 0.3) * 10;
  camera.lookAt(0, 2, 0);

  renderer.render(scene, camera);
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
s