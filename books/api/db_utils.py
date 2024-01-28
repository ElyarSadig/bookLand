from django.db import connection


def info_dict(query, list_of_args):
    with connection.cursor() as cursor:
        cursor.execute(query, list_of_args)
        results = cursor.fetchall()
        data = [dict(zip([col[0] for col in cursor.description], row)) for row in results]

    return data


class BookManagementDBUtils:

    @classmethod
    def get_all_languages(cls):
        query = """
            SELECT * FROM Languages
        """
        return info_dict(query, [])

    @classmethod
    def get_all_categories(cls):
        query = """
            SELECT * FROM Categories        
        """
        return info_dict(query, [])

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
                    c.name as category,
                    l.name as language,
                    bf.bookdemofile
                FROM books b
                INNER JOIN users u ON u.id = b.userid
                INNER JOIN languages l ON b.languageid = l.id
                INNER JOIN bookfiles bf ON b.id = bf.bookid
                INNER JOIN bookcategories bc ON b.id = bc.bookid
                INNER JOIN categories c ON c.id = bc.categoryid
                WHERE b.id = %s AND b.isdelete = FALSE
                """
        return info_dict(query=query, list_of_args=[book_id])

    @classmethod
    def get_book_review_counts(cls, book_id):
        query = """
            SELECT
                ROUND(COALESCE(AVG(r.rating), 0), 1) as reviewaverage,
                COALESCE(COUNT(r.rating), 0) as reviewcount
            FROM books b
            INNER JOIN (
                SELECT
                    bookid,
                    rating
                FROM reviews
            ) r ON b.id = r.bookid
            WHERE b.id = %s
            GROUP BY
                b.id;
        """
        return info_dict(query=query, list_of_args=[book_id])


    @classmethod
    def get_book_categories(cls, book_id):
        query = """
            SELECT
                c.name as category_name
            FROM books b
            INNER JOIN bookcategories bc ON b.id = bc.bookid
            INNER JOIN categories c ON bc.categoryid = c.id
            WHERE b.id = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [book_id])
            results = cursor.fetchall()
            return results

    @classmethod
    def has_user_bought_book(cls, user_id, book_id):
        query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM public.UserBooks
                    WHERE UserId = %s AND BookId = %s
                ) AS has_bought
            """

        with connection.cursor() as cursor:
            cursor.execute(query, [user_id, book_id])
            result = cursor.fetchone()
            return result[0]

    @classmethod
    def get_original_book_filepath(cls, book_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT BookOriginalFile FROM BookFiles WHERE BookId = %s;", [book_id])
            result = cursor.fetchone()

            return result[0]

