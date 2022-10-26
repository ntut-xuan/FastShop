INSERT INTO `user` (uid, email, password, firstname, lastname, sex, birthday)
VALUES (
    0,
    'test@email.com',
    -- test
    'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff',
    'Huang',
    'Han-Xuan',
    0,
    1666604387
  ),
  (
    1,
    'other@email.com',
    -- other
    '82a5cfd03cdcb713c8d7dfce41e6f0a92f6dc560e6dda56c11eb1a207aaa7689b07a1de30967fc040f8b0ef0672c1c2ad96fcacb95fb995f52ae5d657c094547',
    'Uriah',
    'Xuan',
    0,
    1666604387
  );


CREATE TABLE `test_table` (
  account TEXT PRIMARY KEY,
  password TEXT NOT NULL
);

INSERT INTO `test_table` (`account`, `password`)
  VALUES ('my_account', '#my_password'),
    ('other_account', '#other_password');
