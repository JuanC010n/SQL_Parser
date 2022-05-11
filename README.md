# SQL_Parser
In this project, I have created a parser in Lark that can parse may of the methods in the select statement from the language SQL. 
In SQL select statemets there are many combinations that can occur; there are where clauses where. values are compared, there exists the posibility of checkingg
if the value is null or if it exists, you can group them or order them by values while also having the prder be ascending or descending, there are
also unions of select statements and some more which I could not implement.

This parser is not able to recogise words that have number embedded in them, while the python implementation also has problems with values that
have an undercore that separates them, also the python implementation is not able to compare columns to words while it is able to compare them to numbers, 
finally the python implementation is not able to read the "*" operator, which is strange as it is a word and with the lark parser on the website, 
it is able to create the tree with it.

In order to run this python script from mac:
- We will first need to clone the repository
  git clone https://github.com/JuanC010n/SQL_Parser.git
- Then we will need to install pip3:
  python3 get-pip.py
- Then we will need to install both the pandas and the lark libraries:
  pip3 install pandas
  pip3 install lark
- Then we will need to go to the correct folder:
  cd SQL_Parser
- Finally we can then run the main file and work through the program, there are several examples already laid out in order to test the 
  translation, there is also another file in the repository with more extensive tests that can be done through the lark IDE website:
  python3 main.py
