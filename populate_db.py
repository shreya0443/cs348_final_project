# populate_db.py
from datetime import datetime
from app import app, db  # Import your Flask app and db instance
from models import Spirit, Location, Exorcist  # Import your models

def populate_database():
    with app.app_context():
        try:
            # Clear existing data (be careful with this in production!)
            db.session.query(Spirit).delete()
            db.session.query(Location).delete()
            db.session.query(Exorcist).delete()
            
            # Add locations (Mob Psycho 100 inspired)
            locations = [
                Location(id=22222, name="Salt Middle School"),
                Location(id=22223, name="Black Vinegar Middle School"),
                Location(id=22224, name="Spice City Downtown"),
                Location(id=22225, name="Claw Headquarters"),
                Location(id=22226, name="Abandoned Hospital"),
                Location(id=22227, name="Mogami's Haunted Mansion"),
                Location(id=22228, name="Ramen Shop"),
                Location(id=22229, name="Seasoning City Center")
            ]
            db.session.add_all(locations)
            
            # Add exorcists (Mob Psycho characters)
            exorcists = [
                Exorcist(id=11111, name="Shigeo Kageyama (Mob)", success_rate=1.0),
                Exorcist(id=11112, name="Reigen Arataka", success_rate=0.8),
                Exorcist(id=11113, name="Teruki Hanazawa", success_rate=0.7),
                Exorcist(id=11114, name="Ritsu Kageyama", success_rate=0.6),
                Exorcist(id=11115, name="Dimple (when helpful)", success_rate=0.5)
            ]
            db.session.add_all(exorcists)
            
            # Add spirits (Mob Psycho spirits)
            spirits = [
                Spirit(id=33333, name="Dimple", type="Mischievous", location_id=22222, threat_level="Low", status="Active"),
                Spirit(id=33334, name="Evil Spirit", type="Vengeful", location_id=22223, threat_level="Medium", status="Active"),
                Spirit(id=33335, name="Urban Legend Ghost", type="Cursed", location_id=22226, threat_level="High", status="Active"),
                Spirit(id=33336, name="Tsuchinoko", type="Cryptid", location_id=22224, threat_level="Low", status="Active"),
                Spirit(id=33337, name="Claw Boss Spirit", type="Possessive", location_id=22225, threat_level="High", status="Active"),
                Spirit(id=33338, name="Mogami", type="Evil", location_id=22227, threat_level="High", status="Active", reported_at=datetime(2025, 2, 15)),
                Spirit(id=33339, name="Ramen Shop Ghost", type="Hungry", location_id=22228, threat_level="Low", status="Active", reported_at=datetime(2025, 1, 10)),
                Spirit(id=33340, name="Toichiro's Spirit", type="Powerful", location_id=22229, threat_level="High", status="Exorcised", reported_at=datetime(2024, 12, 5)),
                Spirit(id=33341, name="Scarf Face Spirit", type="Vengeful", location_id=22223, threat_level="Medium", status="Active", reported_at=datetime(2025, 3, 1))
            ]
            db.session.add_all(spirits)
            
            # Commit changes
            db.session.commit()
            print("Successfully populated database with Mob Psycho 100 data!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    populate_database()