class SearchResult(object):

    score = -1

    def __init__(self, document, score):
        self.document = document
        self.score = score

    def __str__(self):
        return "score=" + str(self.score) + " " + self.document + "\n"

    def __gt__(self, other):
        return self.score > other.score

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score
