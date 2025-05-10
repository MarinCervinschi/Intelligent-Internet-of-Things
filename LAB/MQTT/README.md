# MQTT Laboratory

## Project Description

The goal of this project is to create an IoT application scenario for monitoring electric vehicles using the MQTT protocol. The system is designed with the following specifications:

- **Data Producer**: The connected vehicle acts as the data producer, publishing:
  - **InfoData**: General vehicle information.
  - **TelemetryData**: Real-time telemetry data.
- **MQTT Topics**:
  - InfoData is published to `/iot/user/<user>/vehicle/<vehicle_id>/info`.
  - TelemetryData is published to `/iot/user/<user>/vehicle/<vehicle_id>/telemetry`.
  - Both topics are associated with a broker requiring authentication and are organized under a base topic `/iot/user/<user>`.
- **Message Behavior**:
  - Upon connection, the vehicle publishes retained InfoData messages.
  - TelemetryData messages are sent every 3 seconds.
- **MQTT Consumer**:
  - Subscribes to the following topics to receive InfoData and TelemetryData for all registered vehicles:
    - `/iot/user/<user>/vehicle/+/info`
    - `/iot/user/<user>/vehicle/+/telemetry`

### Example Data

- **InfoData** (JSON format):

  ```json
  {
    "uuid": "vehicle-0001",
    "manufacturer": "Tesla",
    "model": "Model Y",
    "driverId": "driver00001"
  }
  ```

- **TelemetryData** (JSON format):
  ```json
  {
    "geoLocation": {
      "latitude": 17.11294002770684,
      "longitude": 47.584728688577236,
      "altitude": 0.0
    },
    "batteryLevel": 98.96001084539103,
    "speedKmh": 77.04069775640971,
    "engineTemperature": 83.32024176635812,
    "timestamp": 1635339698884
  }
  ```

## Setup Python Environment

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
3. Install the required packages using `pyproject.toml`:
   ```bash
   pip install .
   ```
   Alternatively, if you want to install the dependencies in editable mode (useful for development):
   ```bash
   pip install -e .
   ```

## MQTT Broker Configuration

- The MQTT broker is configured using the Eclipse Mosquitto Docker image. Check the configuration file [mosquitto.conf](/mqtt-broker/mosquitto/config/mosquitto.conf) for details.
- The broker is set to require authentication for all clients. The username and password are defined in the [docker-compose.yml](/mqtt-broker/docker-compose.yml) file.

### Running the MQTT Broker

1. Ensure Docker is installed and running on your machine.
2. Navigate to the `mqtt-broker` directory.
3. Run the following command to start the MQTT broker:
   ```bash
   docker-compose up -d
   ```
4. To see the logs, check the `mqtt-broker/mosquitto/log` directory. The logs will show the connection status of the clients and any messages published or received.
5. To stop the broker, run:
   ```bash
   docker-compose down
   ```

## Running the Application
1. Ensure the MQTT broker is running.
2. Open a terminal and run the following command to start the MQTT consumer:
   ```bash
   python mqtt_vehicle_data_consumer.py
   ```
4. Open another terminal and run the following command to start the MQTT producer:
   ```bash
   python mqtt_vehicle_emulator.py
   ```
5. The consumer will subscribe to the topics and print the received messages to the console.
6. The producer will publish InfoData and TelemetryData messages to the broker every 3 seconds.
7. To stop the producer and consumer, use `Ctrl+C` in their respective terminals.