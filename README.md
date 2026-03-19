# Christy's Home Finds

二手物品拍賣 + 房間租賃系統，使用 Vue 3 + Vite + Pinia + Vue Router 建置。

## 🚀 快速開始

```bash
# 安裝依賴
npm install

# 開發模式
npm run dev

# 打包
npm run build
```

## 📁 資料夾結構

```
christy-home-finds/
├── index.html
├── vite.config.js
├── package.json
├── public/
│   └── favicon.svg
└── src/
    ├── main.js                    # App 入口
    ├── App.vue                    # 根元件 (Header + RouterView + Toast)
    ├── assets/
    │   └── main.css               # 全域 CSS 變數與 Utility Classes
    ├── router/
    │   └── index.js               # Vue Router 路由設定
    ├── stores/                    # Pinia 狀態管理
    │   ├── cart.js                # 購物車 (add / remove / clear)
    │   ├── orders.js              # 訂單 & Waiting List
    │   ├── products.js            # 商品資料
    │   └── toast.js               # 全域 Toast 通知
    ├── views/                     # 頁面層元件
    │   ├── ShopView.vue           # Shop 主頁
    │   ├── RentView.vue           # Room for Rent 頁
    │   └── OrdersView.vue         # My Orders 頁
    └── components/
        ├── shared/                # 共用元件
        │   ├── AppHeader.vue      # 頂部導覽列
        │   ├── BaseModal.vue      # 可重用 Modal 框架
        │   └── ToastNotification.vue
        ├── shop/                  # Shop 相關元件
        │   ├── ProductGrid.vue    # 商品格線
        │   ├── ProductCard.vue    # 單一商品卡片
        │   ├── ProductDetailModal.vue  # 商品詳情跳窗
        │   ├── CartBubble.vue     # 右下角購物車按鈕
        │   ├── CartModal.vue      # 購物車 & 結帳跳窗
        │   └── OrderSuccessModal.vue   # 預訂成功跳窗
        ├── rent/                  # Room for Rent 相關元件
        │   ├── RoomGallery.vue    # 房間圖片輪播
        │   ├── RentCalendar.vue   # 日曆選日元件
        │   ├── RentConfirmModal.vue    # 預約確認跳窗
        │   └── RentSuccessModal.vue    # 預約成功跳窗
        └── orders/                # My Orders 相關元件
            ├── OrderPickupBanner.vue   # 取貨資訊橫幅
            └── OrderItemList.vue       # 訂單物品列表
```

## 🏗 技術架構

| 技術 | 用途 |
|------|------|
| Vue 3 (Composition API) | UI 框架 |
| Vite | 開發 / 打包工具 |
| Pinia | 全域狀態管理 |
| Vue Router 4 | SPA 路由 |

## 📦 Stores 說明

- **`cart.js`** — 購物車 items、total、count，提供 add / remove / clear / has
- **`orders.js`** — 儲存所有訂單與各商品的 waiting list；提供 addOrder / cancelItem / findOrder / getWaitingList
- **`products.js`** — 商品資料來源；提供 getByCategory / search / markSoldOut
- **`toast.js`** — 輕量全域 Toast；呼叫 `toast.show('訊息')` 即可

## 🔌 元件溝通模式

- **Props / Emits** — 父子元件資料傳遞
- **provide / inject** — ShopView 向深層子元件提供 `openCartModal()` 與 `onOrderSuccess()`
- **Pinia** — 跨元件共享狀態（購物車、訂單、Toast）
