from sqlmodel import Session
from main import Complaint, engine

complaints = [
    Complaint(title="Pothole on Main Street", description="Large pothole damaging vehicles", status="open"),
    Complaint(title="Streetlight not working", description="Dark street, unsafe at night", status="claimed", volunteer="Team A"),
    Complaint(title="Overflowing garbage bin", description="Needs urgent cleaning", status="sponsored", sponsor="Green NGO"),
    Complaint(title="Broken bench in park", description="Dangerous for children", status="completed"),
]

with Session(engine) as session:
    for c in complaints:
        session.add(c)
    session.commit()
print("✅ Seed data inserted")
