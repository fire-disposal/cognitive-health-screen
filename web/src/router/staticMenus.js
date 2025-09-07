// 静态菜单配置，原始数据迁移自后端
export const staticMenus = [
  {
    name: "系统管理",
    path: "/system",
    menu_type: "catalog",
    order: 1,
    icon: "carbon:gui-management",
    is_hidden: false,
    component: "Layout",
    keepalive: false,
    redirect: "/system/user",
    children: [
      { name: "用户管理", path: "user", order: 1, icon: "material-symbols:person-outline-rounded", component: "/system/user" },
      { name: "角色管理", path: "role", order: 2, icon: "carbon:user-role", component: "/system/role" },
      { name: "菜单管理", path: "menu", order: 3, icon: "material-symbols:list-alt-outline", component: "/system/menu" },
      { name: "API管理", path: "api", order: 4, icon: "ant-design:api-outlined", component: "/system/api" },
      { name: "审计日志", path: "auditlog", order: 6, icon: "ph:clipboard-text-bold", component: "/system/auditlog" }
    ]
  },
  {
    name: "健康管理",
    path: "/health",
    menu_type: "catalog",
    order: 2,
    icon: "mdi:heart-pulse",
    is_hidden: false,
    component: "Layout",
    keepalive: false,
    redirect: "/health/patient",
    children: [
      { name: "病人管理", path: "patient", order: 1, icon: "material-symbols:person-outline-rounded", component: "/health/patient" },
      { name: "设备管理", path: "device", order: 2, icon: "carbon:user-role", component: "/health/device" },
      { name: "健康数据", path: "health_data", order: 3, icon: "ant-design:api-outlined", component: "/health/health_data" },
      { name: "健康评估", path: "assessment", order: 4, icon: "mdi:clipboard-check-multiple", component: "/health/assessment" },
      { name: "告警中心", path: "alert", order: 5, icon: "mdi:bell-alert-outline", component: "/health/alert" },
      { name: "统计分析", path: "analysis", order: 7, icon: "mdi:chart-line", component: "/health/analysis" }
    ]
  },
  {
    name: "数字孪生",
    path: "/twinview",
    menu_type: "menu",
    order: 4,
    icon: "material-symbols:view-in-ar",
    is_hidden: false,
    component: "/twinview",
    keepalive: false,
    children: []
  }
];