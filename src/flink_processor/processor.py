from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.datastream.functions import ProcessFunction
from pyflink.common.serialization import SimpleStringSchema
# from pyflink.common import Configuration
from src.common.utils import parse_log, read_kafka_config

# def configure_flink_for_kubernetes():
#   config = Configuration()
#   config.set_string("jobmanager.rpc.address", "flink-jobmanager")
#   config.set_integer("taskmanager.numberOfTaskSlots", 4)
#   config.set_integer("parallelism.default", 2)
#   return config

# env = StreamExecutionEnvironment.get_execution_environment(configure_flink_for_kubernetes())

class LogProcessor(ProcessFunction):
  def process_element(self, value, ctx):
    log = parse_log(value)
    if log and 'error' in log.get('message', '').lower():
      print(f"Critical log found: {log}")
      #TODO: Add notification logic here

def create_kafka_consumer(topic, properties):
  return FlinkKafkaConsumer(
    topics=topic,
    deserialization_schema=SimpleStringSchema(),
    properties={
      'bootstrap.servers': read_kafka_config()['bootstrap_servers'],
      'group.id': read_kafka_config()['logs_group_id'],
      'auto.offset.reset': read_kafka_config()['offset_reset']
    }
  )

def main():
  env = StreamExecutionEnvironment.get_execution_environment()
  kafka_consumer = create_kafka_consumer(read_kafka_config()['logs_topic'])
  ds = env.add_source(kafka_consumer)
  ds.process(LogProcessor()).print()
  env.execute("Flink Log Processor")

if __name__ == "__main__":
  main()
