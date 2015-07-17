from HTMLParser import HTMLParser

# Usage:
# parser.feed(contents)
# text = parser.get_text()

class HTML2TextParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []
    def handle_data(self, data):
        self.text.append(data)
        return data
    def get_text(self):
        return ' '.join(self.text)

