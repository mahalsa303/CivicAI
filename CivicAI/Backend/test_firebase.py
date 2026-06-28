from services.firebase_service import db

db.collection("test").add({
    "message": "Firebase Connected"
})

print("Success")