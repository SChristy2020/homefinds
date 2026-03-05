import { defineStore } from 'pinia'
import { ref } from 'vue'
import en from '@/locales/en'
import zhTW from '@/locales/zh-TW'
import zhCN from '@/locales/zh-CN'

const messages = { en, 'zh-TW': zhTW, 'zh-CN': zhCN }

export const useI18nStore = defineStore('i18n', () => {
  const locale = ref('zh-TW')

  function setLocale(lang) {
    locale.value = lang
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
