#!/usr/bin/python3

import os
import psycopg2
import re
import string
import sys
import urllib.parse as up

_PUNCTUATION = frozenset(string.punctuation)

def _remove_punc(token):
    """Removes punctuation from start/end of token."""
    i = 0
    j = len(token) - 1
    idone = False
    jdone = False
    while i <= j and not (idone and jdone):
        if token[i] in _PUNCTUATION and not idone:
            i += 1
        else:
            idone = True
        if token[j] in _PUNCTUATION and not jdone:
            j -= 1
        else:
            jdone = True
    return "" if i > j else token[i:(j+1)]

def _get_tokens(query):
    rewritten_query = []
    tokens = re.split('[ \n\r]+', query)
    for token in tokens:
        cleaned_token = _remove_punc(token)
        if cleaned_token:
            if "'" in cleaned_token:
                cleaned_token = cleaned_token.replace("'", "''")
            rewritten_query.append(cleaned_token)
    return rewritten_query



def search(query, query_type):
    
    rewritten_query = _get_tokens(query)
    length = len(rewritten_query)

    """TODO
    Your code will go here. Refer to the specification for projects 1A and 1B.
    But your code should do the following:
    1. Connect to the Postgres database.
    2. Graciously handle any errors that may occur (look into try/except/finally).
    3. Close any database connections when you're done.
    4. Write queries so that they are not vulnerable to SQL injections.
    5. The parameters passed to the search function may need to be changed for 1B. 
    """

    try :
        #up.uses_netloc.append("postgres")
        #url = up.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(database=os.environ["RDS_DB_NAME"],
            user=os.environ["RDS_USERNAME"],
            password=os.environ["RDS_PASSWORD"],
            host=os.environ["RDS_HOSTNAME"],
            port=os.environ["RDS_PORT"]
        )
        conn.autocommit = True
        cursor = conn.cursor()
        if query_type == "and":
            print("and")
            cursor.execute("CREATE OR REPLACE VIEW search_view AS SELECT s.song_name, s.artist_name, s.page_link FROM (SELECT * FROM tfidf as a INNER JOIN song as b ON a.song_id = b.song_id INNER JOIN artist as c ON b.artist_id = c.artist_id) as s WHERE token in %s GROUP BY s.song_name, s.page_link, s.artist_name HAVING COUNT(token) = %s ORDER BY sum(score) DESC;", (tuple(rewritten_query), length))
            
        elif query_type == "or":
            print("or")
            cursor.execute("CREATE OR REPLACE VIEW search_view AS SELECT s.song_name, s.artist_name, s.page_link FROM (SELECT * FROM tfidf as a INNER JOIN song as b ON a.song_id = b.song_id INNER JOIN artist as c ON b.artist_id = c.artist_id) as s WHERE token in %s GROUP BY s.song_name, s.page_link, s.artist_name ORDER BY SUM(score) DESC;", (tuple(rewritten_query),))    

    except:
       print('could not connect')
    finally:
        if (conn):
            cursor.close()
            conn.close()
            print("Connection closed")

def get_length():
    page = []
    try: 
        conn2 = psycopg2.connect(database=os.environ["RDS_DB_NAME"],
            user=os.environ["RDS_USERNAME"],
            password=os.environ["RDS_PASSWORD"],
            host=os.environ["RDS_HOSTNAME"],
            port=os.environ["RDS_PORT"]
        )
        cursor = conn2.cursor()
        cursor.execute("SELECT * FROM search_view")
        page = cursor.fetchall()
    except:
       print('could not connect')
    finally:
        if (conn2):
            cursor.close()
            conn2.close()
            print("Connection closed")
    return len(page)

def page_results(page):
    offset = page*20
    page = []
    try: 
        conn3 = psycopg2.connect(database=os.environ["RDS_DB_NAME"],
            user=os.environ["RDS_USERNAME"],
            password=os.environ["RDS_PASSWORD"],
            host=os.environ["RDS_HOSTNAME"],
            port=os.environ["RDS_PORT"]
        )
        cursor = conn3.cursor()
        cursor.execute("SELECT * FROM search_view OFFSET %s LIMIT 20;", (offset,))
        page = cursor.fetchall()
    except:
       print('could not connect')
    finally:
        if (conn3):
            cursor.close()
            conn3.close()
            print("Connection closed")
    return page
            
if __name__ == "__main__":
    if len(sys.argv) > 2:
        search(' '.join(sys.argv[2:]), sys.argv[1].lower())
        print(get_length())
    else:
        print("USAGE: python3 search.py [or|and] term1 term2 ...")

