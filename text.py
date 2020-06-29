import jinja2
import os
from jinja2 import Template
from new_analysis import *
latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)
template = latex_jinja_env.get_template('Jinja-text.tex')

raw_tex = template.render(q1=Q_list[0].content,q2=Q_list[1].content,q3=Q_list[2].content,q4=Q_list[3].content,q5=Q_list[4].content,q6=Q_list[5].content,q7=Q_list[6].content,q8=Q_list[7].content,q9=Q_list[8].content,q10=Q_list[9].content,q11=Q_list[10].content)

filehandle = open('temp.tex', 'w')
filehandle.write(raw_tex)
filehandle.close()

c=input("Please enter the Company name.")

template = latex_jinja_env.get_template('temp.tex')

raw_tex = template.render(v1=Q_list[0].cond,v2=Q_list[1].cond,v3=Q_list[2].cond,v4=Q_list[3].cond,v5=Q_list[4].cond,v6=Q_list[5].cond,v7=Q_list[6].cond,v8=Q_list[7].cond,v9=Q_list[8].cond,v10=Q_list[9].cond,v11=Q_list[10].cond,org=c, company=c)
filehandle = open('Graphs/report.tex', 'w')
filehandle.write(raw_tex)
filehandle.close()

template = latex_jinja_env.get_template('Graphs/report.tex', 'w')
raw_tex=template.render(n1=Q_list[0].n,n1i=Q_list[0].ni,n2=Q_list[1].n,n3=Q_list[2].n,m3=Q_list[2],n4=Q_list[3].n,n4i=Q_list[3].ni,n5=Q_list[4].n,n5_2=Q_list[4].n2,n6=Q_list[5].n,n7=Q_list[6].n,n8=Q_list[7].n,n8_2=Q_list[7].n2,n9=Q_list[8].n,n10=Q_list[9].n,n11=Q_list[10].n,company=c, org=c)
#raw_tex=template.render(n1=Q_list[0].n,n2=Q_list[1].n,n3=Q_list[2].n,m3=Q_list[2],n4=Q_list[3].n,n5=Q_list[4].n,n6=Q_list[5].n,n7=Q_list[6].n,n8=Q_list[7].n,n9=Q_list[8].n,n10=Q_list[9].n,n11=Q_list[10].n,company=c, org=c)
filehandle = open('Graphs/report.tex', 'w')
filehandle.write(raw_tex)
filehandle.close()

template = latex_jinja_env.get_template('Graphs/report.tex', 'w')
raw_tex = template.render(m3=Q_list[2].m, n5_2=Q_list[4].n2, n8_2=Q_list[7].n2,n1i=Q_list[0].ni, company=c,org=c)
#raw_tex = template.render(m3=Q_list[2], company=c,org=c)
filehandle = open('Graphs/report.tex', 'w')
filehandle.write(raw_tex)
filehandle.close()

os.chdir('Graphs')
os.system('xelatex report.tex')
os.system('open report.pdf')
