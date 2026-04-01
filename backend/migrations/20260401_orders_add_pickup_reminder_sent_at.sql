ALTER TABLE orders
  ADD COLUMN pickup_reminder_sent_at DATETIME NULL AFTER pickup_time;
