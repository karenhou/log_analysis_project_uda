#!/usr/bin/env python

# Database code for the DB news.

import psycopg2

DBNAME = "news"


def get_query_results(query, database_name=DBNAME):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        # connect to database
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        # pass in the query
        c.execute(query)
        rows = c.fetchall()
        db.close()
        # return the results of query
        return rows
    except psycopg2.Error as e:
        print "Unable to connect to database"
        raise e


def list_most_pop_articles():
    # list top 3 most viewed articles
    results = get_query_results(
        "select title, views_num from total_views "
        "order by views_num desc limit 3")
    print("What are the most popular three articles of all time?")
    for articles, views in results:
        print(str(articles) + "--" + str(views) + " views")


def list_most_pop_authors():
    # Rank arthors by views of their articles
    results = get_query_results(
        "select name, sum(views_num) as author_total from rank_author "
        "group by rank_author.name "
        "order by author_total desc")
    print("Who are the most popular article authors of all time?")
    for author, views in results:
        print(str(author) + "--" + str(views) + " views")


def list_http_errors():
    # list the days that has more than 1% of https request errors
    results = get_query_results(
        "select * from result_table where result > 0.01")
    print("On which days did more than 1% of requests lead to errors?")
    for date, error in results:
        print(str(date) + "--" + '{:.1f}'.format(error * 100) + '% errors')

if __name__ == '__main__':
    list_most_pop_articles()
    list_most_pop_authors()
    list_http_errors()
