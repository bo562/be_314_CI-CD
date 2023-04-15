-- ---------------------------- 
-- Tradie System Schema Script 
-- --------------------------- 
  
  
-- ---------------------------- 
-- From: 000_drop_all.sql 
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS associated_service;
DROP TABLE IF EXISTS authorisation;
DROP TABLE IF EXISTS bid_status;
DROP TABLE IF EXISTS billing;
DROP TABLE IF EXISTS billing_type;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS professional;
DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS request_bid;
DROP TABLE IF EXISTS request_status;
DROP TABLE IF EXISTS request_subscription;
DROP TABLE IF EXISTS request_transaction;
DROP TABLE IF EXISTS security_question;
DROP TABLE IF EXISTS service;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS subscription;
DROP TABLE IF EXISTS transaction;
DROP TABLE IF EXISTS transaction_status;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_question;

SET FOREIGN_KEY_CHECKS = 1;  
  
-- ---------------------------- 
-- From: 010_user.sql 
CREATE TABLE user (
     user_id            MEDIUMINT NOT NULL AUTO_INCREMENT,
     first_name         VARCHAR(100) NOT NULL,
     last_name          VARCHAR(100) NOT NULL,
     email_address      VARCHAR(200) NOT NULL,
     mobile             VARCHAR(20) NOT NULL,
     password           VARCHAR(32) NOT NULL,
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
     card_number        VARCHAR(256) NOT NULL,
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
     retired            DATETIME,
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
     FOREIGN KEY (service_id) REFERENCES service(service_id),
     FOREIGN KEY (request_status_id) REFERENCES request_status(request_status_id)
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
     FOREIGN KEY (billing_type_id) REFERENCES billing_type(billing_type_id),
     FOREIGN KEY (billing_id) REFERENCES billing(billing_id),
     FOREIGN KEY (transaction_status_id) REFERENCES transaction_status(transaction_status_id)
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
     PRIMARY KEY (bid_status_id)
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
INSERT INTO service (service_name) values ('Tree Removal');

INSERT INTO service (service_name) values ('Roof Cleaning');

INSERT INTO service (service_name) values ('Fence Installation');

INSERT INTO service (service_name) values ('Plumbing');

INSERT INTO service (service_name) values ('Oven Repairs');

COMMIT;  
  
-- ---------------------------- 
-- From: 330_insert_request_status.sql 
INSERT INTO request_status (status_name) values ('New');

INSERT INTO request_status (status_name) values ('Pending Acceptance');

INSERT INTO request_status (status_name) values ('Pending Completion');

INSERT INTO request_status (status_name) values ('Complete');

INSERT INTO request_status (status_name) values ('Archived');

COMMIT;  
  
-- ---------------------------- 
-- From: 340_insert_bid_status.sql 
INSERT INTO bid_status (status_name) values ('Active');

INSERT INTO bid_status (status_name) values ('Accepted');

INSERT INTO bid_status (status_name) values ('Rejected');

COMMIT;  
  
-- ---------------------------- 
-- From: 350_insert_transaction_status.sql 
INSERT INTO transaction_status (status_name) values ('Accepted');

INSERT INTO transaction_status (status_name) values ('Rejected');

COMMIT;  
  
-- ---------------------------- 
-- From: 360_insert_security_question.sql 
INSERT INTO security_question (question) VALUES('What was your first car?');

INSERT INTO security_question (question) VALUES('What was the name of the first street you lived on?');

INSERT INTO security_question (question) VALUES('What was the name of your first pet?');

INSERT INTO security_question (question) VALUES('What city were you born in?');

INSERT INTO security_question (question) VALUES('What was your childhood nickname?');

COMMIT;  
  
