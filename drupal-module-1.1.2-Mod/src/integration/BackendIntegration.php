<?php

namespace Drupal\crm_integration\integration;

use Drupal\crm_integration\integration\Traits\Campaign;
use Drupal\crm_integration\integration\Traits\TargetList;
use Drupal\crm_integration\integration\Traits\Webform;
use Drupal\crm_integration\integration\Traits\Website;
use GuzzleHttp\Client as GuzzleClient;
use GuzzleHttp\Exception\RequestException;
use stdClass;

class BackendIntegration
{
    use Website, Webform, Campaign, TargetList;

    protected GuzzleClient $client;
    protected string $baseUrl;
    protected array $defaultHeaders = [];

    public function __construct(
        string $base_url,
        ?string $api_key = null,
        array $extra_headers = []
    ) {
        $this->baseUrl = rtrim($base_url, '/');

        $headers = array_merge([
            'Accept' => 'application/json',
            'Content-Type' => 'application/json',
        ], $extra_headers);

        if ($api_key) {
            $headers['Authorization'] = 'Token ' . $api_key;
        }

        $this->defaultHeaders = $headers;

        $this->client = new GuzzleClient([
            'base_uri' => $this->baseUrl,
            'http_errors' => false,
            'timeout' => 10,
        ]);
    }

    /* ------------------------------------------------------------------
     *  CONTATTI
     * ------------------------------------------------------------------ */

    public function sendContact(array $values): stdClass
    {
        $response = $this->request('POST', '/contacts', $values);

        if ($response->status === 409 && isset($response->body->id)) {
            return $this->updateContact($response->body->id, $values);
        }

        $this->assertSuccess($response);

        return $response->body;
    }

    public function updateContact(string $contact_id, array $values): stdClass
    {
        $response = $this->request('PUT', "/contacts/{$contact_id}", $values);
        $this->assertSuccess($response);
        return $response->body;
    }

    /* ------------------------------------------------------------------
     *  ALLEGATI
     * ------------------------------------------------------------------ */

    public function sendAttachment(
        string $name,
        string $mime_type,
        string $content,
        array $metadata = []
    ): string {
        $payload = array_merge([
            'name' => $name,
            'mime_type' => $mime_type,
            'content_base64' => base64_encode($content),
        ], $metadata);

        $response = $this->request('POST', '/attachments', $payload);
        $this->assertSuccess($response);

        return $response->body->id;
    }

    /* ------------------------------------------------------------------
     *  CORE HTTP
     * ------------------------------------------------------------------ */

    protected function request(
        string $method,
        string $uri,
        array $payload = [],
        array $query = []
    ): stdClass {
        try {
            $options = [
                'headers' => $this->defaultHeaders,
            ];

            if (!empty($payload)) {
                $options['json'] = $payload;
            }

            if (!empty($query)) {
                $options['query'] = $query;
            }

            // Ensure URI is relative (without leading /) so Guzzle uses the base_uri
            // Guzzle treats URIs starting with / as absolute paths from root
            if (str_starts_with($uri, '/')) {
                $uri = substr($uri, 1); // Remove leading /
            }
            if (str_starts_with($uri, 'api/')) {
                $uri = substr($uri, 4); // Remove /api prefix to avoid /api/api
            }

            $full_url = $this->baseUrl . '/' . $uri;
            \Drupal::logger('crm_integration')->info("[REQUEST] $method $full_url");

            $response = $this->client->request($method, $uri, $options);

            $body = (string) $response->getBody();
            $parsedBody = $body ? json_decode($body) : new stdClass();

            \Drupal::logger('crm_integration')->info("[RESPONSE] Status: {$response->getStatusCode()}");

            return (object) [
                'status' => $response->getStatusCode(),
                'body' => $parsedBody,
            ];

        } catch (RequestException $e) {
            \Drupal::logger('crm_integration')->error("[REQUEST_ERROR] " . $e->getMessage());
            throw new \RuntimeException(
                'Backend request failed: ' . $e->getMessage(),
                $e->getCode(),
                $e
            );
        }
    }

    protected function assertSuccess(stdClass $response): void
    {
        if ($response->status < 200 || $response->status >= 300) {
            $exception = new \RuntimeException(
                'Backend error (' . $response->status . ')',
                $response->status
            );

            // Propaga eventuale ID (es. 409 Conflict)
            if (isset($response->body->id)) {
                $exception->id = $response->body->id;
            }

            throw $exception;
        }
    }

    /* ------------------------------------------------------------------
     *  BACKEND API (USATI DAI TRAIT)
     * ------------------------------------------------------------------ */

    protected function backendPost(string $resource, array $payload): stdClass
    {
        // baseUrl already includes /api, so just pass resource directly
        \Drupal::logger('crm_integration')->info("[backendPost] POST $this->baseUrl/$resource");
        $response = $this->request('POST', $resource, $payload);
        \Drupal::logger('crm_integration')->info("[backendPost] Response status: {$response->status}");
        $this->assertSuccess($response);
        return $response->body;
    }

    protected function backendPut(string $resource, array $payload): stdClass
    {
        $response = $this->request('PUT', $resource, $payload);
        $this->assertSuccess($response);
        return $response->body;
    }

    protected function backendGet(string $resource, array $query = []): stdClass
    {
        $response = $this->request('GET', $resource, [], $query);
        $this->assertSuccess($response);
        return $response->body;
    }
}