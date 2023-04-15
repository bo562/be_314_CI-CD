CREATE TABLE address (
     address_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     street_number      VARCHAR(50) NOT NULL,
     street_name        VARCHAR(200) NOT NULL,
     suburb             VARCHAR(50) NOT NULL,
     postcode           INT NOT NULL,
     PRIMARY KEY (address_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE UNIQUE INDEX ak_address_user_id ON address(user_id);