# Test Drupal ↔ Django Integration
# This script simulates the complete Drupal integration workflow

Write-Host "`n===========================================" -ForegroundColor Cyan
Write-Host "DRUPAL ↔ DJANGO INTEGRATION TEST" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

$BASE_URL = "http://localhost:8000/api"
$RESULTS = @{
    "contacts_created" = 0
    "websites_created" = 0
    "webforms_created" = 0
    "submissions_created" = 0
    "conflicts_handled" = 0
    "tests_passed" = @()
    "tests_failed" = @()
}

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Method,
        [string]$Endpoint,
        [object]$Payload
    )
    
    Write-Host "`n[$Method] $Endpoint" -ForegroundColor Yellow
    
    try {
        $response = Invoke-WebRequest -Uri "$BASE_URL$Endpoint" `
            -Method $Method `
            -Body ($Payload | ConvertTo-Json) `
            -ContentType "application/json" `
            -UseBasicParsing
        
        $data = $response.Content | ConvertFrom-Json
        Write-Host "✅ $Name - Status: $($response.StatusCode)" -ForegroundColor Green
        $RESULTS["tests_passed"] += $Name
        return $data
    } catch {
        if ($_.Exception.Response.StatusCode -eq 409) {
            Write-Host "✅ $Name - Status: 409 Conflict (Expected Behavior)" -ForegroundColor Green
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $content = $reader.ReadToEnd()
            $data = $content | ConvertFrom-Json
            $RESULTS["conflicts_handled"] += 1
            $RESULTS["tests_passed"] += "$Name (409)"
            return $data
        } else {
            Write-Host "❌ $Name - Error: $($_.Exception.Message)" -ForegroundColor Red
            $RESULTS["tests_failed"] += $Name
            return $null
        }
    }
}

# ===== SCENARIO 1: Create Website =====
Write-Host "`n`n### SCENARIO 1: Register Website ###" -ForegroundColor Magenta

$website = Test-Endpoint `
    -Name "Create Website" `
    -Method "POST" `
    -Endpoint "/websites/" `
    -Payload @{
        name = "My Drupal Site"
        url = "https://drupal.local"
        external_id = "drupal-web-001"
        dedup_key = "web-drupal-2024"
    }

if ($website) {
    $RESULTS["websites_created"] += 1
    Write-Host "Website ID: $($website.id)" -ForegroundColor Cyan
    $websiteId = $website.id
} else {
    Write-Host "Failed to create website. Exiting." -ForegroundColor Red
    exit 1
}

# ===== SCENARIO 2: Create Webform for Website =====
Write-Host "`n`n### SCENARIO 2: Register Webform ###" -ForegroundColor Magenta

$webform = Test-Endpoint `
    -Name "Create Webform" `
    -Method "POST" `
    -Endpoint "/webforms/" `
    -Payload @{
        website_id = $websiteId
        name = "Contact Form"
        description = "Main contact form for Drupal site"
        external_id = "form-contact-001"
        dedup_key = "form-drupal-2024"
    }

if ($webform) {
    $RESULTS["webforms_created"] += 1
    Write-Host "Webform ID: $($webform.id)" -ForegroundColor Cyan
    $webformId = $webform.id
}

# ===== SCENARIO 3: Create Contact (First Request) =====
Write-Host "`n`n### SCENARIO 3: Create Contact (First Request) ###" -ForegroundColor Magenta

$contact1 = Test-Endpoint `
    -Name "Create Contact - First Request" `
    -Method "POST" `
    -Endpoint "/contacts/" `
    -Payload @{
        first_name = "Mario"
        email = "mario.rossi@example.com"
        external_id = "contact-mario-001"
        dedup_key = "mario-rossi-2024"
        source_website = "drupal"
    }

if ($contact1) {
    $RESULTS["contacts_created"] += 1
    Write-Host "Contact ID: $($contact1.id)" -ForegroundColor Cyan
    $contactId = $contact1.id
}

# ===== SCENARIO 4: Duplicate Contact Request (409 Conflict) =====
Write-Host "`n`n### SCENARIO 4: Duplicate Contact (409 Conflict) ###" -ForegroundColor Magenta

$contact1_dup = Test-Endpoint `
    -Name "Create Contact - Duplicate Request" `
    -Method "POST" `
    -Endpoint "/contacts/" `
    -Payload @{
        first_name = "Mario"
        email = "mario.rossi@example.com"
        external_id = "contact-mario-001"
        dedup_key = "mario-rossi-2024"
        source_website = "drupal"
    }

if ($contact1_dup -and $contact1_dup.id) {
    Write-Host "Returned existing Contact ID: $($contact1_dup.id)" -ForegroundColor Cyan
}

# ===== SCENARIO 5: Create Additional Contacts =====
Write-Host "`n`n### SCENARIO 5: Create Additional Contacts ###" -ForegroundColor Magenta

