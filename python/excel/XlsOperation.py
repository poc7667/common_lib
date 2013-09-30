#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.path.append('/Users/hsu-wei-cheng/common_lib/python')
#standard lib
import argparse
import pprint
import re
import os
import time
import string
import difflib
from pprint import pprint
from timeit import default_timer as timer
#3rd part lib
#load custom library (remember to set PYTHONPATH in your .bashrc)
from color_print import *
from debug_tool import *
import xlrd
import xlwt
from xlutils.copy import copy as xlscopy
# from __future__ import division # division
from collections import OrderedDict

class ConvertHelper():
    def get_xy_range(self, start, end):
        '''
        Ex : A1 E5 => (0,0,4,4)
        '''
        try:
            s = self.get_xy(start)
            e = self.get_xy(end)
            if e[0]-s[0] < 0 :
                raise
            if e[1]-s[1] < 0 :
                raise
            return s + e # return (1,2,5,5)
            pass
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("[Error]\n", exc_type, fname, exc_tb.tb_lineno)
            sys.exit(e)
            raise e

    def get_xy(self, cell_pos):
        try:
            c = re.split('(\d+)',cell_pos)                
            col = ord(c[0].lower() ) - ord('a')
            row = int(c[1]) - 1
            return ( row, col )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("[Error]\n", exc_type, fname, exc_tb.tb_lineno)
            sys.exit(e)
            raise e

    
class ReadWrite(ConvertHelper):
    """docstring for XLS"""

    def rd_range(self, sht, i_row, i_col, n_row, n_col):
        '''
        Read Range of Fileds
        return [[row,col,val],.....]
        '''
        try:
            rng_list=[]
            for i in range(i_row, i_row + n_row):
                if i >= sht.nrows : continue
                for j in range(i_col, i_col + n_col):
                    try:
                        if j >= sht.ncols : continue
                        rng_list.append([i, j, self.get_cell(sht, i, j)])                        
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print("[Error]\n", exc_type, fname, exc_tb.tb_lineno)
                        sys.exit(e)
                        raise e
            return rng_list
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("[Error]\n", exc_type, fname, exc_tb.tb_lineno)
            sys.exit(e)
            raise e
    def wrt_cell(self, sht, row,  col, val):
        try:
            self.col_idx = col # remember current col idx

            sht.write( row, col, val)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("[Error]\n", exc_type, fname, exc_tb.tb_lineno)
            print col, val
            sys.exit(e)
            raise e        

    def remove_tailing_float(self, row, col):
        val = self.sht.cell_value(row, col)
        # 在Excel讀取 12 都會自動轉換為浮點 12.0
        # http://kasicass.blog.163.com/blog/static/395619200724105023952/
        if ( type(val) == float ):
            if ( val == int(val) ):
                val = int(val)
            
        return str(val).strip()

    def get_cell(self, sht, row, col):
        try:
            # c_type
            c_type = sht.cell(row, col).ctype
            c_val = sht.cell_value(row, col)
            return c_val

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("[Error]\n", exc_type, fname, exc_tb.tb_lineno)
            sys.exit(e) 
            raise e 

    def get_str(self, cell_pos):
        try:
            row, col = self.get_xy(cell_pos)
            val =  str(self.sht.cell_value(row, col)).lstrip("'").rstrip("'")
            return val.strip() if val else None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("[Error]\n", exc_type, fname, exc_tb.tb_lineno)
            sys.exit(e)
            raise e

    def get_num(self,cell_pos):
        try:
            row, col = self.get_xy(cell_pos)
            try:
                val =  abs(float(self.sht.cell_value(row, col)))
            except:
                val = None

            return val
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("[Error]\n", exc_type, fname, exc_tb.tb_lineno)
            print(val)
            sys.exit(e)
            raise e

class XlsTools(ConvertHelper, ReadWrite):

    def find_all_cells_contains(self, s, sht, *rng_in_sht):
        '''
        回傳所有要找的Cell
        '''
        try:
            all_list=[]
            if len(rng_in_sht) == 1:
                arg_val = rng_in_sht[0]
                if len(arg_val)==2:
                    #Convert A1, E5 => (1,1,4,4)
                    scan_rng = self.get_xy_range(arg_val[0], arg_val[1])
                else:
                    sys.exit()

            elif len(rng_in_sht) == 0:
                scan_rng = (0, 0, sht.nrows - 1 , sht.n_cols - 1)
            else: #
                sys.exit("find_all_cell_index error")

            for i in range(scan_rng[0], scan_rng[2]+1):
                for j in range(scan_rng[1], scan_rng[3]+1):
                    c_val = str(self.get_cell(sht, i, j))
                    if s in c_val:
                        print(c_val)
                        all_list.append((i, j, c_val))

            return all_list

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("[Error]\n", exc_type, fname, exc_tb.tb_lineno)
            sys.exit(e)
            raise e

'''
class FormalFormat():
    def get_note(self, s):

        if s: # remove leading zero , convert scientific
            try:
                s=str(int(float(s)))
            except:
                pass
            s=s.lstrip("0").strip()

        if s and s.endswith(".0"):
            return str(s[:-2])
        elif s:
            return str(s)
        else:
            return None
    def get_date(self, s):
        if s:
            if len(s.split('/'))==2: # if already ok!!
                return s
            new_s = s.replace("'",'')
            new_s = new_s.split('/')[1:] # 102/04/1 -> 04 1
            ret_s =''
            for i in new_s: # 04 1 -> 04/01
                if len(i)==1:
                    j='0'+i
                elif len(i) == 2 : j=i
                else: 
                    print s
                    print i
                    print(len(i))
                    sys.exit("FormalFormat get_date")
                ret_s += '/'+ j
            # /04/01 -> 04/01
            return ret_s[1:]
        else:
            return None
        pass
    pass
    def get_money(self, s):
        if s and s.endswith('.0'):
            s = s[:-2]
        if s:
            new_s = s.replace(',','').strip()
            if new_s.isdigit():
                return new_s
            else:
                print("get_money failed : %s" % s)
                return None
        else:
            return None
        pass
'''