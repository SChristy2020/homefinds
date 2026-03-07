<template>
  <div>
    <!-- Lookup form -->
    <div v-if="!userStore.currentUser" class="orders-lookup">
      <div class="lookup-title">{{ i18n.t('orders.lookupTitle') }}</div>
      <div class="form-group">
        <label>{{ i18n.t('orders.namePlaceholder') }}</label>
        <input v-model="form.name" :placeholder="i18n.t('orders.namePlaceholder')" />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="your@email.com" />
      </div>
      <div class="form-group" style="margin-bottom:16px;">
        <label>Phone</label>
        <input v-model="form.phone" placeholder="(xxx)xxx-xxxx" />
      </div>
      <button class="btn-primary" :disabled="userStore.loading" @click="handleLookup">
        {{ userStore.loading ? '...' : i18n.t('orders.sent') }}
      </button>
      <p v-if="userStore.error" class="error-msg">{{ i18n.t('orders.error') }}</p>
    </div>

    <!-- Logged in -->
    <div v-else>
      <template v-if="foundOrder && !foundOrder._noOrders">
        <OrderPickupBanner :order="foundOrder" @notify="handleNotify" />
        <OrderItemList :order="foundOrder" @cancel="handleCancel" />
      </template>

      <div v-else class="no-orders-state">
        <p class="greeting">
          {{ userStore.currentUser.salutation }} {{ userStore.currentUser.last_name }}，{{ i18n.t('orders.noOrders') }}
        </p>
      </div>

      <button class="btn-outline mt-16 back-btn" @click="reset">
        <ArrowLeft :size="14" />{{ i18n.t('orders.back') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ArrowLeft } from 'lucide-vue-next'
import { useOrdersStore } from '@/stores/orders'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { useI18nStore } from '@/stores/i18n'
import OrderPickupBanner from '@/components/orders/OrderPickupBanner.vue'
import OrderItemList from '@/components/orders/OrderItemList.vue'

const ordersStore = useOrdersStore()
const userStore = useUserStore()
const toast = useToastStore()
const i18n = useI18nStore()

const form = ref({ name: '', email: '', phone: '' })
const foundOrder = ref(null)

async function handleLookup() {
  const user = await userStore.lookup(form.value.name, form.value.email, form.value.phone)
  if (user) {
    const result = ordersStore.findOrder(form.value.name, form.value.email, form.value.phone)
    foundOrder.value = result || { _noOrders: true }
  }
}

function handleCancel(productId) {
  ordersStore.cancelItem(foundOrder.value.id, productId)
  toast.show(i18n.t('orders.cancelToast'))
  foundOrder.value = ordersStore.orders.find(o => o.id === foundOrder.value.id) || null
}

function handleNotify() {
  toast.show(i18n.t('orders.notifyToast'))
}

function reset() {
  foundOrder.value = null
  userStore.logout()
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
.back-btn { display: inline-flex; align-items: center; gap: 5px; }
.no-orders-state {
  text-align: center; padding: 60px 20px; color: var(--mid);
}
.greeting { font-size: 1rem; }
</style>
