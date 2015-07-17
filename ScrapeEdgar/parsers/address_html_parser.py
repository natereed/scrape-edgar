from HTMLParser import HTMLParser
import re

class AddressHTMLParser(HTMLParser):
    count = 0
    tag = None
    address_index = -1
    address1 = None
    address2 = None

    cusip_index = -1

    def handle_starttag(self, tag, attrs):
        self.tag = tag
        self.count += 1
    def handle_endtag(self, tag):
        self.tag = None
    def handle_data(self, data):
        if not self.tag:
            return

        if re.search(r'Address of Issuer', data, flags=re.IGNORECASE):
            self.address_index = self.count
        elif self.count == self.address_index + 1:
            self.address1 = data.strip()
        elif self.count == self.address_index + 2:
            self.address2 = data.strip()

        # TBD: Any addresses take more than 2 lines?

    def address(self):
        if self.address1 and self.address2:
            return ', '.join([self.address1, self.address2])
        else:
            return self.address1