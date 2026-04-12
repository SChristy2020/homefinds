<template>
  <section class="admin-section analytics-section">
    <h2 class="section-title">數據分析</h2>

    <div v-if="loading" class="analytics-loading">載入中...</div>

    <template v-else>
      <!-- ── Doughnut row ─────────────────────────────────────── -->
      <div class="donut-row">
        <div class="donut-card">
          <div class="donut-label">商品數</div>
          <div class="donut-body">
            <div class="donut-wrap">
              <canvas ref="prodCanvas"></canvas>
              <div class="donut-center">
                <span class="donut-num">{{ data.products.total }}</span>
              </div>
            </div>
            <ul class="donut-legend">
              <li><span class="dot" style="background:#507f70"></span>已售出 {{ data.products.sold }}</li>
              <li><span class="dot" style="background:#89D5C9"></span>未售出 {{ data.products.unsold }}</li>
            </ul>
          </div>
        </div>

        <div class="donut-card">
          <div class="donut-label">Users</div>
          <div class="donut-body">
            <div class="donut-wrap">
              <canvas ref="userCanvas"></canvas>
              <div class="donut-center">
                <span class="donut-num">{{ totalUsers }}</span>
              </div>
            </div>
            <ul class="donut-legend">
              <li v-for="(count, locale) in data.users_by_locale" :key="locale">
                <span class="dot" :style="{ background: localeColor(locale) }"></span>
                {{ locale }} {{ count }}
              </li>
            </ul>
          </div>
        </div>

        <div class="donut-card">
          <div class="donut-label">購物訂單數</div>
          <div class="donut-body">
            <div class="donut-wrap">
              <canvas ref="shopOrderCanvas"></canvas>
              <div class="donut-center">
                <span class="donut-num">{{ totalShopOrders }}</span>
              </div>
            </div>
            <ul class="donut-legend">
              <li v-for="(item, i) in shopOrderLegend" :key="item.label">
                <span class="dot" :style="{ background: item.color }"></span>
                {{ item.label }} {{ item.value }}
              </li>
            </ul>
          </div>
        </div>

        <div class="donut-card">
          <div class="donut-label">租屋訂單數</div>
          <div class="donut-body">
            <div class="donut-wrap">
              <canvas ref="rentOrderCanvas"></canvas>
              <div class="donut-center">
                <span class="donut-num">{{ totalRentOrders }}</span>
              </div>
            </div>
            <ul class="donut-legend">
              <li v-for="item in rentOrderLegend" :key="item.label">
                <span class="dot" :style="{ background: item.color }"></span>
                {{ item.label }} {{ item.value }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- ── Line charts ─────────────────────────────────────── -->
      <div class="line-charts-row">
        <div class="line-card">
          <div class="line-label">購物訂單金額與訂單數</div>
          <canvas ref="shopLineCanvas"></canvas>
        </div>
        <div class="line-card">
          <div class="line-label">租屋訂單金額與訂單數</div>
          <canvas ref="rentLineCanvas"></canvas>
        </div>
      </div>
    </template>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { api } from '@/utils/api'
import {
  Chart,
  ArcElement, DoughnutController,
  LineElement, PointElement, LineController,
  CategoryScale, LinearScale,
  Tooltip, Legend,
} from 'chart.js'

Chart.register(
  ArcElement, DoughnutController,
  LineElement, PointElement, LineController,
  CategoryScale, LinearScale,
  Tooltip, Legend,
)

// ── Canvas refs ──────────────────────────────────────────────
const prodCanvas      = ref(null)
const userCanvas      = ref(null)
const shopOrderCanvas = ref(null)
const rentOrderCanvas = ref(null)
const shopLineCanvas  = ref(null)
const rentLineCanvas  = ref(null)

const loading = ref(true)
const data    = ref(null)

// chart instances for cleanup
const charts = []

// ── Colour palettes ──────────────────────────────────────────
const BG = ['#507f70', '#89D5C9', '#FAC172', '#E25B45']

// 1. 商品（2 段）
const PROD_COLORS = [BG[0], BG[1]]

// 2. 使用者（3 段）
const LOCALE_ORDER  = ['zh-TW', 'zh-CN', 'en']
const LOCALE_COLORS = { 'zh-TW': BG[0], 'zh-CN': BG[1], 'en': BG[2] }
function localeColor(l) { return LOCALE_COLORS[l] || BG[3] }

// 3. 購物訂單（4 段）
const SHOP_STATUS_ORDER  = ['pending_payment', 'paid', 'picked_up', 'cancelled']
const SHOP_STATUS_LABELS = { pending_payment: '待付款', paid: '已付款', picked_up: '已取貨', cancelled: '已取消' }
const SHOP_STATUS_COLORS = [BG[0], BG[1], BG[2], BG[3]]

// 4. 租屋訂單（5 段，循環取色）
const RENT_STATUS_ORDER  = ['待付訂金', '待入住', '已入住', '已退房', '已取消']
const RENT_STATUS_COLORS = [BG[0], BG[1], BG[2], BG[3], BG[0]]

// ── Computed helpers ─────────────────────────────────────────
const totalUsers = computed(() =>
  Object.values(data.value?.users_by_locale ?? {}).reduce((a, b) => a + b, 0)
)
const totalShopOrders = computed(() =>
  Object.values(data.value?.shop_orders_by_status ?? {}).reduce((a, b) => a + b, 0)
)
const totalRentOrders = computed(() =>
  Object.values(data.value?.rent_orders_by_status ?? {}).reduce((a, b) => a + b, 0)
)
const shopOrderLegend = computed(() =>
  SHOP_STATUS_ORDER.map((k, i) => ({
    label: SHOP_STATUS_LABELS[k],
    value: data.value?.shop_orders_by_status[k] ?? 0,
    color: SHOP_STATUS_COLORS[i],
  }))
)
const rentOrderLegend = computed(() =>
  RENT_STATUS_ORDER.map((k, i) => ({
    label: k,
    value: data.value?.rent_orders_by_status[k] ?? 0,
    color: RENT_STATUS_COLORS[i],
  }))
)

// ── Chart builders ───────────────────────────────────────────
function mkDonut(canvas, values, colors) {
  const c = new Chart(canvas, {
    type: 'doughnut',
    data: { datasets: [{ data: values, backgroundColor: colors, borderWidth: 1, borderColor: '#fff' }] },
    options: {
      cutout: '65%',
      plugins: { legend: { display: false }, tooltip: { callbacks: {
        label: ctx => ` ${ctx.raw}`,
      }}},
      animation: { duration: 600 },
    },
  })
  charts.push(c)
}

function mkLine(canvas, labels, datasets) {
  const c = new Chart(canvas, {
    type: 'line',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { display: true, labels: {
        font: { size: 11 },
        usePointStyle: true,
        pointStyle: 'line',
        pointStyleWidth: 24,
        generateLabels(chart) {
          return chart.data.datasets.map((ds, i) => ({
            text:         ds.label,
            strokeStyle:  ds.borderColor,
            fillStyle:    'transparent',
            lineDash:     ds.borderDash ?? [],
            lineWidth:    2,
            pointStyle:   'line',
            hidden:       !chart.isDatasetVisible(i),
            datasetIndex: i,
          }))
        },
      }}},
      scales: {
        x: { ticks: { font: { size: 10 }, maxRotation: 45, autoSkip: true, maxTicksLimit: 12 } },
        y:  { position: 'left',  ticks: { font: { size: 10 } }, title: { display: true, text: '訂單數', font: { size: 10 } } },
        y2: { position: 'right', ticks: { font: { size: 10 } }, grid: { drawOnChartArea: false }, title: { display: true, text: '金額', font: { size: 10 } } },
      },
      animation: { duration: 600 },
    },
  })
  charts.push(c)
}

