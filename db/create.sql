CREATE TABLE users
(
  pseudo VARCHAR(8) PRIMARY KEY,
  mdp VARCHAR(10) NOT NULL,
  admin BOOL DEFAULT FALSE
);


CREATE TABLE messages
(
  id SERIAL PRIMARY KEY,
  txt text NOT NULL,
  msg_date timestamp not null default CURRENT_TIMESTAMP,
  expediteur VARCHAR(8) NOT NULL REFERENCES users(pseudo),
  canal VARCHAR(10) NOT NULL,
  suppr BOOL DEFAULT FALSE
);
