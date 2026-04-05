ALTER TABLE orders
  ADD COLUMN pre_booking_reminder_sent_at DATETIME NULL AFTER pickup_reminder_sent_at;

ALTER TABLE order_items
  ADD COLUMN current_position INT NULL AFTER price;
