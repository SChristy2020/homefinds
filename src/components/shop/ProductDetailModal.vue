<template>
  <BaseModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)">
    <h2 class="modal-title">{{ i18n.t('productDetail.title') }}</h2>
    <div class="detail-body">
      <div class="detail-img"></div>
      <div class="detail-right">
        <div class="detail-meta">
          <p><strong>{{ product.name }}</strong></p>
          <p>{{ i18n.t('productDetail.originalPrice') }}{{ product.originalPrice || product.price }}</p>
          <p>{{ i18n.t('productDetail.listedOn') }}{{ product.date }}</p>
        </div>
        <div class="detail-price-row">
          <span class="detail-price">${{ product.price }}</span>
          <button
            class="btn-primary"
            style="font-size:0.82rem; padding:7px 16px;"
            :disabled="cart.has(product.id) || product.soldOut"
            @click="handleAddToCart"
          >
            {{ cart.has(product.id) ? i18n.t('productDetail.added') : i18n.t('productDetail.addCart') }}
          </button>
        </div>
      </div>
    </div>

    <div class="waiting-section">
      <div class="waiting-title">{{ i18n.t('productDetail.waitingList') }}</div>
      <div class="waiting-note">{{ i18n.t('productDetail.waitingNote') }}</div>
      <template v-if="waitingList.length === 0">
        <p class="text-sm text-muted">{{ i18n.t('productDetail.noWaiting') }}</p>
      </template>
      <div v-for="(entry, i) in waitingList" :key="i" class="waiting-item">
        {{ i + 1 }}. {{ entry.lastName }} &nbsp; {{ entry.phone }} &nbsp; {{ maskEmail(entry.email) }}
      </div>
    </div>
  </BaseModal>
</template>

<script setup>
import { computed } from 'vue'
import BaseModal from '@/components/shared/BaseModal.vue'
import { useCartStore } from '@/stores/cart'
import { useOrdersStore } from '@/stores/orders'
import { useToastStore } from '@/stores/toast'
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({ modelValue: Boolean, product: Object })
defineEmits(['update:modelValue'])

const cart = useCartStore()
const ordersStore = useOrdersStore()
const toast = useToastStore()
const i18n = useI18nStore()

const waitingList = computed(() => ordersStore.getWaitingList(props.product?.id))

function handleAddToCart() {
  cart.add(props.product)
  toast.show(i18n.t('productDetail.addedToast', { name: props.product.name }))
}

function maskEmail(email) {
  if (!email) return ''
  const [local, domain] = email.split('@')
  return local.slice(0, 3) + 'xxxxx@' + (domain || 'xxx.xxx.xx')
}
</script>

<style scoped>
.modal-title {
  font-family: var(--font-display);
  font-size: 1.25rem; font-weight: 600;
  margin-bottom: 20px;
}
.detail-body { display: flex; gap: 20px; margin-bottom: 20px; }
.detail-img {
  width: 120px; height: 120px; flex-shrink: 0;
  background: linear-gradient(135deg, #2a2a2a 0%, #4a4040 100%);
  border-radius: var(--radius);
}
.detail-meta { font-size: 0.82rem; color: var(--mid); }
.detail-meta p { margin-bottom: 3px; }
.detail-price-row { display: flex; align-items: center; gap: 10px; margin-top: 12px; }
.detail-price { font-size: 1.5rem; font-weight: 700; color: var(--charcoal); }
.waiting-section { margin-top: 16px; padding-top: 16px; border-top: 1.5px solid var(--border); }
.waiting-title { font-size: 0.85rem; font-weight: 600; margin-bottom: 4px; }
.waiting-note  { font-size: 0.75rem; color: var(--mid); font-style: italic; margin-bottom: 8px; }
.waiting-item  { font-size: 0.78rem; color: var(--mid); padding: 3px 0; }
</style>
