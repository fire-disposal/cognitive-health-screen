<script setup>
import { ref, computed } from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NTabPane,
  NTabs,
  NImage,
  NSelect,
  NSpace,
  NCard,
} from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import { useUserStore, useAppStore } from '@/store'
import { themeColorMap, logoTypeMap } from '~/settings/theme'
import api from '@/api'

const userStore = useUserStore()
const appStore = useAppStore()

const isLoading = ref(false)

// ================= 用户信息表单 ====================
const infoFormRef = ref(null)

// 获取 theme 选项
const themeOptions = Object.keys(themeColorMap).map((key) => ({
  label: key.charAt(0).toUpperCase() + key.slice(1),
  value: key,
}))

// 从 store 获取当前主题，确保 fallback
const currentTheme = computed(() => {
  const theme = userStore.theme
  return themeOptions.some((opt) => opt.value === theme) ? theme : themeOptions[0].value
})

// 初始化表单
const infoForm = ref({
  avatar: userStore.avatar,
  username: userStore.name,
  email: userStore.email,
  theme: userStore.theme,
  logo_type: appStore.logoType,
})

const logoOptions = Object.entries(logoTypeMap).map(([key, value]) => ({
  label: value.label,
  value: key,
}))

const getCurrentLogoSrc = computed(() => {
  return logoTypeMap[infoForm.value.logo_type]?.icon || logoTypeMap.type1.icon
})

async function updateProfile() {
  try {
    isLoading.value = true
    const valid = await infoFormRef.value?.validate()
    if (!valid) return

    const { theme, logo_type, username, email, avatar } = infoForm.value

    if (theme && theme !== userStore.theme) {
      await api.updateUserTheme(theme)
      appStore.setTheme(theme)
      userStore.setUserInfo({ ...userStore.$state.userInfo, theme })
    }

    if (logo_type && logo_type !== appStore.logoType) {
      await api.updateUserLogo(logo_type)
      appStore.setLogoType(logo_type)
      userStore.setUserInfo({ ...userStore.$state.userInfo, logo_type })
    }

    if (username !== userStore.name || email !== userStore.email || avatar !== userStore.avatar) {
      await api.updateUser({
        id: userStore.userId,
        username,
        email,
        avatar,
      })
      userStore.setUserInfo({
        ...userStore.$state.userInfo,
        username,
        email,
        avatar,
      })
    }

    $message.success('信息更新成功')
  } catch (e) {
    console.error(e)
    $message.error('信息更新失败')
  } finally {
    isLoading.value = false
  }
}

const infoFormRules = {
  username: [
    {
      required: true,
      message: '请输入用户名',
      trigger: ['input', 'blur'],
    },
  ],
}

// ================ 修改密码表单 ==================
const passwordFormRef = ref(null)
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

async function updatePassword() {
  isLoading.value = true
  passwordFormRef.value?.validate(async (err) => {
    if (!err) {
      const data = { ...passwordForm.value, id: userStore.userId }
      try {
        const res = await api.updatePassword(data)
        $message.success(res.msg)
        passwordForm.value = {
          old_password: '',
          new_password: '',
          confirm_password: '',
        }
      } catch (e) {
        $message.error('密码更新失败')
      } finally {
        isLoading.value = false
      }
    }
  })
}

function validatePasswordStartWith(rule, value) {
  return (
    !!passwordForm.value.new_password &&
    passwordForm.value.new_password.startsWith(value) &&
    passwordForm.value.new_password.length >= value.length
  )
}
function validatePasswordSame(rule, value) {
  return value === passwordForm.value.new_password
}

const passwordFormRules = {
  old_password: [{ required: true, message: '请输入旧密码', trigger: ['input', 'blur'] }],
  new_password: [{ required: true, message: '请输入新密码', trigger: ['input', 'blur'] }],
  confirm_password: [
    { required: true, message: '请确认密码', trigger: ['input', 'blur'] },
    { validator: validatePasswordStartWith, message: '两次密码输入不一致', trigger: 'input' },
    { validator: validatePasswordSame, message: '两次密码输入不一致', trigger: ['blur'] },
  ],
}
</script>

