# -*- coding: utf-8 -*-
class Document(object):
    id = -1
    name = u''
    rawText = u''
    tokens = []
    url = ''

    def __init__(self, id, name, rawtext, tokens, url, pages):
        self.id = id
        self.name = name
        self.tokens = tokens
        for line in rawtext:
            self.rawText = self.rawText + line
            if len(rawtext) > 50:
                break
        self.url = url
        self.pages = pages

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __str__(self):
        return str(self.id) + " " + self.name + " " + self.url

    def serialize(self):
        return{
            'name': self.name,
            'rawText': self.rawText[:50],
            'url': self.url,
            'pages': self.pages
        }
