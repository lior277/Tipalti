class PageHelper:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str):
        self.driver.open(url)

    def get_title(self) -> str:
        return self.driver.page.title()

    def get_url(self) -> str:
        return self.driver.page.url

    def wait_for_load(self):
        self.driver.page.wait_for_load_state("domcontentloaded")

    def refresh(self):
        self.driver.page.reload()

    def go_back(self):
        self.driver.page.go_back()