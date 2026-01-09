<?php

namespace Drupal\crm_integration\integration\Traits;

use stdClass;

trait Webform
{
  public function sendWebform(
    string $webformId,
    string $name,
    string $description,
    string $websiteId
  ): string {

    try {
      $response = $this->backendPost('/webforms', [
        'external_id' => $webformId,
        'name' => $name,
        'description' => $description,
        'website_id' => $websiteId,
        'dedup_key' => "{$websiteId}|{$webformId}",
      ]);

      return $response->id;

    } catch (\RuntimeException $e) {

      // Webform già esistente
      if ($e->getCode() === 409 && property_exists($e, 'id')) {
        return $e->id;
      }

      throw $e;
    }
  }

  public function sendWebformSubmission(
    string $websiteId,
    string $webformId,
    string $submissionId,
    array $values
  ): void {

    // 1️⃣ Costruzione payload leggibile
    $extraData = $this->buildSubmissionData($values);

    $payload = [
      'external_id' => $submissionId,
      'data' => $extraData,
      'dedup_key' => "{$websiteId}|{$webformId}|{$submissionId}",
    ];

    // 2️⃣ Associazione contatto (se email presente)
    if (!empty($values['email'])) {
      $contactId = $this->getOrCreateContactByEmail($values['email']);
      $payload['contact_id'] = $contactId;
    }

    // 3️⃣ Invio submission
    try {
      $this->backendPost(
        "/webforms/{$webformId}/submissions",
        $payload
      );
    } catch (\RuntimeException $e) {

      // Submission duplicata → ok
      if ($e->getCode() !== 409) {
        throw $e;
      }
    }
  }

  /* ------------------------------------------------------------------
   *  Helpers
   * ------------------------------------------------------------------ */

  protected function buildSubmissionData(array $values): string
  {
    $output = '';

    foreach ($values as $name => $value) {
      if ($value !== null && $name !== 'email') {
        $output .= "- **{$name}**: {$value}\n";
      }
    }

    return $output;
  }

  protected function getOrCreateContactByEmail(string $email): string
  {
    // Cerca contatto
    $response = $this->backendGet('/contacts', [
      'email' => $email,
    ]);

    if (isset($response->items[0])) {
      $contactId = $response->items[0]->id;

      // aggiornamento minimo (opzionale)
      $this->backendPut("/contacts/{$contactId}", [
        'first_name' => $email,
      ]);

      return $contactId;
    }

    // Crea contatto
    $contact = $this->backendPost('/contacts', [
      'first_name' => $email,
      'email' => $email,
    ]);

    return $contact->id;
  }
}
