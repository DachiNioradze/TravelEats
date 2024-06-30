from ext import app, db
from model import User
from datetime import datetime

with app.app_context():
    db.create_all()
    birth_date = datetime.strptime("12/10/2009", "%d/%m/%Y").date()

    admin_user = User("default.png","admin", birth_date, "adminpassword123", "male", "admin@gmail.com", "admin")
    db.session.add(admin_user)
    db.session.commit()