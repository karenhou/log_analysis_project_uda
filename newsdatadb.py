# Database code for the DB news.

import psycopg2

DBNAME = "news"

# list top 3 most viewed articles
def list_most_pop_articles():
    # connect to database news
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # send sql cmd
    c.execute("select title, views_num from total_views order by views_num desc limit 3")  # NOQA
    rows = c.fetchall()
    print("What are the most popular three articles of all time?")
    for articles, views in rows:
        print(str(articles) + "--" + str(views) + " views")
    return rows
    # close database connection
    db.close()

# Rank arthors by views of their articles
def list_most_pop_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select name, sum(views_num) as author_total from rank_author group by rank_author.name order by author_total desc")  # NOQA
    rows = c.fetchall()
    print("Who are the most popular article authors of all time?")
    for author, views in rows:
        print(str(author) + "--" + str(views) + " views")
    return rows
    db.close()

# list the days that has more than 1% of https request errors
def list_http_errors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from result_table where result > 0.01")
    rows = c.fetchall()
    print("On which days did more than 1% of requests lead to errors?")
    for date, error in rows:
        print(str(date) + "--" + '{:.1f}'.format(error * 100) + '% errors')
    return rows
    db.close()
