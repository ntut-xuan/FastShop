INSERT INTO `user` (`email`, `password`, `firstname`, `lastname`, `gender`, `birthday`)
VALUES (
    'test@email.com',
    -- test
    'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff',
    'Han-Xuan',
    'Huang',
    0,
    1024963200  -- 2002-06-25 00:00:00
  ),
  (
    'other@email.com',
    -- other
    'e25ac3845f8cbe12801a2dfa5a89d4c55dc47900f3b6edc9a9ee590f3c2b9312f665d0039c93828b7b58f33950bc817a0955a9c5000a8d3e280569f08745ca68',
    'Xuan',
    'Uriah',
    0,
    1024963200  -- 2002-06-25 00:00:00
  );

INSERT INTO `item` (name,count,description,original,discount,avatar) VALUES
	 ('apple',10,'This is an apple.',30,25,'xx-S0m3-aVA7aR-0f-a991e-xx'),
	 ('tilapia',3,'This is a tilapia.',50,45,'xx-S0m3-aVA7aR-0f-ti1a9iA-xx');

INSERT INTO `tag` (name) VALUES
	 ('seafood'),
	 ('fruit'),
	 ('grocery');

INSERT INTO `tag_of_item` (item_id,tag_id) VALUES
	 (1,1),
	 (1,3),
	 (2,2),
	 (2,3);

INSERT INTO `shopping_cart` (user_id,item_id,count) VALUES
	 (1,1,5),
	 (1,2,3),
	 (2,2,3);
