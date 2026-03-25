# Test 1: Brute Force Detection
Write-Host "=== Testing Brute Force Detection ===" -ForegroundColor Cyan
$bruteForceBody = @{
    input_type = "log"
    content = @"
FAILED login attempt for user admin
FAILED login attempt for user admin
FAILED login attempt for user admin
FAILED login attempt for user admin
FAILED login attempt for user admin
FAILED login attempt for user admin
"@
    options = @{
        mask = $true
        block_high_risk = $true
        log_analysis = $true
    }
} | ConvertTo-Json

Write-Host "Request Body:" -ForegroundColor Yellow
$bruteForceBody
Write-Host ""

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/analyze" -Method POST -ContentType "application/json" -Body $bruteForceBody -UseBasicParsing
$result = $response.Content | ConvertFrom-Json
Write-Host "Response:" -ForegroundColor Yellow
$result | ConvertTo-Json -Depth 10
Write-Host ""

# Test 2: Chat Token Detection
Write-Host "=== Testing Chat Token Detection ===" -ForegroundColor Cyan
$chatBody = @{
    input_type = "chat"
    content = "Hi my token is Bearer eyJhbGciOiJIUzI1NiJ9.test and secret=mysecretkey"
    options = @{
        mask = $true
        block_high_risk = $true
        log_analysis = $false
    }
} | ConvertTo-Json

Write-Host "Request Body:" -ForegroundColor Yellow
$chatBody
Write-Host ""

$response2 = Invoke-WebRequest -Uri "http://localhost:8000/api/analyze" -Method POST -ContentType "application/json" -Body $chatBody -UseBasicParsing
$result2 = $response2.Content | ConvertFrom-Json
Write-Host "Response:" -ForegroundColor Yellow
$result2 | ConvertTo-Json -Depth 10
