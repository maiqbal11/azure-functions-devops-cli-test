<#
.SYNOPSIS
    Runs Azure Functions E2E Tests on the local development environment
.DESCRIPTION
    Spin up `func host start` and run tests on local machine
.EXAMPLE
    ./run_all_tests_local.ps1
.EXAMPLE
    ./run_all_tests_local.ps1 -AppPath v2\dotnet\2
.EXAMPLE
    ./run_all_tests_local.ps1 -AppPath v2\dotnet\2 -DefaultPort 7071
#>
param (
    [ValidatePattern("v[\d|\.]+\\\w+\\[\d|\.]+")]
    [string]$AppPath = $null, # v2\dotnet\2

    [int]$DefaultPort = 7071 # func host start --port 7071
)

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$TestAppsPath = "$ProjectRoot\test_apps"
$TestsPath = "$ProjectRoot\tests"

# Check virtual environment
if (-not $env:VIRTUAL_ENV) {
    Write-Warning "Please run this script in a Python virtual environment with requirements.txt resolved"
    return
}

# Check function core tools
$CoreTools = Get-Command "func" -ErrorAction SilentlyContinue
if (-not $CoreTools) {
    Write-Warning "Please ensure you have function core tools installed"
    return
}

# Start tests discovery
$AppPaths = @()
if ($AppPath) {
    $AppPaths = @($AppPath)
} else {
    foreach ($hostVersion in (Get-ChildItem $TestAppsPath)) {
        foreach ($language in (Get-ChildItem $hostVersion)) {
            foreach ($workerVersion in (Get-ChildItem $language)) {
                $hostVersionName = $hostVersion.BaseName
                $languageName = $language.BaseName
                $workerVersionName = $workerVersion.BaseName
                $AppPaths += "$hostVersionName\$languageName\$workerVersionName"
            }
        }
    }
}

# Start function hosts
$JobNames = @()
for ($i = 0; $i -lt $AppPaths.Count; $i++) {
    $app = $AppPaths[$i]
    $testApp = "$TestAppsPath\$app"

    # Start func host
    $port = $DefaultPort + $i
    $jobName = "AzureFunctionsCoreTools$port"
    Start-Job -Name "$jobName" -ScriptBlock {
        cd $args[0]
        func host start --port $args[1]
    } -ArgumentList @("$testApp", "$port") -ErrorAction SilentlyContinue
    # Record Jobs
    $JobNames += $jobName
}

# Start tests
Start-Sleep -Seconds 10
for ($i = 0; $i -lt $AppPaths.Count; $i++) {
    $app = $AppPaths[$i]
    $testDir = "$TestsPath\$app"

    # Start test
    $port = $DefaultPort + $i
    $testName = "TestAzureFunctionsCoreTools$port"
    Start-Job -Name "$testName" -ScriptBlock {
        cd $args[0]
        $port = $args[1]
        $env:FunctionAppUrl = "http://localhost:$port"
        python -B -m pytest $args[2]
    } -ArgumentList @("$ProjectRoot", "$port", "$testDir")
}

# Collect tests
$currentJobNames = $JobNames
try {
    while ($currentJobNames.Count -gt 0) {
        $newJobNames = @()
        foreach ($jobName in $currentJobNames) {
            $testName = "Test$jobName"
            $testJob = Get-Job -Name @($testName)
            if ($testJob.State -eq "Running") {
                $newJobNames += $jobName
            }
            if ($testJob.State -eq "Completed") {
                $message = Receive-Job -Name @($testName)
                Write-Output $message
            }
        }
        $currentJobNames = $newJobNames
        Start-Sleep -Seconds 1
    }
} finally {
    foreach ($jobName in $JobNames) {
        $testName = "Test$jobName"
        Write-Output "Cleaning Up Jobs $testName, $jobName"
        Remove-Job -Name @($testName, $jobName) -Force
    }
}
