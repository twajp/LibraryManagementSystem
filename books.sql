CREATE TABLE BookList(
id int(4) not null primary key,
title varchar(50) not null,
author varchar(50) not null,
publisher varchar(50) not null,
date_of_purchase char(10) not null,
due_date int(10) not null DEFAULT 0,
who_has_this int(10) not null DEFAULT 0);

INSERT INTO BookList VALUES
(0001,'日本国紀','百田尚樹','幻冬社','2022-01-01',0,0),
(0002,'永遠の0','百田尚樹','講談社','2022-01-01',0,0),
(0003,'海賊と呼ばれた男','百田尚樹','講談社','2022-01-01',0,0),
(0004,'風の中のマリア','百田尚樹','講談社','2022-01-01',0,0),
(0005,'モンスター','百田尚樹','幻冬舎','2022-01-01',0,0),
(0006,'錨を上げよ','百田尚樹','講談社','2022-01-01',0,0),
(0007,'夢を売る男','百田尚樹','太田出版','2022-01-01',0,0),
(0008,'フォルトゥナの瞳','百田尚樹','新潮社','2022-01-01',0,0),
(0009,'殉愛','百田尚樹','幻冬舎','2022-01-01',0,0),
(0010,'カエルの楽園','百田尚樹','新潮社','2022-01-01',0,0),
(0011,'野良犬の値段','百田尚樹','幻冬舎','2022-01-01',0,0),
(0012,'偽善者たちへ','百田尚樹','新潮新書','2022-01-01',0,0),
(0013,'大放言','百田尚樹','新潮新書','2022-01-01',0,0),
(0014,'鋼のメンタル','百田尚樹','新潮新書','2022-01-01',0,0),
(0015,'雑談力','百田尚樹','PHP新書','2022-01-01',0,0),
(0016,'逃げる力','百田尚樹','PHP新書','2022-01-01',0,0),
(0017,'偽善者たちへ','百田尚樹','新潮新書','2022-01-01',0,0),
(0018,'バカの国','百田尚樹','新潮新書','2022-01-01',0,0),
(0019,'禁断の中国史','百田尚樹','飛鳥新社','2022-01-01',0,0),
(0020,'日本よ、世界の真ん中で咲き誇れ','安倍晋三','ワック・マガジンズ','2022-01-01',0,0);


CREATE TABLE BookReview(
id int(4) not null primary key,
book_id int(4) not null,
user_id int(4) not null,
date_of_review char(10) not null,
book_review varchar(1000) not null,
book_star int(1));

INSERT INTO BookReview VALUES
(0001, 0001, 'akasaka', '2022-01-02', 'とても勉強になります' || CHAR(13) || CHAR(10) || 'また読みたいです', 5),
(0002, 0001, 'fujioka', '2022-01-02', 'とてもおもしろいです' || CHAR(13) || CHAR(10) || 'また読みたいです', 5),
(0003, 0001, 'suzuki', '2022-01-02', 'とても感心しました' || CHAR(13) || CHAR(10) || 'また読みたいです', 5),
(0004, 0002, 'akasaka', '2022-01-03', '非常に勉強になります' || CHAR(13) || CHAR(10) || 'また読みたいです', 5),
(0005, 0002, 'fujioka', '2022-01-03', '非常におもしろいです' || CHAR(13) || CHAR(10) || 'また読みたいです', 5),
(0006, 0002, 'suzuki', '2022-01-03', '非常に感心しました' || CHAR(13) || CHAR(10) || 'また読みたいです', 5),
(0007, 0003, 'akasaka', '2022-01-04', '勉強になります' || CHAR(13) || CHAR(10) || 'また読みたいです', 5),
(0008, 0003, 'fujioka', '2022-01-04', 'おもしろいです' || CHAR(13) || CHAR(10) || 'また読みたいです', 5),
(0009, 0003, 'suzuki', '2022-01-04', '感心しました' || CHAR(13) || CHAR(10) || 'また読みたいです', 5);


CREATE TABLE UserList(
id int(4) not null primary key,
user_id int(4) not null,
password varchar(64) not null);

INSERT INTO UserList VALUES 
(0000, 'Admin', 'password'),
(0001, 'akasaka', 'password'),
(0002, 'fujioka', 'password'),
(0003, 'suzuki', 'password'),
(0004, 'testuser', 'password');
