import threading
from datetime import datetime

from deepsearch.htmlParser.profile import HTMLParserProfile
from deepsearch.logger.logger import log
from deepsearch.requestResource.profile import RequestProfile


class ProfileSearchReources(threading.Thread):
    id: int
    name: str
    URL: str
    last_check: str
    search_text: str
    status: str
    html_parser_profile: HTMLParserProfile
    check_links: bool
    result: list[dict]

    def __init__(self, profile: dict, index: int, searchtext: str, check: bool) -> None:
        super().__init__()
        self.id = index
        self.name = profile["name"]
        self.URL = profile["URL"]
        self.last_check = profile["last_check"]
        self.status = profile["status"]
        self.search_text = searchtext
        self.request_profile = RequestProfile(profile["request_profile"], index)
        self.html_parser_profile = HTMLParserProfile(
            profile["html_parser_result_profile"]
        )
        self.result = []
        self.check_links = check
        log(
            (
                (
                    f'[+] The profile of the search resource "{self.name}" was created successfully',
                    "green",
                ),
            )
        )

    def run(self) -> dict:
        log(((f'[!] The search for the "{self.name}" resource has begun', "yellow"),))
        response = self.request_profile.request(self.search_text)
        if response["status"] == "error":
            log(
                (
                    (
                        f'[-] The search resource "{self.name}" does not respond to HTTP requests',
                        "red",
                    ),
                )
            )
            return {}
        links = self.html_parser_profile(response["response"].text)
        if not self.check_links:
            self.result = links
            log(
                (
                    (
                        f'[!] The search for the "{self.name}" resource has been completed ({len(self.result)} links found)',
                        "green",
                    ),
                )
            )
            return
        checks_links = []
        for link in links:
            temp = self.request_profile.request(link["url"])
            if temp["status"] == "success":
                checks_links.append(
                    {
                        "title": link["title"],
                        "url": link["url"],
                        "check": True,
                        "status": temp["status"],
                    }
                )
        self.result = checks_links
        log(
            (
                (
                    f'[!] The search for the "{self.name}" resource has been completed ({len(self.result)} links found, cheked {len(checks_links)} links)',
                    "green",
                ),
            )
        )

    def check(self) -> bool:
        if self.request_profile.check(self.URL, True):
            log(((f"[!] The {self.name} resource is operational", "green"),))
            self.status = "online"
        else:
            log(((f"[!] The {self.name} resource is not operational", "red"),))
            self.status = "offline"
        self.last_check = datetime.now().strftime("%d.%m.%Y %H:%M")
        return self.status == "online"

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "URL": self.URL,
            "status": self.status,
            "last_check": self.last_check,
            "request_profile": self.request_profile.__dict__(),
            "html_parser_result_profile": self.html_parser_profile.__dict__(),
        }
