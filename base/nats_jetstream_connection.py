import asyncio
from nats.aio.client import Client as NATS
from nats.js import JetStreamContext
from nats.errors import TimeoutError, NoStreamFoundError
import logging

logging.basicConfig(level=logging.INFO)

class NatsJetStreamConnection:
    """
    A class to manage NATS connection and JetStream context.
    """
    def __init__(self, servers, **conn_options):
        self.servers = servers
        self.conn_options = conn_options
        self.nc: NATS = None
        self.js: JetStreamContext = None

    async def __aenter__(self):
        """Connects to NATS and initializes JetStream context."""
        try:
            self.nc = await nats.connect(servers=self.servers, **self.conn_options)
            self.js = self.nc.jetstream()
            logging.info(f"Connected to NATS server at {self.servers}")
            return self
        except Exception as e:
            logging.error(f"Failed to connect to NATS: {e}")
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Drains the connection and closes it."""
        if self.nc:
            try:
                await self.nc.drain()
                logging.info("NATS connection drained and closed.")
            except TimeoutError:
                await self.nc.close()
                logging.warning("NATS connection closed with timeout.")

    async def publish_message(self, subject: str, message: bytes):
        """Publishes a message to a JetStream subject."""
        try:
            ack = await self.js.publish(subject, message)
            logging.info(f"Published message to {subject}, Stream: {ack.stream}, Sequence: {ack.seqno}")
        except NoStreamFoundError:
            logging.error(f"Cannot publish: No stream configured for subject '{subject}'")
        except Exception as e:
            logging.error(f"Error publishing message: {e}")

    async def create_stream(self, name: str, subjects: list[str]):
        """Creates a new JetStream stream if it doesn't exist."""
        try:
            await self.js.add_stream(name=name, subjects=subjects)
            logging.info(f"Stream '{name}' created/updated for subjects {subjects}")
        except Exception as e:
            logging.error(f"Error creating stream '{name}': {e}")

    async def subscribe_pull(self, stream_name: str, durable_name: str, subject: str):
        """
        Creates a pull consumer subscription and fetches messages.
        Note: This is a basic example; actual consumption requires a loop.
        """
        try:
            psub = await self.js.pull_subscribe(subject, durable_name)
            logging.info(f"Subscribed to {subject} with durable consumer {durable_name}")
            # Example of fetching messages (usually done in a continuous loop)
            msgs = await psub.fetch(1, timeout=5)
            for msg in msgs:
                print(f"Received message: {msg.data.decode()}")
                await msg.ack()
        except TimeoutError:
            logging.warning("No messages fetched within timeout period.")
        except Exception as e:
            logging.error(f"Error during pull subscription: {e}")
