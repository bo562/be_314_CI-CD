-- If retired is null then the record is active
CREATE TABLE billing (
	 billing_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     name               CHAR(100) NOT NULL,
     card_number        CHAR(10) NOT NULL,
     expiry_date        DATE NOT NULL,
     ccv                INT NOT NULL,
     billing_type_id    INT NOT NULL,       
     retired            DATE,
     PRIMARY KEY (billing_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);
CREATE UNIQUE INDEX uc_billing_user_id ON billing(user_id, billing_type_id, retired);

