<?php

namespace Drupal\crm_integration\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

class CRMForm extends ConfigFormBase
{

  protected function getEditableConfigNames(): array
  {
    return ['crm_integration.settings'];
  }

  public function getFormId(): string
  {
    return 'crm_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state): array
  {
    $config = $this->config('crm_integration.settings');

    $form['site_url'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Site URL'),
      '#description' => $this->t('The URL of the site.'),
      '#required' => TRUE,
      '#default_value' => $config->get('site_url') ?: \Drupal::request()->getSchemeAndHttpHost(),
    ];

    $form['crm_api_base_url'] = [
      '#type' => 'textfield',
      '#title' => $this->t('CRM API Base URL'),
      '#description' => $this->t('Base URL for the CRM API (e.g. https://crm.example.com/api).'),
      '#required' => TRUE,
      '#default_value' => $config->get('crm_api_base_url'),
    ];

    // Token element for the api key of the crm.
    $form['crm_api_key'] = [
      '#type' => 'password',
      '#title' => $this->t('CRM API Key'),
      '#description' => $this->t('The API key of the CRM. Leave empty if you do not want to change it.'),
      '#default_value' => $config->get('crm_api_key'),
    ];

    // Token element for mailjet newsletter api key public.
    $form['mailjet_api_key_public'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Mailjet API Key Public'),
      '#description' => $this->t('The public API key of the Mailjet newsletter.'),
      '#default_value' => $config->get('mailjet_api_key_public'),
    ];

    // Token element for mailjet newsletter api key private.
    $form['mailjet_api_key_private'] = [
      '#type' => 'password',
      '#title' => $this->t('Mailjet API Key Private'),
      '#description' => $this->t('The private API key of the Mailjet newsletter. Leave empty if you do not want to change it.'),
      '#default_value' => $config->get('mailjet_api_key_private'),
    ];

    // Checkbox element for synchronizing webform submissions on crm_integration.
    $form['syncronize'] = [
      '#type' => 'checkbox',
      '#title' => $this->t('Sync drupal user with crm_integration'),
      '#description' => $this->t('if checked, drupal users will be synced with crm_integration'),
      '#default_value' => $config->get('syncronize'),
    ];

    // Fieldset for webform checkboxes.
    $form['webforms'] = [
      '#type' => 'fieldset',
      '#title' => $this->t('Webforms'),
    ];

    // Add a description to the fieldset.
    $form['webforms']['description'] = [
      '#type' => 'item',
      '#markup' => $this->t('Select the webforms you want to synchronize.'),
    ];

    // Get a list of all webforms without templates - only if webform module is enabled.
    if (\Drupal::moduleHandler()->moduleExists('webform')) {
      $webforms = \Drupal::entityTypeManager()->getStorage('webform')->loadMultiple();
      if (is_array($webforms)) {
        $webforms = array_filter($webforms, static function ($webform) {
          return method_exists($webform, 'isTemplate') && !$webform->isTemplate();
        });
      }

      // Create checkboxes for each webform.
      foreach ($webforms as $webform_id => $webform) {
        $form['webforms']['webform_' . $webform_id] = [
          '#type' => 'checkbox',
          '#title' => $webform->label(),
          '#default_value' => $config->get('webform_' . $webform_id),
        ];
      }
    } else {
      $form['webforms']['message'] = [
        '#type' => 'item',
        '#markup' => $this->t('Webform module is not installed. Please install it to manage webform synchronization.'),
      ];
    }

    return parent::buildForm($form, $form_state);
  }

  public function submitForm(array &$form, FormStateInterface $form_state): void
  {
    $config = $this->configFactory->getEditable('crm_integration.settings');

    // Save the site URL.
    $config->set('site_url', $form_state->getValue('site_url'));

    $config->set('crm_api_base_url', $form_state->getValue('crm_api_base_url'));

    // Save the api key.
    $value = $form_state->getValue('crm_api_key');
    if (!empty($value)) {
      $config->set('crm_api_key', $value);
    }

    $value = $form_state->getValue('mailjet_api_key_public');
    if (!empty($value)) {
      $config->set('mailjet_api_key_public', $value);
    }

    $value = $form_state->getValue('mailjet_api_key_private');
    if (!empty($value)) {
      $config->set('mailjet_api_key_private', $value);
    }

    // Save the checkbox value for synchronizing webform submissions on crm_integration.
    $config->set('syncronize', $form_state->getValue('syncronize'));

    // Save the checkbox values for each webform.
    foreach ($form_state->getValues() as $key => $value) {
      if (strncmp($key, 'webform_', strlen('webform_')) === 0) {
        $config->set($key, $value);
      }
    }

    $config->save();

    parent::submitForm($form, $form_state);
  }

}
