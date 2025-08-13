from datetime import datetime

from app.core.security import get_hash_password
from app.db.session import get_db
from app.db.models import User
from app.core.config import settings


def create_admin_account():
    db_generator = get_db()  # Create the generator
    db = next(db_generator)  # Get the database session
    try:
        with db.begin():
            admin = db.query(User.username).filter(
                User.username == settings.HR_ADMIN_USERNAME).first()
            if not admin:
                new_user = User(
                    name=settings.HR_ADMIN_USERNAME,
                    username=settings.HR_ADMIN_USERNAME,
                    hash_password=get_hash_password(settings.HR_ADMIN_PASSWORD),
                    role=settings.default_admin_role,
                    is_active=settings.default_admin_active,
                    created_date=datetime.now(),
                    updated_date=datetime.now()
                )
                db.add(new_user)
    finally:
        db_generator.close()  # Ensure the generator is properly closed


def display_startup_message():
    """Display a rectangle message on app startup."""
    message = (
        "########################################\n"
        "#                                      #\n"
        "#     HR Recruitment Application       #\n"
        "#                                      #\n"
        "########################################"
    )
    print(f"[INFO]\n{message}")
    
    
def format_candidate_name(candidate_name: str):
    return "_".join(candidate_name.split())
