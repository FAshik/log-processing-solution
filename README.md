# Log Processing Solution

This project processes logs in real-time to identify and notify about critical events. It includes solutions using:
- Kafka Consumer for pre-processing logs.
- Apache Flink for stream processing and proactive notifications.

## Project Structure
- **kafka_consumer**: Kafka consumer-based log processing solution.
- **flink_processor**: Flink-based log processing solution for high-scale, time-based log aggregation.
- **common**: Shared utilities and configurations.
- **scripts**: Helpful shell scripts for setup and execution.
- **config**: Configuration files for Kafka, Flink, and other components.
- **docs**: Documentation and guides.

## Getting Started
1. Install dependencies listed in the respective directories.
2. Follow instructions in **docs/installation.md**.
3. Execute setup scripts in **src/scripts/setup_environment.sh**.

