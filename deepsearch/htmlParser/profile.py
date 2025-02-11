from bs4 import BeautifulSoup


class Filter:
    @staticmethod
    def remove(source_text: str, remove_sub_str: str) -> str:
        return source_text.replace(remove_sub_str, "")

    @staticmethod
    def deleteBefore(source_text: str, remove_sub_str: str) -> str:
        return source_text[
            source_text.index(remove_sub_str) + len(remove_sub_str) : len(source_text)
        ]

    filter_functions = {"remove": remove, "remove_before": deleteBefore}


class HTMLParserProfile:
    block_selector: str

    def __init__(self, dict_profile: dict) -> None:
        self.block_selector = dict_profile["block"]
        self.title_selector = dict_profile["title"]
        self.URL_result_selector = dict_profile["URL_result"]

    def _filter_link(self, link: str, filters: list[str]) -> str:
        result_link = link
        for filter in filters:
            result_link = Filter.filter_functions[filter](result_link, filters[filter])
        return result_link

    def __call__(self, response_text: str) -> list[dict]:
        soup = BeautifulSoup(response_text, "html.parser")
        blocks = soup.select(self.block_selector)
        results_links = []
        for block in blocks:
            url = ""
            block_title = block.select_one(self.title_selector["selector"])
            title = (
                (
                    block_title.get(self.title_selector["attribut"])
                    if self.title_selector["attribut"] != "content"
                    else block_title.text
                )
                if block_title is not None
                else ("")
            )
            if self.URL_result_selector["attribut"] == "content":
                url = block.select_one(self.URL_result_selector["selector"])
                url = "" if url is None else url.text.strip()
            else:
                url = block.select_one(self.URL_result_selector["selector"]).get(
                    self.URL_result_selector["attribut"]
                )
            results_links.append(
                {
                    "title": title.strip(),
                    "url": self._filter_link(
                        url, self.URL_result_selector["filters"]
                    ).strip(),
                }
            )
        return results_links

    def __dict__(self):
        return {
            "block": self.block_selector,
            "title": self.title_selector,
            "URL_result": self.URL_result_selector,
        }
