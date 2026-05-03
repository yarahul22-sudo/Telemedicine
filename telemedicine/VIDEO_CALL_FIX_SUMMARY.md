# Video Call Connection Error - FIXED

## Issues Identified & Fixed

### 1. **Missing `uid` Property on CustomUser Model** ❌ → ✅
**Problem:**
- Token generation code called `request.user.uid` but CustomUser didn't have this property
- This caused AttributeError when doctor tried to join video call

**Fix Applied:**
```python
# In users/models/base.py
@property
def uid(self):
    """Alias for id (Firebase UID)"""
    return self.id
```

**File Modified:** `users/models/base.py`

---

### 2. **Poor Error Handling in Token Generation** ❌ → ✅
**Problem:**
- No logging when token fetch failed
- Generic error message "Connection error" without details
- Difficult to debug what went wrong

**Fix Applied:**
- Added comprehensive debug logging to `generate_video_token()` view
- Validates Twilio credentials before use
- Checks if appointment exists in Firestore
- Validates user authorization (patient or doctor)
- Provides specific error messages for each failure case
- Returns detailed error information to client

**Improvements:**
```python
print(f"DEBUG: Token Request - Patient: {patient_id}, Doctor: {doctor_id}, User: {user_id}")
print(f"DEBUG: Generating Twilio Token - Identity: {identity}, Room: {room_name}")
print(f"DEBUG: Token generated successfully, length: {len(jwt_token)}")
```

**File Modified:** `appointments/views.py`

---

### 3. **Inadequate Client-Side Error Handling** ❌ → ✅
**Problem:**
- Fetch errors silently caught and showed generic "Connection error"
- No response status checking
- Audio elements not properly handled
- Participant connection issues not logged

**Fixes Applied:**
```javascript
// Check response status
if (!resp.ok) {
    const errorData = await resp.json();
    console.error('Token fetch error:', resp.status, errorData);
    throw new Error(`Failed to get token: ${errorData.error || resp.statusText}`);
}

// Add network quality monitoring
networkQuality: { local: 1, remote: 1 },

// Improved codec preferences
preferredCodecs: [
    { codec: 'VP9', enable: true },
    { codec: 'VP8', enable: true },
    { codec: 'H264', enable: true }
]
```

**File Modified:** `templates/video-call.html`

---

### 4. **Participant Connection & Track Handling Issues** ❌ → ✅
**Problem:**
- Tracks not properly logged when attached
- Audio elements showing in video area
- No handling for participant reconnection events
- Missing error handling for track attachment failures

**Fixes Applied:**
```javascript
// Proper audio element handling
if (track.kind === 'audio') {
    const audioEl = track.attach();
    audioEl.style.display = 'none';  // Hide audio element
    document.body.appendChild(audioEl);
}

// Added reconnection listeners
activeRoom.on('participantReconnecting', p => {
    console.log('Participant reconnecting:', p.sid);
    statusText.textContent = 'Reconnecting...';
});

activeRoom.on('participantReconnected', p => {
    console.log('Participant reconnected:', p.sid);
    statusText.textContent = 'Connected';
});
```

**File Modified:** `templates/video-call.html`

---

## Testing the Fixes

### Method 1: Run Diagnostic Script
```bash
cd telemedicine
python test_video_connection.py
```

This checks:
- ✓ Twilio credentials configured
- ✓ Firestore connection working
- ✓ Appointments exist in database
- ✓ Token generation works
- ✓ User permissions correct

### Method 2: Browser Console Testing
1. Open video call page as doctor
2. Press F12 to open DevTools
3. Go to Console tab
4. Look for these debug logs:

**Expected Success Logs:**
```
Fetching token from: /api/appointments/[id]/video-token/
Token received: { token: "...", room_name: "...", identity: "..." }
Creating local tracks with constraints: { audio: true, video: { ... } }
Created 2 local tracks
Connecting to Twilio room: appointment_[id] with identity: Dr. John Smith
Successfully connected to Twilio room
Participant connected: [sid] Jane Patient
Subscribing to video track from Jane Patient
Track subscribed: video from Jane Patient
Video element attached
```

### Method 3: Network Tab Testing
1. Open video call
2. Press F12 → Network tab
3. Filter: `appointment.*video-token`
4. Check response:

**Expected Response (200 OK):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "room_name": "appointment_abc123",
  "identity": "Dr. John Smith"
}
```

---

## What Changed

### Files Modified: 3

1. **`users/models/base.py`**
   - Added `uid` property property to CustomUser
   - Lines: 48-51

2. **`appointments/views.py`**
   - Enhanced `generate_video_token()` with comprehensive logging
   - Added credentials validation
   - Added error details to response
   - Lines: 438-494

3. **`templates/video-call.html`**
   - Improved `connectToCall()` function with error handling
   - Improved `participantConnected()` function with logging
   - Improved `trackSubscribed()` function with proper DOM handling
   - Added reconnection event listeners
   - Lines: 365-435, 437-469

### Files Added: 2

1. **`DEBUG_VIDEO_CALL.md`** - Troubleshooting guide
2. **`test_video_connection.py`** - Diagnostic script

---

## Doctor Side Connection Flow (Now Fixed)

```
Doctor opens video call
    ↓
[connectToCall() executes]
    ↓
Fetch token from /api/appointments/{id}/video-token/
    ↓
[Server validates]:
  - User is authenticated
  - User is doctor or patient
  - Appointment exists in Firestore
  - Twilio credentials valid
    ↓
✓ Token generated successfully
    ↓
[Client creates local tracks]:
  - Audio track ✓
  - Video track ✓
    ↓
[Client connects to Twilio room with token]
    ↓
✓ Successfully connected to Twilio
    ↓
[Wait for patient to join]
    ↓
✓ Patient joins room
    ↓
[Attach participant tracks]:
  - Video track → Display in main area
  - Audio track → Hidden element
    ↓
✓ Video call connected and working!
```

---

## Verification Checklist

- [x] CustomUser has `uid` property
- [x] Token generation includes detailed logging
- [x] Token generation validates credentials
- [x] Token generation validates user authorization
- [x] Token response includes all required fields
- [x] Client properly checks response status
- [x] Client logs token fetch errors
- [x] Client properly attaches video tracks
- [x] Client properly hides audio elements
- [x] Client logs participant connection
- [x] Client handles reconnection events
- [x] Browser console shows detailed debug logs
- [x] Twilio SDK version correct (2.26.2)

---

## Next Steps for Doctor-Patient Video Calls

### Before Starting Call:
1. Ensure both have camera/mic permissions granted
2. Test audio/video locally before connecting
3. Check stable internet connection

### During Call:
1. Monitor browser console for any errors
2. If connection drops, page will show "Reconnecting..."
3. Use mute/unmute buttons to control audio/video

### If Still Having Issues:
1. Run `python test_video_connection.py` to verify setup
2. Check browser console logs (F12 → Console)
3. Check Django server logs for errors
4. Verify Twilio credentials in `.env` file

---

## Error Messages Now Fixed

| Old Message | New Message | Status |
|---|---|---|
| "Connection error" | "Connection failed: 403" or specific error | ✓ Clear |
| No logging | Full debug logs in console | ✓ Visible |
| Silent failures | Detailed error with cause | ✓ Debuggable |

---

## Summary
The video call connection error on doctor's side is now **FIXED** by:
1. ✓ Adding missing `uid` property to CustomUser
2. ✓ Improving token generation with full logging
3. ✓ Adding comprehensive error handling on client
4. ✓ Properly handling track attachment and audio

Doctor and patient should now successfully connect to video calls without connection errors!
