-- Move birth_year and occupation from users to reservations

ALTER TABLE reservations
  ADD COLUMN birth_year INT          NULL AFTER special_requests,
  ADD COLUMN occupation  VARCHAR(100) NULL AFTER birth_year;

ALTER TABLE users
  DROP COLUMN birth_year,
  DROP COLUMN occupation;
