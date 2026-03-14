<template>
  <div>
    <!-- Lookup form -->
    <div v-if="!userStore.currentUser" class="orders-lookup">
      <div class="lookup-title">{{ i18n.t('orders.lookupTitle') }}</div>
      <div class="form-group">
        <label>{{ i18n.t('orders.namePlaceholder') }}</label>
        <input v-model="form.name" :placeholder="i18n.t('orders.namePlaceholder')" :class="{ 'input-error': errors.name }" @input="onNameInput" />
        <p v-if="errors.name" class="field-error">{{ errors.name }}</p>
      </div>
      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="your@email.com" :class="{ 'input-error': errors.email }" @input="errors.email = ''" />
        <p v-if="errors.email" class="field-error">{{ errors.email }}</p>
      </div>
      <div class="form-group" style="margin-bottom:16px;">
        <label>Phone</label>
        <input v-model="form.phone" placeholder="(xxx)xxx-xxxx" :class="{ 'input-error': errors.phone }" @input="errors.phone = ''" />
        <p v-if="errors.phone" class="field-error">{{ errors.phone }}</p>
      </div>
      <button class="btn-primary" :disabled="userStore.loading" @click="handleLookup">
        {{ userStore.loading ? '...' : i18n.t('orders.sent') }}
      </button>
      <p v-if="userStore.error" class="error-msg">{{ i18n.t('orders.error') }}</p>
    </div>

    <!-- Logged in -->
    <div v-else>
      <!-- No orders -->
      <div v-if="ordersStore.orders.length === 0" class="no-orders-state">
        <p class="greeting">
          {{ userStore.currentUser.salutation }} {{ userStore.currentUser.last_name }}，{{ i18n.t('orders.noOrders') }}
        </p>
      </div>

      <!-- Orders table -->
      <div v-else class="orders-table-wrap">
        <p class="orders-greeting">
          {{ i18n.t('orders.greeting', { name: userStore.currentUser.first_name }) }}
        </p>

        <!-- DataTable toolbar -->
        <div class="dt-toolbar">
          <div class="dt-info">
            {{ i18n.t('orders.dtShowing', { from: dtFrom, to: dtTo, total: filteredOrders.length }) }}
          </div>
          <input v-model="searchQuery" class="dt-search" :placeholder="i18n.t('orders.dtSearch')" />
        </div>

        <table class="orders-table">
          <thead>
            <tr>
              <th class="sortable" @click="toggleSort('id')">
                {{ i18n.t('orders.orderNo') }}<SortIcon col="id" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th class="sortable" @click="toggleSort('items')">
                {{ i18n.t('orders.itemCount') }}<SortIcon col="items" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th class="sortable" @click="toggleSort('total')">
                {{ i18n.t('orders.orderTotal') }}<SortIcon col="total" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th class="sortable" @click="toggleSort('paid')">
                {{ i18n.t('orders.payStatus') }}<SortIcon col="paid" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th class="sortable" @click="toggleSort('pickup')">
                {{ i18n.t('orders.pickupTimeLabel') }}<SortIcon col="pickup" :active="sortColumn" :dir="sortDirection" />
              </th>
              <th class="sortable" @click="toggleSort('created')">
                {{ i18n.t('orders.createdAt') }}<SortIcon col="created" :active="sortColumn" :dir="sortDirection" />
              </th>
            </tr>
          </thead>
          <tbody v-for="order in paginatedOrders" :key="order.id">
            <!-- Order summary row -->
            <tr class="order-row" :class="{ expanded: expandedOrderId === order.id }" @click="toggleExpand(order.id)">
              <td class="td-order-no">{{ formatOrderId(order.id) }}</td>
              <td>{{ activeItemCount(order) }}</td>
              <td>{{ orderTotal(order) }}</td>
              <td :class="order.is_paid ? 'status-paid' : 'status-unpaid'">
                {{ order.is_paid ? i18n.t('orders.paid') : i18n.t('orders.unpaid') }}
              </td>
              <td class="td-pickup">
                <template v-if="editingOrderId !== order.id">
                  <span>{{ formatDate(order.pickup_time) }}</span>
                  <button class="btn-edit-icon" @click.stop="startEditPickup(order)" title="編輯">
                    <Pencil :size="12" />
                  </button>
                </template>
                <template v-else>
                  <div class="pickup-edit-wrap" @click.stop>
                    <PickupDatePicker v-model="editPickupValue" />
                    <div class="pickup-edit-actions">
                      <button class="btn-save-pickup" @click.stop="savePickupTime(order)">{{ i18n.t('orders.savePickup') }}</button>
                      <button class="btn-cancel-pickup" @click.stop="cancelEditPickup">{{ i18n.t('orders.cancelPickupEdit') }}</button>
                    </div>
                  </div>
                </template>
              </td>
              <td class="td-created">{{ formatDateTime(order.created_at) }}</td>
            </tr>

            <!-- Expanded items row -->
            <tr v-if="expandedOrderId === order.id" class="expand-row">
              <td colspan="6">
                <OrderItemList :items="order.items.filter(i => i.status !== 'cancelled')" @cancel="handleCancel" />

                <!-- Total summary -->
                <div class="order-summary">
                  <span class="summary-label">
                    {{ i18n.t('cart.itemCountPrefix') }} {{ activeItemCount(order) }} {{ i18n.t('cart.itemCountSuffix') }}
                  </span>
                  <span class="summary-price">
                    <span v-if="hasDiscount(order)" class="strikethrough">${{ orderOriginalTotal(order) }}</span>
                    ${{ orderTotal(order) }}
                  </span>
                </div>

                <!-- Not-first warning -->
                <p v-if="hasNotFirstPosition(order)" class="not-first-warning">
                  {{ i18n.t('orderSuccess.notFirstWarning') }}
                </p>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="dt-pagination">
          <button class="dt-page-btn" :disabled="currentPage === 1" @click="currentPage = 1">«</button>
          <button class="dt-page-btn" :disabled="currentPage === 1" @click="currentPage--">‹</button>
          <button
            v-for="p in pageNumbers"
            :key="p"
            class="dt-page-btn"
            :class="{ active: p === currentPage }"
            @click="currentPage = p"
          >{{ p }}</button>
          <button class="dt-page-btn" :disabled="currentPage === totalPages" @click="currentPage++">›</button>
          <button class="dt-page-btn" :disabled="currentPage === totalPages" @click="currentPage = totalPages">»</button>
        </div>
      </div>

      <!-- 購物須知 -->
      <div class="shopping-guide-wrap">
        <ShoppingGuideContent />
      </div>

      <button class="btn-outline mt-16 back-btn" @click="reset">
        <ArrowLeft :size="14" />{{ i18n.t('orders.back') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ArrowLeft, Pencil, ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-vue-next'
import { useOrdersStore } from '@/stores/orders'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { useI18nStore } from '@/stores/i18n'
import OrderItemList from '@/components/orders/OrderItemList.vue'
import ShoppingGuideContent from '@/components/shared/ShoppingGuideContent.vue'
import PickupDatePicker from '@/components/shared/PickupDatePicker.vue'

const ordersStore = useOrdersStore()
const userStore = useUserStore()
const toast = useToastStore()
const i18n = useI18nStore()

const form = ref({ name: '', email: '', phone: '' })
const errors = ref({ name: '', email: '', phone: '' })

const expandedOrderId = ref(null)

// ── DataTable state ───────────────────────────────────────────────────────────
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 10
const sortColumn = ref('id')
const sortDirection = ref('desc')

const filteredOrders = computed(() => {
  let orders = ordersStore.orders
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    orders = orders.filter(o =>
      formatOrderId(o.id).toLowerCase().includes(q) ||
      (o.is_paid ? i18n.t('orders.paid') : i18n.t('orders.unpaid')).toLowerCase().includes(q)
    )
  }
  return [...orders].sort((a, b) => {
    let aVal, bVal
    if (sortColumn.value === 'id')     { aVal = a.id; bVal = b.id }
    else if (sortColumn.value === 'items')  { aVal = activeItemCount(a); bVal = activeItemCount(b) }
    else if (sortColumn.value === 'total')  { aVal = parseFloat(orderTotal(a)); bVal = parseFloat(orderTotal(b)) }
    else if (sortColumn.value === 'paid')   { aVal = a.is_paid ? 1 : 0; bVal = b.is_paid ? 1 : 0 }
    else if (sortColumn.value === 'pickup') { aVal = a.pickup_time || ''; bVal = b.pickup_time || '' }
    else if (sortColumn.value === 'created') { aVal = a.created_at || ''; bVal = b.created_at || '' }
    else { aVal = a.id; bVal = b.id }
    if (aVal < bVal) return sortDirection.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortDirection.value === 'asc' ? 1 : -1
    return 0
  })
})

const totalPages = computed(() => Math.ceil(filteredOrders.value.length / pageSize))
const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredOrders.value.slice(start, start + pageSize)
})
const dtFrom = computed(() => filteredOrders.value.length === 0 ? 0 : (currentPage.value - 1) * pageSize + 1)
const dtTo = computed(() => Math.min(currentPage.value * pageSize, filteredOrders.value.length))
const pageNumbers = computed(() => {
  const total = totalPages.value
  const cur = currentPage.value
  const delta = 2
  const range = []
  for (let i = Math.max(1, cur - delta); i <= Math.min(total, cur + delta); i++) range.push(i)
  return range
})

