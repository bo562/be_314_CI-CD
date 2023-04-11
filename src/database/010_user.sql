CREATE TABLE user (
     user_id            MEDIUMINT NOT NULL AUTO_INCREMENT,
     first_name         CHAR(100) NOT NULL,
     last_name          CHAR(100) NOT NULL,
     email_address      CHAR(100) NOT NULL,
     mobile             CHAR(100) NOT NULL,
     password           CHAR(100) NOT NULL,
     PRIMARY KEY (user_id)
);
CREATE UNIQUE INDEX ak_user_email ON user(email_address);

