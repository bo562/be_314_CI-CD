-- If retired is null then the record is active
CREATE TABLE billing_type (
	 billing_type_id    INT NOT NULL,
     billint_type_name  CHAR(100) NOT NULL,
     retired            DATE,
     PRIMARY KEY (billing_type_id)
);
CREATE INDEX idx_billing_type_name ON billing_type(billint_type_name);
CREATE UNIQUE INDEX uc_address_user_id ON billing_type(billint_type_name, retired);

INSERT INTO billing_type
	(billing_type_id, billint_type_name,retired)
  VALUES
    (1, 'Out', null);
INSERT INTO billing_type
	(billing_type_id, billint_type_name,retired)
  VALUES
    (2, 'In', null);
COMMIT;

