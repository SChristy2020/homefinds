<template>
  <div>
    <!-- Lookup form -->
    <div v-if="!foundOrder" class="orders-lookup">
      <div class="lookup-title">請輸入以下資訊以確認</div>
      <div class="form-group">
        <label>Name (Last Name)</label>
        <input v-model="form.name" placeholder="Last Name" />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="your@email.com" />
      </div>
      <div class="form-group" style="margin-bottom:16px;">
        <label>Phone</label>
        <input v-model="form.phone" placeholder="(xxx)xxx-xxxx" />
      </div>
      <button class="btn-primary" @click="handleLookup">Sent</button>
      <p v-if="hasError" class="error-msg">找不到相關訂單，請確認資訊是否正確</p>
    </div>

    <!-- Order result -->
    <div v-else>
      <OrderPickupBanner :order="foundOrder" @notify="handleNotify" />
      <OrderItemList :order="foundOrder" @cancel="handleCancel" />
      <button class="btn-outline mt-16" @click="reset">← 返回</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useOrdersStore } from '@/stores/orders'
import { useToastStore } from '@/stores/toast'
import OrderPickupBanner from '@/components/orders/OrderPickupBanner.vue'
import OrderItemList from '@/components/orders/OrderItemList.vue'

const ordersStore = useOrdersStore()
const toast = useToastStore()

const form = ref({ name: '', email: '', phone: '' })
const foundOrder = ref(null)
const hasError = ref(false)

function handleLookup() {
  hasError.value = false
  const result = ordersStore.findOrder(form.value.name, form.value.email, form.value.phone)
  if (result) {
    foundOrder.value = result
  } else {
    hasError.value = true
  }
}

function handleCancel(productId) {
  ordersStore.cancelItem(foundOrder.value.id, productId)
  toast.show('已取消訂單')
  // Refresh reference
  foundOrder.value = ordersStore.orders.find(o => o.id === foundOrder.value.id) || null
}

function handleNotify() {
  toast.show('已通知 Christy!')
}

function reset() {
  foundOrder.value = null
  hasError.value = false
  form.value = { name: '', email: '', phone: '' }
}
</script>

<style scoped>
.orders-lookup {
  max-width: 380px; margin: 40px auto; text-align: center;
}
.lookup-title {
  font-family: var(--font-display);
  font-size: 1.2rem; margin-bottom: 24px;
  color: var(--charcoal);
}
.error-msg {
  margin-top: 10px; font-size: 0.8rem; color: var(--red);
}
</style>
