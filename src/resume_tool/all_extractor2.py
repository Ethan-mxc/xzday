#!/usr/bin/env python
# encoding:utf-8

from date_extractor import *
from school_name_extractor import *
from major_extractor import *
from degree_extractor import *
from school_ship_extractor import *
from skill_extractor  import *
from project_extractor import *

import chardet

import re

space_pattern = re.compile('\s')

input_encode = 'utf-8'

def init_info_dic():
    result = {}
    result['start_date'] = ''
    result['end_date'] = ''
    result['school'] = ''
    result['major'] = ''
    result['degree'] = '' 
    return result

# 获取教育经历的数目
def get_education_number(from_date, from_school):
    if from_school == 0 or from_school == 0:
        return max(from_date, from_school)
    else:
        return min(from_date, from_school)

# 替换str中所有在list中出现的字符串
def replace_list_from_str(str, str_list):
    for s in str_list:
        str = str.replace(s, ' ')
    return str


def skill_info_extract(input_str):
    skill_list = skill_extract(input_str);
    return skill_list 

#项目相关
def project_info_extract(input_str):
    project_list,project_score = project_extract(input_str);
    return project_list,project_score   


#奖学金相关
def ship_info_extract(input_str):
    ship_list = ship_extract(input_str);
    return ship_list
    
    
    
# PS: 解析的格式是utf-8
def school_info_extract(input_str):
    result = []
    if len(input_str.strip()) == 0:
        return result
    #input_str_src = space_pattern.sub('', input_str)
    
    
    #时间
    date_list = date_extract(input_str)
    tmp_str = replace_list_from_str(input_str, date_list)
    # for d in date_list:
    # print d
 #   school_list = school_name_extract(input_str)
    # for d in school_list:
    # print d
    
    #专业
    major_list = major_extract(input_str)
    tmp_str = replace_list_from_str(tmp_str, major_list)
    # for d in major_list:
    # print d
    
    #学历
    degree_list = degree_extract(input_str)
    tmp_str = replace_list_from_str(tmp_str, degree_list)
    # for d in degree_list:
    # print d
    
    #学校
    school_list = school_name_extract(tmp_str)

    date_number = get_education_number_from_date(input_str)
    school_number = get_education_number_from_school_name(input_str)
    education_number = get_education_number(school_number, date_number)

    for i in range(0, education_number):
        tmp = init_info_dic()
        j = i * 2
        if j < len(date_list):
            tmp['start_date'] = date_list[j]
        j += 1
        if j < len(date_list):
            tmp['end_date'] = date_list[j]

        if i < len(school_list):
            tmp['school'] = school_list[i]

        if i < len(major_list):
            tmp['major'] = major_list[i]

        if i < len(degree_list):
            tmp['degree'] = degree_list[i]

        if tmp['end_date'] == '' and (input_str.__contains__(u"至今") or input_str.__contains__(u"致今")):
            tmp['end_date'] = '1970/01/01'

        result.append(tmp)
    return result

def process(input_file_path):
    result_list = []
    items = []
    items.__sizeof__()
    all_line = ""
    school_info_list = []
    for line in open(input_file_path, 'r'):
        try:
            line = line.strip().decode('utf-8') # 设置编码格式
        except:
            try:
                line = line.strip().decode('gb2312') 
            except:
                continue  
        all_line = all_line +line     
        info_list = school_info_extract(line)  
        for info in info_list:
            if len(info_list) != 0:
                school_info_list.append(info)
            
    result_list.append(school_info_list)
    #整体分析
    
    #奖学金分析
    ship_list = ship_info_extract(all_line)
    for ship in ship_list:
        print "奖学金相关:"+ship
    
    result_list.append(ship_list) 
    #关键词分析
    skill_list = skill_info_extract(all_line)
    for temp in skill_list:
        print "能力:"+temp
    
    result_list.append(skill_list) 
    
    project_list,socre_list = project_info_extract(all_line)
    
    for i in range (0,len(project_list)):
        print "项目:"+project_list[i],socre_list[i]
    
    result_list.append(project_list)  
    result_list.append(socre_list)    
    return result_list
    


def main():
    print 'this is main'
    input_file_path = r'12.txt'
    #input_file_path = 'data/test'
    result_dic = process(input_file_path)


if __name__ == '__main__':
    main()
