import sys
import os
from datetime import datetime

# Adjust path to find the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app
from extensions import db
from models.models import (
    CharacterClass, Species, Alignment,
    ItemType, Rarity, Region, Difficulty,
    Character, Item, Quest, Inventory, CharacterQuest
)

LOOKUP_SEED_DATA = {
    CharacterClass: [{"ClassName": "Warrior", "Description": "A powerful melee fighter."}],
    Species: [{"SpeciesName": "Human"}],
    Alignment: [{"AlignmentName": "Lawful Good"}],
    ItemType: [{"TypeName": "Weapon"}],
    Rarity: [{"RarityName": "Common"}],
    Region: [{"RegionName": "The Verdant Vale"}],
    Difficulty: [{"DifficultyName": "Novice"}],
}

def seed_lookup_tables():
    for model, rows in LOOKUP_SEED_DATA.items():
        if model.query.count() == 0:
            for row in rows:
                db.session.add(model(**row))
            print(f"✅ Seeded {model.__tablename__}")
    db.session.commit()

def seed_core_data():
    # Fetch lookups inside the function, while app context is active
    classes = {c.ClassName: c for c in CharacterClass.query.all()}
    species = {s.SpeciesName: s for s in Species.query.all()}
    alignments = {a.AlignmentName: a for a in Alignment.query.all()}
    item_types = {i.TypeName: i for i in ItemType.query.all()}
    rarities = {r.RarityName: r for r in Rarity.query.all()}
    regions = {r.RegionName: r for r in Region.query.all()}
    difficulties = {d.DifficultyName: d for d in Difficulty.query.all()}

    # Characters
    char = Character(
        CharacterName="Thorin Ironblade",
        ClassID=classes["Warrior"].ClassID,
        SpeciesID=species["Human"].SpeciesID, # Changed to Human as per your LOOKUP_SEED_DATA
        AlignmentID=alignments["Lawful Good"].AlignmentID,
        Level=12
    )
    db.session.add(char)
    db.session.commit()
    
    # Items
    item = Item(ItemName="Iron Sword", ItemTypeID=item_types["Weapon"].ItemTypeID, RarityID=rarities["Common"].RarityID)
    db.session.add(item)
    db.session.commit()

    # Quests
    quest = Quest(QuestName="Defend the Vale", RegionID=regions["The Verdant Vale"].RegionID, DifficultyID=difficulties["Novice"].DifficultyID)
    db.session.add(quest)
    db.session.commit()

    # Inventory & CharacterQuest
    db.session.add(Inventory(CharacterID=char.CharacterID, ItemID=item.ItemID))
    db.session.add(CharacterQuest(CharacterID=char.CharacterID, QuestID=quest.QuestID, CompletionDate=datetime.now()))
    db.session.commit()
    print("✅ Seeded Core Data")

def seed():
    app = create_app()
    with app.app_context():
        # IMPORTANT: Use the db instance from extensions
        from extensions import db
        
        # This will now work because db is linked to app inside create_app()
        db.create_all() 
        
        seed_lookup_tables()
        seed_core_data()
        print("\nSeed complete.")

if __name__ == "__main__":
    seed()