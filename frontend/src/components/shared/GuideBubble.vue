<template>
  <div class="guide-bubble-wrapper">
    <div class="guide-bubble" @click="open = true" :title="i18n.t('guide.title')">
      <HelpCircle :size="22" />
    </div>

    <Teleport to="body">
      <transition name="modal-fade">
        <div v-if="open" class="guide-overlay" @click.self="open = false">
          <div class="guide-modal">
            <div class="guide-header">
              <h2 class="guide-title">{{ i18n.t('guide.title') }}</h2>
              <button class="guide-close" @click="open = false">
                <X :size="20" />
              </button>
            </div>

            <!-- Tabs -->
            <div class="guide-tabs">
              <button
                class="guide-tab"
                :class="{ active: activeTab === 'shopping' }"
                @click="activeTab = 'shopping'"
              >{{ i18n.t('guide.sectionTitle') }}</button>
              <button
                class="guide-tab"
                :class="{ active: activeTab === 'rent' }"
                @click="activeTab = 'rent'"
              >{{ i18n.t('guide.rentSectionTitle') }}</button>
            </div>

            <div class="guide-body">
              <ShoppingGuideContent v-if="activeTab === 'shopping'" />
              <template v-else>
                <div v-if="roomBookingDescription" class="rent-guide-content" v-html="roomBookingDescription"></div>
                <p v-else class="rent-guide-empty">{{ i18n.t('guide.rentGuideEmpty') }}</p>
              </template>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { HelpCircle, X } from 'lucide-vue-next'
import ShoppingGuideContent from '@/components/shared/ShoppingGuideContent.vue'
import { useI18nStore } from '@/stores/i18n'
import { api } from '@/utils/api'

const i18n = useI18nStore()
const open = ref(false)
const activeTab = ref('shopping')
const roomBookingMap = ref({})
const roomBookingDescription = computed(() =>
  roomBookingMap.value[i18n.locale] || roomBookingMap.value['zh-TW'] || ''
)

onMounted(async () => {
  try {
    const rooms = await api.get('/api/room')
    if (rooms.length) {
      const map = {}
      for (const t of (rooms[0].translations || [])) {
        map[t.locale] = t.booking_description || ''
      }
      roomBookingMap.value = map
    }
  } catch {}
})
</script>

<style scoped>
.guide-bubble-wrapper {
  position: fixed;
  bottom: 160px;
  right: 32px;
  z-index: 200;
}

.guide-bubble {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--button);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  transition: transform 0.2s, background 0.2s;
}
.guide-bubble:hover { transform: scale(1.08); background: var(--accent); }
.guide-bubble svg { display: block; }

/* Overlay */
.guide-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.guide-modal {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 540px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.guide-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
  border-bottom: 1px solid #f0ede8;
  flex-shrink: 0;
}

.guide-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--charcoal);
  margin: 0;
}

.guide-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #f5f3ef;
  color: var(--charcoal);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
  flex-shrink: 0;
}
.guide-close:hover { background: #ebe8e2; }

/* Tabs */
.guide-tabs {
  display: flex;
  border-bottom: 1.5px solid #f0ede8;
  flex-shrink: 0;
}
.guide-tab {
  flex: 1;
  background: none;
  border: none;
  border-bottom: 2.5px solid transparent;
  margin-bottom: -1.5px;
  padding: 10px 12px;
  font-size: .9rem;
  font-weight: 600;
  color: var(--mid);
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s;
  white-space: nowrap;
  text-align: center;
}
.guide-tab:hover { color: var(--charcoal); }
.guide-tab.active {
  color: var(--charcoal);
  border-bottom-color: var(--accent, #c9a96e);
}

.guide-body {
  overflow-y: auto;
  padding: 20px 24px 24px;
}

.rent-guide-content { font-size: .9rem; color: #444; line-height: 1.6; }
.rent-guide-content :deep(ul), .rent-guide-content :deep(ol) { padding-left: 1.5em; }
.rent-guide-content :deep(ul) { list-style-type: disc; }
.rent-guide-content :deep(ol) { list-style-type: decimal; }
.rent-guide-content :deep(ul ul) { list-style-type: circle; }
.rent-guide-content :deep(ul ul ul) { list-style-type: square; }
.rent-guide-content :deep(blockquote) { margin-left: 1.5em; padding-left: 0.75em; border-left: 3px solid var(--border); }
.rent-guide-content :deep(iframe) { width: 100% !important; max-width: 100%; height: 320px; border: none; border-radius: 6px; display: block; margin: 8px 0; }
.rent-guide-content :deep(.map-embed) { width: 100%; }
.rent-guide-empty { font-size: 0.82rem; color: var(--mid); font-style: italic; }

/* Modal transition */
.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.2s; }
.modal-fade-enter-from,
.modal-fade-leave-to { opacity: 0; }
.modal-fade-enter-active .guide-modal,
.modal-fade-leave-active .guide-modal { transition: transform 0.2s; }
.modal-fade-enter-from .guide-modal,
.modal-fade-leave-to .guide-modal { transform: translateY(12px); }
</style>
