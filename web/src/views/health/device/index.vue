<script setup>
import { ref, h, onMounted } from 'vue'
import { NCard, NSpace, NForm, NFormItem, NInput, NButton, NSelect, NModal, NDescriptions, NDescriptionsItem, NTag, NDropdown, NStatistic, NGrid, NGridItem, NSwitch } from 'naive-ui'
import CrudTable from '@/components/table/CrudTable.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'
import { useCRUD } from '@/composables'

const $table = ref(null)
const queryItems = ref({})
const statistics = ref({
  total: 0,
  bound: 0,
  unbound: 0,
  status_online: 0,
  status_offline: 0
})

const detailModalVisible = ref(false)
const detailDevice = ref({})
const actionModalVisible = ref(false)
const actionType = ref('')
const actionTarget = ref(null)
const bindModalVisible = ref(false)
const patientOptions = ref([])
const selectedPatientId = ref(null)

const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd
} = useCRUD({
  name: '设备',
  initForm: {},
  doCreate: api.createDevice,
  doUpdate: (id, data) => api.updateDevice(id, data),
  doDelete: (id) => api.deleteDevice(id),
  refresh: () => $table.value?.handleSearch()
})

const columns = [
  { title: '设备ID', key: 'device_id', align: 'center' },
  { title: '名称', key: 'name', align: 'center' },
  { title: '状态', key: 'status', align: 'center', render: row => h(NTag, { type: row.status === 'online' ? 'success' : 'error' }, () => row.status === 'online' ? '在线' : '离线') },
  { title: '绑定用户', key: 'current_patient_id', align: 'center', render: row => row.current_patient_id ? h(NTag, { type: 'info' }, () => row.current_patient_name || row.current_patient_id) : '-' },
  {
    title: '操作',
    key: 'actions',
    align: 'center',
    fixed: 'right',
    width: 220,
    render: row => {
      const menuOptions = [
        ...(row.current_patient_id
          ? [{ label: '解绑用户', key: 'unbind' }]
          : [{ label: '绑定用户', key: 'bind' }]
        ),
        { label: '删除设备', key: 'delete' }
      ]
      return h(NSpace, { size: 16 }, () => [
        h(NButton, { size: 'small', type: 'primary', onClick: () => showDetail(row) }, { default: () => '详情' }),
        h(NDropdown, {
          options: menuOptions,
          trigger: 'click',
          onSelect: key => handleAction(key, row)
        }, {
          default: () => h(NButton, { size: 'small', type: 'default' }, { default: () => '绑定/解绑/更多' })
        })
      ])
    }
  }
]

function showDetail(row) {
  detailDevice.value = { ...row }
  detailModalVisible.value = true
}

function handleAction(type, row) {
  actionType.value = type
  actionTarget.value = row
  if (type === 'bind') {
    fetchPatientOptions()
    selectedPatientId.value = null
    bindModalVisible.value = true
  } else {
    actionModalVisible.value = true
  }
}

async function confirmAction() {
  if (actionType.value === 'unbind') {
    // 解绑设备与用户，使用后端新接口
    if (actionTarget.value.current_patient_name) {
      await api.unbindDeviceByUsername(actionTarget.value.current_patient_name, actionTarget.value.device_id)
    }
    actionTarget.value.current_patient_id = null
    actionTarget.value.current_patient_name = null
    $table.value?.handleSearch()
  } else if (actionType.value === 'delete') {
    await handleDelete(actionTarget.value.id)
  }
  actionModalVisible.value = false
}

async function fetchPatientOptions() {
  try {
    const res = await api.getPatientList({ page: 1, page_size: 9999 })
    patientOptions.value = res.data?.map(p => ({
      label: `${p.name} (${p.patient_id})`,
      value: p.id
    })) || []
  } catch (e) {}
}

async function confirmBind() {
  if (!actionTarget.value || !selectedPatientId.value) return
  // 设备绑定用户，直接更新设备 current_patient_id 字段
  await api.updateDevice(actionTarget.value.id, { current_patient_id: selectedPatientId.value })
  bindModalVisible.value = false
  $table.value?.handleSearch()
}

async function fetchStatistics() {
  try {
    const res = await api.getDeviceStatistics()
    // 兼容后端聚合结构
    statistics.value.total = res.total || 0
    statistics.value.bound = res.bound || 0
    statistics.value.unbound = res.unbound || 0
    statistics.value.status_online = (res.status_stat && res.status_stat.online) || 0
    statistics.value.status_offline = (res.status_stat && res.status_stat.offline) || 0
  } catch (e) {}
}

onMounted(() => {
  $table.value?.handleSearch()
  fetchStatistics()
})
</script>

