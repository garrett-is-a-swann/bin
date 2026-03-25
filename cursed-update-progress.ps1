Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

[ComImport, Guid("ea1afb91-9e28-4b86-90e9-9e9f8a5eefaf")]
[InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface ITaskbarList3 {
    void HrInit();
    void AddTab(IntPtr hwnd);
    void DeleteTab(IntPtr hwnd);
    void ActivateTab(IntPtr hwnd);
    void SetActiveAlt(IntPtr hwnd);
    void MarkFullscreenWindow(IntPtr hwnd, bool fFullscreen);
    void SetProgressValue(IntPtr hwnd, ulong ullCompleted, ulong ullTotal);
    void SetProgressState(IntPtr hwnd, int tbpFlags);
}

[ComImport, Guid("56fdf344-fd6d-11d0-958a-006097c9a090")]
[ClassInterface(ClassInterfaceType.None)]
public class TaskbarInstance {}
"@

$type = [System.Type]::GetTypeFromCLSID([System.Guid]"56fdf344-fd6d-11d0-958a-006097c9a090")
$taskbar = [System.Activator]::CreateInstance($type)
[ITaskbarList3].GetMethod("HrInit").Invoke($taskbar, $null)
Write-Host "HrInit called"

$proc = Get-Process discord | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
Write-Host "Process: $proc"
Write-Host "PID: $($proc.Id)"
$hwnd = $proc.MainWindowHandle
Write-Host "HWND: $hwnd"
Write-Host "Progress value: $($args[0])"

[ITaskbarList3].GetMethod("SetProgressValue").Invoke($taskbar, @([IntPtr]$hwnd, [uint64]$args[0], [uint64]100))