function buildCharts() {
  const d = data.value

  // Products doughnut
  mkDonut(prodCanvas.value, [d.products.sold, d.products.unsold], PROD_COLORS)

  // Users doughnut
  const locales = Object.keys(d.users_by_locale)
  mkDonut(userCanvas.value, locales.map(l => d.users_by_locale[l]), locales.map(localeColor))

  // Shop orders doughnut
  mkDonut(
    shopOrderCanvas.value,
    SHOP_STATUS_ORDER.map(k => d.shop_orders_by_status[k] ?? 0),
    SHOP_STATUS_COLORS,
  )

  // Rent orders doughnut
  mkDonut(
    rentOrderCanvas.value,
    RENT_STATUS_ORDER.map(k => d.rent_orders_by_status[k] ?? 0),
    RENT_STATUS_COLORS,
  )

  const LC = ['#507f70', '#89D5C9', '#FAC172', '#E25B45']

  // Shop line chart
  const sl = d.shop_daily.labels
  mkLine(shopLineCanvas.value, sl, [
    { label: '每日訂單數',   data: d.shop_daily.daily_count,  borderColor: LC[0], backgroundColor: 'transparent', yAxisID: 'y',  tension: 0.3, pointRadius: 2 },
    { label: '每日訂單金額', data: d.shop_daily.daily_amount, borderColor: LC[1], backgroundColor: 'transparent', yAxisID: 'y2', tension: 0.3, pointRadius: 2 },
    { label: '累積訂單數',   data: d.shop_daily.cum_count,   borderColor: LC[2], backgroundColor: 'transparent', yAxisID: 'y',  tension: 0.3, pointRadius: 2, borderDash: [4,3] },
    { label: '累積訂單金額', data: d.shop_daily.cum_amount,  borderColor: LC[3], backgroundColor: 'transparent', yAxisID: 'y2', tension: 0.3, pointRadius: 2, borderDash: [4,3] },
  ])

  // Rent line chart
  const rl = d.rent_daily.labels
  mkLine(rentLineCanvas.value, rl, [
    { label: '每日訂單數',   data: d.rent_daily.daily_count,  borderColor: LC[0], backgroundColor: 'transparent', yAxisID: 'y',  tension: 0.3, pointRadius: 2 },
    { label: '每日訂單金額', data: d.rent_daily.daily_amount, borderColor: LC[1], backgroundColor: 'transparent', yAxisID: 'y2', tension: 0.3, pointRadius: 2 },
    { label: '累積訂單數',   data: d.rent_daily.cum_count,   borderColor: LC[2], backgroundColor: 'transparent', yAxisID: 'y',  tension: 0.3, pointRadius: 2, borderDash: [4,3] },
    { label: '累積訂單金額', data: d.rent_daily.cum_amount,  borderColor: LC[3], backgroundColor: 'transparent', yAxisID: 'y2', tension: 0.3, pointRadius: 2, borderDash: [4,3] },
  ])
}

