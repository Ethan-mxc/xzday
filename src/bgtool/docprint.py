# -*- coding: cp936 -*-
__author__ = 'corey'
# -*- coding:utf-8 -*-
import docx

def printdoc():
    
    document = docx.Document("./1.docx")
    #��ӡÿ�����������
    for paragraph in document.paragraphs:
        print paragraph.text
    #��ӡÿ����������
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                print cell.text
        
printdoc()
