from app import app, db
from models import Spirit, Location, Exorcist

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add locations if none exist
        if not Location.query.first():
            locations = [
                Location(name="Haunted Mansion"),
                Location(name="Abandoned Hospital"),
                Location(name="Dark Forest"),
                Location(name="Old Schoolhouse"),
                Location(name="Cursed Temple")
            ]
            db.session.add_all(locations)
            db.session.commit()
        
        # Add exorcists if none exist
        if not Exorcist.query.first():
            exorcists = [
                Exorcist(name="Reigen Arataka", success_rate=95.0),
                Exorcist(name="Mob", success_rate=99.9),
                Exorcist(name="Dimple", success_rate=75.0),
                Exorcist(name="Serizawa", success_rate=85.0),
                Exorcist(name="Tome", success_rate=60.0)
            ]
            db.session.add_all(exorcists)
            db.session.commit()
        
        # Add spirits if none exist
        if not Spirit.query.first():
            # Get locations first
            mansion = Location.query.filter_by(name="Haunted Mansion").first()
            hospital = Location.query.filter_by(name="Abandoned Hospital").first()
            forest = Location.query.filter_by(name="Dark Forest").first()
            
            spirits = [
                Spirit(
                    name="The Weeping Bride",
                    type="Apparition",
                    location_id=mansion.id,
                    threat_level="High"
                ),
                Spirit(
                    name="Dr. Scalpel",
                    type="Poltergeist",
                    location_id=hospital.id,
                    threat_level="Medium"
                ),
                Spirit(
                    name="Forest Guardian",
                    type="Nature Spirit",
                    location_id=forest.id,
                    threat_level="Low"
                ),
                Spirit(
                    name="The Laughing Jester",
                    type="Malevolent Entity",
                    location_id=mansion.id,
                    threat_level="High"
                ),
                Spirit(
                    name="Lost Child",
                    type="Ghost",
                    location_id=hospital.id,
                    threat_level="Low"
                )
            ]
            db.session.add_all(spirits)
            db.session.commit()
        
        print("Database initialized with sample data!")

if __name__ == "__main__":
    init_db()