<template>
  <CommonPage :show-header="false">
    <div class="flex justify-center p-6">
      <n-card style="width: 640px" title="账户设置" bordered>
        <n-tabs type="segment" animated>
          <!-- 修改信息 -->
          <n-tab-pane name="info" tab="修改信息">
            <n-form
              ref="infoFormRef"
              label-placement="left"
              label-align="left"
              label-width="100"
              :model="infoForm"
              :rules="infoFormRules"
            >
              <n-form-item label="头像" path="avatar">
                <n-space align="center">
                  <n-image width="64" height="64" :src="infoForm.avatar" preview-disabled />
                  <n-input
                    v-model:value="infoForm.avatar"
                    placeholder="请输入头像链接"
                    style="width: 300px"
                  />
                </n-space>
              </n-form-item>

              <n-form-item label="Logo 设置" path="logo_type">
                <n-space vertical>
                  <n-select
                    v-model:value="infoForm.logo_type"
                    :options="logoOptions"
                    placeholder="选择 Logo 类型"
                    style="width: 300px"
                  />
                  <n-image
                    v-if="infoForm.logo_type"
                    :src="getCurrentLogoSrc"
                    width="48"
                    height="48"
                    object-fit="contain"
                  />
                </n-space>
              </n-form-item>

              <NFormItem label="主题配色" path="theme">
                <div style="display: flex; align-items: center">
                  <NSelect
                    v-model:value="infoForm.theme"
                    :options="themeOptions"
                    style="min-width: 160px"
                  />
                  <div
                    v-if="themeColorMap[infoForm.theme]"
                    style="margin-left: 16px; display: flex; gap: 4px"
                  >
                    <span
                      v-for="(color, idx) in themeColorMap[infoForm.theme]"
                      :key="idx"
                      :style="{
                        display: 'inline-block',
                        width: '24px',
                        height: '24px',
                        background: color,
                        borderRadius: '4px',
                        border: '1px solid #eee',
                      }"
                    ></span>
                  </div>
                </div>
              </NFormItem>

              <n-form-item label="用户名" path="username">
                <n-input v-model:value="infoForm.username" placeholder="请输入用户名" clearable />
              </n-form-item>

              <n-form-item label="邮箱" path="email">
                <n-input v-model:value="infoForm.email" placeholder="请输入邮箱" clearable />
              </n-form-item>

              <n-space justify="end" class="mt-4">
                <n-button
                  type="primary"
                  :loading="isLoading"
                  icon="i-mdi-check"
                  @click="updateProfile"
                >
                  更新信息
                </n-button>
              </n-space>
            </n-form>
          </n-tab-pane>

          <!-- 修改密码 -->
          <n-tab-pane name="password" tab="修改密码">
            <n-form
              ref="passwordFormRef"
              label-placement="left"
              label-align="left"
              label-width="100"
              :model="passwordForm"
              :rules="passwordFormRules"
            >
              <n-form-item label="旧密码" path="old_password">
                <n-input
                  v-model:value="passwordForm.old_password"
                  type="password"
                  placeholder="请输入旧密码"
                  show-password-on="click"
                  clearable
                />
              </n-form-item>

              <n-form-item label="新密码" path="new_password">
                <n-input
                  v-model:value="passwordForm.new_password"
                  type="password"
                  :disabled="!passwordForm.old_password"
                  placeholder="请输入新密码"
                  show-password-on="click"
                  clearable
                />
              </n-form-item>

              <n-form-item label="确认密码" path="confirm_password">
                <n-input
                  v-model:value="passwordForm.confirm_password"
                  type="password"
                  :disabled="!passwordForm.new_password"
                  placeholder="请再次输入新密码"
                  show-password-on="click"
                  clearable
                />
              </n-form-item>

              <n-space justify="end" class="mt-4">
                <n-button
                  type="primary"
                  :loading="isLoading"
                  icon="i-mdi-lock-reset"
                  @click="updatePassword"
                >
                  修改密码
                </n-button>
              </n-space>
            </n-form>
          </n-tab-pane>
        </n-tabs>
      </n-card>
    </div>
  </CommonPage>
</template>

<style scoped>
.mt-4 {
  margin-top: 1rem;
}
</style>
