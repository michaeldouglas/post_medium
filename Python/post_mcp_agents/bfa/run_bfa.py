import asyncio
import subprocess
import sys
import signal
from watchfiles import awatch

class GracefulReloadServer:
    def __init__(self, module="src.app", host="0.0.0.0", port=8000):
        self.module = module
        self.host = host
        self.port = port
        self.process = None
        self.should_exit = False

    def start_server(self):
        """Inicia o servidor Uvicorn como subprocesso"""
        print(f"Starting server {self.module} on {self.host}:{self.port}")
        self.process = subprocess.Popen([
            sys.executable,
            "-m", "uvicorn",
            f"{self.module}:app",
            "--host", self.host,
            "--port", str(self.port),
            "--log-level", "debug"
        ])

    def stop_server(self):
        """Para o servidor atual"""
        if self.process and self.process.poll() is None:
            print("Stopping server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Server did not terminate in time, killing...")
                self.process.kill()
            self.process = None

    def signal_handler(self, signum, frame):
        """Intercepta sinais SIGINT/SIGTERM para shutdown"""
        print(f"Received signal {signum}, shutting down gracefully...")
        self.should_exit = True
        self.stop_server()

    async def watch_and_reload(self, watch_dir="src"):
        """Monitora a pasta e reinicia o servidor em caso de mudanças"""
        self.start_server()

        async for changes in awatch(watch_dir):
            if self.should_exit:
                break
            print(f"Detected changes: {changes}")
            self.stop_server()
            self.start_server()

    def run(self):
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, self.signal_handler)

        try:
            asyncio.run(self.watch_and_reload())
        except KeyboardInterrupt:
            print("KeyboardInterrupt received, shutting down...")
            self.stop_server()


if __name__ == "__main__":
    server = GracefulReloadServer(module="src.app", host="0.0.0.0", port=8000)
    server.run()
