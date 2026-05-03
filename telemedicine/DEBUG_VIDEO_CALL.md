# Video Call Connection Issues - Troubleshooting Guide

## Problem Summary
Doctor side shows "connection error" during video call with patient.

## Root Causes Fixed

### 1. **Token Generation Issues**
- **Issue**: `request.user.uid` attribute didn't exist on CustomUser
- **Fix**: Added `@property uid` to CustomUser model that aliases to `id` (Firebase UID)

### 2. **Poor Error Handling**
- **Issue**: No error logging when token fetch failed
- **Fix**: Added comprehensive console logging and error messages

### 3. **Participant Connection Issues**
- **Issue**: Tracks not properly attached, audio elements not hidden
- **Fix**: Improved `participantConnected` and `trackSubscribed` functions with proper DOM handling

## Verification Steps

### Step 1: Check Twilio Credentials
```bash
# In Django shell
python manage.py shell
from django.conf import settings
print(f"Account SID: {settings.TWILIO_ACCOUNT_SID}")
print(f"API Key: {settings.TWILIO_API_KEY}")
print(f"API Secret: {settings.TWILIO_API_SECRET}")
```

**Expected**: All three should have non-empty values from `.env`

### Step 2: Check Browser Console Logs
1. Open video-call page (both as patient and doctor)
2. Open DevTools (F12) → Console tab
3. Look for logs starting with "DEBUG:" or "ERROR:"
4. **Expected doctor logs**:
   ```
   Fetching token from: /api/appointments/[id]/video-token/
   Token received: { token: "...", room_name: "...", identity: "..." }
   Creating local tracks with constraints: { audio: true, video: { width: 1280, height: 720 } }
   Created 2 local tracks
   Connecting to Twilio room: appointment_[id] with identity: Dr. [Name]
   Successfully connected to Twilio room
   Participant connected: [sid] [patient-name]
   ```

### Step 3: Test Token Generation API Directly
```bash
# Get appointment ID from database
# Then test the endpoint

curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/appointments/[appointment_id]/video-token/
```

**Expected Response**:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "room_name": "appointment_[id]",
  "identity": "Dr. Name"
}
```

### Step 4: Verify Firebase User Data
```bash
python manage.py shell
from telemedicine.firestore_db import db

# Check if appointment exists with patient_id and doctor_id
doc = db.collection('appointments').document('[appointment_id]').get()
print(doc.to_dict())
```

**Expected**: Should show both `patient_id` and `doctor_id` fields

### Step 5: Check Network Tab
1. During video call, open DevTools → Network tab
2. Look for requests to `/api/appointments/.../video-token/`
3. **Expected**: Status 200 with valid token response
4. **If 401/403**: Authentication issue - check token/session
5. **If 404**: Appointment not found - verify appointment ID

## Common Issues & Solutions

### Issue: "403 Forbidden" on token endpoint
**Solution**: 
- Ensure user is logged in
- Verify that user ID matches either `patient_id` or `doctor_id` in appointment
- Check role is correct (patient or doctor)

### Issue: "404 Not Found" on token endpoint  
**Solution**:
- Verify appointment ID in URL matches database
- Ensure Firestore collection path is correct
- Check that appointment document exists

### Issue: Token generated but still "connection error"
**Solution**:
- Check Twilio credentials in `.env`
- Verify Twilio account has video capability enabled
- Check browser console for Twilio SDK errors
- Ensure both client and server have same video SDK version (2.26.2)

### Issue: Can hear audio but no video
**Solution**:
- Camera permissions not granted - browser should show camera permission prompt
- Check `trackSubscribed` function is being called
- Verify video track is being attached to DOM

### Issue: One-way video (only patient sees doctor)
**Solution**:
- Check doctor's camera is enabled/not muted
- Verify doctor's local video preview appears
- Check browser console for track attachment errors
- Ensure both participants are in same Twilio room

## Debug Endpoints

### For Developer Testing
Add these temporary debug endpoints to `appointments/views.py`:

```python
@api_view(['GET'])
def debug_video_token(request, appointment_id):
    """Debug endpoint - remove in production"""
    from telemedicine.firestore_db import db
    
    # Check auth
    print(f"User: {request.user}, UID: {request.user.uid}")
    
    # Check appointment
    doc = db.collection('appointments').document(str(appointment_id)).get()
    print(f"Appointment exists: {doc.exists}")
    print(f"Appointment data: {doc.to_dict()}")
    
    # Try token generation
    return generate_video_token(request, appointment_id)
```

Then access: `http://localhost:8000/api/appointments/[id]/video-token/` (DEBUG version)

## Monitoring in Production

### Enable Logging
Add to `settings.py`:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'appointments': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Monitor Twilio Dashboard
1. Go to https://www.twilio.com/console/video/rooms
2. Check active rooms and participants
3. Monitor connection quality metrics
4. Check for API errors in Twilio console

## Files Modified
1. `appointments/views.py` - Enhanced token generation with logging
2. `templates/video-call.html` - Improved error handling and logging
3. `users/models/base.py` - Added `uid` property to CustomUser

## Next Steps if Still Having Issues

1. **Check Twilio Account**:
   - Verify account is active and has credit
   - Check API key permissions (should have Video grants)

2. **Browser Compatibility**:
   - Test with Chrome/Firefox (best support)
   - Check browser has camera/mic permissions

3. **Network**:
   - Check firewall/NAT isn't blocking WebRTC
   - Verify both participants have stable internet

4. **Collect Logs**:
   - Save browser console logs
   - Check Django server logs
   - Check Twilio dashboard logs
   - Share with development team
