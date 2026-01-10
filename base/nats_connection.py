
import asyncio
import nats
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NatsConnectionManager:
    """
    A class to manage the NATS connection, including async connect,
    publish, subscribe, and drain/close operations.
    """
    def __init__(self, servers=["nats://localhost:4222"], **conn_args):
        self.servers = servers
        self.conn_args = conn_args
        self.nc = nats.aio.client.Client()
        self._is_connected = False

    async def connect(self):
        """Establish connection to the NATS server(s)."""
        logging.info(f"Attempting to connect to NATS servers: {self.servers}")
        try:
            # Set up callbacks for connection events
            self.conn_args['reconnected_cb'] = self._reconnected_callback
            self.conn_args['disconnected_cb'] = self._disconnected_callback
            self.conn_args['error_cb'] = self._error_callback
            
            await self.nc.connect(servers=self.servers, **self.conn_args)
            self._is_connected = True
            #logging.info(f"Successfully connected to NATS at {self.nc.connected_url.normalized_url}")
        except NoServersError as e:
            logging.error(f"No NATS servers available: {e}")
            self._is_connected = False
            raise
        except Exception as e:
            logging.error(f"An unexpected connection error occurred: {e}")
            self._is_connected = False
            raise

    async def close(self):
        """Gracefully drain and close the connection."""
        if self._is_connected and not self.nc.is_closed:
            logging.info("Draining and closing NATS connection...")
            try:
                await self.nc.drain()
                self._is_connected = False
                logging.info("Connection closed.")
            except ConnectionClosedError:
                logging.warning("Connection already closed during drain attempt.")
            except Exception as e:
                logging.error(f"Error during NATS connection close: {e}")
        else:
            logging.info("Connection already closed or not established.")

    async def publish(self, subject: str, data: bytes):
        """Publish a message to a subject."""
        if self._is_connected:
            await self.nc.publish(subject, data)
            logging.info(f"Published message to '{subject}'")
        else:
            logging.warning("Cannot publish: NATS client is not connected.")

    async def subscribe(self, subject: str,queue_gr, callback):
        """Subscribe to a subject with a given callback function."""
        if self._is_connected:
            sid = await self.nc.subscribe(subject,queue=queue_gr, cb=callback)
            logging.info(f"Subscribed to '{subject}' with subscription ID {sid}")
            return sid
        else:
            logging.warning("Cannot subscribe: NATS client is not connected.")
            return None
    
    # --- Private Callback Methods ---
    async def _reconnected_callback(self):
        logging.info(f"Reconnected to NATS server at {self.nc.connected_url.normalized_url}")

    async def _disconnected_callback(self):
        logging.warning("NATS connection disconnected.")
    
    async def _error_callback(self, err):
        logging.error(f"NATS error: {err}")