
##Instruction to Run File
    Get vagrant Up and running.
    set up the database with the help of newsdata.sql
    run the file with following command
        python news.py


#The Design process of queries

###The First Query:- get_most_popular_three_article
>    select articles.title, result.num from (select replace(path,'/article/', '')
>    as path_slug ,count(*)
>    as num from log group by path having path like '/article/%')as result,articles
>    where result.path_slug = articles.slug order by result.num desc limit 3;

     In this query first I am running the subquery in from part where I am getting
     all the post which had been viewed. The replace method is just triming the /article/
     part of path so we can match with slug part. We get this table as result, and We
     are joining with articles on our path_slug from log and slug from articles. and now we have all
     the things that need for this query to run. I have grouped the query in inner form query.

###The Second Query:- get_most_popular_authors
>    select authors.name, sum(result.num)as total_views from (select replace(path,'/article/', '')
>    as path_slug, count(*) as num from log group by path having path like '/article/%')as result,
>    articles, authors where result.path_slug = articles.slug and articles.author=authors.id 
>    group by authors.name order by total_views desc;

    In this above Sql query we are donging same thing as we above did for first table we are using inner query
    to get a table called result. and we are joining it with articles and author. and applying necessary conditions
    that we don't get unnecessary rows. 
    
###The Thrid Query:- get_error_rate_of_day:
>    select error.dateofday::timestamp::date as tata, (sum(error.total_error)/sum( total.total_request))as 
>    error_rate from (select time::timestamp::date  as dateofday, count(*) as total_error from log 
>    where log.status like '5%' or log.status like '4%' group by dateofday) as error,
>    (select time::timestamp::date as dateofday, count(*) as total_request from log group by dateofday)as total
>    where error.dateofday=total.dateofday group by tata ;    

    In the above query we are first getting the error message rows from logs and after that we are joining with 
    them according to date with a table which is dervied from same table but it counts total request each day.
    Now we have each day's error request and total requests. We have divided by the total request. So now we have 
    error percentage. We can easily print out with the help of python round function.
    