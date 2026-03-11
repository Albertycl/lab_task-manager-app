<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>Task Manager</q-toolbar-title>
        <q-badge color="green" class="q-mr-sm">{{ backendVersion }}</q-badge>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

export default {
  name: 'MainLayout',
  setup () {
    const backendVersion = ref('...')

    onMounted(async () => {
      try {
        const { data } = await api.get('/health')
        backendVersion.value = data.version
      } catch {
        backendVersion.value = 'offline'
      }
    })

    return { backendVersion }
  }
}
</script>
