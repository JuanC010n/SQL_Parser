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
ordr_by : (or_by (funct_cols)* word) ((comma word)*)
grp_by : (gr_by (funct_cols)* word) ((comma word)*) 
nest_eq : (wher (wording_cond|cond) (nestin)*)*
column_eq : cols "=" sel cols+ (from tab+) (innj)* (wher cond)* (or_by word sort)* (",")*
nestin : ("IN"|"In"|"in"|"NOT" "IN"|"not" "in"| "Not" "In") (((sel cols+)* ((from tab+) (innj)*)* (grp_by word (sort)*)* (or_by word (sort)*)*)|word)
cols : (funct_cols)* (word | "*"|word comma | "*" comma|word"."word comma| word"."word)
word : WORD|WORD("_")WORD|WORD(("_")WORD)*"."WORD("_"WORD)*|"*"
comma : ","|" "
exists : sel cols+ from tab wher exists_op sel cols from tab wher (wording_cond|cond)+ end
exists_op: "EXISTS"|"Exists"|"exists"
union : (sel cols+ from tab+) (wher (wording_cond|cond)+ (nestin)*)* union_op (sel cols+ from tab+) (wher (wording_cond|cond)+ (nestin)*)* (grp_by word (sort)*)* (hav (wording_cond|cond)* )* ((or_by word) (sort)*)* end
union_op: ("UNION"|"UNION" "ALL")
tab : word|"," word
sel : "SELECT"|"select"|"Select"
from : "from"|"FROM"|"From" 
wher : "WHERE"|"Where"|"where"
or_by : ("ORDER" "BY"|"Order" "by"|"order" "by"|"order" "_" "by")
gr_by : ("GROUP" "BY"|"Group" "by"|"group" "by"|"group" "_" "by")
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
cond_op : ("AND"|"OR"|"NOT"|"and"|"or"|"not")
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
    program = "SELECT COUNT(CustomerID), Country FROM Customers GROUP BY Country HAVING COUNT(CustomerID) = 1 ORDER BY COUNT(CustomerID) DESC;"

    parse_tree = parser.parse(program)
    print(parse_tree.pretty())
    print(translate(parse_tree))


    # print(parse_tree.pretty())
def createDatabase() :
    conn = sqlite3.connect('test2_database')
    c = conn.cursor()

    c.execute('''
                  CREATE TABLE IF NOT EXISTS products
                  ([product_id] INTEGER PRIMARY KEY, [product_name] TEXT)
                  ''')

    c.execute('''
                  CREATE TABLE IF NOT EXISTS prices
                  ([product_id] INTEGER PRIMARY KEY, [price] INTEGER)
                  ''')
    conn.commit()

def translate(t):
  if t.data == 'start':
    return ''.join(map(translate, t.children))
  elif t.data == "typ":
    return ''.join(map(translate, t.children))
  elif t.data == "sel":
    return ''.join(map(translate, t.children)) + 'SELECT '
  elif t.data == "cols":
      return ''.join(map(translate, t.children))
  elif t.data == "ordr_by":
      return ''.join(map(translate, t.children)) + " ORDER BY "
  elif t.data == "grp_by":
      return ''.join(map(translate, t.children)) + " GROUP BY "
  elif t.data == "hav":
      return ''.join(map(translate, t.children)) + " HAVING "
  elif t.data == "or_by":
      return ''.join(map(translate, t.children))
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
      return '(' + block + ')'
  elif t.data == "comma":
      return ''.join(map(translate, t.children))
  elif t.data == "from":
      return 'FROM '.join(map(translate, t.children)) + ' FROM '
  elif t.data == "tab":
      return ''.join(map(translate, t.children))
  elif t.data == "wher":
      return ''.join(map(translate, t.children)) + 'WHERE'
  elif t.data == "s_desc":
      return ''.join(map(translate, t.children)) + 'DESC'
  elif t.data == "cond":
      return ''.join(map(translate, t.children))
  elif t.data == "wording_cond":
      return ''.join(map(translate, t.children))
  elif t.data == "comparator":
      return ''.join(map(translate, t.children))
  elif t.data == "wording_condres":
      block = t.children[0]
      return ' ' + block
  elif t.data == "end":
      return ''.join(map(translate, t.children)) + ';'



  else:
    print(t.data)
    raise SyntaxError("bad tree")




def search(input) :
    conn = sqlite3.connect('test2_database')
    c = conn.cursor()
    c.execute(input)
    names2 = ['column 1', 'column 2', 'column 3', 'column 4']

    df = pd.DataFrame(c.fetchall(), columns=names2)
    print(df)
if __name__ == '__main__':
    search("SELECT * FROM prices;")
    parser()



