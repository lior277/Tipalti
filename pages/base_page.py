class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)
