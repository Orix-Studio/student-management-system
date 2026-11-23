-- setup.sql: run this ONCE in DataGrip, logged in as root.
-- It (re)builds the sms database with the 6 students used in the lecture,
-- and creates the app user sms_app with only the rights it needs.
-- WARNING: DROP DATABASE deletes everything in sms.

DROP DATABASE IF EXISTS sms;
CREATE DATABASE sms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sms;

CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL UNIQUE,
    class_name VARCHAR(10)  NOT NULL
) ENGINE=InnoDB;

INSERT INTO student (first_name, last_name, email, class_name) VALUES
    ('Amir',  'Hassan', 'amir@school.no',  '2A'),
    ('Emma',  'Berg',   'emma@school.no',  '2A'),
    ('Jonas', 'Lie',    'jonas@school.no', '2B'),
    ('Sara',  'Khan',   'sara@school.no',  '2B'),
    ('Nora',  'Haugen', 'nora@school.no',  '2A'),
    ('Ali',   'Dahl',   'ali@school.no',   '2B');

-- The app user (least privilege: read only for now).
-- Use the SAME password here and in your .env
CREATE USER IF NOT EXISTS 'sms_app'@'%' IDENTIFIED BY 'ChangeMe123!';
GRANT SELECT ON sms.* TO 'sms_app'@'%';
-- Lecture 2, Part 5 adds:  GRANT INSERT ON sms.* TO 'sms_app'@'%';
FLUSH PRIVILEGES;
