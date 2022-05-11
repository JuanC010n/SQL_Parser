import sqlite3
import pandas as pd
from lark import Lark
my_grammar = """
start: union|exists|null|typ
typ : sel dist* cols+ (from tab+) (innj)* (wher (wording_cond|cond)+ (nestin)*)* ((grp_by) sort*)* (hav (wording_cond|cond)* )* ((ordr_by) sort*)* end
dist : "distinct"|"Distinct"|"DISTINCT"
havng : "Having"|"having"|"HAVING"
hav : havng (funct_cols)* word*   
null: sel cols+ wher tab null_op end
null_op: "Is" "NULL"|"Is" "Not" "NULL"|"IS" "Null"|"is" "not" "null"|"IS" "NOT" "NULL"|"is" "null"
ordr_by : (or_by (funct_cols)* word) (((comma|commas) word)*)
grp_by : (gr_by (funct_cols)* word) (((comma|commas) word)*) 
nest_eq : (wher (wording_cond|cond) (nestin)*)*
column_eq : cols "=" sel cols+ (from tab+) (innj)* (wher cond)* (or_by word sort)* (",")*
nestin : ("IN"|"In"|"in"|"NOT" "IN"|"not" "in"| "Not" "In") (((sel cols+)* ((from tab+) (innj)*)* (grp_by word (sort)*)* (or_by word (sort)*)*)|word)
cols : (funct_cols)* (word | "*"|word (comma|commas) | "*" (comma|commas)|word"."word (comma|commas)| word"."word)
word : WORD|WORD(underscore)WORD|WORD((underscore)WORD)*"."WORD(underscore WORD)*|"*"
comma : ","
commas :" "
exists : sel cols+ from tab wher exists_op sel cols from tab wher (wording_cond|cond)+ end
exists_op: "EXISTS"|"Exists"|"exists"
union : (sel cols+ from tab+) (wher (wording_cond|cond)+ (nestin)*)* union_op typ
union_op: ("UNION"|"UNION" "ALL")
tab : word|"," word
sel : "SELECT"|"select"|"Select"
from : "from"|"FROM"|"From" 
wher : "WHERE"|"Where"|"where"
or_by : ("ORDER" "BY"|"Order" "by"|"order" "by"|"order" underscore "by")
gr_by : ("GROUP" "BY"|"Group" "by"|"group" "by"|"group" underscore "by")
wording_cond : (word|","word|word"."word)
wording_condres : (word|","word|word"."word|NUMBER)
cons : [/(["'])(.*?[^\\])\1/]
innj : ("INNER" "JOIN"|"Inner" "join"| "inner" "join"
|"LEFT" "JOIN"|"Left" "Join"| "left" "join"
|"RIGHT" "JOIN"|"Right" "Join"| "right" "join"
|"FULL" "JOIN"|"Full" "Join"| "full" "join"
|"FULL" "OUTER" "JOIN"|"Full" "Outer" "Join"| "full" "outer" "join") tab innj_op cond
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
def parser():
    parser = Lark(my_grammar)
    program = "SELECT City FROM Customers UNION SELECT City FROM Suppliers GROUP BY trina ASC ORDER BY City ;"

    parse_tree = parser.parse(program)
    print(parse_tree.pretty())
    print(translate(parse_tree))
    #search(translate(parse_tree))


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
                  ([product_id] INTEGER PRIMARY KEY, [price] INTEGER)
                  ''')
    c.execute('''
                      CREATE TABLE IF NOT EXISTS Customers
                      ([customer_id] INTEGER PRIMARY KEY, [name] TEXT, [age] INTEGER)
                      ''')
    conn.commit()

def translate(t):
  if t.data == 'start':
    return ''.join(map(translate, t.children))
  if t.data == 'cond_op':
    return ''.join(map(translate, t.children))
  elif t.data == "typ":
    return ''.join(map(translate, t.children))
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
  elif t.data == "comma":
      return ''.join(map(translate, t.children)) + ","
  elif t.data == "commas":
      return ''.join(map(translate, t.children))
  elif t.data == "from":
      return 'FROM '.join(map(translate, t.children)) + ' FROM '
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
      block = t.children[0]
      return ' ' + str(block)
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
    names2 = ['column 1',"Column 2","Column 3"]

    df = pd.DataFrame(c.fetchall(), columns=names2)
    print(df)
if __name__ == '__main__':
    #createDatabase()
    #search("SELECT * FROM Customers;")
    parser()



