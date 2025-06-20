@echo off
echo [1/5] Disconnecting old ADB connections...
adb disconnect

echo [2/5] Switching device to TCP/IP mode on port 5555...
adb tcpip 5555

echo [3/5] Waiting for device to initialize...
timeout /t 3 >nul

echo [4/5] Getting device IP address from wlan0...
FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^| find "inet "') DO set ipfull=%%G
FOR /F "tokens=1 delims=/" %%G IN ("%ipfull%") DO set ip=%%G

if defined ip (
    echo [5/5] Connecting to device at %ip%...
    adb connect %ip%
) else (
    echo [!] Automatic IP detection failed.
    echo [!] Trying manual IP fallback...

    :: === Edit this manually if needed ===
    set DEVICE_IP=192.168.1.5
    set ADB_PORT=5555
    adb connect %DEVICE_IP%:%ADB_PORT%
)

echo  Done.

