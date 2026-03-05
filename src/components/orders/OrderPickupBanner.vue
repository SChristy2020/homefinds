<template>
  <div class="pickup-banner">
    <div class="pickup-row">
      <span class="pickup-time">
        預計取貨時間: <strong>{{ order.pickupTime }}</strong>
      </span>
      <button class="btn-notify" @click="$emit('notify')">Notify Christy</button>
    </div>
    <p class="pickup-note">Christy將會在你到達前把東西準備好! 謝謝!</p>
  </div>
</template>

<script setup>
defineProps({ order: Object })
defineEmits(['notify'])
</script>

<style scoped>
.pickup-banner {
  background: var(--warm-white); border: 1.5px solid var(--border);
  border-radius: var(--radius); padding: 16px 20px; margin-bottom: 20px;
}
.pickup-row { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; }
.pickup-time { font-size: 0.88rem; }
.pickup-time strong { font-size: 1rem; }
.pickup-note { font-size: 0.78rem; color: var(--mid); margin-top: 6px; }
.btn-notify {
  padding: 7px 16px; background: var(--charcoal); color: #fff;
  border: none; border-radius: var(--radius); font-size: 0.8rem;
  font-family: var(--font-body); cursor: pointer; transition: background 0.18s;
}
.btn-notify:hover { background: var(--accent); }
</style>