onMounted(async () => {
  try {
    data.value = await api.get('/api/analytics')
  } finally {
    loading.value = false
  }
  await nextTick()
  buildCharts()
})

onUnmounted(() => {
  charts.forEach(c => c.destroy())
  charts.length = 0
})
</script>

<style scoped>
.analytics-section { /* inherits .admin-section */ }

.analytics-loading {
  padding: 40px; text-align: center;
  color: var(--mid); font-size: 0.9rem;
}

.section-title {
    font-family: var(--font-display);
    font-size: 1rem;
    font-weight: 600;
    color: var(--charcoal);
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Doughnut row ─────────────────────────── */
.donut-row {
  display: flex; flex-wrap: wrap; gap: 20px;
  margin-bottom: 28px;
}
.donut-card {
  flex: 1 1 160px;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
}
.donut-label {
  font-size: 0.8rem; font-weight: 600;
  color: var(--charcoal); font-family: var(--font-body);
  text-align: center;
}
.donut-body {
  display: flex; flex-direction: row; align-items: flex-end; gap: 12px;
}
.donut-wrap {
  position: relative; width: 110px; height: 110px; flex-shrink: 0;
}
.donut-wrap canvas { width: 100% !important; height: 100% !important; }
.donut-center {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  pointer-events: none;
}
.donut-num {
  font-size: 1.3rem; font-weight: 700;
  color: var(--charcoal); font-family: var(--font-display);
}
.donut-legend {
  list-style: none; padding: 0; margin: 0;
  font-size: 0.72rem; color: var(--charcoal);
  font-family: var(--font-body);
  display: flex; flex-direction: column; gap: 4px;
}
.donut-legend li { display: flex; align-items: center; gap: 5px; }
.dot {
  width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0;
}

/* ── Line charts row ──────────────────────── */
.line-charts-row {
  display: flex; flex-wrap: wrap; gap: 20px;
}
.line-card {
  flex: 1 1 300px;
  display: flex; flex-direction: column; gap: 8px;
}
.line-label {
  font-size: 0.8rem; font-weight: 600;
  color: var(--charcoal); font-family: var(--font-body);
}
.line-card canvas { width: 100% !important; }
</style>
