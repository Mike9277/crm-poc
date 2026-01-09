<?php /** @noinspection PhpLanguageLevelInspection */

/** @noinspection TransitiveDependenciesUsageInspection */

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\DowngradeLevelSetList;

// Fix strange PHP not finding MHASH constants issue
if (! defined('MHASH_XXH32')) {
  define('MHASH_XXH32', 38);
}

if (! defined('MHASH_XXH64')) {
  define('MHASH_XXH64', 39);
}

if (! defined('MHASH_XXH3')) {
  define('MHASH_XXH3', 40);
}

if (! defined('MHASH_XXH128')) {
  define('MHASH_XXH128', 41);
}

return RectorConfig::configure()
  ->withFileExtensions([
    'module',
    'theme',
    'install',
    'profile',
    'inc',
    'engine'
  ])
  ->withPaths(['src', 'crm_integration.module'])
  ->withDowngradeSets(php72: TRUE)
  //    ->withSets([
  //        DowngradeLevelSetList::DOWN_TO_PHP_72,
  //    ])
  // A. whole set
  //    ->withPreparedSets(typeDeclarations: true)
  //    // B. or few rules
  //    ->withRules([
  //        TypedPropertyFromAssignsRector::class
  //    ])
  ;
