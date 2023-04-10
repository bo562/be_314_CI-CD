CREATE TABLE transaction (
     transaction_id          MEDIUMINT NOT NULL AUTO_INCREMENT,
     amount                  DECIMAL(15,2) NOT NULL,
     transaction_date        DATETIME NOT NULL,
     transaction_status_id   INT NOT NULL,
     user_id                 MEDIUMINT NOT NULL,
     billing_type_id         INT NOT NULL,
     billing_id              MEDIUMINT NOT NULL,
     PRIMARY KEY (transaction_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id),
     FOREIGN KEY (billing_type_id) REFERENCES billing_type(billing_type_id),
     FOREIGN KEY (billing_id) REFERENCES billing(billing_id)
);

CREATE INDEX idx_transaction_date ON transaction(user_id, transaction_date);