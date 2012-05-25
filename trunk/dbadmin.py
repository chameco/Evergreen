from src import base
import sqlite3
import cPickle as pickle
import sys
import os
def main():
    conn = sqlite3.connect("entity.db")
    if sys.argv[1] == "add":
        cur = conn.cursor()
        new = base.entity((100, 100), data={"facing" : 0, "name" : sys.argv[2]})
        temp = pickle.dumps(new.serialize())
        cur.execute("insert into chars values (?,?)", (sys.argv[2], temp))
        conn.commit()
    elif sys.argv[1] == "remove":
        cur = conn.cursor()
        cur.execute("delete from chars where name=?", (sys.argv[2],))
        conn.commit()
    conn.close()
if __name__ == "__main__":
    main()
