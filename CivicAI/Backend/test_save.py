from services.firebase_service import save_issue

save_issue({
    "category": "Road Damage",
    "severity": "High",
    "status": "Open"
})

print("Saved")