watch(searchQuery, () => { currentPage.value = 1 })

function toggleSort(col) {
  if (sortColumn.value === col) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = col
    sortDirection.value = 'asc'
  }
  currentPage.value = 1
}

// Sort icon inline component
const SortIcon = {
  props: ['col', 'active', 'dir'],
  components: { ChevronUp, ChevronDown, ChevronsUpDown },
  template: `
    <span class="sort-icon">
      <ChevronUp v-if="active === col && dir === 'asc'" :size="12" />
      <ChevronDown v-else-if="active === col && dir === 'desc'" :size="12" />
      <ChevronsUpDown v-else :size="12" />
    </span>
  `
}

onMounted(async () => {
  if (userStore.currentUser && ordersStore.orders.length === 0) {
    await ordersStore.fetchOrdersByUser(userStore.currentUser.id)
  }
})
const editingOrderId = ref(null)
const editPickupValue = ref('')

function onNameInput() {
  form.value.name = form.value.name.replace(/[^a-zA-Z\u4e00-\u9fff\u3400-\u4dbf\s'-]/g, '')
  errors.value.name = ''
}

function validate() {
  errors.value = { name: '', email: '', phone: '' }
  if (!form.value.name.trim()) {
    errors.value.name = i18n.t('orders.invalidName')
  }
  const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRe.test(form.value.email)) {
    errors.value.email = i18n.t('orders.invalidEmail')
  }
  const phoneRe = /^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$/
  if (!phoneRe.test(form.value.phone.trim())) {
    errors.value.phone = i18n.t('orders.invalidPhone')
  }
  return !errors.value.name && !errors.value.email && !errors.value.phone
}

async function handleLookup() {
  if (!validate()) return
  const user = await userStore.lookup(form.value.name, form.value.email, form.value.phone)
  if (user) {
    await ordersStore.fetchOrdersByUser(user.id)
  }
}

function toggleExpand(orderId) {
  expandedOrderId.value = expandedOrderId.value === orderId ? null : orderId
  if (editingOrderId.value && editingOrderId.value !== orderId) {
    editingOrderId.value = null
  }
}

function startEditPickup(order) {
  editingOrderId.value = order.id
  editPickupValue.value = toPickerFormat(order.pickup_time)
}

function cancelEditPickup() {
  editingOrderId.value = null
  editPickupValue.value = ''
}

async function savePickupTime(order) {
  const isoStr = fromPickerFormat(editPickupValue.value)
  await ordersStore.updatePickupTime(order.id, isoStr)
  toast.show(i18n.t('orders.savePickupToast'))
  editingOrderId.value = null
}

async function handleCancel(itemId) {
  await ordersStore.cancelOrderItem(itemId)
  toast.show(i18n.t('orders.cancelToast'))
}

function reset() {
  ordersStore.clearOrders()
  expandedOrderId.value = null
  editingOrderId.value = null
  userStore.logout()
  form.value = { name: '', email: '', phone: '' }
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function formatOrderId(id) {
  return 'S' + String(id).padStart(6, '0')
}

function activeItemCount(order) {
  return order.items.filter(i => i.status !== 'cancelled').length
}

function orderTotal(order) {
  return order.items
    .filter(i => i.status !== 'cancelled')
    .reduce((s, i) => s + i.price, 0)
    .toFixed(2)
    .replace(/\.00$/, '')
}

function orderOriginalTotal(order) {
  return order.items
    .filter(i => i.status !== 'cancelled')
    .reduce((s, i) => s + (i.original_price || i.price), 0)
    .toFixed(2)
    .replace(/\.00$/, '')
}

function hasDiscount(order) {
  return order.items.some(i => i.status !== 'cancelled' && i.original_price && i.original_price > i.price)
}

function hasNotFirstPosition(order) {
  return order.items.some(i => i.status !== 'cancelled' && i.waiting_position > 1)
}

function formatDate(isoStr) {
  if (!isoStr) return '—'
  const d = new Date(isoStr)
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`
}

function formatDateTime(isoStr) {
  if (!isoStr) return '—'
  const d = new Date(isoStr)
  const date = `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`
  const time = `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
  return `${date} ${time}`
}

function toPickerFormat(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const year = d.getFullYear()
  const hour = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${month}/${day}/${year} ${hour}:${min}`
}

function fromPickerFormat(str) {
  if (!str) return null
  const parts = str.match(/(\d+)\/(\d+)\/(\d+)\s+(\d+):(\d+)/)
  if (!parts) return null
  return new Date(+parts[3], +parts[1] - 1, +parts[2], +parts[4], +parts[5]).toISOString()
}
</script>

<style scoped>
/* ── Lookup form ─────────────────────────────────────────────────────────── */
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
.field-error {
  margin-top: 4px; font-size: 0.75rem; color: var(--red); text-align: left;
}
.input-error { border-color: var(--red) !important; }

/* ── No orders ───────────────────────────────────────────────────────────── */
.no-orders-state {
  text-align: center; padding: 60px 20px; color: var(--mid);
}
.greeting { font-size: 1rem; }

/* ── Orders greeting ─────────────────────────────────────────────────────── */
.orders-greeting {
  font-size: 1rem; font-weight: 600;
  color: var(--charcoal);
  margin-bottom: 16px;
}

/* ── Orders table ────────────────────────────────────────────────────────── */
.orders-table-wrap {
  width: 100%; overflow-x: auto;
}
.orders-table {
  width: 100%; border-collapse: collapse;
  font-size: 0.88rem;
}
.orders-table thead tr {
  border-bottom: 2px solid var(--border);
}
.orders-table th {
  text-align: left; padding: 8px 12px;
  font-size: 0.82rem; font-weight: 600; color: var(--mid);
  white-space: nowrap;
}
.order-row {
  cursor: pointer; border-bottom: 1px solid var(--border);
  transition: background 0.15s;
}
.order-row:hover { background: var(--warm-white); }
.order-row.expanded {
  background: #edf4f4;
  border-bottom: none;
  font-weight: 600;
}
.orders-table td {
  padding: 10px 12px; vertical-align: middle;
}
.td-order-no { font-weight: 600; color: var(--charcoal); }

/* Payment status */
.status-paid   { color: #2e7d32; font-weight: 600; }
.status-unpaid { color: var(--mid); }

/* Pickup time cell */
.td-pickup { white-space: nowrap; }
.td-created { white-space: nowrap; color: var(--mid); font-size: 0.82rem; }
.btn-edit-icon {
  background: none; border: none; cursor: pointer;
  color: var(--accent); padding: 2px 4px; margin-left: 4px;
  border-radius: 3px; vertical-align: middle;
  transition: opacity 0.15s;
}
.btn-edit-icon:hover { opacity: 0.7; }

/* Inline pickup edit */
.pickup-edit-wrap {
  display: flex; flex-direction: column; gap: 6px; min-width: 220px;
}
.pickup-edit-actions {
  display: flex; gap: 6px;
}
.btn-save-pickup {
  padding: 4px 12px; background: var(--charcoal); color: #fff;
  border: none; border-radius: var(--radius); font-size: 0.78rem;
  cursor: pointer; transition: opacity 0.15s;
}
.btn-save-pickup:hover { opacity: 0.8; }
.btn-cancel-pickup {
  padding: 4px 10px; background: none; color: var(--mid);
  border: 1px solid var(--border); border-radius: var(--radius);
  font-size: 0.78rem; cursor: pointer;
}
.btn-cancel-pickup:hover { border-color: var(--charcoal); color: var(--charcoal); }

/* ── Expand row ──────────────────────────────────────────────────────────── */
.expand-row > td {
  padding: 0;
  background: #fff;
  border-top: 1px solid var(--border);    
  border-top: 1.5px solid #858585;
  border-bottom: 1.5px solid #858585;
}

/* ── Order summary ───────────────────────────────────────────────────────── */
.order-summary {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; border-top: 1px solid var(--border);
  font-size: 0.88rem; font-weight: 600;
}
.summary-price { display: flex; align-items: center; gap: 6px; }
.strikethrough {
  text-decoration: line-through; color: var(--mid); font-weight: 400;
  font-size: 0.82rem;
}
.not-first-warning {
  margin: 0; padding: 8px 16px 12px;
  color: var(--red, #c0392b); font-size: 0.8rem; font-weight: 600;
}

/* ── Shopping guide ──────────────────────────────────────────────────────── */
.shopping-guide-wrap {
  width: 100%; margin-top: 24px;
  border-top: 1.5px solid var(--border); padding-top: 20px;
}

/* ── Back button ─────────────────────────────────────────────────────────── */
.back-btn { display: inline-flex; align-items: center; gap: 5px; }
.mt-16 { margin-top: 16px; }

/* ── DataTable toolbar ───────────────────────────────────────────────────── */
.dt-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px; gap: 12px; flex-wrap: wrap;
}
.dt-info {
  font-size: 0.78rem; color: var(--mid);
}
.dt-search {
  padding: 5px 10px; border: 1px solid var(--border); border-radius: var(--radius);
  font-size: 0.82rem; color: var(--charcoal); background: #fff;
  outline: none; min-width: 180px;
}
.dt-search:focus { border-color: var(--charcoal); }

/* ── Sortable headers ────────────────────────────────────────────────────── */
.orders-table th.sortable {
  cursor: pointer; user-select: none;
}
.orders-table th.sortable:hover { color: var(--charcoal); }
.sort-icon {
  display: inline-flex; vertical-align: middle;
  margin-left: 3px; opacity: 0.6;
}

/* ── Pagination ──────────────────────────────────────────────────────────── */
.dt-pagination {
  display: flex; align-items: center; justify-content: flex-end;
  gap: 4px; margin-top: 12px; flex-wrap: wrap;
}
.dt-page-btn {
  padding: 4px 10px; border: 1px solid var(--border); border-radius: var(--radius);
  background: #fff; font-size: 0.8rem; color: var(--charcoal);
  cursor: pointer; transition: background 0.12s, border-color 0.12s;
  min-width: 32px; text-align: center;
}
.dt-page-btn:hover:not(:disabled):not(.active) { border-color: var(--charcoal); }
.dt-page-btn.active {
  background: var(--charcoal); color: #fff; border-color: var(--charcoal);
}
.dt-page-btn:disabled { opacity: 0.35; cursor: default; }
</style>
