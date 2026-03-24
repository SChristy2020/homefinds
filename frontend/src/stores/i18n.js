import { defineStore } from 'pinia'
import { ref } from 'vue'
import en from '@/locales/en'
import zhTW from '@/locales/zh-TW'
import zhCN from '@/locales/zh-CN'

const messages = { en, 'zh-TW': zhTW, 'zh-CN': zhCN }

const STORAGE_KEY = 'homefinds_locale'
const SUPPORTED = ['en', 'zh-TW', 'zh-CN']

function getSavedLocale() {
  const saved = localStorage.getItem(STORAGE_KEY)
  return SUPPORTED.includes(saved) ? saved : 'en'
}

export const useI18nStore = defineStore('i18n', () => {
  const locale = ref(getSavedLocale())

  function setLocale(lang) {
    locale.value = lang
    localStorage.setItem(STORAGE_KEY, lang)
  }

  function t(key, params = {}) {
    const msgs = messages[locale.value]
    const keys = key.split('.')
    let val = msgs
    for (const k of keys) val = val?.[k]
    if (Array.isArray(val)) return val
    if (typeof val === 'string') {
      return val.replace(/\{(\w+)\}/g, (_, k) => params[k] ?? '')
    }
    return val ?? key
  }

  return { locale, setLocale, t }
})
