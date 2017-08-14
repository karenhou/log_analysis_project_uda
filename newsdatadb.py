#!/usr/bin/env python

# Database code for the DB news.

import psycopg2

DBNAME = "news"

def connect(database_name):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        raise e

# list top 3 most viewed articles
def list_most_pop_articles():
    # connect to database news
    db, c = connect(DBNAME)
    # send sql cmd
    c.execute("select title, views_num from total_views order by views_num desc limit 3")  # NOQA
    rows = c.fetchall()
    # close database connection
    db.close()
    print("What are the most popular three articles of all time?")
    for articles, views in rows:
        print(str(articles) + "--" + str(views) + " views")
    return rows

# Rank arthors by views of their articles
def list_most_pop_authors():
    db, c = connect(DBNAME)
    c.execute("select name, sum(views_num) as author_total from rank_author group by rank_author.name order by author_total desc")  # NOQA
    rows = c.fetchall()
    db.close()
    print("Who are the most popular article authors of all time?")
    for author, views in rows:
        print(str(author) + "--" + str(views) + " views")
    return rows

# list the days that has more than 1% of https request errors
def list_http_errors():
    db, c = connect(DBNAME)
    c.execute("select * from result_table where result > 0.01")
    rows = c.fetchall()
    db.close()
    print("On which days did more than 1% of requests lead to errors?")
    for date, error in rows:
        print(str(date) + "--" + '{:.1f}'.format(error * 100) + '% errors')
    return rows

if __name__ == '__main__':
    list_most_pop_articles()
    list_most_pop_authors()
    list_http_errors()

