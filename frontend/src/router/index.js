/*
 * @Author: Christy qsa8647332@gmail.com
 * @Date: 2026-03-05 21:21:42
 * @LastEditors: Christy qsa8647332@gmail.com
 * @LastEditTime: 2026-03-05 21:33:10
 * @FilePath: \homefinds\src\router\index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import { createRouter, createWebHashHistory } from 'vue-router'
import ShopView from '@/views/ShopView.vue'
import RentView from '@/views/RentView.vue'
import OrdersView from '@/views/OrdersView.vue'
import AdminView from '@/views/AdminView.vue'

const routes = [
  { path: '/',       name: 'shop',   component: ShopView },
  { path: '/rent',   name: 'rent',   component: RentView },
  { path: '/orders', name: 'orders', component: OrdersView },
  { path: '/admin',  name: 'admin',  component: AdminView },
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL), //正確引導到 homefinds/
  routes,
})

router.afterEach((to) => {
  if (window.gtag) {
    window.gtag('event', 'page_view', {
      page_title: document.title,
      page_location: window.location.href,
      page_path: to.fullPath,
    })
  }
})

export default router
