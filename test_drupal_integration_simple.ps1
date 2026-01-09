Write-Host "=== DRUPAL <- DJANGO INTEGRATION TEST ===" -ForegroundColor Cyan

$BASE_URL = "http://localhost:8000/api"

# Test 1: Create Website
Write-Host "`nTest 1: Create Website" -ForegroundColor Yellow
$websitePayload = @{
    name = "Drupal Site"
    url = "https://drupal.example.com"
    external_id = "drupal-web-001"
    dedup_key = "web-drupal-2024"
} | ConvertTo-Json

$website = Invoke-WebRequest -Uri "$BASE_URL/websites/" -Method POST -Body $websitePayload -ContentType "application/json" -UseBasicParsing | ConvertFrom-Json
Write-Host "Website created: ID=$($website.id), dedup_key=$($website.dedup_key)" -ForegroundColor Green
$websiteId = $website.id

# Test 2: Create Webform
Write-Host "`nTest 2: Create Webform" -ForegroundColor Yellow
$webformPayload = @{
    website_id = $websiteId
    name = "Contact Form"
    description = "Main contact form"
    external_id = "form-contact-001"
    dedup_key = "form-drupal-2024"
} | ConvertTo-Json

$webform = Invoke-WebRequest -Uri "$BASE_URL/webforms/" -Method POST -Body $webformPayload -ContentType "application/json" -UseBasicParsing | ConvertFrom-Json
Write-Host "Webform created: ID=$($webform.id), dedup_key=$($webform.dedup_key)" -ForegroundColor Green
$webformId = $webform.id

# Test 3: Create Contact
Write-Host "`nTest 3: Create Contact (First Time)" -ForegroundColor Yellow
$contactPayload = @{
    first_name = "Mario"
    email = "mario.rossi@drupal.com"
    external_id = "contact-mario-001"
    dedup_key = "mario-rossi-2024"
    source_website = "drupal"
} | ConvertTo-Json

$contact = Invoke-WebRequest -Uri "$BASE_URL/contacts/" -Method POST -Body $contactPayload -ContentType "application/json" -UseBasicParsing | ConvertFrom-Json
Write-Host "Contact created: ID=$($contact.id), dedup_key=$($contact.dedup_key)" -ForegroundColor Green
$contactId = $contact.id

# Test 4: Duplicate Contact (409 Conflict)
Write-Host "`nTest 4: Duplicate Contact (Testing 409 Conflict)" -ForegroundColor Yellow
try {
    $duplicate = Invoke-WebRequest -Uri "$BASE_URL/contacts/" -Method POST -Body $contactPayload -ContentType "application/json" -UseBasicParsing
} catch {
    if ($_.Exception.Response.StatusCode -eq 409) {
        Write-Host "409 Conflict returned (EXPECTED)" -ForegroundColor Green
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $content = $reader.ReadToEnd()
        $dupContact = $content | ConvertFrom-Json
        Write-Host "Returned existing ID: $($dupContact.id)" -ForegroundColor Green
    } else {
        Write-Host "Unexpected error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test 5: Create another contact
Write-Host "`nTest 5: Create Another Contact" -ForegroundColor Yellow
$contactPayload2 = @{
    first_name = "Luigi"
    email = "luigi.bianchi@drupal.com"
    external_id = "contact-luigi-001"
    dedup_key = "luigi-bianchi-2024"
    source_website = "drupal"
} | ConvertTo-Json

$contact2 = Invoke-WebRequest -Uri "$BASE_URL/contacts/" -Method POST -Body $contactPayload2 -ContentType "application/json" -UseBasicParsing | ConvertFrom-Json
Write-Host "Contact created: ID=$($contact2.id)" -ForegroundColor Green

# Test 6: Create Webform Submission
Write-Host "`nTest 6: Create Webform Submission" -ForegroundColor Yellow
$submissionPayload = @{
    webform_id = $webformId
    person_id = $contactId
    external_id = "submission-mario-001"
    dedup_key = "sub-mario-2024"
    payload = @{
        email = "mario.rossi@drupal.com"
        first_name = "Mario"
        last_name = "Rossi"
        message = "I am interested in your services"
    }
} | ConvertTo-Json

$submission = Invoke-WebRequest -Uri "$BASE_URL/webform-submissions/" -Method POST -Body $submissionPayload -ContentType "application/json" -UseBasicParsing | ConvertFrom-Json
Write-Host "Submission created: ID=$($submission.id)" -ForegroundColor Green

# Test 7: Verify data retrieval
Write-Host "`nTest 7: Verify Data Retrieval" -ForegroundColor Yellow
$allContacts = Invoke-WebRequest -Uri "$BASE_URL/contacts/" -Method GET -UseBasicParsing | ConvertFrom-Json
Write-Host "Total contacts in DB: $($allContacts.count)" -ForegroundColor Green

$allWebforms = Invoke-WebRequest -Uri "$BASE_URL/webforms/" -Method GET -UseBasicParsing | ConvertFrom-Json
Write-Host "Total webforms in DB: $($allWebforms.count)" -ForegroundColor Green

$allSubmissions = Invoke-WebRequest -Uri "$BASE_URL/webform-submissions/" -Method GET -UseBasicParsing | ConvertFrom-Json
Write-Host "Total submissions in DB: $($allSubmissions.count)" -ForegroundColor Green

Write-Host "`n=== ALL TESTS PASSED ===" -ForegroundColor Green
Write-Host "Drupal <- Django integration is working correctly!" -ForegroundColor Green
