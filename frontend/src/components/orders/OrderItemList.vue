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
        <tr v-for="(item, index) in items" :key="item.id" class="item-row">
          <!-- 編圖：序號 + 縮圖 -->
          <td class="td-thumb">
            <div class="thumb-wrap">
              <span class="item-index">{{ index + 1 }}</span>
              <img v-if="item.image_url" :src="item.image_url" class="item-img" alt="" />
              <div v-else class="item-img item-img-placeholder"></div>
            </div>
          </td>

          <!-- 物品名稱 -->
          <td class="td-name">{{ item.product_name || '—' }}</td>

          <!-- 可取貨時間 -->
          <td class="td-avail">{{ formatAvailableTime(item.available_time) }}</td>

          <!-- 價錢 -->
          <td class="td-price">
            <span v-if="item.original_price && item.original_price > item.price" class="strikethrough">${{ fmtPrice(item.original_price) }}</span>
            ${{ fmtPrice(item.price) }}
          </td>

          <!-- 目前順位 -->
          <td class="td-position">
            <span class="position-badge">{{ formatPosition(item.waiting_position) }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({ items: Array })
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
  background: #faf9f7;
}
.item-row { border-bottom: 1px solid var(--border); }
.item-row:last-child { border-bottom: none; }
.item-table td { padding: 10px 12px; vertical-align: middle; }

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

/* 可取貨時間 */
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
</style>
