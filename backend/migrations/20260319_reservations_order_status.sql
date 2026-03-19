-- 移除舊的付款狀態欄位，新增統一訂單狀態欄位
ALTER TABLE reservations
  DROP COLUMN deposit_paid,
  DROP COLUMN fully_paid,
  ADD COLUMN order_status ENUM('待付訂金', '待入住', '已入住', '已退房', '已取消')
    NOT NULL DEFAULT '待付訂金'
    AFTER is_early_bird;
