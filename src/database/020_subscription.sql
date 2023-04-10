CREATE TABLE subscription (
    subscription_id    MEDIUMINT NOT NULL AUTO_INCREMENT,
     subscription_name  CHAR(100),
     fee                DECIMAL(10,2) NOT NULL,
     PRIMARY KEY (subscription_id)
);
CREATE UNIQUE INDEX idx_subscription_name ON subscription(subscription_name);

