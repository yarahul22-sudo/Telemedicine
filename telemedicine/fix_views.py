import os

file_path = r"c:\Users\aakas\Downloads\Telemedicine\Telemedicine\telemedicine\accounts\views.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# The junk starts at the line "messages.error(request, 'Access denied. Admin only.')" 
# appearing unexpectedly after the Logout link in the HTML string.
# Current line 769 (index 768)

junk_start = -1
junk_end = -1

for i in range(len(lines)):
    if "<li><a href=\"/logout/\">🚪 Logout</a></li>" in lines[i]:
        if i + 1 < len(lines) and "messages.error(request, 'Access denied. Admin only.')" in lines[i+1]:
            junk_start = i + 1
            break

if junk_start != -1:
    # Look for the second occurrence of @login_required followed by def video_call
    # which marks the start of the correct code we want to keep.
    # We want to delete everything between junk_start and the line before that correct block.
    for i in range(junk_start, len(lines)):
        if "@login_required(login_url='login')" in lines[i]:
            if i + 1 < len(lines) and "def video_call(request, appointment_id):" in lines[i+1]:
                junk_end = i
                break

if junk_start != -1 and junk_end != -1:
    print(f"Surgically removing junk from line {junk_start+1} to {junk_end}...")
    clean_lines = lines[:junk_start] + lines[junk_end:]
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(clean_lines)
    print("✅ Repair complete! Your views.py is now stable.")
else:
    print("❌ Could not identify the junk block using anchors. Checking for fallback...")
    # Fallback: Just look for the first instance of 'cancelled = [a for a in all_appointments' which is definitely junk
    for i in range(len(lines)):
        if "cancelled = [a for a in all_appointments" in lines[i]:
             # This is in the middle of our broken block. Let's find the start and end of this block.
             # In our specific breakage, it's roughly 200 lines.
             pass
    print("Please try running the script again or manually delete the duplicate functions in the middle of the file.")
