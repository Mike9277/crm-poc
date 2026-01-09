<?php

namespace Drupal\crm_integration\integration\Traits;

use stdClass;

trait Campaign
{
  public function sendCampaign(
    string $name,
    int $mailjetId,
    string $websiteId,
    array $targetListsIds
  ): string {

    try {
      $response = $this->backendPost('/campaigns', [
        'name' => $name,
        'mailjet_id' => $mailjetId,
        'website_id' => $websiteId,
        'target_lists_ids' => $targetListsIds,
      ]);

      return $response->id;

    } catch (\RuntimeException $e) {

      // Duplicato / already exists
      if ($e->getCode() === 409) {
        if (property_exists($e, 'id')) {
          return $e->id;
        }
      }

      throw $e;
    }
  }

  public function getCampaign(string $mailjetId): ?stdClass
  {
    $response = $this->backendGet('/campaigns', [
      'mailjet_id' => $mailjetId,
    ]);

    if (!isset($response->items) || count($response->items) === 0) {
      return null;
    }

    return $response->items[0];
  }

  public function updateCampaign(string $campaignId, array $values): stdClass
  {
    return $this->backendPut("/campaigns/{$campaignId}", $values);
  }
}