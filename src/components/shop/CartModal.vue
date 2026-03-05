<template>
  <BaseModal :modelValue="modelValue" size="lg" @update:modelValue="$emit('update:modelValue', $event)">
    <h2 class="modal-title">{{ i18n.t('cart.title') }}</h2>

    <div v-if="cart.items.length === 0" class="empty-state">
      <div class="empty-state-icon"><ShoppingCart :size="40" /></div>
      <p>{{ i18n.t('cart.empty') }}</p>
    </div>

    <template v-else>
      <!-- Cart Items -->
      <div class="cart-items">
        <div v-for="item in cart.items" :key="item.id" class="cart-item-card">
          <div class="cart-item-img"></div>
          <div class="cart-item-price">
            <div v-if="item.originalPrice" class="strikethrough" style="font-size:0.7rem;">${{ item.originalPrice }}</div>
            ${{ item.price }}
          </div>
          <button class="btn-outline" style="font-size:0.72rem;padding:3px 10px;" @click="cart.remove(item.id)">{{ i18n.t('cart.cancel') }}</button>
        </div>
      </div>

      <div class="section-divider"></div>

      <!-- Checkout Form -->
      <UserInfoForm v-model="form" />

      <div class="total-row">
        <span class="total-label">{{ i18n.t('cart.total') }}: ${{ cart.total }}</span>
        <button class="btn-primary" :disabled="!isValid" @click="handleConfirm">{{ i18n.t('cart.confirm') }}</button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { ShoppingCart } from 'lucide-vue-next'
import BaseModal from '@/components/shared/BaseModal.vue'
import UserInfoForm from '@/components/shared/UserInfoForm.vue'
import { useCartStore } from '@/stores/cart'
import { useOrdersStore } from '@/stores/orders'
import { useI18nStore } from '@/stores/i18n'

defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue'])

const cart = useCartStore()
const ordersStore = useOrdersStore()
const onOrderSuccess = inject('onOrderSuccess')
const i18n = useI18nStore()

const form = ref({ firstName: '', lastName: '', salutation: 'Mr.', email: '', phone: '' })

const isValid = computed(() =>
  form.value.firstName && form.value.lastName &&
  form.value.email && form.value.phone &&
  cart.items.length > 0
)

function handleConfirm() {
  if (!isValid.value) return
  const order = ordersStore.addOrder({ ...form.value }, cart.items)
  cart.clear()
  emit('update:modelValue', false)
  onOrderSuccess(order)
  form.value = { firstName: '', lastName: '', salutation: 'Mr.', email: '', phone: '' }
}
</script>

<style scoped>
.modal-title {
  font-family: var(--font-display);
  font-size: 1.25rem; font-weight: 600;
  margin-bottom: 20px;
}
.cart-items { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 4px; }
.cart-item-card {
  border: 1.5px solid var(--border); border-radius: var(--radius);
  padding: 10px; text-align: center; width: 110px;
}
.cart-item-img {
  width: 80px; height: 80px; margin: 0 auto 6px;
  background: linear-gradient(135deg, #2a2a2a 0%, #4a4040 100%);
  border-radius: 3px;
}
.cart-item-price { font-size: 0.85rem; font-weight: 600; margin-bottom: 6px; }
.total-row {
  display: flex; align-items: center; justify-content: space-between;
  margin-top: 16px; padding-top: 14px; border-top: 1.5px solid var(--border);
}
.total-label { font-size: 1.1rem; font-weight: 600; }
</style>
