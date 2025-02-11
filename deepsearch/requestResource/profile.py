import requests

from deepsearch.logger.logger import log
from deepsearch.torProxyController.controller import ProxyController


class RequestProfile:
    id_resources: int
    type: str
    url: str
    tor_network: bool
    proxy: ProxyController

    def __init__(self, request_profile: dict, index: int) -> None:
        if not request_profile.get("user_agent"):
            self.user_agent = (
                "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
            )
        self.id_resources = index
        self.type = request_profile["type"]
        self.url = request_profile["url"]
        self.tor_network = request_profile["tor_network"]
        log(
            (
                (
                    f"----Creating an onion proxy on port {9060 + (self.id_resources * 2)}",
                    "green",
                ),
            )
        )
        self.proxy = ProxyController(9060 + (self.id_resources * 2))
        self.proxy.create()

    def request(self, search_text: str) -> dict:
        try:
            kwargs_response = {
                "url": self.url.replace("%s", search_text),
                "headers": {"User-Agent": self.user_agent},
            }
            response = requests.get(
                **(
                    kwargs_response | {"proxies": self.proxy.get_proxy_dict()}
                    if self.tor_network
                    else kwargs_response
                )
            )
            return {"status": "success", "response": response}
        except requests.exceptions.ConnectionError:
            return {"status": "error"}

    def check(self, url: str, onion: bool) -> bool:
        try:
            requests.get(
                **(
                    {"url": url, "proxies": self.proxy.get_proxy_dict()}
                    if onion
                    else {"url": url}
                )
            )
            return True

        except requests.exceptions.ConnectionError:
            return False

    def __dict__(self):
        return {"type": self.type, "url": self.url, "tor_network": self.tor_network}
