<?php

namespace Drupal\crm_integration\integration\Traits;

use stdClass;

trait TargetList
{
  public function sendList(string $name, int $mailjetId): string
  {
    try {
      $response = $this->backendPost('/target-lists', [
        'name' => $name,
        'mailjet_id' => $mailjetId,
      ]);

      return $response->id;

    } catch (\RuntimeException $e) {

      // Lista già esistente
      if ($e->getCode() === 409 && property_exists($e, 'id')) {
        return $e->id;
      }

      throw $e;
    }
  }

  public function getList(string $mailjetId): ?stdClass
  {
    $response = $this->backendGet('/target-lists', [
      'mailjet_id' => $mailjetId,
    ]);

    if (!isset($response->items) || count($response->items) === 0) {
      return null;
    }

    return $response->items[0];
  }

  public function updateList(string $listId, array $values): string
  {
    $response = $this->backendPut("/target-lists/{$listId}", $values);
    return $response->id;
  }

  public function sendListContacts(string $listId, array $contactIds): bool
  {
    $response = $this->backendPost(
      "/target-lists/{$listId}/contacts",
      ['contact_ids' => $contactIds]
    );

    return (bool) ($response->success ?? true);
  }
}