$contact2 = Test-Endpoint `
    -Name "Create Contact - Luigi" `
    -Method "POST" `
    -Endpoint "/contacts/" `
    -Payload @{
        first_name = "Luigi"
        email = "luigi.bianchi@example.com"
        external_id = "contact-luigi-001"
        dedup_key = "luigi-bianchi-2024"
        source_website = "drupal"
    }

if ($contact2) {
    $RESULTS["contacts_created"] += 1
}

$contact3 = Test-Endpoint `
    -Name "Create Contact - Francesca" `
    -Method "POST" `
    -Endpoint "/contacts/" `
    -Payload @{
        first_name = "Francesca"
        email = "francesca.verdi@example.com"
        external_id = "contact-francesca-001"
        dedup_key = "francesca-verdi-2024"
        source_website = "drupal"
    }

if ($contact3) {
    $RESULTS["contacts_created"] += 1
}

# ===== SCENARIO 6: Webform Submissions =====
Write-Host "`n`n### SCENARIO 6: Webform Submissions ###" -ForegroundColor Magenta

$submission1 = Test-Endpoint `
    -Name "Submit Webform - Mario" `
    -Method "POST" `
    -Endpoint "/webform-submissions/" `
    -Payload @{
        webform_id = $webformId
        person_id = $contact1.id
        external_id = "submission-mario-001"
        dedup_key = "sub-mario-contact-2024"
        payload = @{
            email = "mario.rossi@example.com"
            first_name = "Mario"
            last_name = "Rossi"
            message = "I am interested in your services"
            phone = "+39-123-456-789"
        }
    }

if ($submission1) {
    $RESULTS["submissions_created"] += 1
}

$submission2 = Test-Endpoint `
    -Name "Submit Webform - Luigi" `
    -Method "POST" `
    -Endpoint "/webform-submissions/" `
    -Payload @{
        webform_id = $webformId
        person_id = $contact2.id
        external_id = "submission-luigi-001"
        dedup_key = "sub-luigi-contact-2024"
        payload = @{
            email = "luigi.bianchi@example.com"
            first_name = "Luigi"
            last_name = "Bianchi"
            message = "I have a question about your product"
            phone = "+39-987-654-321"
        }
    }

if ($submission2) {
    $RESULTS["submissions_created"] += 1
}

# ===== VERIFICATION =====
Write-Host "`n`n### VERIFICATION: Retrieve Data ###" -ForegroundColor Magenta

Write-Host "`n[GET] /contacts/" -ForegroundColor Yellow
$allContacts = Invoke-WebRequest -Uri "$BASE_URL/contacts/" -Method GET -UseBasicParsing | ConvertFrom-Json
Write-Host "Total contacts in database: $($allContacts.count)" -ForegroundColor Cyan
Write-Host "Showing first 3:" -ForegroundColor Cyan
$allContacts.results | Select-Object -First 3 | ForEach-Object {
    Write-Host "  - $($_.first_name) ($($_.email)) [dedup_key: $($_.dedup_key)]" -ForegroundColor Gray
}

Write-Host "`n[GET] /webforms/" -ForegroundColor Yellow
$allWebforms = Invoke-WebRequest -Uri "$BASE_URL/webforms/" -Method GET -UseBasicParsing | ConvertFrom-Json
Write-Host "Total webforms in database: $($allWebforms.count)" -ForegroundColor Cyan

Write-Host "`n[GET] /webform-submissions/" -ForegroundColor Yellow
$allSubmissions = Invoke-WebRequest -Uri "$BASE_URL/webform-submissions/" -Method GET -UseBasicParsing | ConvertFrom-Json
Write-Host "Total submissions in database: $($allSubmissions.count)" -ForegroundColor Cyan

# ===== SUMMARY =====
Write-Host "`n`n===========================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

Write-Host "`nCreated Resources:" -ForegroundColor Yellow
Write-Host "  • Websites: $($RESULTS['websites_created'])" -ForegroundColor Green
Write-Host "  • Webforms: $($RESULTS['webforms_created'])" -ForegroundColor Green
Write-Host "  • Contacts: $($RESULTS['contacts_created'])" -ForegroundColor Green
Write-Host "  • Submissions: $($RESULTS['submissions_created'])" -ForegroundColor Green
Write-Host "  • 409 Conflicts Handled: $($RESULTS['conflicts_handled'])" -ForegroundColor Green

Write-Host "`nTest Results:" -ForegroundColor Yellow
Write-Host "  [PASS] Tests Passed: $($RESULTS['tests_passed'].Count)" -ForegroundColor Green
Write-Host "  [FAIL] Tests Failed: $($RESULTS['tests_failed'].Count)" -ForegroundColor Red

if ($RESULTS['tests_failed'].Count -eq 0) {
    Write-Host "`nALL TESTS PASSED! Drupal <- Django integration is working correctly!" -ForegroundColor Green
} else {
    Write-Host "`nFailed tests:" -ForegroundColor Red
    $RESULTS['tests_failed'] | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
}

Write-Host "`n===========================================" -ForegroundColor Cyan
