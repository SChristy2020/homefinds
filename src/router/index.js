import { createRouter, createWebHistory } from 'vue-router'
import ShopView from '@/views/ShopView.vue'
import RentView from '@/views/RentView.vue'
import OrdersView from '@/views/OrdersView.vue'

const routes = [
  { path: '/',       name: 'shop',   component: ShopView },
  { path: '/rent',   name: 'rent',   component: RentView },
  { path: '/orders', name: 'orders', component: OrdersView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
