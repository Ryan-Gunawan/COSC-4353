from app import app, db
from models import User

def promote_to_admin(email):
    # Open the application context
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            user.admin = True
            db.session.commit()
            print(f"User {user.email} is now an admin.")
        else:
            print("User not found")

if __name__ == "__main__":
    email = input("Enter email of user to promote to admin: ")
    promote_to_admin(email)
