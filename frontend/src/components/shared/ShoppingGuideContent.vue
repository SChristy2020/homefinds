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
        <li>
          {{ i18n.t('guide.step3LocationLabel') }}
          <a class="location-info" href="https://maps.app.goo.gl/HiHjmGr1PLTvgbex9" target="_blank" rel="noopener">
            <span class="location-name">{{ i18n.t('guide.step3LocationName') }}</span>
            <span class="location-address">{{ i18n.t('guide.step3LocationAddress') }}</span>
          </a>
        </li>
      </ul>
      <img src="/images/pickup-location.jpg" alt="Pickup Location" class="pickup-map-img" />
      <iframe
        class="pickup-map-iframe"
        src="https://maps.google.com/maps?q=2031+Honeycutt+Dr+Suite+1100,+Durham,+NC+27707&output=embed"
        allowfullscreen
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
      ></iframe>
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
.guide-content { font-size: .9rem; }
.guide-content-title {
  font-size: 1.2rem; font-weight: 700;
  color: var(--charcoal); margin: 0 0 12px;
}
.guide-step { margin-bottom: 12px; }
.guide-step h4 {
  font-size: 1rem; font-weight: 700;
  color: var(--accent, #c9a96e); margin: 0 0 6px;
}
.guide-step p { font-size: 0.9rem; color: #555; margin: 0 0 4px; }
.guide-step ul {
  margin: 0; padding-left: 18px;
  display: flex; flex-direction: column; gap: 4px;
}
.guide-step li { font-size: 0.9rem; color: #444; line-height: 1.5; }
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
  font-size: 0.9rem; color: #555;
  margin: 8px 0 0; padding-top: 10px;
  border-top: 1px solid #dde5ef;
}
.guide-contact a { color: var(--accent, #c9a96e); text-decoration: none; }
.guide-contact a:hover { text-decoration: underline; }
.location-info {
  display: flex; flex-direction: column; gap: 2px;
  margin-top: 4px; padding: 6px 10px;
  background: #f9f7f4; border-radius: 6px;
}
.location-info { color: inherit; text-decoration: none; }
.location-info:hover .location-name { text-decoration: underline; }
.location-name { font-weight: 600; color: var(--accent, #c9a96e); }
.location-address { font-size: 0.78rem; color: #666; }
.pickup-map-img {
  width: 100%; max-width: 360px;
  margin: 8px auto 0; border-radius: 8px;
  display: block;
}
.pickup-map-iframe {
  width: 100%; height: 200px;
  margin-top: 8px; border-radius: 8px;
  border: none; display: block;
}
</style>
