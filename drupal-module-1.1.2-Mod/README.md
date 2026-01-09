# CRM Integration
Versions: [D7](https://gitlab.trust-itservices.com/crm/drupal-module/-/tree/7.x) | [D8+](https://gitlab.trust-itservices.com/crm/drupal-module/-/tree/8.x)

This module provides a basic integration with the CRM API. It allows to sync users and Webform submissions with the CRM.

## Installation
Run this command to add the repo to composer.json:
```bash
composer config repositories.crm vcs git@gitlab.trust-itservices.com:crm/drupal-module.git
```
> Note: It's recommended to use SSH agent forwarding to use your local agent for authentication.
> If you can't use SSH change the URL to `https://gitlab.trust-itservices.com/crm/drupal-module.git` and use your GitLab credentials or a personal/project access token.
> Then run this command to install the latest version of the module:
> ```bash
> composer require trust-itservices/crm_integration
> ```

## Configuration
The module provides a configuration form where you can set the needed settings.
Set the CRM API base URL and the API key in the configuration form.
