-- 新增 admin_notes 欄位到 orders 表
-- 僅 admin 可讀取與編輯

ALTER TABLE orders
ADD COLUMN admin_notes TEXT NULL COMMENT '管理員備註（僅 admin 可讀寫）';
