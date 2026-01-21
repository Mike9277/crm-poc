<?php

namespace Drupal\crm_integration\integration\Traits;

use stdClass;

trait Website
{
  public function sendWebsite(string $name, string $url): string
  {
    try {
      \Drupal::logger('crm_integration')->info("[Website.sendWebsite] Posting to 'websites' with name='$name', url='$url'");
      $response = $this->backendPost('websites', [
        'name' => $name,
        'url' => $url,
      ]);

      return $response->id;

    } catch (\RuntimeException $e) {

      // Website già esistente
      if ($e->getCode() === 409 && property_exists($e, 'id')) {
        return $e->id;
      }

      throw $e;
    }
  }

  public function sendWebsiteUser(
    string $websiteId,
    string $contactId,
    string $userEmail,
    array $consents,
    string $createdAt,
    string $modifiedAt,
    ?string $lastLogin = null,
    array $extraData = []
  ): stdClass {

    $data = $this->buildWebsiteUserData($extraData);

    $isAccepted = !empty($consents[$userEmail]['isAccepted']);
    $ppgUpdated = $consents[$userEmail]['ppgUpdated'] ?? null;

    $payload = [
      'website_id' => $websiteId,
      'contact_id' => $contactId,
      'email' => $userEmail,
      'data' => $data,
      'dedup_key' => "{$websiteId}|{$contactId}",
      'ppg_accepted' => $isAccepted,
      'ppg_updated_at' => $ppgUpdated ? date('Y-m-d H:i:s', $ppgUpdated) : null,
      'created_at' => date('Y-m-d H:i:s', $createdAt),
      'modified_at' => date('Y-m-d H:i:s', $modifiedAt),
      'last_login' => $lastLogin ? date('Y-m-d H:i:s', $lastLogin) : null,
    ];

    try {
      return $this->backendPost("websites/{$websiteId}/users", $payload);

    } catch (\RuntimeException $e) {

      // Website user già esistente → update
      if ($e->getCode() === 409 && property_exists($e, 'id')) {
        return $this->backendPut("website-users/{$e->id}", $payload);
      }

      throw $e;
    }
  }

  public function updateWebsiteUser(
    string $websiteUserId,
    array $values
  ): stdClass {
    return $this->backendPut("website-users/{$websiteUserId}", $values);
  }

  /* ------------------------------------------------------------------
   *  Helpers
   * ------------------------------------------------------------------ */

  protected function buildWebsiteUserData(array $extraData): string
  {
    $output = '';

    foreach ($extraData as $field) {
      if ($field->value !== null) {
        $output .= "- **{$field->getFieldDefinition()->getLabel()}**: {$field->value}\n";
      } elseif ($field->getValue() !== null) {
        $values = implode(', ', array_column($field->getValue(), 'target_id'));
        $output .= "- **{$field->getFieldDefinition()->getLabel()}**: {$values}\n";
      }
    }

    return $output;
  }
}