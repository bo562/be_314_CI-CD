CREATE TABLE security_question (
     security_question_id  MEDIUMINT NOT NULL AUTO_INCREMENT,
     question              VARCHAR(2000) NOT NULL,
     retired               DATETIME NOT NULL,
     PRIMARY KEY (security_question_id)
);

