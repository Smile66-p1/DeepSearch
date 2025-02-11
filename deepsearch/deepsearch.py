import json
import os
import time
from pathlib import Path

from deepsearch.logger.logger import log
from deepsearch.profileReources.profile import ProfileSearchReources

BASE_DIR = Path(__file__).resolve().parent


def getSearchResources() -> dict:
    search_resources = {}
    with open(BASE_DIR / "conf" / "searchresources.json", "rb") as f:
        search_resources = json.load(f)
        f.close()
    return search_resources


def setSearchResources(searchResources: list[ProfileSearchReources]) -> None:
    search_resources = [resource.__dict__() for resource in searchResources]
    with open(BASE_DIR / "conf" / "searchresources.json", "w+") as f:
        json.dump(search_resources, f)
        f.close()


def checkresources() -> None:
    profilesResources: list[dict[str:ProfileSearchReources, str:str]] = []
    log((("[!] Importing scan resources", "yellow"),))
    search_resources = getSearchResources()
    log((("[+] Done", "green"),))
    log((("[!] Creating profiles for search resources", "yellow"),))
    for index, resource in enumerate(search_resources):
        profilesResources.append(
            {
                "profile": ProfileSearchReources(resource, index, ""),
                "status": "wait",
            }
        )
    log((("[+] Done", "green"),))
    log((("[!] The beginning of verification", "yellow"),))
    for resource in profilesResources:
        resource["profile"].check()
    setSearchResources([resource["profile"] for resource in profilesResources])


def search(**kwargs) -> None:
    profilesResources: list[dict[str:ProfileSearchReources, str:str]] = []
    log((("[!] Importing scan resources", "yellow"),))
    search_resources = getSearchResources()
    log((("[+] Done", "green"),))
    log((("[!] Creating profiles for search resources", "yellow"),))
    for index, resource in enumerate(search_resources):
        profilesResources.append(
            {
                "profile": ProfileSearchReources(
                    resource, index, kwargs.get("searchtext"), kwargs.get("check")
                ),
                "status": "wait",
            }
        )
    log((("[+] Done", "green"),))
    print()
    log((("Start search", "green"),))
    time.sleep(3)
    os.system("clear")
    for thread_index in range(kwargs.get("threads")):
        if thread_index >= len(profilesResources):
            break
        profilesResources[thread_index]["profile"].start()
        profilesResources[thread_index]["status"] = "work"

    result_links = []
    for thread in profilesResources:
        if thread["status"] == "wait":
            continue
        thread["profile"].join()
        result_links += thread["profile"].result

    (BASE_DIR / "output").mkdir(exist_ok=True)
    with open(f"{BASE_DIR / 'output' / kwargs.get('searchtext')}.json", "w+") as f:
        json.dump(result_links, f)
        f.close()
