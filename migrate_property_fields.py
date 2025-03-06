from app import app, db
from sqlalchemy import text

def add_property_fields():
    with app.app_context():
        # Execute raw SQL to add the columns
        db.session.execute(text('''
            ALTER TABLE property 
            ADD COLUMN property_description TEXT,
            ADD COLUMN operation VARCHAR(50) NOT NULL DEFAULT 'Venta',
            ADD COLUMN list_date DATE DEFAULT CURRENT_DATE,
            ADD COLUMN list_status VARCHAR(50) NOT NULL DEFAULT 'Activo',
            ADD COLUMN off_market_date DATE,
            ADD COLUMN close_date DATE,
            ADD COLUMN close_price NUMERIC(12,2)
        '''))
        db.session.commit()
        print("Successfully added new property fields")

if __name__ == '__main__':
    add_property_fields()
