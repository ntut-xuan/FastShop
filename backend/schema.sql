CREATE TABLE IF NOT EXISTS `user` (
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
)
