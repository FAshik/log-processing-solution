import sys
print(sys.path)

from faker import Faker
from src.common.utils import create_kafka_producer, read_kafka_config
import time
import logging

def generate_log_entry(fake):
  return {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "level": fake.random_element(elements=('INFO', 'ERROR', 'DEBUG')),
    "source_ip": fake.ipv4(),
    "message": fake.sentence(),
  }

def produce_logs(producer, topic, fake):
  while True:
    log_entry = generate_log_entry(fake)
    producer.send(topic, value=log_entry)
    logging.info(f"Produced: {log_entry}")
    time.sleep(1)

def main():
  fake = Faker()
  producer = create_kafka_producer()
  topic = read_kafka_config()['logs_topic']
  produce_logs(producer, topic, fake)

if __name__ == "__main__":
  main()