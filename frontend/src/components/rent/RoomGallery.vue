<!--
 * @Author: Christy qsa8647332@gmail.com
 * @Date: 2026-03-16 23:38:15
 * @LastEditors: Christy qsa8647332@gmail.com
 * @LastEditTime: 2026-03-17 01:17:27
 * @FilePath: \homefinds\frontend\src\components\rent\RoomGallery.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="room-gallery">
    <template v-if="images && images.length">
      <img :src="images[current].url" :key="current" class="gallery-img" />
    </template>
    <div v-else class="gallery-placeholder">
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
import { ref, computed } from 'vue'
import { Home, ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps({ images: Array })
const totalSlides = computed(() => props.images?.length || 1)
const current = ref(0)
function prev() { current.value = (current.value - 1 + totalSlides.value) % totalSlides.value }
function next() { current.value = (current.value + 1) % totalSlides.value }
</script>

<style scoped>
.room-gallery {
  flex: 1; min-width: 260px;
  background: rgba(255,255,255,0.2);
  border-radius: 6px;
  position: relative; overflow: hidden;
  display: flex; align-items: center; justify-content: center;
}
.gallery-img {
  width: 100%; height: auto; display: block;
}
.gallery-placeholder {
  color: rgba(255,255,255,0.2);
  text-align: center;
  display: flex; flex-direction: column; align-items: center;
}
.gallery-label { font-size: 0.9rem; font-family: var(--font-body); margin-top: 8px; }
.gallery-nav {
  position: absolute; top: 50%; transform: translateY(-50%);
  background: rgba(0,0,0,0.15); border: none;
  color: #fff; width: 36px; height: 36px;
  border-radius: 50%; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.18s;
}
.gallery-nav:hover { background: rgba(0,0,0,0.3); }
.gallery-nav.left  { left: 12px; }
.gallery-nav.right { right: 12px; }
.gallery-dots {
  position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 6px;
}
.dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: rgba(0,0,0,0.35); cursor: pointer;
  transition: background 0.2s;
}
.dot.active { background: #fff; }
</style>
