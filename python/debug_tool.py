# -*- coding: utf-8 -*-
#!/usr/bin/python


def mk_log(msg,out_file="./log.txt"):
    try:       
        f = open(out_file, 'a')
        #ietrate list
        if type(msg)==type(list) or type(msg)==type(dict) :
            for lst in msg:
                f.write(lst+'\n')
        else:
            f.write(msg+'\n')
        f.close()    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()                  
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("[Error]\n",exc_type, fname, exc_tb.tb_lineno, e)                        


def debug_print(new_cnt, func_name="NULL", flag=True):
    global _debug_cnt
    
    _debug_cnt=new_cnt

    def p(msg):
        global _debug_cnt
        if flag: 
            print("%s[%i] : %s" % (func_name,_debug_cnt, msg))
        _debug_cnt+=1

    return p

