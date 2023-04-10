CREATE TABLE billing_type (
     billing_type_id    INT NOT NULL AUTO_INCREMENT,
     billing_type_name  CHAR(100) NOT NULL,
     retired            DATE,
     PRIMARY KEY (billing_type_id)
);

CREATE INDEX idx_billing_type_name ON billing_type(billing_type_name);

CREATE UNIQUE INDEX uc_address_user_id ON billing_type(billing_type_name, retired);