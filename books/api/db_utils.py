from django.db import connection


def info_dict(query, list_of_args):
    with connection.cursor() as cursor:
        cursor.execute(query, list_of_args)
        results = cursor.fetchall()
        data = [dict(zip([col[0] for col in cursor.description], row)) for row in results]

    return data


class BookManagementDBUtils:

    @classmethod
    def get_book_detail(cls, book_id):
        query = """
                SELECT
                    b.id as book_id,
                    b.bookname,
                    u.publicationsname as publisher,
                    b.authorname,
                    b.translatorname,
                    b.releaseddate,
                    b.bookcoverimage,
                    b.price,
                    b.description,
                    b.numberofpages,
                    l.name as language,
                    ROUND(COALESCE(AVG(r.review_average), 0), 1) as reviewaverage,
                    COALESCE(r.reviewcount, 0) as reviewcount,
                    bf.bookdemofile
                FROM books b
                LEFT JOIN users u ON u.id = b.userid
                LEFT JOIN languages l ON b.languageid = l.id
                LEFT JOIN bookfiles bf ON b.id = bf.bookid
                LEFT JOIN (
                    SELECT
                        bookid,
                        AVG(rating) as review_average,
                        COUNT(*) as reviewcount
                    FROM reviews
                    GROUP BY bookid
                ) r ON b.id = r.bookid
                WHERE b.id = %s
                GROUP BY
                    b.id,
                    u.publicationsname,
                    l.name,
                    bf.bookdemofile,
                    r.review_average,
                    r.reviewcount;
                """
        return info_dict(query=query, list_of_args=[book_id])
