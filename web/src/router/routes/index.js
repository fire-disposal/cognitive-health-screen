const Layout = () => import('@/layout/index.vue')

export const basicRoutes = [
  {
    path: '/',
    redirect: '/workbench', // 默认跳转到首页
    meta: { order: 0 },
  },
  {
    name: '工作台',
    path: '/workbench',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/workbench/index.vue'),
        name: `工作台Default`,
        meta: {
          title: '工作台',
          icon: 'icon-park-outline:workbench',
          affix: true,
        },
      },
    ],
    meta: { order: 1 },
  },
  {
    name: '个人中心',
    path: '/profile',
    component: Layout,
    isHidden: true,
    children: [
      {
        path: '',
        component: () => import('@/views/profile/index.vue'),
        name: `个人中心Default`,
        meta: {
          title: '个人中心',
          icon: 'user',
          affix: true,
        },
      },
    ],
    meta: { order: 99 },
  },
  {
    name: '403',
    path: '/403',
    component: () => import('@/views/error-page/403.vue'),
    isHidden: true,
  },
  {
    name: '404',
    path: '/404',
    component: () => import('@/views/error-page/404.vue'),
    isHidden: true,
  },
  {
    name: 'Login',
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    isHidden: true,
    meta: {
      title: '登录页',
    },
  },
  {
    name: 'PatientDetail',
    path: '/health/patient/detail/:id',
    component: () => import('@/views/health/patient/detail.vue'),
    isHidden: true,
    meta: {
      title: '病人详情',
    },
  },
  {
    name: 'CognitiveAssessment',
    path: '/health/assessment/cognitive',
    component: () => import('@/views/health/assessment/cognitive.vue'),
    isHidden: true,
    meta: {
      title: '认知功能评估',
    },
  },
  {
    name: 'PhysiologicalAssessment',
    path: '/health/assessment/physiological',
    component: () => import('@/views/health/assessment/physiological.vue'),
    isHidden: true,
    meta: {
      title: '生理健康评估',
    },
  },
  {
    name: 'ADLAssessment',
    path: '/health/assessment/adl',
    component: () => import('@/views/health/assessment/adl.vue'),
    isHidden: true,
    meta: {
      title: '日常生活能力评估',
    },
  },
  {
    name: 'RiskPrediction',
    path: '/health/assessment/risk-prediction',
    component: () => import('@/views/health/assessment/risk-prediction.vue'),
    isHidden: true,
    meta: {
      title: '风险预测',
    },
  },

]

export const NOT_FOUND_ROUTE = {
  name: 'NotFound',
  path: '/:pathMatch(.*)*',
  redirect: '/404',
  isHidden: true,
}

export const EMPTY_ROUTE = {
  name: 'Empty',
  path: '/:pathMatch(.*)*',
  component: null,
}

const modules = import.meta.glob('@/views/**/route.js', { eager: true })
const asyncRoutes = []
Object.keys(modules).forEach((key) => {
  asyncRoutes.push(modules[key].default)
})

// 加载 views 下每个模块的 index.vue 文件
const vueModules = import.meta.glob('@/views/**/index.vue')

export { asyncRoutes, vueModules }
