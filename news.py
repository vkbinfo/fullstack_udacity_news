import psycopg2


def get_most_popular_three_article():
    query = "select articles.title, result.num from (select replace(path,'/article/', '') as path_slug , count(*) " \
            "as num from log group by path having path like '/article/%')as result,articles " \
            "where result.path_slug = articles.slug order by result.num desc limit 3;"
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    print("Title______________________Views")
    for x in data:
        print(x[0] + '      ' + str(x[1]))


def get_most_popular_authors():
    query = "select authors.name, sum(result.num)as total_views from (select replace(path,'/article/', '')" \
            " as path_slug, count(*) as num from log group by path having path like '/article/%')as result," \
            " articles, authors where result.path_slug = articles.slug and articles.author=authors.id " \
            "group by authors.name order by total_views desc;"
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    print("Author______________________Total_Views")
    for x in data:
        print(x[0] + '      ' + str(x[1]))


def get_error_rate_of_day():
    query = "select error.dateofday::timestamp::date as tata, (sum(error.total_error)/sum( total.total_request))as " \
            "error_rate from (select time::timestamp::date  as dateofday, count(*) as total_error from log " \
            "where log.status like '5%' or log.status like '4%' group by dateofday) as error," \
            "(select time::timestamp::date as dateofday, count(*) as total_request from log group by dateofday)as total" \
            " where error.dateofday=total.dateofday group by tata ;"
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    print("Date______Error_rate")
    for x in data:
        error_percentage = round(x[1], 3) * 100
        if error_percentage > 1:
            print(str(x[0]) + '      ' + str("%.2f" % error_percentage) + '%')


get_most_popular_three_article()
get_most_popular_authors()
get_error_rate_of_day()
