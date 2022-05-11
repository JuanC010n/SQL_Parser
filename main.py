import sqlite3
import pandas as pd
from lark import Lark
my_grammar = """
start: union|exists|null|typ
typ : sel dist* cols_def+ (from tab+) (innj)* (wher (wording_cond|cond)+ (nestin)*)* ((grp_by) sort*)* (hav (wording_cond|cond)* )* ((ordr_by) sort*)* end
dist : "distinct"|"Distinct"|"DISTINCT"
havng : "Having"|"having"|"HAVING"
hav : havng (funct_cols)* word*   
null: sel cols_def+ (from tab+)* wher cols+ null_op end
null_op: null_is|null_not
null_is : "IS" "NULL"|"Is" "Null"|"is" "null"
null_not : "Is" "Not" "NULL"|"is" "not" "null"|"IS" "NOT" "NULL"
ordr_by : (or_by (funct_cols)* word) (((comma|commas) word)*)
grp_by : (gr_by (funct_cols)* word) (((comma|commas) word)*) 
nest_eq : (wher (wording_cond|cond) (nestin)*)*
column_eq : cols "=" sel cols+ (from tab+) (innj)* (wher cond)* (or_by word sort)* (",")*
nestin : ("IN"|"In"|"in"|"NOT" "IN"|"not" "in"| "Not" "In") (((sel cols+)* ((from tab+) (innj)*)* (grp_by word (sort)*)* (or_by word (sort)*)*)|word)
cols_def : (funct_cols)* (cols_def_w | "*"|cols_def_w (comma|commas) | "*" (comma|commas)|cols_def_w"."cols_def_w (comma|commas)| cols_def_w"."cols_def_w)
cols : (funct_cols)* (cols_word | "*"|cols_word (comma|commas) | "*" (comma|commas)|cols_word"."cols_word (comma|commas)| cols_word"."cols_word)
cols_word : WORD|WORD(underscore)WORD|WORD((underscore)WORD)*"."WORD(underscore WORD)*|"*"
cols_def_w : WORD|WORD(underscore)WORD|WORD((underscore)WORD)*"."WORD(underscore WORD)*|"*"
word : WORD|WORD(underscore)WORD|WORD((underscore)WORD)*"."WORD(underscore WORD)*|"*"
comma : ","
commas :" "
exists : sel cols_def+ from tab wher exists_op sel cols from tab wher (wording_cond|cond)+ end
exists_op: "EXISTS"|"Exists"|"exists"
union : (sel cols+ from tab+) (wher (wording_cond|cond)+ (nestin)*)* union_op typ
union_op: ("UNION"|"UNION" "ALL")
tab : tab_word|"," tab_word
tab_word : WORD|WORD(underscore)WORD|WORD((underscore)WORD)*"."WORD(underscore WORD)*|"*"
sel : "SELECT"|"select"|"Select"
from : "from"|"FROM"|"From" 
wher : "WHERE"|"Where"|"where"
or_by : ("ORDER" "BY"|"Order" "by"|"order" "by"|"order" underscore "by")
gr_by : ("GROUP" "BY"|"Group" "by"|"group" "by"|"group" underscore "by")
wording_cond : (word|","word|word"."word)
wording_condres : (word|","word|word"."word|num)
num : NUMBER
cons : [/(["'])(.*?[^\\])\1/]
innj : (innj_n
|innj_lft
|innj_r
|innj_fl
|innj_flo) tab innj_op cond
innj_n : "INNER" "JOIN"|"Inner" "join"| "inner" "join"
innj_lft : "LEFT" "JOIN"|"Left" "Join"| "left" "join"
innj_r : "RIGHT" "JOIN"|"Right" "Join"| "right" "join"
innj_fl : "FULL" "JOIN"|"Full" "Join"| "full" "join"
innj_flo : "FULL" "OUTER" "JOIN"|"Full" "Outer" "Join"| "full" "outer" "join"
sort : s_asc|s_desc
s_asc : "ASC"
s_desc : "DESC"
innj_op : ("ON"|"On"|"on")
cond : (((funct_cols)*) wording_cond comparator) (cond_op (( (funct_cols)* wording_cond comparator)))*
cond_op : (and_op|or_op|not_op)
and_op :"AND"|"and"
or_op : "OR"|"or"
not_op : "NOT"|"not"
underscore : "_"
eq_comp : "="
less_comp : "<"
big_comp : ">"
neq_comp : "!="
comparator : (eq_comp(wording_condres)|big_comp wording_condres
|less_comp wording_condres|neq_comp wording_condres|"<>"wording_condres)
%import common.WORD
%import common.NUMBER
%ignore " "
%ignore "("|")"
%ignore "["|"]"
funct_cols : f_avg|f_sum|f_count|f_min|f_max
f_count : "COUNT"
f_avg : "AVG"
f_sum : "SUM"
f_min : "MIN"
f_max : "MAX"
end : ";"
"""
program_op_list = ["SELECT name FROM Customers where age = 19 ;","SELECT customerId,name,age,City FROM Customers order by age ASC;","SELECT distinct age, name FROM Customers where age in age  ORDER BY age ASC ;", "SELECT COUNT(customerId), Country FROM Customers GROUP BY Country HAVING age = 22 ORDER BY customerId DESC; ", "SELECT name, age, Country FROM Customers WHERE Country IS NOT NULL;", "SELECT City, Country FROM Customers WHERE customerId = 1234 UNION SELECT City, Country FROM Suppliers WHERE Age = 19 ORDER BY City;" ]
columns = []
def parser(list):
    parser = Lark(my_grammar)
    '''
    for i3 in range(0,int(len(program_op_list))):
        parse_tree = parser.parse(program_op_list[i3])
        print(parse_tree.pretty())
        print(translate(parse_tree))
        search(translate(parse_tree))
'''
    parse_tree = parser.parse(list)
    print(parse_tree.pretty())
    print(translate(parse_tree))
    search(translate(parse_tree))


    # print(parse_tree.pretty())
