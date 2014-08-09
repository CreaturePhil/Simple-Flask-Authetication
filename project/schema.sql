create table if not exists users (
  id integer primary key autoincrement,
  username varchar(64) not null unique,
  password varchar(52) not null
);
