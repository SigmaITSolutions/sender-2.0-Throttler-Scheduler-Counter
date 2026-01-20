import nats
from nats.js import JetStreamContext
from typing import Optional

class NATSManager:
    _instance: Optional['NATSManager'] = None

    def __init__(self):
        self.nc = nats.NATS()
        self.js: Optional[JetStreamContext] = None

    @classmethod
    async def get_instance(cls, servers: list = "nats://localhost:4222"):
        if cls._instance is None:
            cls._instance = cls()
            await cls._instance.connect(servers)
        return cls._instance

    async def connect(self, servers: list):
        """Establish connection and initialize JetStream."""
        try:
            # allow_reconnect is True by default
            await self.nc.connect(
                servers=servers,
                reconnected_cb=self._reconnected_cb,
                disconnected_cb=self._disconnected_cb,
                error_cb=self._error_cb
            )
            self.js = self.nc.jetstream()
            print(f"Successfully connected to NATS at {servers}")
        except Exception as e:
            print(f"Failed to connect to NATS: {e}")
            raise

    # Callbacks for robust monitoring
    async def _reconnected_cb(self):
        print(f"Reconnected to NATS: {self.nc.connected_url.netloc}")

    async def _disconnected_cb(self):
        print("Disconnected from NATS...")

    async def _error_cb(self, e):
        print(f"NATS Error: {e}")

    async def close(self):
        """Gracefully close the connection."""
        if self.nc.is_connected:
            await self.nc.drain()
            print("Connection drained and closed.")

    def get_js(self) -> JetStreamContext:
        """Returns the JetStream context."""
        if not self.js:
            raise RuntimeError("JetStream context not initialized. Call connect() first.")
        return self.js