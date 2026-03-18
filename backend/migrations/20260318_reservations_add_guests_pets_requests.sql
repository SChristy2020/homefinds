ALTER TABLE reservations
  ADD COLUMN has_guests_or_pets      TINYINT(1) NOT NULL DEFAULT 0 AFTER fully_paid,
  ADD COLUMN guests_pets_description TEXT       NULL     AFTER has_guests_or_pets,
  ADD COLUMN special_requests        TEXT       NULL     AFTER guests_pets_description;