def createDatabase() :
    conn = sqlite3.connect('test2_database')
    c = conn.cursor()

    c.execute('''
                  CREATE TABLE IF NOT EXISTS Products
                  ([product_id] INTEGER PRIMARY KEY, [product_name] TEXT)
                  ''')

    c.execute('''
                  CREATE TABLE IF NOT EXISTS Prices
                  ([productId] INTEGER PRIMARY KEY, [price] INTEGER)
                  ''')
    c.execute('''
                      CREATE TABLE IF NOT EXISTS Customers
                      ([customerId] INTEGER PRIMARY KEY, [name] TEXT, [age] INTEGER,[City] TEXT, [Country] TEXT)
                      ''')
    c.execute('''
                      CREATE TABLE IF NOT EXISTS Suppliers
                      ([customerId] INTEGER PRIMARY KEY, [name] TEXT, [age] INTEGER, [Country] TEXT,[City] TEXT,[nOrders] INTEGER)
                      ''')
    c.execute('''
                      INSERT INTO Customers (customerId,name, age,City,Country)
                        VALUES
                            (1234,'Juan',22,'Madrid','Spain'),
                            (235,'James',26,'Madrid','Spain'),
                            (7893,'Michael',22,'Bath','UK'),
                            (79326,'Pedro',19,'Sevilla','Spain');
                      ''')
    c.execute('''
                      INSERT INTO Suppliers (customerId,name, age,Country,City,nOrders)
                        VALUES
                            (1234,'Juan',22,'Madrid','Spain',345),
                            (7893,'Michael',22,'Bath','UK',8879),
                            (79326,'Pedro',19,'Sevilla','Spain',112002);
                      ''')
    c.execute('''
                      INSERT INTO Prices (productId, price)
                        VALUES
                            (28916,99),
                            (881619,100),
                            (726381763,99),
                            (112,100),
                            (221,100);
                      ''')
    conn.commit()

