-- syntax of SQLite

CREATE TABLE IF NOT EXISTS `user` (
  `uid` INTEGER PRIMARY KEY AUTOINCREMENT,
  `email` TEXT NOT NULL,
  `password` TEXT NOT NULL,
  `firstname` TEXT NOT NULL,
  `lastname` TEXT NOT NULL,
  `gender` INT NOT NULL,
  `birthday` INT NOT NULL
);
