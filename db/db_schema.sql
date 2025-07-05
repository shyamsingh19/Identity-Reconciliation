create database identity_reconciliation;

use identity_reconciliation;

CREATE TABLE
    Contact (
        id INT AUTO_INCREMENT PRIMARY KEY,
        phoneNumber VARCHAR(20),
        email VARCHAR(255),
        linkedId INT,
        linkPrecedence ENUM ('primary', 'secondary') NOT NULL,
        createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        deletedAt DATETIME DEFAULT NULL,
        FOREIGN KEY (linkedId) REFERENCES Contact (id)
    );