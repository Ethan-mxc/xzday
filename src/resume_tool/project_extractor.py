# encoding:utf-8
import re
import sys
from tools import *
reload(sys)
sys.setdefaultencoding('utf8')

input_encode = 'utf-8'
# 构建专业知识库
major_set = []
score = {}

dic = ""
if cmp(get_os(),"n")==0:
    dic = sys.path[0]+"\\resume_tool\\project_dic"
else:
    dic = sys.path[0]+"/resume_tool/project_dic"
    
for v in  open(dic, 'r'):
    vs = v.split()
    major_set.append(vs[0])
    score[vs[0]] = vs[1]
    

# 将items（list）所有“!*!!”元素，过滤掉
def drop_null(items):
    result = []
    for item in items:
        if item.strip() == "!*!!":
            continue
        result.append(item.strip())
    return result


# 抽取专业信息,并将日期按照顺序排列存入list
def project_extract(str):
    result_list = []
    score_list = []
    for major in major_set:
        if str.__contains__(major):
            result_list.append(major)
    # 歧义消解 水利 水利水电工程 归并为水利水电工程
    result_list = list(set(result_list))
    for i in range(0, len(result_list)):
        for j in range(0, len(result_list)):
            if i == j:
                continue
            if result_list[i].__contains__(result_list[j]):
                result_list[j] = '!*!!'
    result_list = drop_null(result_list)

    # 歧序消解
    if len(result_list) > 1:
        result_dic = {}
        for item in result_list:
            index = str.find(item)
            result_dic[item] = index
        result_list = sorted(result_dic.items(), key=lambda d: d[1], reverse=False)
        result_list = [v[0] for v in result_list]
    for resultemp in result_list:
        score_list.append(score[resultemp])
        # print type(result_list)
    return result_list,score_list


def process(input_file_path):
    for line in open(input_file_path, 'r'):
        try:
            line = line.strip().decode('utf-8') # 设置编码格式
        except:
            line = line.strip().decode('gb2312') 
        school_list,score_list = project_extract(line)
        for d in school_list:
            print d,score[d]
        #print '-------'


def main():
    print 'this is main'
    input_file_path = 'lcy.txt'
    result_dic = process(input_file_path)


if __name__ == '__main__':
    main()
