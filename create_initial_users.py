from database import SessionLocal, User, init_db
from auth import create_user

init_db()
db = SessionLocal()

# Create a regular user
try:
    create_user(db, "testuser", "testpassword", "test@test.com")
except Exception as e:
    print(f"Could not create testuser: {e}")

# Create an admin user
try:
    admin_user = create_user(db, "admin", "admin", "admin@admin.com")
    admin_user.is_admin = True
    db.commit()
except Exception as e:
    print(f"Could not create admin user: {e}")

db.close()