<template>
  <NSpace vertical size="small">
    <NCard>
      <NGrid :cols="5" :x-gap="8">
        <NGridItem>
          <NStatistic label="设备总数" :value="statistics.total">
            <template #prefix><TheIcon icon="mdi:devices" /></template>
          </NStatistic>
        </NGridItem>
        <NGridItem>
          <NStatistic label="已绑定" :value="statistics.bound">
            <template #prefix><TheIcon icon="mdi:link-variant" /></template>
          </NStatistic>
        </NGridItem>
        <NGridItem>
          <NStatistic label="未绑定" :value="statistics.unbound">
            <template #prefix><TheIcon icon="mdi:link-off" /></template>
          </NStatistic>
        </NGridItem>
        <NGridItem>
          <NStatistic label="在线" :value="statistics.status_online">
            <template #prefix><TheIcon icon="mdi:check-circle" /></template>
          </NStatistic>
        </NGridItem>
        <NGridItem>
          <NStatistic label="离线" :value="statistics.status_offline">
            <template #prefix><TheIcon icon="mdi:close-circle" /></template>
          </NStatistic>
        </NGridItem>
      </NGrid>
    </NCard>
    <NCard>
      <NForm inline :model="queryItems">
        <NFormItem label="设备ID">
          <NInput v-model:value="queryItems.device_id" placeholder="设备ID" clearable />
        </NFormItem>
        <NFormItem label="名称">
          <NInput v-model:value="queryItems.name" placeholder="设备名称" clearable />
        </NFormItem>
        <NFormItem label="状态">
          <NSelect v-model:value="queryItems.status" :options="[{ label: '全部', value: '' }, { label: '在线', value: 'online' }, { label: '离线', value: 'offline' }]" clearable placeholder="状态" style="min-width: 120px;" />
        </NFormItem>
        <NFormItem>
          <NButton type="primary" @click="$table.value?.handleSearch()">查询</NButton>
        </NFormItem>
        <NFormItem>
          <NButton type="primary" @click="handleAdd">新建设备</NButton>
        </NFormItem>
      </NForm>
    </NCard>
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getDeviceList"
    />
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm ref="modalFormRef" :model="modalForm" label-placement="left" :label-width="80">
        <NFormItem label="设备ID" required>
          <NInput v-model:value="modalForm.device_id" placeholder="请输入设备ID" />
        </NFormItem>
        <NFormItem label="名称" required>
          <NInput v-model:value="modalForm.name" placeholder="请输入设备名称" />
        </NFormItem>
        <NFormItem label="描述">
          <NInput v-model:value="modalForm.description" type="textarea" placeholder="请输入设备描述" />
        </NFormItem>
      </NForm>
    </CrudModal>
    <NModal v-model:show="detailModalVisible" title="设备详情" preset="dialog" :style="{ width: '400px' }">
      <NDescriptions :column="1" bordered>
        <NDescriptionsItem label="设备ID">{{ detailDevice.device_id }}</NDescriptionsItem>
        <NDescriptionsItem label="名称">{{ detailDevice.name }}</NDescriptionsItem>
        <NDescriptionsItem label="型号">{{ detailDevice.model || '-' }}</NDescriptionsItem>
        <NDescriptionsItem label="类型">{{ detailDevice.device_type || '-' }}</NDescriptionsItem>
        <NDescriptionsItem label="分组ID">{{ detailDevice.group_id || '-' }}</NDescriptionsItem>
        <NDescriptionsItem label="标签">
          <span v-if="Array.isArray(detailDevice.tags)">{{ detailDevice.tags.join(', ') }}</span>
          <span v-else>-</span>
        </NDescriptionsItem>
        <NDescriptionsItem label="数据类型">
          <span v-if="Array.isArray(detailDevice.data_types)">{{ detailDevice.data_types.join(', ') }}</span>
          <span v-else>-</span>
        </NDescriptionsItem>
        <NDescriptionsItem label="配置">
          <span v-if="detailDevice.config">{{ JSON.stringify(detailDevice.config) }}</span>
          <span v-else>-</span>
        </NDescriptionsItem>
        <NDescriptionsItem label="状态">
          <NTag :type="detailDevice.status === 'online' ? 'success' : 'error'">
            {{ detailDevice.status === 'online' ? '在线' : '离线' }}
          </NTag>
        </NDescriptionsItem>
        <NDescriptionsItem label="绑定用户">
          {{ detailDevice.current_patient_name || detailDevice.current_patient_id || '-' }}
        </NDescriptionsItem>
        <NDescriptionsItem label="创建时间">
          {{ detailDevice.created_at ? new Date(detailDevice.created_at).toLocaleString() : '-' }}
        </NDescriptionsItem>
        <NDescriptionsItem label="描述">
          {{ detailDevice.description || '-' }}
        </NDescriptionsItem>
      </NDescriptions>
    </NModal>
    <NModal v-model:show="actionModalVisible" :title="actionType === 'unbind' ? '解绑用户' : '删除设备'" preset="dialog" :style="{ width: '320px' }">
      <NSpace vertical>
        <div v-if="actionType === 'unbind'">确认解绑该设备与用户？</div>
        <div v-else-if="actionType === 'delete'">确认删除该设备？</div>
        <NSpace justify="end">
          <NButton @click="actionModalVisible = false">取消</NButton>
          <NButton type="primary" @click="confirmAction">确认</NButton>
        </NSpace>
      </NSpace>
    </NModal>
    <NModal v-model:show="bindModalVisible" title="绑定用户" preset="dialog" :style="{ width: '320px' }">
      <NSpace vertical>
        <NForm label-placement="left" :label-width="80">
          <NFormItem label="选择用户" required>
            <NSelect
              v-model:value="selectedPatientId"
              :options="patientOptions"
              placeholder="请选择要绑定的用户"
              filterable
            />
          </NFormItem>
        </NForm>
        <NSpace justify="end">
          <NButton @click="bindModalVisible = false">取消</NButton>
          <NButton type="primary" @click="confirmBind">绑定</NButton>
        </NSpace>
      </NSpace>
    </NModal>
  </NSpace>
</template>

