import subprocess
from pathlib import Path

from stem.control import Controller


class ProxyController:
    port: int
    controll_port: int
    controller: Controller

    def __init__(self, port: int) -> None:
        self.port = port
        self.controll_port = port + 1

    def create(self) -> None:
        DIR = Path(__file__).resolve().parent
        subprocess.run(
            [DIR / "create_new_proxy.sh", f"{self.port}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # self.controller = Controller.from_port(port=self.port+1)

    # def update_port(self) -> None:
    #     self.controller.authenticate()
    #     self.controller.signal(Signal.NEWNYM)

    def get_proxy_dict(self) -> dict:
        return {
            "http": f"socks5h://127.0.0.1:{self.port}",
            "https": f"socks5h://127.0.0.1:{self.port}",
        }
