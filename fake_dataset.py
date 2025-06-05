import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for English locale
fake = Faker('en_IN') # Using en_IN for Indian context, though general 'en_US' is fine too

# --- Configuration ---
NUM_PATIENTS = 5000 # Number of unique patients
NUM_VISITS_PER_PATIENT = 1 # Average number of visits per patient (can be randomized)
MAX_DRUGS_PER_PRESCRIPTION = 5 # Maximum number of drugs in one prescription
MIN_DRUGS_PER_PRESCRIPTION = 1 # Minimum number of drugs in one prescription
OUTPUT_FILENAME = './fake_prescriptions.csv'

# --- List of Common (Fake) Drugs and Conditions ---
# More realistic names can be added
common_drugs = [
    "Paracetamol", "Ibuprofen", "Amoxicillin", "Azithromycin", "Omeprazole",
    "Metformin", "Lisinopril", "Atorvastatin", "Amlodipine", "Levothyroxine",
    "Prednisone", "Pantoprazole", "Cetirizine", "Sertraline", "Fluoxetine",
    "Insulin", "Ventolin", "Warfarin", "Hydrochlorothiazide", "Diazepam",
    "Furosemide", "Gabapentin", "Tramadol", "Codeine", "Doxycycline",
    "Nifedipine", "Simvastatin", "Ciprofloxacin", "Ranitidine", "Aspirin"
]

common_conditions = [
    "Common Cold", "Flu", "Hypertension", "Diabetes Type 2", "Asthma",
    "Allergies", "Depression", "Anxiety", "Infection (Bacterial)",
    "Acid Reflux", "Hyperlipidemia", "Pain (Acute)", "Migraine",
    "Thyroid Disorder", "Arthritis", "Bronchitis", "Pneumonia",
    "Urinary Tract Infection", "Cardiac Arrhythmia", "Dermatitis"
]

# Define some plausible drug combinations for stronger rules (optional, but good for testing)
# These will be explicitly added to some prescriptions
plausible_combinations = [
    ("Paracetamol", "Ibuprofen"), # Pain/Fever
    ("Metformin", "Insulin"),    # Diabetes management
    ("Lisinopril", "Hydrochlorothiazide"), # Hypertension
    ("Amoxicillin", "Omeprazole"), # Antibiotic + Acid reflux (if antibiotic causes upset stomach)
    ("Atorvastatin", "Lisinopril"), # Cholesterol + BP (common comorbidities)
    ("Sertraline", "Diazepam"), # Depression + Anxiety
    ("Ventolin", "Prednisone") # Asthma exacerbation
]

# --- Generate Data ---
data = []
prescription_id_counter = 1

for _ in range(NUM_PATIENTS):
    patient_id = fake.uuid4() # Unique patient ID
    patient_gender = random.choice(['Male', 'Female', 'Other'])
    patient_age = random.randint(18, 90) # Age range

    num_visits = random.randint(1, NUM_VISITS_PER_PATIENT + 2) # Randomize visits a bit

    for _ in range(num_visits):
        prescription_date = fake.date_time_between(
            start_date='-2y', end_date='now'
        ).strftime('%Y-%m-%d %H:%M:%S')

        # Randomly select a condition (optional, but adds context)
        condition = random.choice(common_conditions)

        # Determine number of drugs for this prescription
        num_drugs = random.randint(MIN_DRUGS_PER_PRESCRIPTION, MAX_DRUGS_PER_PRESCRIPTION)

        # Generate a set of unique drugs for this prescription
        prescribed_drugs = set()

        # Introduce some plausible combinations for stronger rules
        if random.random() < 0.3: # 30% chance to include a plausible combination
            combo = random.choice(plausible_combinations)
            prescribed_drugs.add(combo[0])
            prescribed_drugs.add(combo[1])

        # Fill the rest with random drugs until max_drugs_per_prescription
        while len(prescribed_drugs) < num_drugs:
            prescribed_drugs.add(random.choice(common_drugs))

        data.append({
            'PatientID': patient_id,
            'PrescriptionID': f'PRES-{prescription_id_counter:05d}',
            'PrescriptionDate': prescription_date,
            'Condition': condition,
            'PatientAge': patient_age,
            'PatientGender': patient_gender,
            'DrugsPrescribed': ','.join(sorted(list(prescribed_drugs))) # Store as comma-separated string
        })
        prescription_id_counter += 1

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv(OUTPUT_FILENAME, index=False)

print(f"Fake medical prescription dataset generated: {OUTPUT_FILENAME}")
print(f"Total prescriptions: {len(df)}")
print("\nFirst 5 rows:")
print(df.head())
print("\nSome common drugs and conditions included:")
print(f"Drugs: {random.sample(common_drugs, 5)}")
print(f"Conditions: {random.sample(common_conditions, 3)}")