from transformers import pipeline
from src.common.utils import parse_log, create_kafka_consumer, read_kafka_config
import logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

logging.basicConfig(level=logging.INFO)

def process_message(message):
  log = parse_log(message.value.decode('utf-8'))
  print(f"Received log: {log}")
  if log['level'] == 'ERROR':
    process_log(log['message'])
    print(f"Processed log: {log['message']}")

def consume_logs():
  consumer = create_kafka_consumer(read_kafka_config()['logs_topic'])
  for message in consumer:
    process_message(message)

def train_model(log_entries, labels):
  model = make_pipeline(CountVectorizer(), MultinomialNB())
  model.fit(log_entries, labels)
  joblib.dump(model, 'log_classifier.pkl')
  print("Model trained and saved as log_classifier.pkl")

def load_model():
  return joblib.load('log_classifier.pkl')

def process_log(log_entry):
  model = pipeline("text-classification", model="distilbert-base-uncased")
  prediction = model(log_entry)
  print(prediction)

  # Load the trained model
  classifier = load_model()
  label = classifier.predict([log_entry])
  print(f"Log entry classified as: {label[0]}")

if __name__ == "__main__":
  log_entries = ["Error: failed to connect to database", "Warning: deprecated API usage"]
  labels = ["ERROR", "WARNING"]
  
  train_model(log_entries, labels)
  
  consume_logs()
