ALTER TABLE reservations
  ADD COLUMN original_price   DECIMAL(10,2) NULL AFTER total_price,
  ADD COLUMN special_price    DECIMAL(10,2) NULL AFTER original_price,
  ADD COLUMN early_bird_price DECIMAL(10,2) NULL AFTER special_price,
  ADD COLUMN is_early_bird    TINYINT(1)    NOT NULL DEFAULT 0 AFTER early_bird_price;
