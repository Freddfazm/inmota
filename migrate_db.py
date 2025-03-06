from app import app, db

def add_garage_spaces_column():
    with app.app_context():
        # Execute raw SQL to add the column
        db.session.execute('ALTER TABLE property ADD COLUMN garage_spaces INTEGER NOT NULL DEFAULT 0')
        db.session.commit()
        print("Successfully added garage_spaces column")

if __name__ == '__main__':
    add_garage_spaces_column()
