# News database analysis project
This is the log analysis project for udacity nano full stack web courses that analysis database news base on following three questions.
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirement
Please setup an environment with Python, PostgreSQL and psycopg2 installed

## Download database
Download the database news [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) which contain a file `newsdata.sql`

Install database with this command  `psql -d news -f newsdata.sql`


## Install
In order to run the newsdatadb.py smoothly. You should first create following views:

**total_views**
```
create view total_views as 
select path, count(path) as views_num, articles.slug, articles.title, articles.author 
from log left join articles 
on path ='/article/'||slug
where path !='/'
and status = '200 OK'
and path not like '%spam%' 
and path not like '%20%' 
and path not like '%ATH%' 
group by path, slug, title, author 
order by views_num desc;
```
**rank_author**
```
create view rank_author as 
select views_num, author, name 
from total_views, authors 
where author = id 
order by author desc;
```
**total_connection**
```
create view total_connection as
select time::timestamp::date as date, count(time) as total_connt
from log
group by date
order by date;
```
**bad_connection**
```
create view bad_connection as
select time::timestamp::date as date, count(time) as bad_connt_num
from log
where status = '404 NOT FOUND'
group by date
order by date;
```
**comparing_table**
```
create view comparing_table as
select bad_connection.date, bad_connt_num, total_connt from bad_connection, total_connection where bad_connection.date = total_connection.date;
```
**result_table**
```
create view result_table as
select a.date, round(a.bad_connt_num::NUMERIC/a.total_connt::NUMERIC,3) as result from comparing_table as a;
```

## Usage
There are three functions defined you can call to answer the following questions.
1. What are the most popular three articles of all time? 
```python
list_most_pop_articles()
```
2. Who are the most popular article authors of all time?
```python
list_most_pop_authors()
```
3. On which days did more than 1% of requests lead to errors?
```python
list_http_errors()
```

## Output
Open up result.txt shuold give you an idea of what above function calls return