# This class parses the 8-k 4.1 exhibit, which describes the instruments being issued.
# See: https://www.law.cornell.edu/cfr/text/17/229.601

# I haven't been able to find an example of this form that is actually populated with CUSIP's, so I
# haven't implemented this yet.
class Parser8k41:
    def __init__(self, doc):
        self.doc = doc

    def parse(self):
        return {}
        return None

#f = open("EX-4.1.html", "r")
#doc = f.read()
#f.close()

#parser = Parser8k41(doc)
#results = parser.parse()


