<script setup>
import { ref, onMounted, h } from 'vue'
import { NCard, NSpace, NForm, NFormItem, NInput, NButton, NSelect, NDatePicker, NDrawer, NDrawerContent, NDescriptions, NDescriptionsItem, NPopconfirm } from 'naive-ui'
import CrudTable from '@/components/table/CrudTable.vue'
import { useCRUD } from '@/composables'
import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'

const $table = ref(null)
const queryItems = ref({})
const detailDrawerVisible = ref(false)
const detailData = ref({})

const dataTypeOptions = [
  { label: '心率', value: 'heart_rate' },
  { label: '血压', value: 'blood_pressure' },
  { label: '血氧', value: 'blood_oxygen' },
  { label: '体温', value: 'temperature' },
  { label: '血糖', value: 'blood_glucose' }
]

const {
  handleDelete
} = useCRUD({
  name: '健康数据',
  doDelete: api.deleteHealthData,
  refresh: () => $table.value?.handleSearch()
})

const columns = [
  {
    title: '设备',
    key: 'device',
    width: 140,
    render(row) {
      return row.device?.name || row.device_id || '-'
    }
  },
  {
    title: '患者',
    key: 'patient',
    width: 140,
    render(row) {
      return row.patient?.name || row.patient_name || row.patient_id || '-'
    }
  },
  { title: '分类', key: 'category', width: 100 },
  { title: '分区', key: 'partition', width: 100 },
  { title: '归档', key: 'archived', width: 60, render(row) { return row.archived ? '是' : '否' } },
  {
    title: '载荷',
    key: 'payload',
    width: 180,
    render(row) {
      if (!row.payload) return '-'
      const str = JSON.stringify(row.payload)
      return str.length > 40 ? str.slice(0, 40) + '...' : str
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 120,
    fixed: 'right',
    render(row) {
      return [
        h(NButton, { size: 'small', type: 'primary', onClick: () => showDetail(row) }, { default: () => '详情' }),
        h(NPopconfirm, { onPositiveClick: () => handleDelete({ id: row.id }) }, {
          trigger: () => h(NButton, { size: 'small', type: 'error' }, { default: () => '删除' }),
          default: () => '确认删除？'
        })
      ]
    }
  }
]

function showDetail(row) {
  detailData.value = { ...row }
  detailDrawerVisible.value = true
}

onMounted(() => {
  $table.value?.handleSearch()
})
</script>

<template>
  <NSpace vertical size="small">
    <NCard>
      <NForm inline :model="queryItems">
        <NFormItem label="设备ID">
          <NInput v-model:value="queryItems.device_id" placeholder="设备ID" clearable />
        </NFormItem>
        <NFormItem label="患者ID">
          <NInput v-model:value="queryItems.patient_id" placeholder="患者ID" clearable />
        </NFormItem>
        <NFormItem label="类型">
          <NSelect v-model:value="queryItems.data_type" :options="dataTypeOptions" clearable placeholder="类型" />
        </NFormItem>
        <NFormItem label="时间">
          <NDatePicker v-model:value="queryItems.timeRange" type="datetimerange" clearable placeholder="时间范围" />
        </NFormItem>
        <NFormItem>
          <NButton type="primary" @click="$table.value?.handleSearch()">查询</NButton>
        </NFormItem>
      </NForm>
    </NCard>
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getHealthDataList"
    />
    <NDrawer v-model:show="detailDrawerVisible" placement="right" :width="400">
      <NDrawerContent>
        <template #header>数据详情</template>
        <NDescriptions :column="1" bordered>
          <NDescriptionsItem label="设备">
            {{ detailData.device?.name || detailData.device_id || '-' }}
          </NDescriptionsItem>
          <NDescriptionsItem label="患者">
            {{ detailData.patient?.name || detailData.patient_name || detailData.patient_id || '-' }}
          </NDescriptionsItem>
          <NDescriptionsItem label="分类">{{ detailData.category }}</NDescriptionsItem>
          <NDescriptionsItem label="分区">{{ detailData.partition }}</NDescriptionsItem>
          <NDescriptionsItem label="归档">{{ detailData.archived ? '是' : '否' }}</NDescriptionsItem>
          <NDescriptionsItem label="过期时间">{{ detailData.expires_at ? detailData.expires_at : '-' }}</NDescriptionsItem>
          <NDescriptionsItem label="载荷">
            <span v-if="detailData.payload">
              {{ JSON.stringify(detailData.payload, null, 2).slice(0, 200) }}<span v-if="JSON.stringify(detailData.payload).length > 200">...</span>
            </span>
            <span v-else>-</span>
          </NDescriptionsItem>
        </NDescriptions>
      </NDrawerContent>
    </NDrawer>
  </NSpace>
</template>
