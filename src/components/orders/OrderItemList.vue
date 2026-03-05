<template>
  <div>
    <div class="list-label">這些是你的 orders:</div>
    <div v-if="order.items.length === 0" class="empty-state">
      <div class="empty-state-icon">📦</div>
      <p>目前沒有訂單</p>
    </div>
    <div v-else class="items-grid">
      <div v-for="item in order.items" :key="item.id" class="item-card">
        <div class="item-img"></div>
        <div class="item-price">
          <span v-if="item.originalPrice" class="strikethrough" style="font-size:0.7rem;">${{ item.originalPrice }}</span>
          ${{ item.price }}
        </div>
        <button class="btn-danger" @click="$emit('cancel', item.id)">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ order: Object })
defineEmits(['cancel'])
</script>

<style scoped>
.list-label { font-size: 0.88rem; font-weight: 600; margin-bottom: 14px; }
.items-grid { display: flex; gap: 14px; flex-wrap: wrap; }
.item-card {
  border: 1.5px solid var(--border); border-radius: var(--radius);
  padding: 10px; text-align: center; width: 120px;
  background: var(--warm-white);
}
.item-img {
  width: 80px; height: 80px; margin: 0 auto 6px;
  background: linear-gradient(135deg, #2a2a2a 0%, #4a4040 100%);
  border-radius: 3px;
}
.item-price { font-size: 0.85rem; font-weight: 600; margin-bottom: 6px; }
</style>
