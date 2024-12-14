from database import Base, engine
from models import User  # Import your models here

# Create all tables in the database
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
