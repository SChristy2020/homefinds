import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/utils/api'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function lookup(lastName, email, phone) {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams({ last_name: lastName, email, phone })
      const user = await api.get(`/api/users/lookup?${params}`)
      currentUser.value = user
      return user
    } catch (err) {
      error.value = err.detail || '查無此用戶'
      currentUser.value = null
      return null
    } finally {
      loading.value = false
    }
  }

  function logout() {
    currentUser.value = null
    error.value = null
  }

  return { currentUser, loading, error, lookup, logout }
})
