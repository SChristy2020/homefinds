<template>
  <div class="admin-view">

    <!-- ===== 商品管理 ===== -->
    <section class="admin-section">
      <div class="section-header">
        <h2 class="section-title">
          商品管理
          <button class="icon-btn section-add-btn" @click="openAddProd" title="新增商品"><PlusCircle :size="16"/></button>
          <button class="icon-btn section-add-btn" @click="openMarketingModal" title="發送促銷通知"><Mail :size="16"/></button>
        </h2>
        <div class="table-controls">
          <button class="icon-btn" @click="prodSearchOpen = !prodSearchOpen" title="搜尋"><Search :size="16"/></button>
        </div>
      </div>
      <Transition name="slide-down">
        <div v-if="prodSearchOpen" class="search-bar">
          <Search :size="14" class="search-icon"/>
          <input v-model="prodSearch" placeholder="搜尋商品..." autofocus />
        </div>
      </Transition>
      <div class="admin-category-pills">
        <button
          class="admin-pill"
          :class="{ active: prodCategoryFilter.length === 0 }"
          @click="prodCategoryFilter = []"
        >全部</button>
        <button
          v-for="cat in categories"
          :key="cat.id"
          class="admin-pill"
          :class="{ active: prodCategoryFilter.includes(getCatName(cat, 'en')) }"
          @click="toggleProdCategory(getCatName(cat, 'en'))"
        >{{ getCatName(cat, 'zh-TW') || getCatName(cat, 'en') }}</button>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th class="sortable-th" @click="setProdSort('id')">id<component :is="prodSortKey==='id' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='id' ? 'sort-active' : 'sort-inactive'" /></th>
              <th></th>
              <th class="sortable-th" @click="setProdSort('name')">zh名稱<component :is="prodSortKey==='name' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='name' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setProdSort('code')">代號<component :is="prodSortKey==='code' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='code' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setProdSort('category')">類別<component :is="prodSortKey==='category' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='category' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setProdSort('original_price')">原價<component :is="prodSortKey==='original_price' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='original_price' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setProdSort('price')">定價<component :is="prodSortKey==='price' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='price' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setProdSort('status')">狀態<component :is="prodSortKey==='status' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='status' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setProdSort('is_visible')">顯示<component :is="prodSortKey==='is_visible' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='is_visible' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setProdSort('sort')">排序<component :is="prodSortKey==='sort' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='sort' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setProdSort('pickup_available_time')">最快取貨日<component :is="prodSortKey==='pickup_available_time' ? (prodSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="prodSortKey==='pickup_available_time' ? 'sort-active' : 'sort-inactive'" /></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredProducts.length === 0">
              <td colspan="11" class="empty-row">無資料</td>
            </tr>
            <tr v-for="prod in pagedProducts" :key="prod.id">
              <td>{{ prod.id }}</td>
              <td class="prod-thumb-cell">
                <img v-if="prod.images && prod.images.length" :src="prod.images[0].url" class="prod-table-thumb" />
                <div v-else class="prod-table-thumb-placeholder"></div>
              </td>
              <td><div class="prod-name-cell">{{ getProdName(prod, 'zh-TW') }}</div></td>
              <td>{{ prod.code }}</td>
              <td>{{ prod.category }}</td>
              <td>{{ prod.original_price != null ? '$' + prod.original_price : '-' }}</td>
              <td>${{ prod.price }}</td>
              <td><span class="status-badge" :class="prod.status">{{ prod.status }}</span></td>
              <td><span class="status-badge" :class="prod.is_visible ? 'available' : 'sold'" style="cursor:pointer" @click="toggleVisible(prod)">{{ prod.is_visible ? '顯示' : '隱藏' }}</span></td>
              <td><input type="number" class="sort-inline-input" :value="prod.sort ?? 0" @change="updateProdSort(prod, $event.target.value)" @keydown.enter="$event.target.blur()" /></td>
              <td>{{ prod.pickup_available_time ? fmtDate(prod.pickup_available_time) : '隨時' }}</td>
              <td><div class="row-actions">
                <button class="action-btn edit" @click="openEditProd(prod)" title="編輯"><Pencil :size="14"/></button>
                <button class="action-btn delete" @click="deleteProduct(prod.id)" title="刪除"><Trash2 :size="14"/></button>
              </div></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="prodTotalPages > 1" class="pagination">
        <button class="page-btn" :disabled="prodPage === 1" @click="prodPage = 1">«</button>
        <button class="page-btn" :disabled="prodPage === 1" @click="prodPage--">‹</button>
        <span class="page-info">{{ prodPage }} / {{ prodTotalPages }}</span>
        <button class="page-btn" :disabled="prodPage === prodTotalPages" @click="prodPage++">›</button>
        <button class="page-btn" :disabled="prodPage === prodTotalPages" @click="prodPage = prodTotalPages">»</button>
      </div>
    </section>

    <!-- ===== 商品類別管理 ===== -->
    <section class="admin-section">
      <div class="section-header">
        <h2 class="section-title">商品類別管理 <button class="icon-btn section-add-btn" @click="openAddCat" title="新增類別"><PlusCircle :size="16"/></button></h2>
        <div class="table-controls">
          <button class="icon-btn" @click="catSearchOpen = !catSearchOpen" title="搜尋"><Search :size="16"/></button>
        </div>
      </div>
      <Transition name="slide-down">
        <div v-if="catSearchOpen" class="search-bar">
          <Search :size="14" class="search-icon"/>
          <input v-model="catSearch" placeholder="搜尋類別..." autofocus />
        </div>
      </Transition>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th class="sortable-th" @click="setCatSort('id')">id<component :is="catSortKey==='id' ? (catSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="catSortKey==='id' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setCatSort('name_zh')">zh名稱<component :is="catSortKey==='name_zh' ? (catSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="catSortKey==='name_zh' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setCatSort('name_cn')">cn名稱<component :is="catSortKey==='name_cn' ? (catSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="catSortKey==='name_cn' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setCatSort('name_en')">en名稱<component :is="catSortKey==='name_en' ? (catSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="catSortKey==='name_en' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setCatSort('code_prefix')">代號<component :is="catSortKey==='code_prefix' ? (catSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="catSortKey==='code_prefix' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setCatSort('product_count')">商品總數<component :is="catSortKey==='product_count' ? (catSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="catSortKey==='product_count' ? 'sort-active' : 'sort-inactive'" /></th>
              <th class="sortable-th" @click="setCatSort('sort_order')">排序<component :is="catSortKey==='sort_order' ? (catSortAsc ? ChevronUp : ChevronDown) : ArrowUpDown" :size="10" :class="catSortKey==='sort_order' ? 'sort-active' : 'sort-inactive'" /></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredCategories.length === 0">
              <td colspan="8" class="empty-row">無資料</td>
            </tr>
            <tr v-for="cat in filteredCategories" :key="cat.id">
              <td>{{ cat.id }}</td>
              <td>{{ getCatName(cat, 'zh-TW') }}</td>
              <td>{{ getCatName(cat, 'zh-CN') }}</td>
              <td>{{ getCatName(cat, 'en') }}</td>
              <td>{{ cat.code_prefix }}</td>
              <td>{{ cat.product_count }}</td>
              <td>{{ cat.sort_order }}</td>
              <td><div class="row-actions">
                <button class="action-btn edit" @click="openEditCat(cat)" title="編輯"><Pencil :size="14"/></button>
                <button class="action-btn delete" @click="deleteCategory(cat.id)" title="刪除"><Trash2 :size="14"/></button>
              </div></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- ===== 租房設定 ===== -->
    <section class="admin-section">
      <h2 class="section-title">租房設定</h2>
      <div v-if="!roomLoaded" class="loading">載入中...</div>
      <div v-else class="room-form">

        <!-- Dates -->
        <div class="form-row">
          <label class="form-label">可租屋日期</label>
          <input type="date" v-model="roomForm.available_from" class="form-input date-input" />
          <span class="form-sep">至</span>
          <input type="date" v-model="roomForm.available_to" class="form-input date-input" />
        </div>

        <!-- Prices -->
        <div class="prices-grid">
          <div class="price-row">
            <label class="form-label">每晚價格</label>
            <input type="number" v-model.number="roomForm.price_per_night" class="form-input price-input" />
            <span class="unit">USD</span>
          </div>
          <div class="price-row">
            <label class="form-label">每7晚價格</label>
            <input type="number" v-model.number="roomForm.price_7_nights" class="form-input price-input" />
            <span class="unit">USD</span>
          </div>
          <div class="price-row">
            <label class="form-label">每30天價格</label>
            <input type="number" v-model.number="roomForm.price_30_days" class="form-input price-input" />
            <span class="unit">USD</span>
          </div>
          <div class="price-row">
            <label class="form-label">全租</label>
            <input type="number" v-model.number="roomForm.price_full_period" class="form-input price-input" />
            <span class="unit">USD</span>
          </div>
        </div>

        <!-- Images -->
        <div class="form-group">
          <label class="form-label">圖片上傳</label>
          <div class="image-list">
            <div
              v-for="(img, idx) in roomImages"
              :key="img.id || img.tempId"
              class="image-item"
              :class="{ 'drag-over': roomDragOver === idx }"
              draggable="true"
              :data-idx="idx"
              data-drag-type="room"
              @dragstart="onDragStart(idx, 'room')"
              @dragover.prevent="roomDragOver = idx"
              @dragleave="roomDragOver = null"
              @drop.prevent="onDrop(idx, 'room'); roomDragOver = null"
              @touchstart="onTouchStart(idx, 'room', $event)"
              @touchmove.prevent="onTouchMove"
              @touchend="onTouchEnd"
            >
              <img v-if="img.url" :src="img.url" class="image-thumb" @error="img.loadErr = true" />
              <div v-else class="image-placeholder">{{ idx + 1 }}</div>
              <button class="image-remove" @click="removeRoomImage(idx)">×</button>
            </div>
            <button class="image-add" @click="addRoomImage" :disabled="roomUploading">
            {{ roomUploading ? '上傳中...' : '+' }}
          </button>
          </div>
          <p class="hint">可拖移圖片改變順序</p>
        </div>

        <!-- Descriptions per locale (HTML editors) -->
        <div class="desc-grid">
          <div v-for="locale in ['zh-TW', 'zh-CN', 'en']" :key="locale" class="form-group">
            <label class="form-label">{{ localeLabel(locale) }}描述</label>
            <HtmlEditor v-model="roomTranslations[locale].description" :room-id="roomId" />
          </div>
          <div v-for="locale in ['zh-TW', 'zh-CN', 'en']" :key="'bd_' + locale" class="form-group">
            <label class="form-label">{{ localeLabel(locale) }}房間預訂​流程​說明</label>
            <HtmlEditor v-model="roomTranslations[locale].booking_description" :room-id="roomId" />
          </div>
        </div>

        <button class="btn-primary save-btn" @click="saveRoom" :disabled="roomSaving">
          {{ roomSaving ? '儲存中...' : '租房設定存檔' }}
        </button>
      </div>
    </section>

    <!-- ===== Category Edit Modal ===== -->
    <BaseModal v-model="showCatModal" no-backdrop-close>
      <h3 class="modal-title">{{ editingCatId ? '編輯類別' : '新增類別' }}</h3>
      <div class="form-group">
        <label class="form-label">代號</label>
        <input v-model="catForm.code_prefix" class="form-input" placeholder="e.g. BED" />
      </div>
      <div class="form-group">
        <label class="form-label">排序</label>
        <input type="number" v-model.number="catForm.sort_order" class="form-input" style="width:100px" />
      </div>
      <div v-if="editingCatId" class="form-group">
        <label class="form-label">商品總數 <span class="hint">（僅顯示，不可編輯）</span></label>
        <input :value="catForm.product_count" disabled class="form-input" />
      </div>
      <div class="form-group">
        <label class="form-label">zh-TW 名稱</label>
        <input v-model="catForm.name_zh" class="form-input" />
      </div>
      <div class="form-group">
        <label class="form-label">zh-CN 名稱</label>
        <input v-model="catForm.name_cn" class="form-input" />
      </div>
      <div class="form-group">
        <label class="form-label">en 名稱</label>
        <input v-model="catForm.name_en" class="form-input" />
      </div>
      <div class="modal-actions">
        <button class="btn-secondary" @click="showCatModal = false">取消</button>
        <button class="btn-primary" @click="saveCatModal" :disabled="catSaving">
          {{ catSaving ? '儲存中...' : '存檔' }}
        </button>
      </div>
    </BaseModal>

    <!-- ===== Product Edit Modal ===== -->
    <BaseModal v-model="showProdModal" size="lg" no-backdrop-close>
      <h3 class="modal-title">{{ editingProdId ? '編輯商品' : '新增商品' }}</h3>

      <!-- Images -->
      <div class="form-group">
        <label class="form-label">圖片</label>
        <div class="image-list">
          <div
            v-for="(img, idx) in prodImages"
            :key="img.id || img.tempId"
            class="image-item"
            :class="{ 'drag-over': prodDragOver === idx }"
            draggable="true"
            :data-idx="idx"
            data-drag-type="prod"
            @dragstart="onDragStart(idx, 'prod')"
            @dragover.prevent="prodDragOver = idx"
            @dragleave="prodDragOver = null"
            @drop.prevent="onDrop(idx, 'prod'); prodDragOver = null"
            @touchstart="onTouchStart(idx, 'prod', $event)"
            @touchmove.prevent="onTouchMove"
            @touchend="onTouchEnd"
          >
            <img v-if="img.url" :src="img.url" class="image-thumb" />
            <div v-else class="image-placeholder">{{ idx + 1 }}</div>
            <button class="image-remove" @click="removeProdImage(idx)">×</button>
          </div>
          <button class="image-add" @click="addProdImage" :disabled="prodUploading">
            {{ prodUploading ? '上傳中...' : '+' }}
          </button>
        </div>
        <p class="hint">可拖移圖片改變順序</p>
      </div>

      <!-- Fields -->
      <div class="form-row-pair">
        <div class="form-row">
          <label class="form-label">代號</label>
          <input v-model="prodForm.code" class="form-input" readonly style="background:#f5f5f5;cursor:default;" />
        </div>
        <div v-if="!editingProdId" class="form-row">
          <label class="form-label">上架日期</label>
          <input type="date" v-model="prodForm.listed_date" class="form-input date-input" />
        </div>
      </div>
      <div class="form-row">
        <label class="form-label">類別</label>
        <select v-model="prodForm.category" class="form-input">
          <option v-for="cat in categories" :key="cat.id" :value="getCatName(cat, 'en')">
            {{ cat.code_prefix }} - {{ getCatName(cat, 'zh-TW') }} ({{ getCatName(cat, 'en') }})
          </option>
        </select>
      </div>
      <div class="form-row-pair">
        <div class="form-row">
          <label class="form-label">原價</label>
          <input type="number" v-model.number="prodForm.original_price" class="form-input" placeholder="無則留空" />
        </div>
        <div class="form-row">
          <label class="form-label">定價</label>
          <input type="number" v-model.number="prodForm.price" class="form-input" />
        </div>
      </div>
      <div class="form-row">
        <label class="form-label">狀態</label>
        <div class="pickup-radio-group">
          <label class="radio-option">
            <input type="radio" v-model="prodForm.status" value="available" /> available
          </label>
          <label class="radio-option">
            <input type="radio" v-model="prodForm.status" value="reserved" /> reserved
          </label>
          <label class="radio-option">
            <input type="radio" v-model="prodForm.status" value="sold" /> sold
          </label>
        </div>
      </div>
      <div class="form-row">
        <label class="form-label">顯示於購物頁</label>
        <div class="pickup-radio-group">
          <label class="radio-option">
            <input type="radio" v-model="prodForm.is_visible" :value="false" /> 隱藏
          </label>
          <label class="radio-option">
            <input type="radio" v-model="prodForm.is_visible" :value="true" /> 顯示
          </label>
        </div>
      </div>
      <div class="form-row">
        <label class="form-label">排序</label>
        <input type="number" v-model.number="prodForm.sort" class="form-input" style="width:100px" />
      </div>
      <div class="form-row">
        <label class="form-label">最快取貨日</label>
        <div class="pickup-radio-group">
          <label class="radio-option">
            <input type="radio" v-model="pickupMode" value="anytime" /> 隨時
          </label>
          <label class="radio-option">
            <input type="radio" v-model="pickupMode" value="date" /> 指定日期起
          </label>
          <input v-if="pickupMode === 'date'" type="date" v-model="prodForm.pickup_available_time" class="form-input date-input" />
        </div>
      </div>

      <!-- Translations -->
      <div v-for="locale in ['zh-TW', 'zh-CN', 'en']" :key="locale" class="translation-block">
        <div class="translation-locale">{{ locale }}</div>
        <div class="form-group">
          <label class="form-label">名稱</label>
          <input v-model="prodTranslations[locale].name" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">描述</label>
          <HtmlEditor v-model="prodTranslations[locale].description" />
        </div>
      </div>

      <template #footer>
        <div class="modal-actions" style="margin-top:0">
          <button class="btn-secondary" @click="showProdModal = false" style="white-space:nowrap">取消</button>
          <button class="btn-primary" @click="saveProdModal" :disabled="prodSaving">
            {{ prodSaving ? '儲存中...' : '存檔' }}
          </button>
        </div>
      </template>
    </BaseModal>

    <input ref="prodFileInput" type="file" accept="image/*" multiple style="display:none" @change="onProdFileChange" />
    <input ref="roomFileInput" type="file" accept="image/*" multiple style="display:none" @change="onRoomFileChange" />

    <!-- ===== Marketing Email Modal ===== -->
    <BaseModal v-model="showMarketingModal" size="xl" no-backdrop-close>
      <h3 class="modal-title">發送促銷通知</h3>
      <p class="marketing-hint">勾選要推薦的商品（僅顯示未售出的商品）：</p>

      <div class="marketing-product-list">
        <label
          v-for="prod in unsoldProducts"
          :key="prod.id"
          class="marketing-product-item"
          :class="{ selected: marketingSelectedIds.includes(prod.id) }"
        >
          <input
            type="checkbox"
            :value="prod.id"
            v-model="marketingSelectedIds"
            class="marketing-checkbox"
          />
          <img
            v-if="prod.images && prod.images.length"
            :src="prod.images[0].url"
            class="marketing-thumb"
          />
          <div v-else class="marketing-thumb-placeholder"></div>
          <div class="marketing-prod-info">
            <span class="marketing-prod-name">{{ getProdName(prod, 'zh-TW') }}</span>
            <span class="marketing-prod-price">${{ prod.price }}</span>
            <span class="marketing-prod-date">{{ prod.listed_date }}</span>
          </div>
        </label>
        <p v-if="unsoldProducts.length === 0" class="empty-row">目前沒有未售出的商品</p>
      </div>

      <div class="modal-actions">
        <button class="btn-secondary" @click="showMarketingModal = false">取消</button>
        <button
          class="btn-primary"
          :disabled="marketingSelectedIds.length === 0 || marketingSending"
          @click="sendMarketingEmail"
        >
          {{ marketingSending ? '發送中...' : `發送通知 (${marketingSelectedIds.length} 件商品)` }}
        </button>
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { Search, ArrowUpDown, ChevronUp, ChevronDown, Pencil, Trash2, PlusCircle, Mail } from 'lucide-vue-next'
import { api } from '@/utils/api'
import { useToastStore } from '@/stores/toast'
import BaseModal from '@/components/shared/BaseModal.vue'
import HtmlEditor from '@/components/shared/HtmlEditor.vue'

const toast = useToastStore()

// ========== HELPERS ==========
function getCatName(cat, locale) {
  return cat.translations?.find(t => t.locale === locale)?.name || '-'
}
function getProdName(prod, locale) {
  return prod.translations?.find(t => t.locale === locale)?.name || '-'
}
function localeLabel(locale) {
  return locale === 'zh-TW' ? 'zh' : locale === 'zh-CN' ? 'cn' : 'en'
}
function fmtDate(dt) {
  if (!dt) return '-'
  const d = new Date(dt)
  return `${String(d.getMonth()+1).padStart(2,'0')}/${String(d.getDate()).padStart(2,'0')}/${d.getFullYear()}`
}

// ========== CATEGORIES ==========
const categories = ref([])
const catSearch = ref('')
const catSearchOpen = ref(false)
const catSortKey = ref('id')
const catSortAsc = ref(true)
const showCatModal = ref(false)
const editingCatId = ref(null)
const catSaving = ref(false)
const catForm = reactive({ code_prefix: '', product_count: 0, sort_order: 0, name_zh: '', name_cn: '', name_en: '' })

async function loadCategories() {
  categories.value = await api.get('/api/categories')
}

const filteredCategories = computed(() => {
  let list = [...categories.value]
  if (catSearch.value.trim()) {
    const q = catSearch.value.toLowerCase()
    list = list.filter(c =>
      c.code_prefix.toLowerCase().includes(q) ||
      c.translations?.some(t => t.name.toLowerCase().includes(q))
    )
  }
  const key = catSortKey.value
  const dir = catSortAsc.value ? 1 : -1
  return list.sort((a, b) => {
    let av, bv
    if (key === 'id') { av = a.id; bv = b.id }
    else if (key === 'name_zh') { av = getCatName(a, 'zh-TW') || ''; bv = getCatName(b, 'zh-TW') || '' }
    else if (key === 'name_cn') { av = getCatName(a, 'zh-CN') || ''; bv = getCatName(b, 'zh-CN') || '' }
    else if (key === 'name_en') { av = getCatName(a, 'en') || ''; bv = getCatName(b, 'en') || '' }
    else if (key === 'code_prefix') { av = a.code_prefix || ''; bv = b.code_prefix || '' }
    else if (key === 'product_count') { av = a.product_count ?? 0; bv = b.product_count ?? 0 }
    else if (key === 'sort_order') { av = a.sort_order ?? 0; bv = b.sort_order ?? 0 }
    else { av = a.id; bv = b.id }
    if (typeof av === 'string') return av.localeCompare(bv) * dir
    return (av - bv) * dir
  })
})

function setCatSort(key) {
  if (catSortKey.value === key) catSortAsc.value = !catSortAsc.value
  else { catSortKey.value = key; catSortAsc.value = true }
}

function openAddCat() {
  editingCatId.value = null
  catForm.code_prefix = ''
  catForm.product_count = 0
  catForm.sort_order = 0
  catForm.name_zh = ''
  catForm.name_cn = ''
  catForm.name_en = ''
  showCatModal.value = true
}

function openEditCat(cat) {
  editingCatId.value = cat.id
  catForm.code_prefix = cat.code_prefix
  catForm.product_count = cat.product_count
  catForm.sort_order = cat.sort_order ?? 0
  catForm.name_zh = getCatName(cat, 'zh-TW')
  catForm.name_cn = getCatName(cat, 'zh-CN')
  catForm.name_en = getCatName(cat, 'en')
  showCatModal.value = true
}

async function saveCatModal() {
  catSaving.value = true
  try {
    if (editingCatId.value) {
      await api.put(`/api/categories/${editingCatId.value}`, { code_prefix: catForm.code_prefix, sort_order: catForm.sort_order })
      await api.put(`/api/categories/${editingCatId.value}/translations/zh-TW`, { locale: 'zh-TW', name: catForm.name_zh })
      await api.put(`/api/categories/${editingCatId.value}/translations/zh-CN`, { locale: 'zh-CN', name: catForm.name_cn })
      await api.put(`/api/categories/${editingCatId.value}/translations/en`,    { locale: 'en',    name: catForm.name_en })
    } else {
      await api.post('/api/categories', {
        code_prefix: catForm.code_prefix,
        sort_order: catForm.sort_order,
        translations: [
          { locale: 'zh-TW', name: catForm.name_zh },
          { locale: 'zh-CN', name: catForm.name_cn },
          { locale: 'en',    name: catForm.name_en },
        ],
      })
    }
    await loadCategories()
    showCatModal.value = false
    toast.show('已儲存')
  } catch (e) {
    toast.show('儲存失敗: ' + (e.detail || e))
  } finally {
    catSaving.value = false
  }
}

async function deleteCategory(id) {
  if (!confirm('確定要刪除此類別？此操作無法復原。')) return
  try {
    await api.delete(`/api/categories/${id}`)
    await loadCategories()
    toast.show('已刪除')
  } catch (e) {
    toast.show('刪除失敗')
  }
}

// ========== PRODUCTS ==========
const products = ref([])
const prodSearch = ref('')
const prodSearchOpen = ref(false)
const prodCategoryFilter = ref([])
const prodSortKey = ref('id')
const prodSortAsc = ref(false)
const prodPage = ref(1)
const prodPageSize = 10
const showProdModal = ref(false)
const editingProdId = ref(null)
const prodSaving = ref(false)
const pickupMode = ref('anytime')
const prodForm = reactive({ code: '', listed_date: '', category: '', original_price: null, price: 0, status: 'available', is_visible: false, sort: 50, pickup_available_time: '' })
const prodTranslations = reactive({
  'zh-TW': { name: '', description: '' },
  'zh-CN': { name: '', description: '' },
  'en':    { name: '', description: '' },
})
const prodImages = ref([])
const deletedProdImageIds = ref([])
const prodDragOver = ref(null)
const prodUploading = ref(false)
const prodFileInput = ref(null)
const dragSrcType = ref(null)
const dragSrcIdx = ref(null)
const touchGhost = ref(null)
const touchOffsetX = ref(0)
const touchOffsetY = ref(0)
const touchDragOver = ref(null)
const suppressCodeGen = ref(false)

async function loadProducts() {
  products.value = await api.get('/api/products')
}

const filteredProducts = computed(() => {
  let list = [...products.value]
  if (prodCategoryFilter.value.length > 0) {
    list = list.filter(p => prodCategoryFilter.value.includes(p.category))
  }
  if (prodSearch.value.trim()) {
    const q = prodSearch.value.toLowerCase()
    list = list.filter(p =>
      p.code.toLowerCase().includes(q) ||
      p.category.toLowerCase().includes(q) ||
      p.translations?.some(t => t.name.toLowerCase().includes(q))
    )
  }
  const key = prodSortKey.value
  const dir = prodSortAsc.value ? 1 : -1
  return list.sort((a, b) => {
    let av, bv
    if (key === 'id') { av = a.id; bv = b.id }
    else if (key === 'name') { av = getProdName(a, 'zh-TW') || ''; bv = getProdName(b, 'zh-TW') || '' }
    else if (key === 'code') { av = a.code || ''; bv = b.code || '' }
    else if (key === 'category') { av = a.category || ''; bv = b.category || '' }
    else if (key === 'original_price') { av = a.original_price ?? -1; bv = b.original_price ?? -1 }
    else if (key === 'price') { av = a.price ?? 0; bv = b.price ?? 0 }
    else if (key === 'status') { av = a.status || ''; bv = b.status || '' }
    else if (key === 'is_visible') { av = a.is_visible ? 1 : 0; bv = b.is_visible ? 1 : 0 }
    else if (key === 'sort') { av = a.sort ?? 0; bv = b.sort ?? 0 }
    else if (key === 'pickup_available_time') { av = a.pickup_available_time || ''; bv = b.pickup_available_time || '' }
    else { av = a.id; bv = b.id }
    if (typeof av === 'string') return av.localeCompare(bv) * dir
    return (av - bv) * dir
  })
})

function setProdSort(key) {
  if (prodSortKey.value === key) prodSortAsc.value = !prodSortAsc.value
  else { prodSortKey.value = key; prodSortAsc.value = true }
}

function toggleProdCategory(enName) {
  const idx = prodCategoryFilter.value.indexOf(enName)
  if (idx === -1) prodCategoryFilter.value.push(enName)
  else prodCategoryFilter.value.splice(idx, 1)
}

const prodTotalPages = computed(() => Math.max(1, Math.ceil(filteredProducts.value.length / prodPageSize)))
const pagedProducts = computed(() => {
  const start = (prodPage.value - 1) * prodPageSize
  return filteredProducts.value.slice(start, start + prodPageSize)
})

watch(filteredProducts, () => { prodPage.value = 1 })

function autoGenerateProdCode(categoryEnName) {
  const cat = categories.value.find(c => getCatName(c, 'en') === categoryEnName)
  if (cat) {
    const prefix = cat.code_prefix
    const maxNum = products.value
      .filter(p => p.code && p.code.startsWith(prefix))
      .map(p => parseInt(p.code.slice(prefix.length), 10))
      .filter(n => !isNaN(n))
      .reduce((max, n) => Math.max(max, n), 0)
    prodForm.code = prefix + (maxNum + 1)
  } else {
    prodForm.code = ''
  }
}

watch(() => prodForm.category, (newCat) => {
  if (!suppressCodeGen.value) autoGenerateProdCode(newCat)
}, { flush: 'sync' })

function openAddProd() {
  editingProdId.value = null
  prodForm.listed_date = new Date().toISOString().slice(0, 10)
  prodForm.category = categories.value.length ? getCatName(categories.value[0], 'en') || '' : ''
  autoGenerateProdCode(prodForm.category)
  prodForm.original_price = null
  prodForm.price = 0
  prodForm.status = 'available'
  prodForm.is_visible = false
  prodForm.sort = 50
  prodForm.pickup_available_time = '2026-04-18'
  pickupMode.value = 'date'
  for (const locale of ['zh-TW', 'zh-CN', 'en']) {
    prodTranslations[locale].name = ''
    prodTranslations[locale].description = ''
  }
  prodImages.value = []
  deletedProdImageIds.value = []
  showProdModal.value = true
}

function openEditProd(prod) {
  suppressCodeGen.value = true
  editingProdId.value = prod.id
  prodForm.code = prod.code
  prodForm.category = prod.category
  suppressCodeGen.value = false
  prodForm.original_price = prod.original_price
  prodForm.price = prod.price
  prodForm.status = prod.status
  prodForm.is_visible = prod.is_visible ?? false
  prodForm.sort = prod.sort ?? 0
  if (prod.pickup_available_time) {
    pickupMode.value = 'date'
    prodForm.pickup_available_time = new Date(prod.pickup_available_time).toISOString().slice(0, 10)
  } else {
    pickupMode.value = 'anytime'
    prodForm.pickup_available_time = ''
  }
  for (const locale of ['zh-TW', 'zh-CN', 'en']) {
    const t = prod.translations?.find(t => t.locale === locale)
    prodTranslations[locale].name = t?.name || ''
    prodTranslations[locale].description = t?.description || ''
  }
  prodImages.value = prod.images ? prod.images.map(img => ({ ...img })) : []
  deletedProdImageIds.value = []
  showProdModal.value = true
}

function addProdImage() {
  prodFileInput.value.click()
}

function padToSquare(file) {
  return new Promise((resolve) => {
    const img = new Image()
    const objectUrl = URL.createObjectURL(file)
    img.onload = () => {
      URL.revokeObjectURL(objectUrl)
      const padding = Math.round(Math.max(img.width, img.height) * 0.05)
      const size = Math.max(img.width, img.height) + padding * 2
      const canvas = document.createElement('canvas')
      canvas.width = size
      canvas.height = size
      const ctx = canvas.getContext('2d')
      ctx.fillStyle = '#ffffff'
      ctx.fillRect(0, 0, size, size)
      const x = Math.round((size - img.width) / 2)
      const y = Math.round((size - img.height) / 2)
      ctx.drawImage(img, x, y, img.width, img.height)
      canvas.toBlob((blob) => {
        resolve(new File([blob], file.name, { type: 'image/jpeg' }))
      }, 'image/jpeg', 0.92)
    }
    img.src = objectUrl
  })
}

async function onProdFileChange(e) {
  const files = Array.from(e.target.files)
  if (!files.length) return
  prodUploading.value = true
  try {
    await Promise.all(files.map(async (file) => {
      const squared = await padToSquare(file)
      const { url } = await api.upload(squared)
      prodImages.value.push({ tempId: Date.now() + Math.random(), url, isNew: true })
    }))
  } catch {
    toast.show('圖片上傳失敗')
  } finally {
    prodUploading.value = false
    e.target.value = ''
  }
}

function removeProdImage(idx) {
  const img = prodImages.value[idx]
  if (img.id) deletedProdImageIds.value.push(img.id)
  prodImages.value.splice(idx, 1)
}

async function saveProdModal() {
  prodSaving.value = true
  try {
    let id = editingProdId.value
    if (!id) {
      const created = await api.post('/api/products', {
        code:                  prodForm.code,
        listed_date:           prodForm.listed_date,
        category:              prodForm.category,
        price:                 prodForm.price,
        original_price:        prodForm.original_price || null,
        status:                prodForm.status,
        is_visible:            prodForm.is_visible,
        sort:                  prodForm.sort,
        pickup_available_time: pickupMode.value === 'date' ? (prodForm.pickup_available_time || null) : null,
        translations: ['zh-TW', 'zh-CN', 'en']
          .filter(l => prodTranslations[l].name)
          .map(l => ({ locale: l, name: prodTranslations[l].name, description: prodTranslations[l].description || null })),
      })
      id = created.id
    } else {
      await api.put(`/api/products/${id}`, {
        code:                  prodForm.code,
        category:              prodForm.category,
        price:                 prodForm.price,
        original_price:        prodForm.original_price || null,
        status:                prodForm.status,
        is_visible:            prodForm.is_visible,
        sort:                  prodForm.sort,
        pickup_available_time: pickupMode.value === 'date' ? (prodForm.pickup_available_time || null) : null,
      })
      for (const locale of ['zh-TW', 'zh-CN', 'en']) {
        if (prodTranslations[locale].name) {
          await api.put(`/api/products/${id}/translations/${locale}`, {
            locale,
            name:        prodTranslations[locale].name,
            description: prodTranslations[locale].description || null,
          })
        }
      }
    }
    for (const imgId of deletedProdImageIds.value) {
      await api.delete(`/api/products/${id}/images/${imgId}`)
    }
    for (let i = 0; i < prodImages.value.length; i++) {
      const img = prodImages.value[i]
      if (img.isNew) {
        await api.post(`/api/products/${id}/images?url=${encodeURIComponent(img.url)}&sort_order=${i}`, {})
      }
    }
    const reorderData = prodImages.value
      .filter(img => img.id)
      .map((img, i) => ({ id: img.id, sort_order: i }))
    if (reorderData.length > 0) {
      await api.put(`/api/products/${id}/images/reorder`, reorderData)
    }
    await Promise.all([loadProducts(), loadCategories()])
    showProdModal.value = false
    toast.show('已儲存')
  } catch (e) {
    toast.show('儲存失敗')
  } finally {
    prodSaving.value = false
  }
}

async function updateProdSort(prod, value) {
  const newSort = parseInt(value, 10) || 0
  if (newSort === (prod.sort ?? 0)) return
  try {
    await api.put(`/api/products/${prod.id}`, { sort: newSort })
    prod.sort = newSort
  } catch (e) {
    toast.show('更新失敗')
  }
}

async function toggleVisible(prod) {
  try {
    await api.put(`/api/products/${prod.id}`, { is_visible: !prod.is_visible })
    prod.is_visible = !prod.is_visible
  } catch (e) {
    toast.show('更新失敗')
  }
}

async function deleteProduct(id) {
  if (!confirm('確定要刪除此商品？此操作無法復原。')) return
  try {
    await api.delete(`/api/products/${id}`)
    await loadProducts()
    toast.show('已刪除')
  } catch (e) {
    toast.show('刪除失敗')
  }
}

// ========== DRAG & DROP ==========
function onDragStart(idx, type) {
  dragSrcType.value = type
  dragSrcIdx.value = idx
}

function onDrop(targetIdx, type) {
  if (dragSrcType.value !== type || dragSrcIdx.value === null || dragSrcIdx.value === targetIdx) return
  const list = type === 'room' ? roomImages.value : prodImages.value
  const [moved] = list.splice(dragSrcIdx.value, 1)
  list.splice(targetIdx, 0, moved)
  dragSrcIdx.value = null
}

function onTouchStart(idx, type, event) {
  dragSrcType.value = type
  dragSrcIdx.value = idx
  const touch = event.touches[0]
  const rect = event.currentTarget.getBoundingClientRect()
  touchOffsetX.value = touch.clientX - rect.left
  touchOffsetY.value = touch.clientY - rect.top
  const ghost = event.currentTarget.cloneNode(true)
  ghost.style.cssText = `position:fixed;width:${rect.width}px;height:${rect.height}px;left:${touch.clientX - touchOffsetX.value}px;top:${touch.clientY - touchOffsetY.value}px;opacity:0.7;pointer-events:none;z-index:9999;border-radius:4px;`
  document.body.appendChild(ghost)
  touchGhost.value = ghost
}

function onTouchMove(event) {
  if (!touchGhost.value) return
  const touch = event.touches[0]
  touchGhost.value.style.left = (touch.clientX - touchOffsetX.value) + 'px'
  touchGhost.value.style.top = (touch.clientY - touchOffsetY.value) + 'px'
  touchGhost.value.style.display = 'none'
  const el = document.elementFromPoint(touch.clientX, touch.clientY)
  touchGhost.value.style.display = ''
  const item = el?.closest('[data-drag-type]')
  if (item) {
    const idx = parseInt(item.dataset.idx)
    const type = item.dataset.dragType
    if (!isNaN(idx)) {
      touchDragOver.value = { idx, type }
      if (type === 'prod') { prodDragOver.value = idx; roomDragOver.value = null }
      else { roomDragOver.value = idx; prodDragOver.value = null }
    }
  } else {
    touchDragOver.value = null
    prodDragOver.value = null
    roomDragOver.value = null
  }
}

function onTouchEnd() {
  if (touchGhost.value) {
    document.body.removeChild(touchGhost.value)
    touchGhost.value = null
  }
  if (touchDragOver.value) {
    onDrop(touchDragOver.value.idx, touchDragOver.value.type)
    touchDragOver.value = null
  }
  prodDragOver.value = null
  roomDragOver.value = null
  dragSrcIdx.value = null
  dragSrcType.value = null
}

// ========== ROOM ==========
const roomLoaded = ref(false)
const roomSaving = ref(false)
const roomId = ref(null)
const roomDragOver = ref(null)
const roomImages = ref([])
const deletedRoomImageIds = ref([])
const roomUploading = ref(false)
const roomFileInput = ref(null)
const roomForm = reactive({
  available_from: '',
  available_to: '',
  price_per_night: 0,
  price_7_nights: null,
  price_30_days: null,
  price_full_period: null,
})
const roomTranslations = reactive({
  'zh-TW': { description: '', booking_description: '' },
  'zh-CN': { description: '', booking_description: '' },
  'en':    { description: '', booking_description: '' },
})

async function loadRoom() {
  try {
    const rooms = await api.get('/api/room')
    if (rooms.length) {
      const room = rooms[0]
      roomId.value = room.id
      roomForm.available_from    = room.available_from
      roomForm.available_to      = room.available_to
      roomForm.price_per_night   = room.price_per_night
      roomForm.price_7_nights    = room.price_7_nights
      roomForm.price_30_days     = room.price_30_days
      roomForm.price_full_period = room.price_full_period
      for (const locale of ['zh-TW', 'zh-CN', 'en']) {
        const t = room.translations?.find(t => t.locale === locale)
        roomTranslations[locale].description         = t?.description || ''
        roomTranslations[locale].booking_description = t?.booking_description || ''
      }
      roomImages.value = room.images ? room.images.map(img => ({ ...img })) : []
    }
  } catch (e) {
    // API 錯誤或無資料時仍顯示表單
  } finally {
    roomLoaded.value = true
  }
}

function addRoomImage() {
  roomFileInput.value.click()
}

async function onRoomFileChange(e) {
  const files = Array.from(e.target.files)
  if (!files.length) return
  roomUploading.value = true
  try {
    await Promise.all(files.map(async (file) => {
      const squared = await padToSquare(file)
      const { url } = await api.upload(squared)
      roomImages.value.push({ tempId: Date.now() + Math.random(), url, isNew: true })
    }))
  } catch {
    toast.show('圖片上傳失敗')
  } finally {
    roomUploading.value = false
    e.target.value = ''
  }
}

function removeRoomImage(idx) {
  const img = roomImages.value[idx]
  if (img.id) deletedRoomImageIds.value.push(img.id)
  roomImages.value.splice(idx, 1)
}

async function saveRoom() {
  roomSaving.value = true
  try {
    if (!roomId.value) {
      const created = await api.post('/api/room', {
        available_from:    roomForm.available_from    || new Date().toISOString().slice(0, 10),
        available_to:      roomForm.available_to      || new Date().toISOString().slice(0, 10),
        price_per_night:   roomForm.price_per_night   || 0,
        price_7_nights:    roomForm.price_7_nights    || null,
        price_30_days:     roomForm.price_30_days     || null,
        price_full_period: roomForm.price_full_period || null,
      })
      roomId.value = created.id
    } else {
      await api.put(`/api/room/${roomId.value}`, {
        available_from:    roomForm.available_from,
        available_to:      roomForm.available_to,
        price_per_night:   roomForm.price_per_night,
        price_7_nights:    roomForm.price_7_nights || null,
        price_30_days:     roomForm.price_30_days || null,
        price_full_period: roomForm.price_full_period || null,
      })
    }
    for (const locale of ['zh-TW', 'zh-CN', 'en']) {
      await api.put(`/api/room/${roomId.value}/translations/${locale}`, {
        locale,
        description:         roomTranslations[locale].description || null,
        booking_description: roomTranslations[locale].booking_description || null,
      })
    }
    for (const imgId of deletedRoomImageIds.value) {
      await api.delete(`/api/room/${roomId.value}/images/${imgId}`)
    }
    deletedRoomImageIds.value = []
    for (let i = 0; i < roomImages.value.length; i++) {
      const img = roomImages.value[i]
      if (img.isNew) {
        await api.post(`/api/room/${roomId.value}/images?url=${encodeURIComponent(img.url)}&sort_order=${i}`, {})
        delete img.isNew
      }
    }
    const reorderData = roomImages.value
      .filter(img => img.id)
      .map((img, i) => ({ id: img.id, sort_order: i }))
    if (reorderData.length > 0) {
      await api.put(`/api/room/${roomId.value}/images/reorder`, reorderData)
    }
    await loadRoom()
    toast.show('租房設定已儲存')
  } catch (e) {
    toast.show('儲存失敗')
  } finally {
    roomSaving.value = false
  }
}

// ========== MARKETING ==========
const showMarketingModal = ref(false)
const marketingSelectedIds = ref([])
const marketingSending = ref(false)

const unsoldProducts = computed(() =>
  products.value
    .filter(p => p.status !== 'sold')
    .sort((a, b) => (b.listed_date || '').localeCompare(a.listed_date || ''))
)

function openMarketingModal() {
  marketingSelectedIds.value = []
  showMarketingModal.value = true
}

async function sendMarketingEmail() {
  if (marketingSelectedIds.value.length === 0) return
  const { useUserStore } = await import('@/stores/user')
  const userStore = useUserStore()
  const adminId = userStore.currentUser?.id
  if (!adminId) return toast.show('無法取得管理員身份')
  marketingSending.value = true
  try {
    await api.post('/api/marketing/send', {
      product_ids: marketingSelectedIds.value,
      admin_id: adminId,
    })
    showMarketingModal.value = false
    alert('寄件成功！')
  } catch (e) {
    toast.show('發送失敗: ' + (e.detail || e))
  } finally {
    marketingSending.value = false
  }
}

onMounted(() => {
  loadCategories()
  loadProducts()
  loadRoom()
})
</script>

<style scoped>
.admin-view { display: flex; flex-direction: column; gap: 48px; }

/* Section */
.admin-section {
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  padding: 24px 28px;
}
.section-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px;
}
.section-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 600;
  color: var(--charcoal);
  display: flex; align-items: center; gap: 6px;
}
.table-controls { display: flex; gap: 8px; align-items: center; }
.section-add-btn { color: var(--mid); }

/* Category filter pills */
.admin-category-pills {
  display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px;
}
.admin-pill {
  padding: 3px 12px; border-radius: 20px; font-size: 0.78rem;
  font-family: var(--font-body); cursor: pointer;
  border: 1.5px solid var(--border); background: var(--bg); color: var(--mid);
  transition: all 0.15s;
}
.admin-pill.active, .admin-pill:hover {
  background: var(--button); color: #fff; border-color: var(--button);
}

/* Search bar */
.search-bar {
  display: flex; gap: 8px; align-items: center;
  background: var(--bg); border: 1.5px solid var(--border);
  border-radius: var(--radius); padding: 5px 12px; margin-bottom: 14px;
}
.search-bar input {
  border: none; background: transparent;
  font-family: var(--font-body); font-size: 0.82rem;
  outline: none; flex: 1; color: var(--charcoal);
}
.search-icon { color: var(--mid); flex-shrink: 0; }

/* DataTable */
.table-wrap { overflow-x: auto; }
.data-table {
  width: 100%; border-collapse: collapse;
  font-size: 0.8rem; font-family: var(--font-body);
}
.data-table th {
  text-align: left; padding: 8px 10px;
  border-bottom: 1.5px solid var(--border);
  color: var(--mid); font-weight: 600;
  white-space: nowrap;
}
.sortable-th {
  cursor: pointer; user-select: none;
}
.sortable-th:hover { color: var(--charcoal); }
.sort-active { vertical-align: middle; margin-left: 2px; }
.sort-inactive { vertical-align: middle; margin-left: 2px; opacity: 0.3; }
.sort-inline-input {
  width: 60px; padding: 2px 4px; text-align: center;
  border: 1px solid var(--border); border-radius: 4px;
  background: transparent; color: inherit; font-size: inherit;
}
.sort-inline-input:focus { outline: none; border-color: var(--button); background: var(--accent-light); }
.data-table td {
  padding: 8px 10px;
  border-bottom: 1px solid var(--border);
  color: var(--charcoal); vertical-align: middle;
}
.data-table tr:last-child td { border-bottom: none; }
.data-table tbody tr { transition: background 0.15s; cursor: default; }
.data-table tbody tr:hover td { background: var(--light); }
.empty-row { text-align: center; color: var(--light); padding: 20px; }

/* Row actions */
.row-actions { display: flex; gap: 6px; align-items: center; }
.action-btn {
  background: none; border: none; cursor: pointer;
  padding: 4px; border-radius: 3px;
  display: flex; align-items: center;
  transition: background 0.15s, color 0.15s;
}
.action-btn.edit { color: var(--accent); }
.action-btn.edit:hover { background: #fff5f0; }
.action-btn.delete { color: var(--mid); }
.action-btn.delete:hover { color: #c0392b; background: #fff0f0; }

/* Status badge */
.status-badge {
  font-size: 0.72rem; padding: 2px 8px;
  border-radius: 999px; font-weight: 500;
  white-space: nowrap;
}
.status-badge.available { background: #e8f5e9; color: #2e7d32; }
.status-badge.reserved  { background: #fff8e1; color: #f57c00; }
.status-badge.sold      { background: #fce4ec; color: #c62828; }

/* Icon button */
.icon-btn {
  background: none; border: none; cursor: pointer;
  color: var(--charcoal); padding: 4px;
  display: flex; align-items: center;
  transition: color 0.15s;
}
.icon-btn:hover { color: var(--accent); }

/* Room form */
.room-form { display: flex; flex-direction: column; gap: 18px; }
.form-row {
  display: flex; align-items: baseline; gap: 2px; flex-wrap: wrap; padding-bottom: 18px;
}
.form-label {
  font-size: 0.82rem; font-weight: 500;
  color: var(--charcoal); min-width: 90px;
  font-family: var(--font-body);
}
.form-input {
  font-family: var(--font-body); font-size: 0.82rem;
  border: 1.5px solid var(--border); border-radius: var(--radius);
  padding: 6px 10px; color: var(--charcoal);
  background: var(--bg); outline: none;
  transition: border-color 0.15s;
  width: -webkit-fill-available;
}
.form-input:focus { border-color: var(--charcoal); }
.form-input:disabled { opacity: 0.5; cursor: not-allowed; }
.date-input { width: 150px; }
.pickup-radio-group { display: flex; flex-direction: row; align-items: center; flex-wrap: wrap; gap: 12px; }
.form-row-pair { display: flex; gap: 16px; flex-wrap: wrap; }
.form-row-pair > .form-row { flex: 1; min-width: 120px; flex-direction: column; align-items: flex-start; padding-bottom: 18px; }
.form-row-pair .form-input { width: 100%; box-sizing: border-box; }
.radio-option { display: flex; align-items: center; gap: 6px; font-size: 0.82rem; cursor: pointer; }
.price-input { width: 120px; }
.form-sep { color: var(--mid); font-size: 0.82rem; }
.unit { font-size: 0.78rem; color: var(--mid); }

.prices-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.price-row { display: flex; align-items: center; gap: 10px; }

.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-textarea {
  font-family: var(--font-body); font-size: 0.82rem;
  border: 1.5px solid var(--border); border-radius: var(--radius);
  padding: 7px 10px; color: var(--charcoal);
  background: var(--bg); outline: none; resize: vertical;
  transition: border-color 0.15s;
}
.form-textarea:focus { border-color: var(--charcoal); }

.desc-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }

/* Images */
.image-list { display: flex; flex-wrap: wrap; gap: 10px; align-items: flex-start; }
.image-item {
  position: relative; width: 72px; height: 72px;
  border: 1.5px solid var(--border); border-radius: 4px;
  overflow: hidden; cursor: grab;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.image-item.drag-over {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px #f9a87566;
}
.image-thumb {
  width: 100%; height: 100%; object-fit: cover;
}
.image-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem; color: var(--light);
  background: var(--border);
}
.image-remove {
  position: absolute; top: 2px; right: 2px;
  background: rgba(0,0,0,0.55); color: #fff;
  border: none; border-radius: 50%;
  width: 18px; height: 18px; font-size: 0.75rem;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  line-height: 1;
}
.image-add {
  width: 72px; height: 72px;
  border: 1.5px dashed var(--border); border-radius: 4px;
  background: none; cursor: pointer;
  font-size: 1.5rem; color: var(--light);
  display: flex; align-items: center; justify-content: center;
  transition: border-color 0.15s, color 0.15s;
}
.image-add:hover { border-color: var(--charcoal); color: var(--charcoal); }

.hint { font-size: 0.72rem; color: var(--light); margin: 0; }

/* Save button */
.save-btn { margin-top: 8px; align-self: center; padding: 10px 40px; }

/* Modal */
.modal-title {
  font-family: var(--font-display);
  font-size: 1.05rem; font-weight: 600;
  color: var(--charcoal); margin-bottom: 20px;
}
.modal-actions {
  display: flex; justify-content: flex-end; gap: 10px;
  margin-top: 24px;
}
.translation-block {
  border-top: 1px solid var(--border);
  padding-top: 14px; margin-top: 10px;
  display: flex; flex-direction: column; gap: 4px;
}
.translation-locale {
  font-size: 0.75rem; font-weight: 600;
  color: var(--mid); text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Buttons */
.btn-primary {
  font-family: var(--font-body); font-size: 0.82rem; font-weight: 500;
  padding: 8px 22px;
  background: var(--charcoal); color: #fff;
  border: 1.5px solid var(--charcoal); border-radius: var(--radius);
  cursor: pointer; transition: opacity 0.15s;
}
.btn-primary:hover:not(:disabled) { opacity: 0.85; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-secondary {
  font-family: var(--font-body); font-size: 0.82rem; font-weight: 500;
  padding: 8px 22px;
  background: transparent; color: var(--charcoal);
  border: 1.5px solid var(--border); border-radius: var(--radius);
  cursor: pointer; transition: background 0.15s;
}
.btn-secondary:hover { background: var(--border); }

.loading { color: var(--mid); font-size: 0.85rem; padding: 20px 0; }

/* Transitions */
.slide-down-enter-active, .slide-down-leave-active { transition: all 0.2s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-6px); }

/* Pagination */
.pagination {
  display: flex; align-items: center; justify-content: center;
  gap: 6px; margin-top: 12px;
}
.page-btn {
  background: none; border: 1px solid var(--border); border-radius: 4px;
  padding: 3px 9px; cursor: pointer; font-size: 0.85rem; color: var(--charcoal);
  transition: background 0.15s;
}
.page-btn:hover:not(:disabled) { background: #f5f5f5; }
.page-btn:disabled { opacity: 0.35; cursor: default; }
.page-info { font-size: 0.85rem; color: var(--mid); min-width: 60px; text-align: center; }

/* Responsive */
@media (max-width: 700px) {
  .prices-grid { grid-template-columns: 1fr; }
  .desc-grid { grid-template-columns: 1fr; }
  .pickup-radio-group { flex-wrap: wrap; }
}

/* Marketing Modal */
.marketing-hint {
  font-size: 0.85rem; color: var(--mid); margin: 0 0 14px;
}
.marketing-product-list {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  max-height: 480px; overflow-y: auto;
  border: 1.5px solid var(--border); border-radius: var(--radius);
  padding: 10px;
}
@media (max-width: 600px) {
  .marketing-product-list { grid-template-columns: 1fr; }
}
.marketing-product-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: var(--radius);
  cursor: pointer; transition: background 0.12s;
  border: 1.5px solid transparent;
}
.marketing-product-item:hover { background: var(--bg); }
.marketing-product-item.selected {
  background: #fdf6ec;
  border-color: var(--gold, #c9a96e);
}
.marketing-checkbox {
  width: 15px; height: 15px; flex-shrink: 0;
  accent-color: var(--gold, #c9a96e); cursor: pointer;
}
.prod-thumb-cell {
  width: 40px; padding: 4px 6px;
}
.prod-table-thumb {
  width: 36px; height: 36px; object-fit: cover;
  border-radius: 4px; display: block;
}
.prod-name-cell {
  max-width: 120px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.prod-table-thumb-placeholder {
  width: 36px; height: 36px; border-radius: 4px;
  background: var(--border);
}
.marketing-thumb {
  width: 44px; height: 44px; object-fit: cover;
  border-radius: 4px; flex-shrink: 0;
}
.marketing-thumb-placeholder {
  width: 44px; height: 44px; border-radius: 4px;
  background: var(--border); flex-shrink: 0;
}
.marketing-prod-info {
  display: flex; flex-direction: column; gap: 2px;
}
.marketing-prod-name { font-size: 0.85rem; color: var(--charcoal); }
.marketing-prod-price { font-size: 0.8rem; color: var(--mid); }
.marketing-prod-date { font-size: 0.75rem; color: var(--accent); }
</style>
