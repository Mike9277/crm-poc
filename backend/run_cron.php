<?php
/**
 * Script temporaneo per eseguire il cron di Drupal.
 */

// Setup
$drupal_root = '/opt/drupal/web';
$_SERVER['HTTP_HOST'] = 'localhost';
$_SERVER['SCRIPT_FILENAME'] = $drupal_root . '/index.php';
$_SERVER['REQUEST_URI'] = '/cron';

// Change to Drupal root
chdir($drupal_root);

// Bootstrap Drupal manualmente
define('DRUPAL_ROOT', $drupal_root);
require_once DRUPAL_ROOT . '/core/includes/bootstrap.inc';
require_once DRUPAL_ROOT . '/core/modules/system/system.install';

try {
    // Autoload
    require_once '/opt/drupal/vendor/autoload.php';
    
    // Includi settings
    $app_root = DRUPAL_ROOT;
    $site_path = 'sites/default';
    require_once $site_path . '/settings.php';

    // Carica il modulo di cron
    \Drupal\Core\DrupalKernel::bootEnvironment();
    
    echo "Executing CRM Integration cron...\n";
    
    // Carica il modulo crm_integration e esegui il suo hook_cron
    $module = 'crm_integration';
    if (\Drupal::moduleHandler()->moduleExists($module)) {
        echo "✓ CRM Integration module found.\n";
        
        // Invoca il hook_cron del modulo
        $function = $module . '_cron';
        if (function_exists($function)) {
            call_user_func($function);
            echo "✓ CRM Integration cron executed.\n";
        } else {
            echo "✗ CRM Integration cron function not found: $function\n";
        }
    } else {
        echo "✗ CRM Integration module not found.\n";
    }
} catch (\Exception $e) {
    echo "✗ Error: " . $e->getMessage() . "\n";
    echo $e->getTraceAsString() . "\n";
}
