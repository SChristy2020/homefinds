import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/utils/api'

const USER_KEY = 'homefinds_user'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(JSON.parse(sessionStorage.getItem(USER_KEY)) || null)
  const loading = ref(false)
  const error = ref(null)

  async function lookup(lastName, email, phone) {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams({ last_name: lastName, email, phone })
      const user = await api.get(`/api/users/lookup?${params}`)
      currentUser.value = user
      sessionStorage.setItem(USER_KEY, JSON.stringify(user))
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
    sessionStorage.removeItem(USER_KEY)
  }

  return { currentUser, loading, error, lookup, logout }
})
