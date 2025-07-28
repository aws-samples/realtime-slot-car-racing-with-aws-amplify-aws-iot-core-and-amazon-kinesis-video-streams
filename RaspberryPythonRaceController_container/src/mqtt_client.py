"""MQTT client for AWS IoT Core communication."""
import asyncio
import json
import logging
import ssl
from typing import Optional, Callable, Dict, Any
from asyncio_mqtt import Client
from asyncio_mqtt.error import MqttError

from . import config
from .security import SecurityValidator, RateLimiter

logger = logging.getLogger(__name__)


class MQTTClient:
    """Async MQTT client for AWS IoT Core communication."""
    
    def __init__(self):
        """Initialize MQTT client."""
        self.client: Optional[Client] = None
        self.connected = False
        self.message_handlers: Dict[str, Callable] = {}
        self.rate_limiter = RateLimiter(config.MAX_QUEUE_SIZE)
        logger.info("MQTT client initialized")
    
    async def connect(self) -> bool:
        """
        Connect to AWS IoT Core.
        
        Returns:
            True if connected successfully, False otherwise
        """
        try:
            # Validate configuration
            if not config.AWS_IOT_ENDPOINT:
                raise ValueError("AWS IoT endpoint not configured")
            
            # Create SSL context with certificate validation
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            self.client = Client(
                hostname=config.AWS_IOT_ENDPOINT,
                port=config.AWS_IOT_PORT,
                client_id=config.AWS_IOT_CLIENT_ID,
                tls_context=context
            )
            
            await self.client.__aenter__()
            self.connected = True
            logger.info(f"Connected to AWS IoT Core: {config.AWS_IOT_ENDPOINT}")
            return True
            
        except Exception as e:
            logger.error(f"MQTT connection failed: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        if self.client and self.connected:
            try:
                await self.client.__aexit__(None, None, None)
                self.connected = False
                logger.info("Disconnected from MQTT broker")
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")
    
    async def subscribe(self, topic: str, handler: Callable[[str, str], None]):
        """
        Subscribe to MQTT topic with message handler.
        
        Args:
            topic: MQTT topic to subscribe to
            handler: Async function to handle messages
        """
        if not self.connected or not self.client:
            raise RuntimeError("MQTT client not connected")
        
        try:
            await self.client.subscribe(topic)
            self.message_handlers[topic] = handler
            logger.info(f"Subscribed to topic: {topic}")
        except Exception as e:
            logger.error(f"Failed to subscribe to {topic}: {e}")
            raise
    
    async def publish(self, topic: str, message: str):
        """
        Publish message to MQTT topic.
        
        Args:
            topic: MQTT topic to publish to
            message: Message to publish
        """
        if not self.connected or not self.client:
            raise RuntimeError("MQTT client not connected")
        
        try:
            await self.client.publish(topic, message)
            logger.debug(f"Published to {topic}")
        except Exception as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise
    
    async def start_message_loop(self):
        """Start the message processing loop."""
        if not self.connected or not self.client:
            raise RuntimeError("MQTT client not connected")
        
        logger.info("Starting MQTT message loop")
        
        try:
            async with self.client.messages() as messages:
                async for message in messages:
                    await self._handle_message(message)
        except MqttError as e:
            logger.error(f"MQTT error in message loop: {e}")
            self.connected = False
        except Exception as e:
            logger.error(f"Unexpected error in message loop: {e}")
            self.connected = False
    
    async def _handle_message(self, message):
        """
        Handle incoming MQTT message.
        
        Args:
            message: MQTT message object
        """
        try:
            topic = message.topic.value
            payload = message.payload.decode('utf-8')
            
            # Rate limiting check
            current_time = int(asyncio.get_event_loop().time() * 1000)
            if not self.rate_limiter.is_allowed(current_time):
                logger.warning("Message rate limit exceeded, dropping message")
                return
            
            # Basic validation
            if len(payload) > SecurityValidator.MAX_JSON_SIZE:
                logger.warning("Message too large, dropping")
                return
            
            logger.debug(f"Received message on {topic}")
            
            # Find and call handler
            handler = self.message_handlers.get(topic)
            if handler:
                await handler(topic, payload)
            else:
                logger.warning(f"No handler for topic: {topic}")
                
        except Exception as e:
            logger.error(f"Message handling error: {e}")
    
    def is_connected(self) -> bool:
        """
        Check if MQTT client is connected.
        
        Returns:
            True if connected, False otherwise
        """
        return self.connected