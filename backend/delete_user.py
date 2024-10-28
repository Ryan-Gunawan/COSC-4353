from app import app, db
from models import User

def delete_user(email):
    # Open the application context
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"Deleted user {user.email} from db")
        else:
            print("User not found")

if __name__ == "__main__":
    email = input("Enter email of user to delete: ")
    delete_user(email)
