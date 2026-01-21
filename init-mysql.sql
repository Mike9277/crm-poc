-- Crea i database
CREATE DATABASE IF NOT EXISTS crm;
CREATE DATABASE IF NOT EXISTS drupal;

-- Crea gli utenti
CREATE USER IF NOT EXISTS 'crm'@'%' IDENTIFIED BY 'crm';
CREATE USER IF NOT EXISTS 'drupal'@'%' IDENTIFIED BY 'drupal';

-- Assegna i permessi
GRANT ALL PRIVILEGES ON crm.* TO 'crm'@'%';
GRANT ALL PRIVILEGES ON drupal.* TO 'drupal'@'%';

FLUSH PRIVILEGES;