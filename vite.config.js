/*
 * @Author: Christy qsa8647332@gmail.com
 * @Date: 2026-03-05 21:21:30
 * @LastEditors: Christy qsa8647332@gmail.com
 * @LastEditTime: 2026-03-05 19:29:15
 * @FilePath: \homefinds\vite.config.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  base: '/homefinds/',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
