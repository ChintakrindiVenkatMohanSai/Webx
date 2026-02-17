let scene,camera,renderer,controls;

function loadModel(url){

scene=new THREE.Scene();
camera=new THREE.PerspectiveCamera(60,window.innerWidth/window.innerHeight,0.1,1000);

renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth,window.innerHeight);
document.getElementById("viewer").appendChild(renderer.domElement);

controls=new THREE.OrbitControls(camera,renderer.domElement);

const light=new THREE.HemisphereLight(0xffffff,0x444444);
scene.add(light);

camera.position.set(0,1,3);

if(url.endsWith(".glb") || url.endsWith(".gltf")){
    const loader=new THREE.GLTFLoader();
    loader.load(url,(gltf)=>{
        scene.add(gltf.scene);
    });
}else{
    const tex=new THREE.TextureLoader().load(url);
    const geo=new THREE.PlaneGeometry(2,2);
    const mat=new THREE.MeshBasicMaterial({map:tex});
    scene.add(new THREE.Mesh(geo,mat));
}

animate();
}

function animate(){
requestAnimationFrame(animate);
renderer.render(scene,camera);
}


// ----------- AR CAMERA -----------
async function startAR(file){

const stream=await navigator.mediaDevices.getUserMedia({
video:{facingMode:"environment"}
});

const video=document.createElement("video");
video.srcObject=stream;
video.autoplay=true;

document.body.appendChild(video);

alert("Basic AR started (extend with WebXR hit-test later)");
}