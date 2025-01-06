from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic, ConfigResource, ConfigResourceType
import json, yaml, os, time
import logging

def parse_log(log_line):
  try:
    logging.info(f"Parsing log: {log_line}")
    return json.loads(log_line)
  except json.JSONDecodeError as e:
    logging.error(f"Failed to parse log: {e}")
    return None

def read_config(config_path):
  with open(config_path, 'r') as file:
    config = yaml.safe_load(file)
  return config

def read_kafka_config():
  config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'kafka_config.yaml')
  return read_config(config_path)

def read_flink_config():
  config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'flink_config.yaml')
  return read_config(config_path)

def create_admin_client():
  return KafkaAdminClient(bootstrap_servers=read_kafka_config()['bootstrap_servers'])

def create_kafka_producer():
  return KafkaProducer(
    bootstrap_servers=read_kafka_config()['bootstrap_servers'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
  )

def create_kafka_consumer(topic):
  return KafkaConsumer(
    topic,
    bootstrap_servers=read_kafka_config()['bootstrap_servers'],
    auto_offset_reset=read_kafka_config()['offset_reset'],
    group_id=read_kafka_config()['logs_group_id']
  )

def topic_exists(topic_name, admin_client):
  if not admin_client:
    admin_client = create_admin_client()
  topic_metadata = admin_client.list_topics()
  return topic_name in topic_metadata

def create_topic(topic_name, num_partitions, replication_factor):
  admin_client = create_admin_client()
  
  if topic_exists(topic_name, admin_client):
    logging.info(f"Topic '{topic_name}' already exists.")
    return
  
  try:
    new_topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    admin_client.create_topics([new_topic])
    logging.info(f"Topic '{topic_name}' created.")
  except Exception as e:
    logging.error(f"Failed to create topic '{topic_name}': {e}")
  finally:
    admin_client.close()

def cleanup_kafka_topic(topic_name):
  admin_client = create_admin_client()
  if not topic_exists(topic_name, admin_client):
    logging.info(f"Topic '{topic_name}' does not exist.")
    return
  
  try:
    admin_client.delete_topics([topic_name])
    logging.info(f"Topic '{topic_name}' deleted.")
  except Exception as e:
    logging.error(f"Failed to delete topic '{topic_name}': {e}")
  finally:
    admin_client.close()

# if __name__ == "__main__":
#   cleanup_kafka_topic('logs')