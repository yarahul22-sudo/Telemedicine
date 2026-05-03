# Device in Use Error - Troubleshooting Guide

## Error Message
```
Video call connection failed:
Device in use
Please refresh and try again.
```

## What This Means
Your browser cannot access the camera and/or microphone because they are already being used by another application or browser tab.

---

## Quick Fix (Try First)

### Option 1: Close Other Browser Tabs
1. Close any other browser tabs that might be using your camera
2. Check for any other video call apps open (Teams, Zoom, Meet, etc.)
3. Refresh the telemedicine page (F5 or Ctrl+R)
4. Try the video call again

### Option 2: Restart Camera/Microphone
1. **Close ALL applications** using your camera:
   - Video call apps (Teams, Zoom, Meet, Skype, Discord)
   - Video recording software (OBS, Camtasia)
   - Security software (some antivirus apps access camera)
2. Close your browser completely
3. Reopen browser and try again

### Option 3: Check Browser Permissions
1. Click the camera icon in your browser address bar
2. Ensure camera and microphone are **"Allow"**
3. Remove any "Block" permissions for telemedicine site
4. Refresh page and try again

---

## Detailed Troubleshooting

### Step 1: Check Active Applications

**Windows:**
```
Ctrl + Shift + Esc  (open Task Manager)
Look for apps using camera:
- Video Call applications
- Security/Antivirus software
- OBS, Camtasia, or streaming software
Close any suspicious apps
```

**Mac:**
```
Press Command + Space (Spotlight)
Type "Activity Monitor"
Search for camera/video related apps
Click and press "Quit"
```

### Step 2: Check Browser Camera Access

**Chrome:**
1. Go to address bar
2. Click the camera icon 🎥
3. Select "Manage"
4. Make sure site permission is "Allow"
5. Refresh page

**Firefox:**
1. Go to address bar
2. Click the camera icon 🎥
3. Check "Allow" is selected
4. Refresh page

**Edge:**
1. Address bar → camera icon 🎥
2. Click "Manage permissions"
3. Ensure camera/mic are "Allow"
4. Refresh page

### Step 3: Restart Browser Completely

**Chrome/Firefox/Edge:**
1. Close ALL tabs (⚠️ save your work first)
2. Close the entire browser
3. Wait 10 seconds
4. Reopen browser
5. Go to telemedicine and try again

### Step 4: Check Physical Camera/Microphone

1. **Is camera connected?**
   - For USB camera: Check cable is plugged in
   - For laptop built-in: No need to check connection

2. **Is microphone working?**
   - Try another app (voice recorder, Discord)
   - If no sound → hardware issue

3. **Is camera LED on?**
   - Green light = camera working
   - No light = might be in use or disabled

---

## Advanced Troubleshooting

### Disable Antivirus Camera Access
Some antivirus software blocks camera. Try:
1. Open Antivirus settings
2. Find "Camera Protection" or "Device Access"
3. Disable or Whitelist telemedicine browser
4. Try video call again

### Check Windows Device Manager
```
Right-click Windows button
Select "Device Manager"
Expand "Cameras"
If red X on camera → Right-click → "Enable"
Restart computer if needed
```

### Check System Settings (Windows)

**Camera Privacy Settings:**
```
Settings → Privacy & Security → Camera
Turn "Camera access" ON
Scroll down and enable for your browser
```

**Microphone Privacy Settings:**
```
Settings → Privacy & Security → Microphone
Turn "Microphone access" ON
Scroll down and enable for your browser
```

### Restart Windows Camera Service (Advanced)

```
Press Windows + R
Type: services.msc
Find: "Windows Camera Frame Server"
Right-click → Restart
Close and try again
```

---

## Fix by Operating System

### Windows 10/11

1. **Settings → Privacy & Security → Camera**
   - Toggle ON: Camera access
   - Scroll and enable browser

2. **Settings → Privacy & Security → Microphone**
   - Toggle ON: Microphone access
   - Scroll and enable browser

3. **Restart computer if still having issues**

