import sys

from flask import Flask, request

import yaml
import json
import re
import argparse
import fileinput

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello, from api yaml extractor!</h1>" \
           "<br>" \
           "Use /api/yaml_extract to actually extract some data"

@app.route('/api/yaml_extract', methods=['GET'])
def api_yaml_exract():
    text = 'text'
    expr = 'expr'
    raw_data = request.get_data()
    try:
        data = json.loads(raw_data.decode("utf-8"))
    except ValueError as e:
        return 'bad request! data cannot be decoded', 400

    if text in data and expr in data:
        return run(data[text], data[expr])
    else:
        return 'bad request! Provide text and expr', 400

class YamlExtracotr:
    def get_array_item(document, item_reference):
        if len(item_reference) == 0:
            print ("Error, no reference provided")
            exit(1)

        current_reference = [x for x in re.split('[\[\]]', item_reference[0]) if x]
        sub_document=document.get(current_reference[0])
        for x in current_reference[1:]:
            sub_document=sub_document[int(x)]
            return sub_document



    def get_item(document,item_reference):
        # print("=====")
        # print (document)
        # print (item_reference)
        if len(item_reference) == 0 :
            return document
        if item_reference[0].find('[')==-1:
            if len(item_reference) == 1:
                return document.get(item_reference[0])
            return get_item(document.get(item_reference[0]), item_reference[1:])
        else:
            extracted_doc_from_array = get_array_item(document,item_reference)
            return get_item(extracted_doc_from_array,item_reference[1:])

def run (text, expression):

    document=yaml.load(text, Loader=yaml.FullLoader)
    expression = expression.split('.')

    return json.dumps(YamlExtracotr.get_item(document,expression))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Extract expression form YAML')
    parser.add_argument('-f', help='YAML Object to be parsed.')
    parser.add_argument('--expr', help='Expresion to find')
    args = parser.parse_args()
    if args.f or args.expr:
        data = args.f
        expr = args.expr
        if data =='-':
            data=sys.stdin.read()
        print (data)
        print(run(data, expr))

    else: # run as a server
        app.run(host='0.0.0.0', port=8888)

