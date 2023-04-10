-- ---------------------------- 
-- Tradie System Schema Script 
-- --------------------------- 
  
  
-- ---------------------------- 
-- From: 010_user.sql 
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
  
-- ---------------------------- 
-- From: 020_subscription.sql 
CREATE TABLE subscription (
     subscription_id    MEDIUMINT NOT NULL AUTO_INCREMENT,
     subscription_name  VARCHAR(100),
     fee                DECIMAL(10,2) NOT NULL,
     PRIMARY KEY (subscription_id)
);

CREATE UNIQUE INDEX idx_subscription_name ON subscription(subscription_name);  
  
-- ---------------------------- 
-- From: 030_client.sql 
CREATE TABLE client (
     client_id          MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     subscription_id    MEDIUMINT,
     PRIMARY KEY (client_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id),
     FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
);
CREATE UNIQUE INDEX ak_client_user_id ON client(user_id);  
  
-- ---------------------------- 
-- From: 040_professional.sql 
CREATE TABLE professional (
     professional_id    MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     subscription_id    MEDIUMINT,
     PRIMARY KEY (professional_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id),
     FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
);

CREATE UNIQUE INDEX ak_professional_user_id ON client(user_id);  
  
-- ---------------------------- 
-- From: 050_address.sql 
CREATE TABLE address (
     address_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     street_number      VARCHAR(50) NOT NULL,
     street_name        VARCHAR(200) NOT NULL,
     suburb             VARCHAR(50) NOT NULL,
     postcode           INT NOT NULL,
     state              VARCHAR(10) NOT NULL,
     PRIMARY KEY (address_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE UNIQUE INDEX ak_address_user_id ON address(user_id);  
  
-- ---------------------------- 
-- From: 060_billing_type.sql 
CREATE TABLE billing_type (
     billing_type_id    INT NOT NULL AUTO_INCREMENT,
     billing_type_name  VARCHAR(100) NOT NULL,
     retired            DATE,
     PRIMARY KEY (billing_type_id)
);

CREATE INDEX idx_billing_type_name ON billing_type(billing_type_name);

CREATE UNIQUE INDEX uc_address_user_id ON billing_type(billing_type_name, retired);  
  
-- ---------------------------- 
-- From: 070_billing.sql 
-- If retired is null then the record is active
CREATE TABLE billing (
     billing_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     name               VARCHAR(100) NOT NULL,
     card_number        VARCHAR(10) NOT NULL,
     expiry_date        DATE NOT NULL,
     ccv                INT NOT NULL,
     billing_type_id    INT NOT NULL,       
     retired            DATE,
     PRIMARY KEY (billing_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE UNIQUE INDEX uc_billing_user_id ON billing(user_id, billing_type_id, retired);  
  
-- ---------------------------- 
-- From: 080_security_question.sql 
CREATE TABLE security_question (
     security_question_id  INT NOT NULL AUTO_INCREMENT,
     question              VARCHAR(2000) NOT NULL,
     retired               DATETIME NOT NULL,
     PRIMARY KEY (security_question_id)
);  
  
-- ---------------------------- 
-- From: 090_user_question.sql 
CREATE TABLE user_question (
     user_question_id     MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id              MEDIUMINT NOT NULL,
     security_question_id INT NOT NULL,
     answer               VARCHAR(2000) NOT NULL,
     PRIMARY KEY (user_question_id),
     FOREIGN KEY (security_question_id) REFERENCES security_question(security_question_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE UNIQUE INDEX uc_user_question_question ON user_question(user_id, security_question_id);  
  
-- ---------------------------- 
-- From: 100_service.sql 
CREATE TABLE service (
     service_id         INT NOT NULL AUTO_INCREMENT,
     service_name       VARCHAR(255) NOT NULL,
     cost               DECIMAL(10,2) NOT NULL,
     retired            DATETIME NOT NULL,
     PRIMARY KEY (service_id)
);

CREATE UNIQUE INDEX uc_service_name ON service(service_name, retired);

  
  
-- ---------------------------- 
-- From: 110_associated_service.sql 
-- ToDo: rename table to provided_service
CREATE TABLE associated_service (
     provided_service_id MEDIUMINT NOT NULL AUTO_INCREMENT,
     service_id          INT NOT NULL,
     professional_id     MEDIUMINT NOT NULL,
     PRIMARY KEY (provided_service_id),
     FOREIGN KEY (service_id) REFERENCES service(service_id),
     FOREIGN KEY (professional_id) REFERENCES professional(professional_id)
);
CREATE UNIQUE INDEX uc_associated_service ON 
    associated_service(professional_id, service_id);  
  
-- ---------------------------- 
-- From: 120_authorisation.sql 
CREATE TABLE authorisation (
     authorisation_id   MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     refresh_token      VARCHAR(255) NOT NULL,
     number_of_uses     INT NOT NULL,   
     invalidated        ENUM('Y','N') NOT NULL,
     PRIMARY KEY (authorisation_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);  
  
-- ---------------------------- 
-- From: 130_session.sql 
CREATE TABLE session (
     session_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     authorisation_id   MEDIUMINT NOT NULL,
     expiry_date        DATETIME NOT NULL,
     access_token       VARCHAR(255) NOT NULL,
     PRIMARY KEY (session_id),
     FOREIGN KEY (authorisation_id) REFERENCES authorisation(authorisation_id)
);  
  
-- ---------------------------- 
-- From: 140_request_status.sql 
CREATE TABLE request_status (
     request_status_id           INT NOT NULL AUTO_INCREMENT,
     status_name                 VARCHAR(100) NOT NULL,
     PRIMARY KEY (request_status_id)
);

CREATE UNIQUE INDEX uc_request_status_name ON request_status(status_name);  
  
-- ---------------------------- 
-- From: 150_request.sql 
CREATE TABLE request (
     request_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     client_id          MEDIUMINT NOT NULL,
     service_id         INT NOT NULL,
     request_date       DATETIME NOT NULL,
     professional_id    MEDIUMINT,
     start_date         DATETIME,
     completion_date    DATETIME,
     instruction        VARCHAR(4000),
     request_status_id  INT NOT NULL,
     PRIMARY KEY (request_id),
     FOREIGN KEY (client_id) REFERENCES client(client_id),
     FOREIGN KEY (professional_id) REFERENCES professional(professional_id),
     FOREIGN KEY (service_id) REFERENCES service(service_id)
);  
  
-- ---------------------------- 
-- From: 160_request_subscription.sql 
CREATE TABLE request_subscription (
     request_id        MEDIUMINT NOT NULL,
     subscription_id   MEDIUMINT NOT NULL,
     PRIMARY KEY (request_id, subscription_id),
     FOREIGN KEY (request_id) REFERENCES request(request_id),
     FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
);  
  
-- ---------------------------- 
-- From: 170_transaction_status.sql 
CREATE TABLE transaction_status (
     transaction_status_id           INT NOT NULL AUTO_INCREMENT,
     status_name                     VARCHAR(100) NOT NULL,
     PRIMARY KEY (transaction_status_id)
);

CREATE UNIQUE INDEX uc_transaction_status_name ON request_status(status_name);  
  
-- ---------------------------- 
-- From: 180_transaction.sql 
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
     FOREIGN KEY (billing_type_id) REFERENCES billing_type(billing_type_id)
     FOREIGN KEY (billing_id) REFERENCES billing(billing_id)
);

CREATE INDEX idx_transaction_date ON transaction(user_id, transaction_date);  
  
-- ---------------------------- 
-- From: 190_request_transaction.sql 
CREATE TABLE request_transaction (
     request_id           MEDIUMINT NOT NULL,
     transaction_id       MEDIUMINT NOT NULL,
     PRIMARY KEY (request_id, transaction_id),
     FOREIGN KEY (request_id) REFERENCES request(request_id),
     FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id)
);  
  
-- ---------------------------- 
-- From: 200_bid_status.sql 
CREATE TABLE bid_status (
     bid_status_id               INT NOT NULL AUTO_INCREMENT,
     status_name                 VARCHAR(100) NOT NULL,
     PRIMARY KEY (bid_status_id),
);

CREATE UNIQUE INDEX uc_bid_status_name ON bid_status(status_name);  
  
-- ---------------------------- 
-- From: 210_request_bid.sql 
CREATE TABLE request_bid (
     request_bid_id               MEDIUMINT NOT NULL AUTO_INCREMENT,
     request_id                   MEDIUMINT NOT NULL,
     professional_id              MEDIUMINT NOT NULL,
     sent_date                    DATETIME NOT NULL,
     accepted_by_client_date      DATETIME,
     professional_cancelled_date  DATETIME,     
     bid_status_id                INT NOT NULL,
     PRIMARY KEY (request_bid_id),
     FOREIGN KEY (professional_id) REFERENCES professional(professional_id),
     FOREIGN KEY (request_id) REFERENCES request(request_id),
     FOREIGN KEY (bid_status_id) REFERENCES bid_status(bid_status_id)
);  
  
-- ---------------------------- 
-- From: 300_insert_billing_type.sql 
INSERT INTO billing_type (billing_type_name,retired) VALUES ('Out', null);

INSERT INTO billing_type (billing_type_name,retired) VALUES ('In', null);

COMMIT;  
  
-- ---------------------------- 
-- From: 310_insert_subscriptions.sql 
INSERT INTO subscription (subscription_name, fee) VALUES ('Subscription', 100.50);

INSERT INTO subscription (subscription_name, fee) VALUES ('Single', 0);

COMMIT;  
  
-- ---------------------------- 
-- From: 320_insert_service.sql 
INSERT INTO service (service_name,  cost, retired) values ('Lawn mowing', 120, null);

INSERT INTO service (service_name,  cost, retired) values ('Weeding', 130, null);

INSERT INTO service (service_name,  cost, retired) values ('Mulching', 150, null);

INSERT INTO service (service_name,  cost, retired) values ('Plumbing Repair', 220, null);

INSERT INTO service (service_name,  cost, retired) values ('Electrical Repair', 250, null);

INSERT INTO service (service_name,  cost, retired) values ('Whitegoods Installation', 110, null);

INSERT INTO service (service_name,  cost, retired) values ('Locks changed', 170, null);

INSERT INTO service (service_name,  cost, retired) values ('Cleaning', 190, null);

commit;  
  
-- ---------------------------- 
-- From: 330_insert_request_status.sql 
INSERT INTO bid_status (status_name) values ('Open');

INSERT INTO bid_status (status_name) values ('Assigned');

INSERT INTO bid_status (status_name) values ('In progress');

INSERT INTO bid_status (status_name) values ('Completed - not paid');

INSERT INTO bid_status (status_name) values ('Completed');

INSERT INTO bid_status (status_name) values ('Cancelled');

COMMIT;  
  
-- ---------------------------- 
-- From: 340_insert_bid_status.sql 
INSERT INTO bid_status (status_name) values ('Active');

INSERT INTO bid_status (status_name) values ('Accepted');

INSERT INTO bid_status (status_name) values ('Rejected');

INSERT INTO bid_status (status_name) values ('Cancelled');

COMMIT;  
  
-- ---------------------------- 
-- From: 350_insert_transaction_status.sql 
INSERT INTO transaction_status (status_name) values ('Accepted');

INSERT INTO transaction_status (status_name) values ('Rejected');

INSERT INTO transaction_status (status_name) values ('Cancelled');

COMMIT;  
  
