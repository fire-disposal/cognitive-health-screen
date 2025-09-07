<template>
  <AppPage :show-footer="true" bg-cover style="background-color: transparent;">
    <canvas ref="particlesCanvas" class="particles-bg fixed inset-0 -z-10 w-full h-full pointer-events-none"></canvas>
    <div
      style="transform: translateY(25px)"
      class="m-auto max-w-1500 min-w-345 f-c-c rounded-10 bg-white bg-opacity-60 p-15 card-shadow"
      dark:bg-dark
    >
      <div hidden w-380 px-20 py-35 md:block>
        <icon-custom-front-page pt-10 text-300 color-primary></icon-custom-front-page>
      </div>

      <div w-320 flex-col px-20 py-35>
        <h5 f-c-c text-20 font-bold color="#333" style="line-height:1.5;">
          数字孪生驱动的认知障碍居家健康监测系统
        </h5>
        <div mt-30>
          <n-input
            v-model:value="loginInfo.username"
            autofocus
            class="h-50 items-center pl-10 text-16"
            placeholder="username"
            :maxlength="20"
          />
        </div>
        <div mt-30>
          <n-input
            v-model:value="loginInfo.password"
            class="h-50 items-center pl-10 text-16"
            type="password"
            show-password-on="mousedown"
            placeholder="password"
            :maxlength="20"
            @keypress.enter="handleLogin"
          />
        </div>

        <div mt-20>
          <n-button
            h-50
            w-full
            rounded-5
            text-16
            type="primary"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </n-button>
        </div>
      </div>
    </div>
  </AppPage>
</template>

<script setup>
import { lStorage, setToken } from '@/utils'
import api from '@/api'
import { addDynamicRoutes } from '@/router'
import { ref, onMounted, computed, watch } from 'vue'
import { useAppStore } from '@/store/modules/app'

const router = useRouter()
const { query } = useRoute()
const appStore = useAppStore()
const isDark = computed(() => appStore.isDark)
const particlesCanvas = ref(null)

const loginInfo = ref({
  username: '',
  password: '',
})

initLoginInfo()

function initLoginInfo() {
  const localLoginInfo = lStorage.get('loginInfo')
  if (localLoginInfo) {
    loginInfo.value.username = localLoginInfo.username || ''
    loginInfo.value.password = localLoginInfo.password || ''
  }
}

const loading = ref(false)
async function handleLogin() {
  const { username, password } = loginInfo.value
  if (!username || !password) {
    $message.warning('请输入用户名和密码')
    return
  }
  try {
    loading.value = true
    $message.loading('登录成功')
    const res = await api.login({ username, password: password.toString() })
    $message.success('登录成功')
    setToken(res.data.access_token)
    await addDynamicRoutes()
    if (query.redirect) {
      const path = query.redirect
      console.log('path', { path, query })
      Reflect.deleteProperty(query, 'redirect')
      router.push({ path, query })
    } else {
      router.push('/')
    }
  } catch (e) {
    console.error('login error', e.error)
  }
  loading.value = false
}

// 粒子动画初始化
onMounted(() => {
  const canvas = particlesCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  function resizeCanvas() {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  resizeCanvas()
  window.addEventListener('resize', resizeCanvas)

  // 粒子参数
  const particleCount = 60
  const particles = []
  const colorsLight = ['#e0e7ff', '#a5b4fc', '#f0abfc', '#bae6fd']
  const colorsDark = ['#334155', '#64748b', '#818cf8', '#f472b6']
  function getColors() {
    return isDark.value ? colorsDark : colorsLight
  }

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 2 + 1.5,
      dx: (Math.random() - 0.5) * 0.8,
      dy: (Math.random() - 0.5) * 0.8,
      color: getColors()[Math.floor(Math.random() * getColors().length)]
    })
  }

  function drawGradient() {
    const grad = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
    if (isDark.value) {
      grad.addColorStop(0, '#18181c')
      grad.addColorStop(1, '#23272f')
    } else {
      grad.addColorStop(0, '#e0e7ff')
      grad.addColorStop(1, '#bae6fd')
    }
    ctx.fillStyle = grad
    ctx.fillRect(0, 0, canvas.width, canvas.height)
  }

  function drawParticles() {
    for (const p of particles) {
      ctx.beginPath()
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx.fillStyle = p.color
      ctx.globalAlpha = 0.7
      ctx.fill()
      ctx.globalAlpha = 1
    }
  }

  function updateParticles() {
    for (const p of particles) {
      p.x += p.dx
      p.y += p.dy
      if (p.x < 0 || p.x > canvas.width) p.dx *= -1
      if (p.y < 0 || p.y > canvas.height) p.dy *= -1
    }
  }

  function animate() {
    drawGradient()
    drawParticles()
    updateParticles()
    requestAnimationFrame(animate)
  }
  animate()

  // 监听暗黑模式切换，动态更新粒子颜色
  watch(isDark, (val) => {
    for (let i = 0; i < particles.length; i++) {
      particles[i].color = getColors()[Math.floor(Math.random() * getColors().length)]
    }
  })
})
</script>
