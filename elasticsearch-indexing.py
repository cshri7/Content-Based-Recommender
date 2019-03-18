import json
from time import sleep
import logging
from elasticsearch import Elasticsearch, RequestsHttpConnection, serializer, compat, exceptions
import glob
import sys, os
from pathlib import Path
import csv

class JSONSerializerPython2(serializer.JSONSerializer):
    def dumps(self, data):
        # don't serialize strings
        if isinstance(data, compat.string_types):
            return data
        try:
            return json.dumps(data, default=self.default, ensure_ascii=True)
        except (ValueError, TypeError) as e:
            raise exceptions.SerializationError(data, e)

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}], serializer=JSONSerializerPython2())
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es

def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
            "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1
                },
            "mappings":{
                "wikibook_items":{
                    "properties": {
                        "title": {
                            "type": "string",
                            "analyzer": "english"
                        },
                        "content": {
                            "type": "string",
                            "analyzer": "english",
                            "fields": {
                                "std": {
                                    "type": "string",
                                    "analyzer": "standard"
                                    }
                                }
                            },
                        }
                    }
                }
            }
    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

es = connect_elasticsearch()
create_index(es, 'wiki_java_programming')

# you can place the absolute path of WikiBooks files on your system here
path_wiki = '/media/tamanna/MyStuff/ASU/Coursework/Fall 2018/CSE 591 - Adaptive Web/Assignment 2/Assign2-ChandniShrivastava/data/*.txt'
files_wiki=glob.glob(path_wiki)
# fw=open(files_wiki[0], 'r')
# print(fw.readlines())
eid = 0
for name in files_wiki:
    fw=open(name, 'r')
    # file_contents = f.readlines()
    file_contents = fw.read().splitlines()
    # print(file_contents)
    doc = {
        'title': Path(name).stem,
        'content' : file_contents
    }
    eid = eid+1
    # store_record(es, 'wikibook_items', es_doc)
    res = es.index(index='wiki_java_programming', doc_type='wikibook_items', id=eid, body=doc, request_timeout=1000)
    fw.close()

path_oracle = '/media/tamanna/MyStuff/ASU/Coursework/Fall 2018/CSE 591 - Adaptive Web/Assignment 2/Assign2-ChandniShrivastava/dataoracle/*.txt'
files_oracle=glob.glob(path_oracle)
# fo=open(files_oracle[0], 'r')
# print(fo.readlines())
# eid = 0
for name in files_oracle:
    fo=open(name, 'r')
    # file_contents = f.readlines()
    file_contents = fo.read().splitlines()
    # print(file_contents)
    doc = {
        'title': Path(name).stem,
        'content' : file_contents
    }
    eid = eid+1
    # store_record(es, 'wikibook_items', es_doc)
    res = es.index(index='wiki_java_programming', doc_type='wikibook_items', id=eid, body=doc, request_timeout=1000)
    fo.close()


# with open('oracle-items.csv', 'r') as _filehandler:
#     csv_file_reader = csv.reader(_filehandler)
#     for row in csv_file_reader:
#         if len()
#         title = row[0] + "_____" + row[1]
#         print title
#         contents = row[2]
#         print contents


# if __name__ == '__main__':
#   logging.basicConfig(level=logging.ERROR)
