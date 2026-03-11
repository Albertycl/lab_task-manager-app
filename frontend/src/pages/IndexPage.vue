<template>
  <q-page class="q-pa-md" style="max-width: 600px; margin: 0 auto;">
    <div class="text-h5 q-mb-md">My Tasks</div>

    <!-- Add task -->
    <div class="row q-mb-lg">
      <q-input
        v-model="newTask"
        placeholder="Add a new task..."
        outlined
        dense
        class="col"
        @keyup.enter="addTask"
      />
      <q-btn
        color="primary"
        icon="add"
        class="q-ml-sm"
        @click="addTask"
        :disable="!newTask.trim()"
      />
    </div>

    <!-- Task list -->
    <q-list bordered separator v-if="tasks.length">
      <q-item v-for="task in tasks" :key="task.id">
        <q-item-section side>
          <q-checkbox
            :model-value="task.done"
            @update:model-value="toggleTask(task)"
          />
        </q-item-section>
        <q-item-section :class="{ 'text-strike text-grey': task.done }">
          {{ task.title }}
        </q-item-section>
        <q-item-section side>
          <q-btn
            flat
            round
            dense
            icon="delete"
            color="red"
            @click="deleteTask(task.id)"
          />
        </q-item-section>
      </q-item>
    </q-list>

    <div v-else class="text-grey text-center q-pa-lg">
      No tasks yet. Add one above!
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'

export default {
  name: 'IndexPage',
  setup () {
    const $q = useQuasar()
    const tasks = ref([])
    const newTask = ref('')

    const fetchTasks = async () => {
      try {
        const { data } = await api.get('/tasks')
        tasks.value = data
      } catch {
        $q.notify({ type: 'negative', message: 'Failed to load tasks' })
      }
    }

    const addTask = async () => {
      if (!newTask.value.trim()) return
      try {
        await api.post('/tasks', { title: newTask.value.trim() })
        newTask.value = ''
        await fetchTasks()
      } catch {
        $q.notify({ type: 'negative', message: 'Failed to add task' })
      }
    }

    const toggleTask = async (task) => {
      try {
        await api.patch(`/tasks/${task.id}`, { done: !task.done })
        await fetchTasks()
      } catch {
        $q.notify({ type: 'negative', message: 'Failed to update task' })
      }
    }

    const deleteTask = async (id) => {
      try {
        await api.delete(`/tasks/${id}`)
        await fetchTasks()
      } catch {
        $q.notify({ type: 'negative', message: 'Failed to delete task' })
      }
    }

    onMounted(fetchTasks)

    return { tasks, newTask, addTask, toggleTask, deleteTask }
  }
}
</script>
