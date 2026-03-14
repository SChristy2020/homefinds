ALTER TABLE order_items
  MODIFY COLUMN status ENUM('reserved', 'cancelled', 'paid', 'sold') NOT NULL DEFAULT 'reserved',
  ADD COLUMN sold_at DATETIME NULL;
