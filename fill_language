#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from googletrans import Translator
from googletrans.models import Translated
from biplist import *
import sys, getopt



# translator = Translator()
# response = translator.translate('你好', dest='en')
# print(response)


def print_usage():
    print("python3 %s <输入language.plist文件> -o <补充翻译后的plist文件>" % sys.argv[0])
    print("-o: 如果不存在，默认覆盖原始文件")

def fillPlist(source_path, dest_path):
    translator = Translator()
    try:
        source_plist = readPlist(source_path)
        # print(source_plist)

        lang_mapping = {
            'cn':'zh-CN',
            'de':'de',
            'en':'en',
            'es':'es',
            'fr':'fr',
            'id':'id',
            'it':'it',
            'ja':'ja',
            'ko':'ko',
            'ru':'ru',
            'th':'th',
            'pt':'pt',
            'tw': 'zh-TW',
        }

        base_lang = 'en'

        for key in source_plist.keys():
            # print('key=>', key, ':', source_plist[key])
            element = source_plist[key]
            for lang in element.keys():
                if len(element[lang]) == 0:
                    if len(element[base_lang]) != 0:
                        response = translator.translate(element[base_lang], dest=lang_mapping[lang])
                        element[lang] = response.text
                        print('key= {}, translate: source={}, target_{}:{}'.format(key, element[base_lang], lang_mapping[lang], element[lang]))

        writePlist(source_plist, dest_path, binary=False)

    except InvalidPlistException as e:
        print("Not a plist:", e)
        sys.exit(2)
    
def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    try:
        opts, args = getopt.getopt(sys.argv[2:], "o:", ["output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        print_usage()
        sys.exit(2)

    source_path = sys.argv[1]
    dest_path = source_path
    for o, a in opts:
        if o in ("-o", "--output"):
            dest_path = a

    fillPlist(source_path, dest_path)



if __name__ == '__main__':
    main()
    
    