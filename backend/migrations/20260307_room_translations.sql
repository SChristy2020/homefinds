-- ─────────────────────────────────────────────
--  Migration: room_translations
--  Date: 2026-03-07
--  描述: 將 room.description 移至 room_translations，
--        並新增多語系「預訂描述」欄位
-- ─────────────────────────────────────────────

USE homefinds;

-- 1. 移除 room 表的 description 欄位
ALTER TABLE room
  DROP COLUMN description;

-- 2. 建立 room_translations 表
CREATE TABLE room_translations (
  id                  INT          NOT NULL AUTO_INCREMENT,
  room_id             INT          NOT NULL,
  locale              ENUM('en','zh-TW','zh-CN') NOT NULL,
  description         TEXT         NULL    COMMENT '房間描述',
  booking_description TEXT         NULL    COMMENT '預訂描述',
  PRIMARY KEY (id),
  UNIQUE KEY uq_room_locale (room_id, locale),
  CONSTRAINT fk_rt_room FOREIGN KEY (room_id)
    REFERENCES room(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
