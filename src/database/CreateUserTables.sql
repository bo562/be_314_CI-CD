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

-- TODO: Drop subscription_name
CREATE TABLE subscription (
	 subscription_id    MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     subscription_name  CHAR(100),
     fee                DECIMAL(10,2) NOT NULL,
     start_date         DATETIME NOT NULL,
     end_date           DATETIME,
     PRIMARY KEY (subscription_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);
CREATE INDEX idx_subscription_user ON subscription(subscription_id, user_id);
CREATE UNIQUE INDEX idx_subscription_user_start ON subscription(user_id, start_date);

-- Note: subscription_id points to the most recent subscription
CREATE TABLE client (
     client_id          MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     subscription_id    MEDIUMINT
     PRIMARY KEY (client_id),
     FOREIGN KEY (subscription_id, user_id) REFERENCES subscription(subscription_id, user_id)
);
CREATE UNIQUE INDEX ak_client_user_id ON client(user_id);

-- Note: subscription_id points to the most recent subscription
CREATE TABLE professional (
     professional_id    MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     subscription_id    MEDIUMINT
     PRIMARY KEY (professional_id),
     FOREIGN KEY (subscription_id, user_id) REFERENCES subscription(subscription_id, user_id)
);
CREATE UNIQUE INDEX ak_client_user_id ON client(user_id);

-- Note: PK id is redundant as AK/FK is unique user_id
-- TODO: remove PK from this table as each user can only have 
-- one address
CREATE TABLE address (
     address_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     street_number      CHAR(100) NOT NULL,
     street_name        CHAR(100) NOT NULL,
     suburb             CHAR(100) NOT NULL,
     postcode           INT NOT NULL,
     state              CHAR(10) NOT NULL,
     PRIMARY KEY (address_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id),
);
CREATE UNIQUE INDEX ak_address_user_id ON address(user_id);

-- If retired is null then the record is active
CREATE TABLE billing_type (
	 billing_type_id    INT NOT NULL,
     billint_type_name  CHAR(100) NOT NULL,
     retired            DATE,
     PRIMARY KEY (billing_type_id),
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

-- If retired is null then the record is active
CREATE TABLE billing (
	 billing_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     card_number        CHAR(100) NOT NULL,
     expiry_date        DATE NOT NULL,
     ccv                INT NOT NULL,
     billing_type_id    INT NOT NULL,       
     retired            DATE,
     PRIMARY KEY (billing_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);
CREATE UNIQUE INDEX uc_billing_user_id ON billing_type(user_id, billing_type_id, retired);

CREATE TABLE authorisation (
	 authorisation_id   MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     refresh_token      VARCHAR(255) NOT NULL,
     number_of_uses     INT NOT NULL,   
     invalidated        ENUM('Y','N') NOT NULL,
     PRIMARY KEY (authorisation_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE session (
	 session_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     authorisation_id   MEDIUMINT NOT NULL,
     expiry_date        DATETIME NOT NULL,
     access_token       VARCHAR(255) NOT NULL,
     PRIMARY KEY (session_id),
     FOREIGN KEY (authorisation_id) REFERENCES authorisation(authorisation_id)
);

CREATE TABLE service (
	 service_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     service_name       VARCHAR(255) NOT NULL,
     cost               DECIMAL(10,2) NOT NULL,
     retired            DATETIME NOT NULL,
     PRIMARY KEY (service_id)
);
CREATE UNIQUE INDEX uc_service_name ON billing_type(service_name, retired);
 
-- ToDo: rename table to provided_service
CREATE TABLE associated_service (
	 provided_service_id MEDIUMINT NOT NULL AUTO_INCREMENT,
     service_id          MEDIUMINT NOT NULL,
     professional_id     MEDIUMINT NOT NULL,
     PRIMARY KEY (provided_service_id),
     FOREIGN KEY (service_id) REFERENCES service(service_id),
     FOREIGN KEY (professional_id) REFERENCES professional(professional_id)
);
CREATE UNIQUE INDEX uc_associated_service ON billing_type(professional_id, service_id);

