let renderer, scene, camera;

async function startAR(file){

if(!navigator.xr){
alert("WebXR not supported on this device");
return;
}

scene=new THREE.Scene();
camera=new THREE.PerspectiveCamera();

renderer=new THREE.WebGLRenderer({alpha:true,antialias:true});
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.xr.enabled=true;

document.body.appendChild(renderer.domElement);

const session=await navigator.xr.requestSession("immersive-ar",{
requiredFeatures:["hit-test"]
});

renderer.xr.setSession(session);

// LOAD IMAGE AS AR OBJECT
const texture=new THREE.TextureLoader().load("/uploads/"+file);
const plane=new THREE.Mesh(
new THREE.PlaneGeometry(1,1),
new THREE.MeshBasicMaterial({map:texture})
);

plane.position.set(0,0,-2);
scene.add(plane);

renderer.setAnimationLoop(()=>{
renderer.render(scene,camera);
});

}


// CAPTURE AR PHOTO
function captureAR(){

const canvas=document.querySelector("canvas");

if(!canvas){
alert("Start AR first");
return;
}

const img=canvas.toDataURL("image/png");

const link=document.createElement("a");
link.href=img;
link.download="AR_Photo.png";
link.click();
}