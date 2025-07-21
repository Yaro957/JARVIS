@echo off
echo [1/6] Disconnecting old ADB connections...
adb disconnect

echo [2/6] Switching device to TCP/IP mode on port 5555...
adb tcpip 5555

echo [3/6] Waiting for device to initialize...
timeout /t 3 >nul

echo [4/6] Getting device IP address from wlan0...
FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^| find "inet "') DO set ipfull=%%G
FOR /F "tokens=1 delims=/" %%G IN ("%ipfull%") DO set phone_ip=%%G

:: Get PC IP (assuming Wi-Fi connection)
FOR /F "tokens=14" %%a IN ('ipconfig ^| findstr /i "IPv4"') DO set pc_ip=%%a

:: Extract subnet (first 3 octets) from both
FOR /F "tokens=1-3 delims=." %%a IN ("%phone_ip%") DO set phone_subnet=%%a.%%b.%%c
FOR /F "tokens=1-3 delims=." %%a IN ("%pc_ip%") DO set pc_subnet=%%a.%%b.%%c

:: Check if same subnet
if "%phone_subnet%"=="%pc_subnet%" (
    echo [5/6] Phone and PC are on the same network (%phone_subnet%.x)
    echo [6/6] Connecting to device at %phone_ip%...
    adb connect %phone_ip%
) else (
    echo [!] Phone and PC are NOT on the same network.
    echo [!] Attempting manual fallback...

    :: === Edit this manually if needed ===
    set DEVICE_IP=192.168.1.5
    set ADB_PORT=5555
    adb connect %DEVICE_IP%:%ADB_PORT%
)

echo Done.
pause
