// THREE.js 
  let scene = new THREE.Scene();
  scene.background = new THREE.Color(0x202030);

  let camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 2000);
  camera.position.set(0,5,25);

  let renderer = new THREE.WebGLRenderer({antialias:true});
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  const ambientLight = new THREE.AmbientLight(0xffffff,0.6);
  scene.add(ambientLight);
  const dirLight = new THREE.DirectionalLight(0xffffff,1);
  dirLight.position.set(5,10,7);
  scene.add(dirLight);

  const baseGeometry = new THREE.CylinderGeometry(8,8,1,64);
  const baseMaterial = new THREE.MeshStandardMaterial({color:0x444444,metalness:0.8,roughness:0.3});
  const base = new THREE.Mesh(baseGeometry,baseMaterial);
  base.position.y=-0.5;
  scene.add(base);

  let optimus, megatron;
  const loader = new THREE.GLTFLoader();
  loader.load("../static/assests/optimus_prime.glb", (gltf)=> {
    optimus=gltf.scene;
    optimus.scale.set(1.5,1.5,1.5);
    const box=new THREE.Box3().setFromObject(optimus);
    const size=new THREE.Vector3();
    box.getSize(size);
    const center=new THREE.Vector3();
    box.getCenter(center);
    optimus.position.sub(center);
    optimus.position.y+=size.y/2;
    optimus.position.x=-5;
    optimus.rotation.y=Math.PI/8;
    base.add(optimus);
  });

  loader.load("../static/assests/megatron.glb", (gltf)=> {
    megatron=gltf.scene;
    megatron.scale.set(0.025,0.025,0.025);
    const box=new THREE.Box3().setFromObject(megatron);
    const size=new THREE.Vector3();
    box.getSize(size);
    const center=new THREE.Vector3();
    box.getCenter(center);
    megatron.position.sub(center);
    megatron.position.y+=size.y/4;
    megatron.position.x=4;
    megatron.rotation.y=-Math.PI;
    base.add(megatron);
  });

  window.addEventListener("scroll",()=> {
    let scrollY=window.scrollY;
    base.rotation.y=scrollY*0.002;
    if(scrollY<window.innerHeight*2){
      camera.position.z=25-(scrollY/window.innerHeight)*16;
      camera.position.y=5-(scrollY/window.innerHeight)*2;
    }
  });

  function animate(){
    requestAnimationFrame(animate);
    renderer.render(scene,camera);
  }
  animate();

  window.addEventListener("resize",()=> {
    camera.aspect=window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
  });

  // Horizontal scroll for mouse wheel
  const horizontalContainer = document.querySelector('.horizontal-scroll-container');
  horizontalContainer.addEventListener('wheel', (e)=>{
    e.preventDefault();
    horizontalContainer.scrollLeft += e.deltaY;
  }, {passive:false});

    // Hide splash  4 seconds
  window.addEventListener("load", () => {
    setTimeout(() => {
      document.getElementById("splash").style.opacity = "0";
      setTimeout(() => {
        document.getElementById("splash").style.display = "none";
      }, 1000); 
    }, 4000);
  });