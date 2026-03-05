<template>
  <div class="room-gallery">
    <div class="gallery-placeholder">
      <Home :size="40" />
      <div class="gallery-label">Room Photos</div>
    </div>
    <button class="gallery-nav left" @click="prev"><ChevronLeft :size="18" /></button>
    <button class="gallery-nav right" @click="next"><ChevronRight :size="18" /></button>
    <div class="gallery-dots">
      <span
        v-for="i in totalSlides"
        :key="i"
        class="dot"
        :class="{ active: current === i - 1 }"
        @click="current = i - 1"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Home, ChevronLeft, ChevronRight } from 'lucide-vue-next'
const totalSlides = 4
const current = ref(0)
function prev() { current.value = (current.value - 1 + totalSlides) % totalSlides }
function next() { current.value = (current.value + 1) % totalSlides }
</script>

<style scoped>
.room-gallery {
  flex: 1; min-width: 260px;
  background: linear-gradient(135deg, #1a1a1a 0%, #2e2e2e 100%);
  border-radius: 6px; min-height: 320px;
  position: relative; overflow: hidden;
  display: flex; align-items: center; justify-content: center;
}
.gallery-placeholder {
  color: rgba(255,255,255,0.2);
  text-align: center;
  display: flex; flex-direction: column; align-items: center;
}
.gallery-label { font-size: 0.9rem; font-family: var(--font-body); margin-top: 8px; }
.gallery-nav {
  position: absolute; top: 50%; transform: translateY(-50%);
  background: rgba(255,255,255,0.15); border: none;
  color: #fff; width: 36px; height: 36px;
  border-radius: 50%; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.18s;
}
.gallery-nav:hover { background: rgba(255,255,255,0.3); }
.gallery-nav.left  { left: 12px; }
.gallery-nav.right { right: 12px; }
.gallery-dots {
  position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 6px;
}
.dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: rgba(255,255,255,0.35); cursor: pointer;
  transition: background 0.2s;
}
.dot.active { background: #fff; }
</style>
