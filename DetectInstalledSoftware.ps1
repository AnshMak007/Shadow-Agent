# Detect-InstalledSoftware.ps1
# Lists installed software from registry

$softwareList = @()

# Registry paths (64-bit and 32-bit)
$regPaths = @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
)

foreach ($path in $regPaths) {
    $apps = Get-ItemProperty $path -ErrorAction SilentlyContinue | ForEach-Object {
        [PSCustomObject]@{
            DisplayName  = $_.DisplayName
            Version      = $_.DisplayVersion
            Publisher    = $_.Publisher
            InstallDate  = $_.InstallDate
            RegistryPath = $path
        }
    }
    $softwareList += $apps
}

# Output as JSON (so your service can parse easily)
$softwareList | Where-Object { $_.DisplayName } | ConvertTo-Json -Depth 3
