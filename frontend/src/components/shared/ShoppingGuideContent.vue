<template>
  <div class="guide-content">
    <h3 class="guide-content-title">{{ i18n.t('guide.sectionTitle') }}</h3>

    <div class="guide-step">
      <h4>{{ i18n.t('guide.step1Title') }}</h4>
      <ul>
        <li v-for="(item, i) in i18n.t('guide.step1Items')" :key="i">{{ item }}</li>
        <li class="warning">{{ i18n.t('guide.step1Warning') }}</li>
      </ul>
    </div>

    <div class="guide-step">
      <h4>{{ i18n.t('guide.step2Title') }}</h4>
      <p>{{ i18n.t('guide.step2Intro') }}</p>
      <ul>
        <li v-for="(item, i) in i18n.t('guide.step2Items').slice(0, 2)" :key="i">{{ item }}</li>
        <li>
          {{ i18n.t('guide.step2PayLabel') }}
          <div class="zelle-info">
            <span>{{ i18n.t('guide.zelleAccount') }}</span>
            <span>{{ i18n.t('guide.zelleName') }}</span>
          </div>
        </li>
        <li v-for="(item, i) in i18n.t('guide.step2Items').slice(2)" :key="'b'+i">{{ item }}</li>
      </ul>
    </div>

    <div class="guide-step">
      <h4>{{ i18n.t('guide.step3Title') }}</h4>
      <ul>
        <li v-for="(item, i) in i18n.t('guide.step3Items')" :key="i">{{ item }}</li>
      </ul>
    </div>

    <p class="guide-contact">
      {{ i18n.t('guide.contact') }}
      <a href="mailto:qsa8647332@gmail.com">qsa8647332@gmail.com</a>
    </p>
  </div>
</template>

<script setup>
import { useI18nStore } from '@/stores/i18n'
const i18n = useI18nStore()
</script>

<style scoped>
.guide-content { font-size: 0.83rem; }
.guide-content-title {
  font-size: 0.92rem; font-weight: 700;
  color: var(--charcoal); margin: 0 0 12px;
}
.guide-step { margin-bottom: 12px; }
.guide-step h4 {
  font-size: 0.88rem; font-weight: 700;
  color: var(--accent, #c9a96e); margin: 0 0 6px;
}
.guide-step p { font-size: 0.82rem; color: #555; margin: 0 0 4px; }
.guide-step ul {
  margin: 0; padding-left: 18px;
  display: flex; flex-direction: column; gap: 4px;
}
.guide-step li { font-size: 0.82rem; color: #444; line-height: 1.5; }
.guide-step li.warning {
  color: #c0392b; font-weight: 600;
  list-style: none; margin-left: -18px;
}
.zelle-info {
  display: flex; flex-direction: column; gap: 2px;
  margin-top: 4px; padding: 6px 10px;
  background: #f9f7f4; border-radius: 6px;
  font-weight: 600; color: var(--charcoal);
}
.guide-contact {
  font-size: 0.82rem; color: #555;
  margin: 8px 0 0; padding-top: 10px;
  border-top: 1px solid #dde5ef;
}
.guide-contact a { color: var(--accent, #c9a96e); text-decoration: none; }
.guide-contact a:hover { text-decoration: underline; }
</style>
