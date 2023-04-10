CREATE TABLE address (
     address_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     street_number      CHAR(100) NOT NULL,
     street_name        CHAR(100) NOT NULL,
     suburb             CHAR(100) NOT NULL,
     postcode           INT NOT NULL,
     state              CHAR(10) NOT NULL,
     PRIMARY KEY (address_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE UNIQUE INDEX ak_address_user_id ON address(user_id);