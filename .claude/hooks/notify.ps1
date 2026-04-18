# Windows PowerShell notification when Claude needs attention.
# Triggers on: permission prompts, idle, auth events.
# Works on Windows 10/11 with PowerShell 5+ (no extra installs needed).

param()

$input_text = $input | Out-String

# Parse JSON input
try {
    $data = $input_text | ConvertFrom-Json
    $message = if ($data.message) { $data.message } else { "Claude needs attention" }
    $title   = if ($data.title)   { $data.title   } else { "Claude Code" }
} catch {
    $message = "Claude needs attention"
    $title   = "Claude Code"
}

# Windows 10/11 toast notification via BurntToast or fallback to balloon
try {
    # Method 1: Use Windows.UI.Notifications (Windows 10+)
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

    $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent(
        [Windows.UI.Notifications.ToastTemplateType]::ToastText02
    )
    $template.SelectSingleNode("//text[@id=1]").InnerText = $title
    $template.SelectSingleNode("//text[@id=2]").InnerText = $message

    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Code")
    $notifier.Show([Windows.UI.Notifications.ToastNotification]::new($template))
} catch {
    # Fallback: System tray balloon (works on all Windows versions)
    try {
        Add-Type -AssemblyName System.Windows.Forms
        $balloon = New-Object System.Windows.Forms.NotifyIcon
        $balloon.Icon = [System.Drawing.SystemIcons]::Information
        $balloon.BalloonTipIcon = "Info"
        $balloon.BalloonTipTitle = $title
        $balloon.BalloonTipText = $message
        $balloon.Visible = $true
        $balloon.ShowBalloonTip(5000)
        Start-Sleep -Milliseconds 5100
        $balloon.Dispose()
    } catch {
        # Silent fallback — never block Claude
    }
}

exit 0
