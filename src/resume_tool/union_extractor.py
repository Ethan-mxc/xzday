#学生会相关
# encoding:utf-8
import re

union_str1 = u"(主席|部长|会长|班长|副主席|副部长|副会长|党支书|团支书|学习委员|宣传委员|生活委员)"
union_pattern1 = re.compile(union_str1)

# 抽取学位信息,并将日期按照顺序排列存入list
def union_extract(str):
    result_list = []
    school_list = union_pattern1.findall(str)
    for d in school_list:
        # print d
        result_list.append(d)
    return result_list

# 会破坏信息排布的顺序


def process(input_file_path):
    for line in open(input_file_path, 'r'):
        try:
            line = line.strip().decode('utf-8') # 设置编码格式
        except:
            line = line.strip().decode('gb2312')   
        degree_list = union_extract(line)
        for d in degree_list:
            print d
        print '-------'

def main():
    print 'this is main'
    input_file_path = 'lcy.txt'
    result_dic = process(input_file_path)

if __name__ == '__main__':
    main()
