# -*- coding: utf-8 -*-
#!/usr/bin/python
bSHOW_COLOR = True    
CODE={
    'ENDC':0,  # RESET COLOR
    'BOLD':1,
    'UNDERLINE':4,
    'BLINK':5,
    'INVERT':7,
    'CONCEALD':8,
    'STRIKE':9,
    'GREY30':90,
    'GREY40':2,
    'GREY65':37,
    'GREY70':97,
    'GREY20_BG':40,
    'GREY33_BG':100,
    'GREY80_BG':47,
    'GREY93_BG':107,
    'DARK_RED':31,
    'RED':91,
    'RED_BG':41,
    'LIGHT_RED_BG':101,
    'DARK_YELLOW':33,
    'YELLOW':93,
    'YELLOW_BG':43,
    'LIGHT_YELLOW_BG':103,
    'DARK_BLUE':34,
    'BLUE':94,
    'BLUE_BG':44,
    'LIGHT_BLUE_BG':104,
    'DARK_MAGENTA':35,
    'PURPLE':95,
    'MAGENTA_BG':45,
    'LIGHT_PURPLE_BG':105,
    'DARK_CYAN':36,
    'AUQA':96,
    'CYAN_BG':46,
    'LIGHT_AUQA_BG':106,
    'DARK_GREEN':32,
    'GREEN':92,
    'GREEN_BG':42,
    'LIGHT_GREEN_BG':102,
    'BLACK':30,
}
if bSHOW_COLOR :
	def termcode(num):
		return '\033[%sm'%num

	def colorstr(astr,color):
		print(termcode(CODE[color])+astr+termcode(CODE['ENDC']))
	def p_red(astr):	
		print(termcode(CODE["RED"])+astr+termcode(CODE['ENDC']))
	def p_yel(astr):	
		print(termcode(CODE["YELLOW"])+astr+termcode(CODE['ENDC']))	
	def p_grn(astr):	
		print(termcode(CODE["GREEN"])+astr+termcode(CODE['ENDC']))		
	def p_blu(astr):	
		print(termcode(CODE["BLUE"])+astr+termcode(CODE['ENDC']))			
else :
	def colorstr(astr,color):
		print(astr)
	def p_red(astr):	
		print(astr)
	def p_yel(astr):	
		print(astr)
	def p_grn(astr):	
		print(astr)
	def p_blu(astr):	
		print(astr)