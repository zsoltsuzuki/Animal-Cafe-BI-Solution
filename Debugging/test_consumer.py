import json
from kafka import KafkaConsumer

# MONITORING UTILITY: Simple Kafka Consumer
# Purpose: To verify real-time data flow from the producer before Spark processing.

# Initialize the Kafka Consumer
consumer = KafkaConsumer(
    'factory_emissions',  # Must match the topic in producer.py
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest', # Start reading from the beginning of the stream
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("-" * 50)
print("LCA STREAM MONITORING TOOL")
print("Listening for factory emission events on 'factory_emissions'...")
print("Press Ctrl+C to exit.")
print("-" * 50)

try:
    for message in consumer:
        # Extracting the payload from the Kafka message
        payload = message.value
        
        # Displaying formatted output for better readability during debugging
        timestamp = payload.get('timestamp')
        factory = payload.get('factory_id')
        material = payload.get('material')
        emissions = payload.get('co2_emissions_kg')
        
        print(f"[{timestamp}] | Factory: {factory} | Material: {material} | CO2 Impact: {emissions} kg")

except KeyboardInterrupt:
    print("\n[INFO] Monitoring tool stopped.")
finally:
    consumer.close()
