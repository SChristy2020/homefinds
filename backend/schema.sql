-- ─────────────────────────────────────────────
--  HomeFinds Database Schema
-- ─────────────────────────────────────────────

CREATE DATABASE IF NOT EXISTS homefinds
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE homefinds;

-- ─── 1. users ────────────────────────────────
CREATE TABLE users (
  id                 INT            NOT NULL AUTO_INCREMENT,
  first_name         VARCHAR(50)    NOT NULL,
  last_name          VARCHAR(50)    NOT NULL,
  salutation         VARCHAR(10)    NOT NULL,
  email              VARCHAR(100)   NOT NULL,
  phone              VARCHAR(20)    NOT NULL,
  zelle_refund       ENUM('phone','email','other') NOT NULL DEFAULT 'phone',
  zelle_refund_other VARCHAR(100)   NULL,
  has_purchase       TINYINT(1)     NOT NULL DEFAULT 0,
  has_reservation    TINYINT(1)     NOT NULL DEFAULT 0,
  is_admin           TINYINT(1)     NOT NULL DEFAULT 0,
  created_at         DATETIME       NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 2. categories ───────────────────────────
CREATE TABLE categories (
  id            INT         NOT NULL AUTO_INCREMENT,
  code_prefix   VARCHAR(10) NOT NULL,
  product_count INT         NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_categories_code_prefix (code_prefix)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 3. category_translations ────────────────
CREATE TABLE category_translations (
  id          INT          NOT NULL AUTO_INCREMENT,
  category_id INT          NOT NULL,
  locale      ENUM('en','zh-TW','zh-CN') NOT NULL,
  name        VARCHAR(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_category_locale (category_id, locale),
  CONSTRAINT fk_ct_category FOREIGN KEY (category_id)
    REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 4. products ─────────────────────────────
CREATE TABLE products (
  id                    INT            NOT NULL AUTO_INCREMENT,
  code                  VARCHAR(50)    NOT NULL,
  category              ENUM('Bedroom','Kitchen','Bathroom','Home & Misc') NOT NULL,
  price                 DECIMAL(10,2)  NOT NULL,
  original_price        DECIMAL(10,2)  NULL,
  status                ENUM('available','reserved','sold') NOT NULL DEFAULT 'available',
  pickup_available_time DATETIME       NULL,
  listed_date           DATE           NOT NULL,
  waiting_list_summary  JSON           NULL COMMENT '候補名單快照 [{"user_id":1,"name":"王小明","is_cancelled":false}]',
  created_at            DATETIME       NOT NULL DEFAULT NOW(),
  updated_at            DATETIME       NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (id),
  UNIQUE KEY uq_products_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 5. product_translations ─────────────────
CREATE TABLE product_translations (
  id          INT          NOT NULL AUTO_INCREMENT,
  product_id  INT          NOT NULL,
  locale      ENUM('en','zh-TW','zh-CN') NOT NULL,
  name        VARCHAR(100) NOT NULL,
  description TEXT         NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_product_locale (product_id, locale),
  CONSTRAINT fk_pt_product FOREIGN KEY (product_id)
    REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 6. product_images ───────────────────────
CREATE TABLE product_images (
  id          INT          NOT NULL AUTO_INCREMENT,
  product_id  INT          NOT NULL,
  url         VARCHAR(500) NOT NULL,
  sort_order  INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  CONSTRAINT fk_pi_product FOREIGN KEY (product_id)
    REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 7. orders ───────────────────────────────
CREATE TABLE orders (
  id           INT        NOT NULL AUTO_INCREMENT,
  order_number VARCHAR(20) NULL,
  user_id      INT        NOT NULL,
  order_status ENUM('pending_payment','paid','cancelled') NOT NULL DEFAULT 'pending_payment',
  paid_at      DATETIME   NULL,
  pickup_time  DATETIME   NULL,
  created_at   DATETIME   NOT NULL DEFAULT NOW(),
  updated_at   DATETIME   NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (id),
  UNIQUE KEY uq_orders_order_number (order_number),
  CONSTRAINT fk_orders_user FOREIGN KEY (user_id)
    REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 8. order_items ──────────────────────────
CREATE TABLE order_items (
  id           INT           NOT NULL AUTO_INCREMENT,
  order_id     INT           NOT NULL,
  product_id   INT           NOT NULL,
  price        DECIMAL(10,2) NOT NULL,
  status       ENUM('reserved','cancelled','paid') NOT NULL DEFAULT 'reserved',
  cancelled_at DATETIME      NULL,
  updated_at   DATETIME      NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (id),
  CONSTRAINT fk_oi_order   FOREIGN KEY (order_id)   REFERENCES orders(id)   ON DELETE CASCADE,
  CONSTRAINT fk_oi_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 9. waiting_list ─────────────────────────
CREATE TABLE waiting_list (
  id           INT       NOT NULL AUTO_INCREMENT,
  product_id   INT       NOT NULL,
  user_id      INT       NOT NULL,
  position     INT       NOT NULL,
  is_cancelled TINYINT(1) NOT NULL DEFAULT 0,
  created_at   DATETIME  NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id),
  CONSTRAINT fk_wl_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  CONSTRAINT fk_wl_user    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 10. reservations ────────────────────────
CREATE TABLE reservations (
  id             INT           NOT NULL AUTO_INCREMENT,
  user_id        INT           NOT NULL,
  check_in       DATE          NOT NULL,
  check_out      DATE          NOT NULL,
  nights         INT           NOT NULL,
  deposit_paid   TINYINT(1)    NOT NULL DEFAULT 0,
  deposit_amount DECIMAL(10,2) NOT NULL,
  total_price    DECIMAL(10,2) NOT NULL,
  fully_paid     TINYINT(1)    NOT NULL DEFAULT 0,
  created_at     DATETIME      NOT NULL DEFAULT NOW(),
  updated_at     DATETIME      NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (id),
  CONSTRAINT fk_res_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 11. room ────────────────────────────────
CREATE TABLE room (
  id                INT           NOT NULL AUTO_INCREMENT,
  available_from    DATE          NOT NULL,
  available_to      DATE          NOT NULL,
  price_per_night   DECIMAL(10,2) NOT NULL,
  price_7_nights    DECIMAL(10,2) NULL COMMENT '7 晚優惠價',
  price_30_days     DECIMAL(10,2) NULL COMMENT '30 天優惠價',
  price_full_period DECIMAL(10,2) NULL COMMENT '整段開放日期全租價',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 12. room_translations ───────────────────
CREATE TABLE room_translations (
  id                  INT          NOT NULL AUTO_INCREMENT,
  room_id             INT          NOT NULL,
  locale              ENUM('en','zh-TW','zh-CN') NOT NULL,
  description         TEXT         NULL    COMMENT '房間描述',
  booking_description TEXT         NULL    COMMENT '預定描述',
  PRIMARY KEY (id),
  UNIQUE KEY uq_room_locale (room_id, locale),
  CONSTRAINT fk_rt_room FOREIGN KEY (room_id)
    REFERENCES room(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ─── 13. room_images ─────────────────────────
CREATE TABLE room_images (
  id         INT          NOT NULL AUTO_INCREMENT,
  room_id    INT          NOT NULL,
  url        VARCHAR(500) NOT NULL,
  sort_order INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  CONSTRAINT fk_ri_room FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
