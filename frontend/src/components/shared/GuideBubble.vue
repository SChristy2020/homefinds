<template>
  <div class="guide-bubble-wrapper">
    <div class="guide-bubble" @click="open = true" :title="i18n.t('guide.title')">
      <BookOpen :size="20" />
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
            <div class="guide-body">
              <section class="guide-section">
                <h3>{{ i18n.t('guide.sectionTitle') }}</h3>

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
                    <li>{{ i18n.t('guide.step2Items')[0] }}</li>
                    <li>{{ i18n.t('guide.step2Items')[1] }}</li>
                    <li>
                      {{ i18n.t('guide.step2PayLabel') }}
                      <div class="zelle-info">
                        <span>{{ i18n.t('guide.zelleAccount') }}</span>
                        <span>{{ i18n.t('guide.zelleName') }}</span>
                      </div>
                    </li>
                    <li>{{ i18n.t('guide.step2Items')[2] }}</li>
                    <li>{{ i18n.t('guide.step2Items')[3] }}</li>
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
              </section>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { BookOpen, X } from 'lucide-vue-next'
import { useI18nStore } from '@/stores/i18n'

const i18n = useI18nStore()
const open = ref(false)
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
  background: var(--charcoal);
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

.guide-body {
  overflow-y: auto;
  padding: 20px 24px 24px;
}

.guide-section h3 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--charcoal);
  margin: 0 0 16px;
}

.guide-step {
  margin-bottom: 20px;
}

.guide-step h4 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--accent, #c9a96e);
  margin: 0 0 8px;
}

.guide-step p {
  font-size: 0.88rem;
  color: #555;
  margin: 0 0 6px;
}

.guide-step ul {
  margin: 0;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.guide-step li {
  font-size: 0.88rem;
  color: #444;
  line-height: 1.55;
}

.guide-step li.warning {
  color: #c0392b;
  font-weight: 600;
  list-style: none;
  margin-left: -18px;
}

.zelle-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 4px;
  padding: 8px 12px;
  background: #f9f7f4;
  border-radius: 8px;
  font-size: 0.88rem;
  color: var(--charcoal);
  font-weight: 600;
}

.guide-contact {
  font-size: 0.88rem;
  color: #555;
  margin: 4px 0 0;
  padding-top: 12px;
  border-top: 1px solid #f0ede8;
}

.guide-contact a {
  color: var(--accent, #c9a96e);
  text-decoration: none;
}
.guide-contact a:hover { text-decoration: underline; }

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