### Mac

1. **System Preferences → Security & Privacy → Camera**
   - Add browser to allowed apps list

2. **System Preferences → Security & Privacy → Microphone**
   - Add browser to allowed apps list

3. **Restart browser and try again**

### Linux

1. **Check device permissions:**
   ```bash
   ls -la /dev/video0
   ```

2. **Add user to video group:**
   ```bash
   sudo usermod -aG video $USER
   ```

3. **Reboot and try again**

---

## Audio-Only Call Alternative

If camera issues persist, try audio-only call:

1. Add `?audio=1` to the video call URL
   ```
   http://localhost:8000/video-call/[appointment-id]/?audio=1
   ```

2. Or tell the doctor to use audio-only mode
3. You can always enable video later

---

## Still Having Issues?

### Collect Debug Information

Open browser console (F12 → Console tab):
```javascript
// Copy this and run in console:
navigator.mediaDevices.enumerateDevices().then(devices => {
  console.log('Available devices:');
  devices.forEach(device => {
    console.log(`${device.kind}: ${device.label} (${device.deviceId})`);
  });
});
```

**Expected output:**
```
Available devices:
audioinput: Built-in Microphone (default) - 123abc...
videoinput: Built-in Camera (default) - 456def...
audiooutput: Speaker (default) - 789ghi...
```

**If you see:**
- No videoinput → Camera hardware issue
- No audioinput → Microphone hardware issue
- Empty list → Driver issue

### Contact IT Support

Provide them with:
1. Device type (laptop/desktop)
2. Operating system (Windows/Mac/Linux)
3. Browser version (Chrome/Firefox/Edge)
4. Whether camera works in other apps
5. Console debug output from above

---

## Prevention Tips

✓ Keep only ONE browser tab with telemedicine open
✓ Close other video call apps before starting
✓ Grant camera/microphone permissions BEFORE clicking join
✓ Use same device each time (avoid switching)
✓ Restart browser after system updates
✓ Keep browser and OS updated

---

## Quick Checklist

Before calling tech support, verify:

- [ ] No other browser tabs with video open
- [ ] No other apps using camera (Teams, Zoom, etc.)
- [ ] Browser permissions set to "Allow" for camera/mic
- [ ] Browser is fully closed and restarted
- [ ] Computer was restarted
- [ ] Privacy settings in OS enable camera/mic access
- [ ] Physical camera is connected (if USB)
- [ ] Camera works in other apps (Photos app, etc.)
- [ ] No antivirus blocking camera access

---

## Error Reference

| Error | Cause | Solution |
|-------|-------|----------|
| Device in use | Camera/mic already used | Close other apps, restart browser |
| Device not found | No camera hardware | Check physical connection or USB cable |
| Permission denied | Browser blocked | Check browser camera permissions |
| Not allowed | OS blocked access | Check Privacy & Security settings |
| Hardware error | Camera failed | Restart computer, update drivers |

---

## Example Fixed Cases

**Case 1: Multiple Tabs**
- User had Zoom open in another tab
- **Fix:** Closed Zoom, refreshed page ✓

**Case 2: Browser Permission**
- Chrome blocked camera access
- **Fix:** Went to Settings → Privacy → enabled camera ✓

**Case 3: Antivirus Block**
- Norton blocked all camera access
- **Fix:** Disabled camera protection, whitelisted browser ✓

**Case 4: Windows Privacy**
- Camera access turned off in Settings
- **Fix:** Settings → Privacy → Enabled camera access ✓

---

## Quick Links

- Chrome Camera Permissions: https://support.google.com/chrome/answer/2693767
- Firefox Camera Permissions: https://support.mozilla.org/en-US/kb/firefox-page-element-permissions
- Windows Camera Privacy: https://support.microsoft.com/en-us/windows/camera-privacy-permissions-in-windows-11-0f6e25d1-f07c-4ea9-b19f-44ce5f4d31f8
- Mac Camera Privacy: https://support.apple.com/en-us/HT210602

