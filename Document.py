# -*- coding: utf-8 -*-

class Document(object):
    id = -1
    name = u''
    rawText = u''
    tokens = []
    url = ''
    query_offset = 0

    def __init__(self, id, name, rawtext, tokens, url, pages):
        self.id = id
        self.name = name
        self.tokens = tokens
        for line in rawtext:
            self.rawText = self.rawText + line
            '''if len(rawtext) > 50:
                break'''
        self.url = url
        self.pages = pages

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __str__(self):
        return str(self.id) + " " + self.name + " " + self.url

    def set_query_offset(self, query):
        for query_token in query:
            if query_token in self.tokens:
                self.query_offset = self.tokens.index(query_token)
                break

    def serialize(self):
        string_to_return = ''
        for i in range(25):
            if self.query_offset + i >= len(self.tokens):
                break
            string_to_return = string_to_return + self.tokens[self.query_offset+i]
        return{
            'name': self.name,
            'rawText': string_to_return, #self.rawText[self.query_offset:self.query_offset+55],
            'url': self.url,
            'pages': self.pages
        }
