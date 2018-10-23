# encoding:utf-8
import re
import sys
from bgtool.codeinit import *
from tools import *
reload(sys)
sys.setdefaultencoding('utf8')

input_encode = 'utf-8'
# 构建专业知识库

# 抽取技能信息,并将日期按照顺序排列存入list
def skill_extract(str):
    result_list = []
    dic = ""
    if cmp(get_os(),"n")==0:
        dic = sys.path[0]+"\\resume_tool\\skill_dic"
    else:
        dic = sys.path[0]+"/resume_tool/skill_dic"
    jieba.load_userdict(dic)
    wordcut = WordCut(str)
    for word, flag in wordcut.cutWords():
        if cmp(flag,"skill")==0:
            if word not in result_list:
                result_list.append(word)
    return result_list


def process(input_file_path):
    with open(input_file_path, "r") as f:
        text = f.read()
    skill_list = skill_extract(text)
    for skill in skill_list:
        print skill



def main():
    print 'this is main'
    input_file_path = 'lcy.txt'
    result_dic = process(input_file_path)


if __name__ == '__main__':
    main()
