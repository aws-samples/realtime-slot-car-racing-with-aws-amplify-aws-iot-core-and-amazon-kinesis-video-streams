"""
MQTT client for AWS IoT Core communication
"""
import asyncio
import json
import ssl
from umqtt.simple import MQTTClient
import config
from logger import log
from security import SecurityValidator, RateLimiter
from compat import ticks_ms

class MQTTClientAsync:
    """Async MQTT client for AWS IoT Core"""
    
    def __init__(self):
        """Initialize MQTT client"""
        self.client = None
        self.connected = False
        self.publish_queue = asyncio.Queue(maxsize=config.MAX_QUEUE_SIZE)
        self.message_queue = asyncio.Queue(maxsize=config.MAX_QUEUE_SIZE)
        self.subscriptions = {}
        self.rate_limiter = RateLimiter(config.MAX_MESSAGE_RATE)
        log.info("MQTT client initialized")
    
    def _message_callback(self, topic, msg):
        """Handle incoming MQTT messages"""
        try:
            # Rate limiting check
            if not self.rate_limiter.is_allowed(ticks_ms()):
                log.warning("Message rate limit exceeded, dropping message")
                return
            
            topic_str = topic.decode('utf-8')
            msg_str = msg.decode('utf-8')
            
            # Basic validation
            if len(msg_str) > SecurityValidator.MAX_JSON_SIZE:
                log.warning("Message too large, dropping")
                return
            
            log.debug(f"Received message on {topic_str}")
            
            # Queue message for processing
            asyncio.create_task(self.message_queue.put((topic_str, msg_str)))
        except Exception as e:
            log.error(f"Message callback error: {e}")
    
    async def connect(self):
        """Connect to AWS IoT Core"""
        try:
            # Validate configuration
            if not config.AWS_IOT_ENDPOINT:
                raise ValueError("AWS IoT endpoint not configured")
            
            # Create SSL context with certificate validation
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            self.client = MQTTClient(
                client_id=config.AWS_IOT_CLIENT_ID,
                server=config.AWS_IOT_ENDPOINT,
                port=config.AWS_IOT_PORT,
                ssl=context
            )
            
            self.client.set_callback(self._message_callback)
            self.client.connect()
            self.connected = True
            log.info(f"Connected to AWS IoT Core: {config.AWS_IOT_ENDPOINT}")
            
            # Subscribe to topics
            await self._subscribe_to_topics()
            
        except Exception as e:
            log.error(f"MQTT connection failed: {e}")
            self.connected = False
    
    async def _subscribe_to_topics(self):
        """Subscribe to required MQTT topics"""
        topics = [
            config.GAME_STATE_UPDATE_TOPIC,
            config.CAR_CONTROL_UPDATE_TOPIC,
            config.TRACK_MQTT_TOPIC_SUB
        ]
        
        for topic in topics:
            try:
                self.client.subscribe(topic)
                log.info(f"Subscribed to topic: {topic}")
            except Exception as e:
                log.error(f"Failed to subscribe to {topic}: {e}")
    
    async def publish(self, topic, message):
        """Queue message for publishing"""
        try:
            await self.publish_queue.put((topic, message))
            log.debug(f"Queued message for {topic}")
        except:
            log.error("Publish queue full, dropping message")
    
    async def get_message(self):
        """Get received message from queue"""
        try:
            return await asyncio.wait_for(self.message_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None
    
    async def _publish_worker(self):
        """Worker coroutine for publishing messages"""
        while True:
            try:
                if self.connected:
                    topic, message = await self.publish_queue.get()
                    self.client.publish(topic, message)
                    log.debug(f"Published to {topic}")
                await asyncio.sleep_ms(50)
            except Exception as e:
                log.error(f"Publish error: {e}")
                await asyncio.sleep_ms(1000)
    
    async def _check_messages_worker(self):
        """Worker coroutine for checking incoming messages"""
        while True:
            try:
                if self.connected:
                    self.client.check_msg()
                await asyncio.sleep_ms(100)
            except Exception as e:
                log.error(f"Check messages error: {e}")
                await asyncio.sleep_ms(1000)
    
    async def start(self):
        """Start MQTT client workers"""
        log.info("Starting MQTT client workers")
        asyncio.create_task(self._publish_worker())
        asyncio.create_task(self._check_messages_worker())
    
    def is_connected(self):
        """Check if MQTT client is connected"""
        return self.connected
    
    async def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client and self.connected:
            self.client.disconnect()
            self.connected = False
            log.info("Disconnected from MQTT broker")