def translate(t):
  columns_temp = ""
  global  columns
  if t.data == 'start':
    return ''.join(map(translate, t.children))
  if t.data == 'cond_op':
    return ''.join(map(translate, t.children))
  if t.data == 'null':
    return ''.join(map(translate, t.children))
  if t.data == 'null_op':
    return ''.join(map(translate, t.children))
  if t.data == 'null_is':
    return "IS NULL" + ''.join(map(translate, t.children))
  if t.data == 'cols_def':
    return ''.join(map(translate, t.children))
  if t.data == 'dist':
      return " DISTINCT " + ''.join(map(translate, t.children))
  if t.data == 'null_not':
    return "IS NOT NULL" + ''.join(map(translate, t.children))
  if t.data == 'innj':
    return   ''.join(map(translate, t.children))
  if t.data == 'innj_n':
    return  " INNER JOIN " + ''.join(map(translate, t.children))
  if t.data == 'innj_lft':
    return  " LEFT JOIN " + ''.join(map(translate, t.children))
  if t.data == 'innj_fl':
    return  " FULL JOIN " + ''.join(map(translate, t.children))
  if t.data == 'innj_flo':
    return  " FULL OUTER JOIN " + ''.join(map(translate, t.children))
  if t.data == 'innj_op':
    return ''.join(map(translate, t.children)) + " ON "
  elif t.data == "typ":
    return ''.join(map(translate, t.children))
  elif t.data == "nestin":
    return " IN " + ''.join(map(translate, t.children))
  elif t.data == "sel":
    return ''.join(map(translate, t.children)) + 'SELECT '
  elif t.data == "s_asc":
    return "ASC " + ''.join(map(translate, t.children))
  elif t.data == "s_desc":
    return "DESC " + ''.join(map(translate, t.children))
  elif t.data == "cols":
      return ''.join(map(translate, t.children))
  elif t.data == "ordr_by":
      return ''.join(map(translate, t.children))
  elif t.data == "grp_by":
      return ''.join(map(translate, t.children))
  elif t.data == "gr_by":
      return ''.join(map(translate, t.children)) + " GROUP BY "
  elif t.data == "hav":
      return ''.join(map(translate, t.children)) + " HAVING "
  elif t.data == "or_by":
      return ''.join(map(translate, t.children)) + " ORDER BY "
  elif t.data == "havng":
      return ''.join(map(translate, t.children))
  elif t.data == "sort":
      return ''.join(map(translate, t.children))
  elif t.data == "gr_by":
      return ''.join(map(translate, t.children))
  elif t.data == "funct_cols":
      return ''.join(map(translate, t.children))
  elif t.data == "f_count":
      return ''.join(map(translate, t.children)) + " COUNT"
  elif t.data == "and_op":
      return ''.join(map(translate, t.children)) + " AND "
  elif t.data == "or_op":
      return ''.join(map(translate, t.children)) + " OR "
  elif t.data == "not_op":
      return ''.join(map(translate, t.children)) + " NOT "
  elif t.data == "f_sum":
      return ''.join(map(translate, t.children)) + " SUM"
  elif t.data == "f_min":
      return ''.join(map(translate, t.children)) + " MIN"
  elif t.data == "f_max":
      return ''.join(map(translate, t.children)) + " MAX"
  elif t.data == "f_avg":
      return ''.join(map(translate, t.children)) + " AVG"
  elif t.data == "eq_comp":
      return ''.join(map(translate, t.children)) + " = "
  elif t.data == "less_comp":
      return ''.join(map(translate, t.children)) + " < "
  elif t.data == "big_comp":
      return ''.join(map(translate, t.children)) + " > "
  elif t.data == "neq_comp":
      return ''.join(map(translate, t.children)) + " != "
  elif t.data == "word":
      block = t.children[0]
      return '(' + block + ')' + " "
  elif t.data == "cols_word":
      block = t.children[0]
      return '(' + block + ')' + " "
  elif t.data == "cols_def_w":
      block = t.children[0]
      columns += block + " "
      return '(' + block + ')' + " "
  elif t.data == "tab_word":
      block = t.children[0]
      return ' ' + block + ' '
  elif t.data == "num":
      block = t.children[0]
      return ' ' + block + ' '
  elif t.data == "comma":
      return ''.join(map(translate, t.children)) + ","
  elif t.data == "commas":
      return ''.join(map(translate, t.children))
  elif t.data == "from":
      return ''.join(map(translate, t.children)) + ' FROM '
  elif t.data == "tab":
      return ''.join(map(translate, t.children))
  elif t.data == "wher":
      return ''.join(map(translate, t.children)) + ' WHERE '
  elif t.data == "s_desc":
      return ''.join(map(translate, t.children)) + 'DESC '
  elif t.data == "cond":
      return ''.join(map(translate, t.children))
  elif t.data == "wording_cond":
      return ''.join(map(translate, t.children))
  elif t.data == "comparator":
      return ''.join(map(translate, t.children))
  elif t.data == "union":
      return ''.join(map(translate, t.children))
  elif t.data == "union_op":
      return ''.join(map(translate, t.children)) + " UNION "
  elif t.data == "wording_condres":
      return ''.join(map(translate, t.children))
  elif t.data == "end":
      return ''.join(map(translate, t.children)) + ';'
# one  limitation is that names can not be used to compare in where clause and that names with underscores get cut
# and also finally names with numbers embedded do not work
  else:
    print(t.data)
    raise SyntaxError("bad tree")





def search(input) :
    conn = sqlite3.connect('test2_database')
    c = conn.cursor()
    c.execute(input)
    fcols = []
    for i in range (1,int(len(columns)/2)):
        if (columns[i] == " "):
            colss = " "
            for i2 in range(0,i):
                colss = colss + columns[i2]

            print("columns",colss)
    fcols = colss.split(" ")
    del fcols[0]

    print("fcols:", fcols)
    names2 = fcols
    df = pd.DataFrame(c.fetchall(), columns=names2)
    print(df)
if __name__ == '__main__':
    createDatabase()
    username = 0
    while (int(username) < 5):
        username = input("Enter Number from 0 to 5: (else enter larger number to finnish)\n")
        if (int(username) < 5):
            parser(program_op_list[int(username)])
        else :
            print("Succesful Exit!")



