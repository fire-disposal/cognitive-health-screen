<template>
  <AppPage>
    <n-result m-auto status="403">
      <template #icon>
        <icon-custom-forbidden text-400px text-primary></icon-custom-forbidden>
      </template>
      <template #footer>
        <n-button type="primary" @click="replace('/')">返回首页</n-button>
      </template>
    </n-result>
  </AppPage>
</template>

<script setup>
const { replace } = useRouter()
</script>
