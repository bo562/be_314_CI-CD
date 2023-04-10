CREATE TABLE user (
     user_id            MEDIUMINT NOT NULL AUTO_INCREMENT,
     first_name         VARCHAR(100) NOT NULL,
     last_name          VARCHAR(100) NOT NULL,
     email_address      VARCHAR(200) NOT NULL,
     mobile             VARCHAR(20) NOT NULL,
     password           VARCHAR(20) NOT NULL,
     PRIMARY KEY (user_id)
);

CREATE UNIQUE INDEX ak_user_email ON user(email_address);