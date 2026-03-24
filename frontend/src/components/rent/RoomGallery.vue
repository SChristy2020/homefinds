<!--
 * @Author: Christy qsa8647332@gmail.com
 * @Date: 2026-03-16 23:38:15
 * @LastEditors: Christy qsa8647332@gmail.com
 * @LastEditTime: 2026-03-24 12:59:42
 * @FilePath: \homefinds\frontend\src\components\rent\RoomGallery.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="room-gallery">
    <template v-if="images && images.length">
      <Carousel v-model="current" :wrap-around="true" snap-align="center" class="room-carousel">
        <Slide v-for="(img, i) in images" :key="i">
          <img :src="img.url" class="gallery-img" />
        </Slide>
      </Carousel>
      <div v-if="images.length > 1" class="gallery-dots">
        <span
          v-for="(_, i) in images"
          :key="i"
          class="dot"
          :class="{ active: i === current }"
          @click="current = i"
        />
      </div>
    </template>
    <div v-else class="gallery-placeholder">
      <Home :size="40" />
      <div class="gallery-label">Room Photos</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Home } from 'lucide-vue-next'
import { Carousel, Slide } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'

const props = defineProps({ images: Array })
const current = ref(0)
</script>

<style scoped>
.room-gallery {
  flex: 1; min-width: 260px;
  background: rgba(255,255,255,0.2);
  border-radius: 6px;
  position: relative; overflow: hidden;
}
.room-carousel {
  width: 100%; height: 100%;
}
.gallery-img {
  width: 100%; height: 100%; object-fit: cover; display: block;
}
.gallery-placeholder {
  color: rgba(255,255,255,0.2);
  text-align: center;
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; height: 100%; padding: 40px 0;
}
.gallery-label { font-size: 0.9rem; font-family: var(--font-body); margin-top: 8px; }
.gallery-dots {
  position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 6px; z-index: 2;
}
.dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: rgba(0,0,0,0.35); cursor: pointer;
  transition: background 0.2s;
}
.dot.active { background: #fff; }
</style>
