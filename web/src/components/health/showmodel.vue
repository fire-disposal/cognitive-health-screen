<template>
  <div class="scene-3d-container">
    <div ref="sceneContainer" class="scene-canvas"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

const props = defineProps({
  modelUrl: {
    type: String,
    required: true
  },
  size: {
    type: Object,
    default: () => ({ width: 400, height: 400 })
  },
  autoRotate: {
    type: Boolean,
    default: true
  },
  rotateSpeed: {
    type: Number,
    default: 0.01
  }
})

const sceneContainer = ref(null)
let scene, camera, renderer, controls, model, animationId

const initThree = () => {
  // 场景
  scene = new THREE.Scene()
  scene.background = null // 透明背景

  // 相机
  camera = new THREE.PerspectiveCamera(
    75,
    props.size.width / props.size.height,
    0.1,
    1000
  )
  camera.position.set(0, 2, 5)

  // 渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(props.size.width, props.size.height)
  renderer.setClearColor(0x000000, 0)
  sceneContainer.value.appendChild(renderer.domElement)

  // 环境光
  const ambientLight = new THREE.AmbientLight(0xffffff, 1.2)
  scene.add(ambientLight)
  const directionalLight = new THREE.DirectionalLight(0xffffff, 2.0)
  directionalLight.position.set(5, 10, 7.5)
  scene.add(directionalLight)
  const hemisphereLight = new THREE.HemisphereLight(0xb1e1ff, 0xb97a20, 3.0)
  scene.add(hemisphereLight)

  // 轨道控制器
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.enablePan = false
  controls.enableZoom = true

  // 加载模型
  loadModel(props.modelUrl)
}

const loadModel = (url) => {
  const loader = new GLTFLoader()
  const dracoLoader = new DRACOLoader()
  dracoLoader.setDecoderPath('/libs/draco/')
  loader.setDRACOLoader(dracoLoader)
  loader.load(
    url,
    (gltf) => {
      model = gltf.scene
      model.position.set(0, 0, 0)
      scene.add(model)
    },
    undefined,
    (error) => {
      // 可根据需要暴露错误处理
      console.error('模型加载失败', error)
    }
  )
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  if (model && props.autoRotate) {
    model.rotation.y += props.rotateSpeed
  }
  controls.update()
  renderer.render(scene, camera)
}

const handleResize = () => {
  if (!camera || !renderer) return
  camera.aspect = props.size.width / props.size.height
  camera.updateProjectionMatrix()
  renderer.setSize(props.size.width, props.size.height)
}

watch(() => props.size, () => {
  handleResize()
}, { deep: true })

onMounted(() => {
  initThree()
  animate()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (animationId) cancelAnimationFrame(animationId)
  if (renderer && sceneContainer.value) {
    sceneContainer.value.removeChild(renderer.domElement)
    renderer.dispose()
  }
})

defineExpose({
  reloadModel: (url) => {
    if (model && model.parent) model.parent.remove(model)
    loadModel(url)
  },
  getThreeInstance: () => ({ scene, camera, renderer, controls, model })
})
</script>