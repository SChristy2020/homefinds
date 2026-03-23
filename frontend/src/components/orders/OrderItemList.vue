<template>
  <div class="item-table-wrap">
    <table class="item-table">
      <thead>
        <tr>
          <th class="th-no">{{ i18n.t('cart.colThumb') }}</th>
          <th>{{ i18n.t('cart.colName') }}</th>
          <th>{{ i18n.t('cart.colPickup') }}</th>
          <th>{{ i18n.t('cart.colPrice') }}</th>
          <th>{{ i18n.t('orderSuccess.colPosition') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in items" :key="item.id" class="item-row" :class="{ 'item-row-sold': item.status === 'sold' }">
          <!-- 縮圖：序號 + 縮圖 -->
          <td class="td-thumb">
            <div class="thumb-wrap">
              <span class="item-index">{{ index + 1 }}</span>
              <img v-if="item.image_url" :src="item.image_url" class="item-img" alt="" />
              <div v-else class="item-img item-img-placeholder"></div>
            </div>
          </td>

          <!-- 物品名稱 -->
          <td class="td-name">{{ item.product_name || '—' }}</td>

          <!-- 最快取貨日 -->
          <td class="td-avail">{{ formatAvailableTime(item.available_time) }}</td>

          <!-- 價錢 -->
          <td class="td-price">
            <span v-if="item.original_price && item.original_price > item.price" class="strikethrough">${{ fmtPrice(item.original_price) }}</span>
            ${{ fmtPrice(item.price) }}
          </td>

          <!-- 目前順位 -->
          <td class="td-position">
            <template v-if="item.status === 'sold'">
              <span class="position-sold">{{ i18n.t('orders.soldAt') }}</span>
              <span class="position-sold-date">{{ formatSoldAt(item.sold_at) }}</span>
            </template>
            <template v-else-if="item.status === 'paid' && orderStatus === 'paid'">
              <span class="position-purchased">{{ i18n.t('orders.purchaseSuccess') }}</span>
            </template>
            <template v-else>
              <span class="position-badge">{{ formatPosition(item.waiting_position) }}</span>
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({ items: Array, orderStatus: String })
defineEmits(['cancel'])
const i18n = useI18nStore()

function fmtPrice(val) {
  return Number(val).toFixed(2).replace(/\.00$/, '')
}

function formatAvailableTime(isoStr) {
  if (!isoStr) return i18n.t('cart.anytime')
  const d = new Date(isoStr)
  if (d <= new Date()) return i18n.t('cart.anytime')
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`
}

function formatPosition(n) {
  if (!n) return '—'
  return i18n.t('orderSuccess.positionFallback', { n })
}

function formatSoldAt(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getMonth() + 1}/${d.getDate()}/${d.getFullYear()}`
}
</script>

<style scoped>
.item-table-wrap { width: 100%; overflow-x: auto; }

.item-table {
  width: 100%; border-collapse: collapse; font-size: 0.85rem;
}
.item-table th {
  text-align: left; padding: 8px 12px;
  font-size: 0.78rem; font-weight: 600; color: var(--mid);
  border-bottom: 1px solid var(--border); white-space: nowrap;
  background: #ffffff;
}
.item-row { border-bottom: 1px solid var(--border); }
.item-row:last-child { border-bottom: none; }
.item-table td { padding: 10px 12px; vertical-align: middle; }

/* 售出 row */
.item-row-sold { background: #f0f0f0; opacity: 0.75; }

/* 縮圖欄 */
.th-no { width: 80px; }
.thumb-wrap { display: flex; align-items: center; gap: 8px; }
.item-index { font-size: 0.78rem; color: var(--mid); min-width: 14px; }
.item-img {
  width: 48px; height: 48px; object-fit: cover;
  border-radius: 4px; flex-shrink: 0;
}
.item-img-placeholder {
  background: linear-gradient(135deg, #ddd 0%, #ccc 100%);
}

/* 物品名稱 */
.td-name { font-weight: 500; color: var(--charcoal); }

/* 最快取貨日 */
.td-avail { color: var(--mid); font-size: 0.82rem; white-space: nowrap; }

/* 價錢 */
.td-price { white-space: nowrap; font-weight: 600; }
.strikethrough {
  text-decoration: line-through; color: var(--mid);
  font-weight: 400; font-size: 0.78rem; margin-right: 4px;
}

/* 目前順位 */
.td-position { white-space: nowrap; }
.position-badge { color: var(--accent); font-weight: 700; font-size: 0.82rem; }
.position-sold { color: var(--red, #c0392b); font-weight: 700; font-size: 0.82rem; display: block; }
.position-sold-date { color: var(--red, #c0392b); font-size: 0.75rem; }
.position-purchased { color: var(--accent); font-weight: 700; font-size: 0.82rem; }
</style>
