#!/usr/bin/env python
"""
Quick Device Access Fixer
Run this to diagnose and fix common camera/microphone issues
"""

import os
import sys
import platform
import subprocess

def print_header(title):
    print("\n" + "="*60)
    print(title.center(60))
    print("="*60)

def print_step(num, text):
    print(f"\n[{num}] {text}")

def run_command(cmd, description=""):
    """Run a command and return success"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def check_windows_camera():
    """Check Windows camera access"""
    print_header("WINDOWS CAMERA CHECK")
    
    # Check if camera is enabled in privacy settings
    print_step(1, "Checking Windows Privacy Settings...")
    
    print("""
To fix camera issues on Windows:

1. Open Settings (Windows + I)
2. Go to: Privacy & Security → Camera
3. Toggle ON: "Camera access"
4. Scroll down and toggle ON: Your browser name
5. Restart your browser

Or run this in PowerShell (as Admin):

# Enable camera access
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Privacy" ^
    /v DisableCameraAccess /t REG_DWORD /d 0 /f

# Restart camera service
Stop-Service -Name "FrameServerService" -Force
Start-Service -Name "FrameServerService"

""")

def check_mac_camera():
    """Check Mac camera access"""
    print_header("MAC CAMERA CHECK")
    
    print("""
To fix camera issues on Mac:

1. Open System Preferences
2. Go to: Security & Privacy → Camera
3. Check that your browser is in the allowed apps list
4. If not listed, add it:
   - Click the lock icon to unlock
   - Click + and select your browser
   - Lock the settings
5. Restart your browser

Or run this in Terminal:

# Grant camera access (may need to be repeated)
sqlite3 ~/Library/Application\\ Support/Google/Chrome/Default/Cookies

# Check camera permission:
launchctl list | grep -i camera

# Restart browser
""")

def check_linux_camera():
    """Check Linux camera access"""
    print_header("LINUX CAMERA CHECK")
    
    print("""
To fix camera issues on Linux:

1. Install necessary packages:
   sudo apt-get install cheese v4l-utils

2. Test camera:
   v4l2-ctl --list-devices
   cheese  # Opens camera test app

3. Fix permissions:
   sudo usermod -aG video $USER
   newgrp video
   # OR restart your computer

4. Check audio device:
   arecord -l
   aplay -l

5. Restart browser and try again
""")

def check_browser_permissions():
    """Guide to check browser permissions"""
    print_header("BROWSER PERMISSIONS CHECK")
    
    print("""
CHROME:
1. Go to any website
2. Click the lock icon 🔒 in address bar
3. Click "Site settings"
4. Find "Camera" and "Microphone"
5. Change from "Ask (default)" to "Allow"

FIREFOX:
1. Click menu button ☰
2. Settings → Privacy & Security
3. Scroll to "Permissions"
4. Click "Settings" next to Camera/Microphone
5. Find telemedicine.local and set to "Allow"

EDGE:
1. Click Settings ⚙️
2. Privacy, search, and services
3. Scroll to "App permissions"
4. Click Camera/Microphone
5. Toggle ON for your browser
""")

def check_running_processes():
    """Check for apps using camera"""
    print_header("CHECKING RUNNING PROCESSES")
    
    system = platform.system()
    
    if system == "Windows":
        print_step(1, "Checking for Windows apps using camera...")
        cmd = "tasklist | findstr /i \"zoom teams skype obs discord\""
        success, output = run_command(cmd)
        if output:
            print("⚠️  Found running apps that might use camera:")
            print(output)
            print("\n💡 Try closing these apps and refreshing your browser")
        else:
            print("✓ No video call apps found running")
    
    elif system == "Darwin":
        print_step(1, "Checking for Mac apps using camera...")
        cmd = "lsof | grep -E '(video|camera|Cameras)' | awk '{print $1}' | sort -u"
        success, output = run_command(cmd)
        if output:
            print("⚠️  Found processes using camera:")
            print(output)
            print("\n💡 Try closing these apps and refreshing your browser")
        else:
            print("✓ No camera access detected from other apps")
    
    elif system == "Linux":
        print_step(1, "Checking for Linux processes using camera...")
        cmd = "lsof /dev/video* 2>/dev/null || echo 'No processes using camera'"
        success, output = run_command(cmd)
        print(output if output else "✓ No processes using camera")

def check_firewall():
    """Check firewall settings"""
    print_header("FIREWALL CHECK")
    
    system = platform.system()
    
    if system == "Windows":
        print("""
Windows Firewall may block camera access:

1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Find your browser (Chrome, Firefox, Edge)
4. Check both Private and Public boxes
5. Click OK

Or run this PowerShell command (as Admin):

New-NetFirewallRule -DisplayName "Allow Camera" `
    -Direction Inbound -Action Allow -Program "%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe"
""")
    
    elif system == "Darwin":
        print("""
Mac Firewall (if enabled):

1. System Preferences → Security & Privacy
2. Click "Firewall Options"
3. Check that your browser is NOT in "Block all incoming connections"
4. Click OK
""")

def show_quick_fixes():
    """Show quick fixes to try"""
    print_header("QUICK FIXES TO TRY")
    
    fixes = [
        ("1. Restart Browser", "Close and reopen your browser completely"),
        ("2. Restart Computer", "Turn off and back on your computer"),
        ("3. Check Tabs", "Close any other browser tabs with video"),
        ("4. Close Other Apps", "Close Zoom, Teams, Skype, Discord, OBS, etc."),
        ("5. Refresh Page", "Press F5 or Ctrl+R to reload telemedicine"),
        ("6. Incognito Mode", "Open video call in private/incognito browser tab"),
        ("7. Different Browser", "Try Chrome, Firefox, or Edge if one fails"),
        ("8. Check Hardware", "Make sure USB camera is plugged in (if applicable)"),
    ]
    
    for title, desc in fixes:
        print(f"\n{title}")
        print(f"   → {desc}")

def main():
    """Main function"""
    system = platform.system()
    
    print_header("TELEMEDICINE VIDEO CALL DEVICE FIX")
    
    print(f"\nDetected OS: {system}")
    print(f"Python: {sys.version.split()[0]}")
    
    print("""
This tool will help you fix camera and microphone issues
for video calls on the telemedicine platform.
""")
    
    # Show quick fixes first
    show_quick_fixes()
    
    # Run OS-specific checks
    if system == "Windows":
        check_windows_camera()
    elif system == "Darwin":
        check_mac_camera()
    elif system == "Linux":
        check_linux_camera()
    
    # Check browser permissions
    check_browser_permissions()
    
    # Check running processes
    check_running_processes()
    
    # Check firewall
    check_firewall()
    
    # Final instructions
    print_header("NEXT STEPS")
    
    print("""
After trying the fixes above:

1. Close ALL browser tabs
2. Close your browser completely
3. Wait 5 seconds
4. Reopen browser
5. Go to telemedicine and try video call again

If still not working:

1. Restart your computer
2. Try a different browser
3. Try from a different computer
4. Contact IT support with:
   - OS and browser version
   - Whether camera works in other apps
   - Screenshots of error messages
""")
    
    print("\n" + "="*60)
    print("Good luck! 🎥📞".center(60))
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
