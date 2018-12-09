# -*- coding: utf-8 -*-
import os
import math
import collections
from SearchResult import SearchResult
from Document import Document
from cutkum.tokenizer import Cutkum

ck = Cutkum()


class TFIDFSearcher(object):
    # will work kinda like project2
    # termDocumentFrequency - nested dictionary
    # structure - {term :{doc : freq}}
    term_document_frequency = {}
    # termDocumentWeight - also nested dictionary
    # use to reduce workload for each query
    # structure - {term :{doc : weight}}
    term_document_weight = {}
    # a workaround for some part
    # structure  - {docId : docNorm}
    docs_norm = {}
    documents = []

    def __init__(self):
        self.documents = self.prepare_documents()
        # build the TFIDF
        for doc in self.documents:
            for token in doc.tokens:
                if self.term_document_frequency == {}:
                    self.term_document_frequency[token] = {}
                    self.term_document_frequency[token][doc.id] = 1
                    self.term_document_weight[token] = {}
                elif token in self.term_document_frequency: # TFIDFSearcher.keys_exists(token, self.term_document_frequency):
                    if doc.id in self.term_document_frequency[token]: # TFIDFSearcher.keys_exists(doc.id, self.term_document_frequency):
                        self.term_document_frequency[token][doc.id] = self.term_document_frequency[token][doc.id] + 1
                    else:
                        self.term_document_frequency[token][doc.id] = 1
                else:
                    self.term_document_frequency[token] = {}
                    self.term_document_frequency[token][doc.id] = 1
                    self.term_document_weight[token] = {}

        for token in self.term_document_frequency:
            for doc_id in self.term_document_frequency[token]:
                weight = self.tf(self.term_document_frequency[token][doc_id]) \
                         * self.idf(len(self.documents), len(self.term_document_frequency[token]))
                self.term_document_weight[token][doc_id] = weight
                if doc_id in self.docs_norm:
                    self.docs_norm[doc_id] = self.docs_norm[doc_id] + weight * weight
                else:
                    self.docs_norm[doc_id] = weight * weight

        for doc_id in self.docs_norm.keys():
            self.docs_norm[doc_id] = math.sqrt(self.docs_norm[doc_id])

    @staticmethod
    def prepare_documents():
        path = os.getcwd() + "/documents/"
        dirs = os.listdir(path)

        docs = []
        doc_id = 0

        # we should read docs_url.txt first I guess
        # docs_url = collections.defaultdict(dict)
        '''with open(path+"docs_url.txt") as f:
            lines = f.readlines()
        lines = [x.strip('\n') for x in lines]
        for line in lines:
            doc_and_url = line.split()
            docs_url[doc_and_url[0]] = doc_and_url[1]
        '''

        # read each file, create document object, put into documents[]
        for file in dirs:
            if file == "docs_url.txt":
                continue
            print(file)

            tokens = []

            with open(path + file, encoding="utf-8") as f:
                lines = f.readlines()
            lines = [x.strip('\n') for x in lines]

            doc_url = lines[0]
            doc_name = lines[1]
            doc_pages = lines[2]
            lines = lines[3:]

            for line in lines:
                #tokens.__add__(ck.tokenize(line))
                for token in ck.tokenize(line):
                    tokens.append(token)

            new_doc = Document(doc_id, doc_name, lines, tokens, doc_url, doc_pages)
            doc_id = doc_id + 1
            print(new_doc.__str__())
            docs.append(new_doc)

        return docs

    def search(self, query, k):
        results = []
        query_term_freq = collections.defaultdict()
        for token in query:
            if token in query_term_freq:
                query_term_freq[token] = query_term_freq[token] + 1
            else:
                query_term_freq[token] = 1

        query_weight = {}
        for token in query:
            # global term_document_weight
            # global documents
            if token not in self.term_document_weight:
                continue
            else:
                weight = TFIDFSearcher.tf(query_term_freq[token]) \
                         * TFIDFSearcher.idf(len(self.documents), len(self.term_document_weight[token]))
                query_weight[token] = weight

        query_norm = 0.0
        for token in query_weight.keys():
            query_norm += query_weight[token] ** 2

        query_norm = math.sqrt(query_norm)
        if query_norm == 0.0:
            return self.documents[:k]

        # global docs_norm
        for doc in self.documents:
            working_tokens = set(doc.tokens)
            working_tokens.intersection_update(set(query_weight))
            score = 0.0
            doc_norm = self.docs_norm[doc.id]
            for token in working_tokens:
                score += query_weight[token] * self.term_document_weight[token][doc.id]
            score = score / (query_norm * doc_norm)
            results.append(SearchResult(doc, score))
            print(doc.name + ' ' + str(score))

        results.sort(reverse=True)
        documents_to_return = []
        if k > len(results):
            k = len(results)
        for i in range(k):
            documents_to_return.append(results[i])#.document) # changed to return the SearchResult for further calculation

        return documents_to_return

    @staticmethod
    def tf(tf):
        return 0.0 if tf == 0 else 1 + math.log10(tf)

    @staticmethod
    def idf(n, df):
        return math.log10(1+n/df)

    @staticmethod
    def keys_exists(element, *keys):

        # Check if *keys (nested) exists in `element` (dict).

        if type(element) is not dict:
            raise AttributeError('keys_exists() expects dict as first argument.')
        if len(keys) == 0:
            raise AttributeError('keys_exists() expects at least two arguments, one given.')

        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return False
        return True
