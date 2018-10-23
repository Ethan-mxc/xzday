# encoding:utf-8
import re

degree_str1 = u"(一等奖学金|二等奖学金|三等奖学金|优秀毕业生|优良毕业生|国家励志奖学金|学生标兵|优秀学生|优秀本科生|三好学生|优秀学生干部)"
degree_pattern1 = re.compile(degree_str1)

# 抽取学位信息,并将日期按照顺序排列存入list
def ship_extract(str):
    result_list = []
    school_list = degree_pattern1.findall(str)
    for d in school_list:
        # print d
        result_list.append(d)
    return result_list

# 会破坏信息排布的顺序
# 该函数并没有被用到
def remove_duplicate_data(degree_list):
    degree_dic = {}
    for k in degree_list:
        if k not in degree_dic:
            degree_dic.setdefault(k, 0)
        else:
            degree_list.remove(k) #去除第一个k对象
    return degree_list

def process(input_file_path):
    for line in open(input_file_path, 'r'):
        try:
            line = line.strip().decode('utf-8') # 设置编码格式
        except:
            line = line.strip().decode('gb2312')   
        degree_list = ship_extract(line)
        for d in degree_list:
            print d
        print '-------'

def main():
    print 'this is main'
    input_file_path = 'lcy.txt'
    result_dic = process(input_file_path)

if __name__ == '__main__':
    main()
