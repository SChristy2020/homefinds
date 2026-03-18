ALTER TABLE users
  ADD COLUMN birth_year  SMALLINT     NULL AFTER phone,
  ADD COLUMN occupation  VARCHAR(100) NULL AFTER birth_year;
