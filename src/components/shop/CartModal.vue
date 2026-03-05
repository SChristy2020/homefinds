<template>
  <BaseModal :modelValue="modelValue" size="lg" @update:modelValue="$emit('update:modelValue', $event)">
    <h2 class="modal-title">My Cart</h2>

    <div v-if="cart.items.length === 0" class="empty-state">
      <div class="empty-state-icon">🛒</div>
      <p>購物車是空的</p>
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
          <button class="btn-outline" style="font-size:0.72rem;padding:3px 10px;" @click="cart.remove(item.id)">Cancel</button>
        </div>
      </div>

      <div class="section-divider"></div>

      <!-- Checkout Form -->
      <div class="form-row">
        <div class="form-group">
          <label>First Name</label>
          <input v-model="form.firstName" placeholder="First Name" />
        </div>
        <div class="form-group">
          <label>Last Name</label>
          <input v-model="form.lastName" placeholder="Last Name" />
        </div>
      </div>
      <div class="form-group">
        <label>稱呼</label>
        <div class="radio-group">
          <label><input type="radio" v-model="form.salutation" value="Mr." /> Mr.</label>
          <label><input type="radio" v-model="form.salutation" value="Miss" /> Miss</label>
        </div>
      </div>
      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="your@email.com" />
      </div>
      <div class="form-group">
        <label>Phone</label>
        <input v-model="form.phone" placeholder="(xxx)xxx-xxxx" />
      </div>

      <div class="total-row">
        <span class="total-label">Total: ${{ cart.total }}</span>
        <button class="btn-primary" :disabled="!isValid" @click="handleConfirm">Confirm</button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import BaseModal from '@/components/shared/BaseModal.vue'
import { useCartStore } from '@/stores/cart'
import { useOrdersStore } from '@/stores/orders'

defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue'])

const cart = useCartStore()
const ordersStore = useOrdersStore()
const onOrderSuccess = inject('onOrderSuccess')

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
