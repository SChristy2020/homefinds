<template>
  <div class="lang-bubble-wrapper">
    <div class="lang-bubble" @click.stop="toggle">
      <Languages :size="20" />
    </div>
    <transition name="fade-up">
      <div v-if="open" class="lang-menu" @click.stop>
        <button
          v-for="lang in langs"
          :key="lang.code"
          class="lang-option"
          :class="{ active: i18n.locale === lang.code }"
          @click="select(lang.code)"
        >
          <span class="lang-flag">{{ lang.flag }}</span>
          {{ lang.label }}
        </button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Languages } from 'lucide-vue-next'
import { useI18nStore } from '@/stores/i18n'

const i18n = useI18nStore()
const open = ref(false)

const langs = [
  { code: 'zh-TW', label: '繁體中文', flag: '🇹🇼' },
  { code: 'zh-CN', label: '简体中文', flag: '🇨🇳' },
  { code: 'en',    label: 'English',  flag: '🇺🇸' },
]

function toggle() { open.value = !open.value }
function select(code) { i18n.setLocale(code); open.value = false }
function close() { open.value = false }

onMounted(() => document.addEventListener('click', close))
onUnmounted(() => document.removeEventListener('click', close))
</script>

<style scoped>
.lang-bubble-wrapper {
  position: fixed;
  bottom: 96px;
  right: 32px;
  z-index: 200;
}

.lang-bubble {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--charcoal);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  transition: transform 0.2s, background 0.2s;
}
.lang-bubble:hover { transform: scale(1.08); background: var(--accent); }
.lang-bubble svg { display: block; }

.lang-menu {
  position: absolute;
  bottom: 60px;
  right: 0;
  background: #fff;
  border-radius: 12px;
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  min-width: 148px;
}

.lang-option {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 10px 16px;
  border: none;
  background: transparent;
  font-size: 0.9rem;
  color: var(--charcoal);
  cursor: pointer;
  transition: background 0.15s;
  text-align: left;
}
.lang-option:hover { background: var(--cream); }
.lang-option.active { font-weight: 700; color: var(--accent); }

.lang-flag { font-size: 1rem; }

.fade-up-enter-active,
.fade-up-leave-active { transition: opacity 0.15s, transform 0.15s; }
.fade-up-enter-from,
.fade-up-leave-to { opacity: 0; transform: translateY(8px); }
</style>
