# Race Controller Container

A containerized version of the Raspberry Pi Race Controller with improved architecture, proper logging, asyncio support, and Docker deployment capabilities.

## Features

- **Async Architecture**: Full asyncio implementation with proper queue-based message passing
- **Standard Logging**: Python's standard logging module with configurable levels
- **Security**: Input validation, rate limiting, and secure MQTT communication
- **Docker Support**: Containerized deployment with health checks
- **ECS Deployment**: CloudFormation template and deployment scripts
- **Comprehensive Tests**: Full test suite with pytest and asyncio support

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MQTT Client   │◄──►│  Race Controller │◄──►│  Serial Client  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Message Queue  │    │  Analytics Queue │    │   Data Queue    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Quick Start

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   export AWS_IOT_ENDPOINT="your-endpoint.iot.region.amazonaws.com"
   export SERIAL_PORT="/dev/ttyUSB0"
   ```

3. **Run Application**:
   ```bash
   python -m src.main
   ```

4. **Run Tests**:
   ```bash
   pytest
   ```

### Docker Deployment

1. **Build and Run Locally**:
   ```bash
   docker-compose up --build
   ```

2. **Deploy to AWS ECS**:
   ```bash
   ./deploy/deploy.sh
   ```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `AWS_IOT_ENDPOINT` | - | AWS IoT Core endpoint |
| `AWS_IOT_CLIENT_ID` | `race-controller` | MQTT client ID |
| `SERIAL_PORT` | `/dev/ttyUSB0` | Serial port for track |
| `SERIAL_BAUDRATE` | `19200` | Serial baud rate |

## API Documentation

### RaceController Class

Main controller managing race state and car data.

#### Methods

- `handle_race_update(json_string)`: Process race state updates
- `handle_car_update(json_string)`: Process car control updates  
- `handle_track_data(int_array)`: Process track sensor data
- `get_lap_time()`: Get next lap time from queue
- `get_analytics()`: Get next analytics data from queue

### MQTTClient Class

Async MQTT client for AWS IoT Core communication.

#### Methods

- `connect()`: Connect to AWS IoT Core
- `subscribe(topic, handler)`: Subscribe to topic with handler
- `publish(topic, message)`: Publish message to topic
- `start_message_loop()`: Start message processing loop

### SerialClient Class

Async serial communication with race track.

#### Methods

- `connect()`: Connect to serial port
- `send_data(data)`: Queue data for sending
- `get_received_data()`: Get received data from queue
- `start()`: Start send/receive workers

## Testing

Run the complete test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_race_controller.py

# Run with verbose output
pytest -v
```

## Deployment

### Prerequisites

- AWS CLI configured
- Docker installed
- Appropriate AWS permissions for ECR and ECS

### Deploy to ECS

The deployment script handles:
- ECR repository creation
- Docker image build and push
- CloudFormation stack deployment
- ECS service configuration

```bash
# Deploy with default settings
./deploy/deploy.sh

# Deploy with custom image tag
IMAGE_TAG=v1.0.0 ./deploy/deploy.sh

# Deploy to specific region
AWS_REGION=us-west-2 ./deploy/deploy.sh
```

### Monitor Deployment

```bash
# View CloudFormation stack
aws cloudformation describe-stacks --stack-name race-controller-stack

# Monitor ECS service
aws ecs describe-services --cluster race-controller-cluster --services race-controller-service

# View logs
aws logs tail /ecs/race-controller --follow
```

## Security Features

- **Input Validation**: All JSON inputs validated and sanitized
- **Rate Limiting**: Protection against message flooding
- **SSL/TLS**: Secure MQTT communication with certificate validation
- **Non-root Container**: Docker container runs as non-root user
- **IAM Roles**: Least privilege access for ECS tasks

## Monitoring

### Health Checks

- Docker health check every 30 seconds
- ECS service health monitoring
- CloudWatch logs integration

### Metrics

- MQTT connection status
- Serial connection status
- Message processing rates
- Error rates and types

## Troubleshooting

### Common Issues

1. **MQTT Connection Failed**:
   - Check AWS IoT endpoint configuration
   - Verify AWS credentials and permissions
   - Check network connectivity

2. **Serial Connection Failed**:
   - Verify serial port exists and permissions
   - Check baud rate configuration
   - Ensure device is connected

3. **Container Won't Start**:
   - Check environment variables
   - Verify Docker permissions
   - Review container logs

### Debug Mode

Enable debug logging:

```bash
# Set log level to DEBUG
export LOG_LEVEL=DEBUG
python -m src.main
```

## Development

### Code Structure

```
src/
├── __init__.py          # Package initialization
├── main.py              # Application entry point
├── config.py            # Configuration settings
├── models.py            # Data models
├── security.py          # Security validation
├── mqtt_client.py       # MQTT communication
├── serial_client.py     # Serial communication
└── race_controller.py   # Main controller logic

tests/
├── __init__.py
├── test_models.py       # Model tests
├── test_security.py     # Security tests
└── test_race_controller.py  # Controller tests
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.