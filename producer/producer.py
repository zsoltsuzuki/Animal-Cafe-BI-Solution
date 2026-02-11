import time
import json
import random
from kafka import KafkaProducer
from faker import Faker

# Initialize Faker for synthetic data generation
fake = Faker()

# Kafka Producer Configuration
# This agent acts as the ingestion layer, transmitting data to the Kafka broker
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    # Serialize data to JSON format before encoding to UTF-8
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Target topic for Supply Chain / LCA emissions data
TOPIC_NAME = 'factory_emissions'

print(f"Starting data stream to topic: '{TOPIC_NAME}'... (Press Ctrl+C to stop)")

try:
    while True:
        # 1. Generate valid operational data
        # Simulating real-time monitoring of manufacturing nodes
        data = {
            'timestamp': int(time.time()),
            'factory_id': f"FAC-{random.randint(100, 999)}",
            'location': fake.country(),
            'material': random.choice(['Steel', 'Aluminum', 'Polyethylene', 'Glass', 'Cardboard']),
            'process_step': random.choice(['Extraction', 'Melting', 'Molding', 'Assembly', 'Packaging']),
            'energy_consumption_kwh': round(random.uniform(50.0, 500.0), 2),
            'co2_emissions_kg': round(random.uniform(10.0, 100.0), 2)
        }

        # 2. SIMULATE DATA ANOMALIES (Synthetic "Dirty Data")
        # 10% probability to generate malformed data for testing validation/cleansing layers
        if random.random() < 0.1:
            anomaly_type = random.choice(['missing_material', 'negative_emission'])
            if anomaly_type == 'missing_material':
                data['material'] = None       # Simulate NULL value
            elif anomaly_type == 'negative_emission':
                data['co2_emissions_kg'] = -99.9  # Simulate logical inconsistency

        # 3. Dispatch payload to the Kafka broker
        producer.send(TOPIC_NAME, value=data)
        
        print(f"Sent Payload: {data['factory_id']} | Material: {data['material']} | CO2: {data['co2_emissions_kg']}kg")
        
        # Simulate variable streaming frequency (0.5 to 2.0 seconds)
        time.sleep(random.uniform(0.5, 2.0))

except KeyboardInterrupt:
    print("\n[INFO] Streaming terminated by user.")
    producer.close()
