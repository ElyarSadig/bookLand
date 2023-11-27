import hashlib
import os

from django.db import connection


def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()


def info_dict(query, user_id):
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        results = cursor.fetchall()
        data = [dict(zip([col[0] for col in cursor.description], row)) for row in results]

    return data


class AccountManagementDBUtils:

    @classmethod
    def get_user_stored_password_and_salt(cls, user_id):
        query = """
                SELECT HashedPassword, Salt FROM public.Users
                WHERE (id = %s)
                """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            stored_password, salt = cursor.fetchone()

        return stored_password, salt

    @classmethod
    def update_password(cls, new_password, user_id):
        salt = os.urandom(32).hex()
        hashed_newpassword = hash_password(new_password, salt)
        query = """
                UPDATE public.Users 
                SET HashedPassword = %s,
                    Salt = %s
                WHERE (id = %s)
                """
        with connection.cursor() as cursor:
            cursor.execute(query, [hashed_newpassword, salt, user_id])

    @classmethod
    def get_username_email(cls, user_id):
        query = """
                SELECT Username, Email FROM public.Users
                WHERE (id = %s)
                """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            username, email = cursor.fetchone()

        return username, email

    @classmethod
    def get_user_bookmarks(cls, user_id):
        query = """
                    SELECT
                        userbookmarks.id as bookmarkid, 
                        books.id as bookid,
                        users.publicationsname as publisher,
                        books.bookname,
                        books.authorname,
                        books.translatorname,
                        books.releaseddate,
                        books.bookcoverimage,
                        books.price,
                        books.description,
                        books.numberofpages,
                        languages.name as language
                    FROM userbookmarks
                    JOIN books ON userbookmarks.bookid = books.id
                    JOIN users ON books.userid = users.id
                    JOIN languages ON books.languageid = languages.id
                    WHERE userbookmarks.userid = %s AND userbookmarks.isdelete = false;
                """
        return info_dict(query=query, user_id=user_id)

    @classmethod
    def get_user_books(cls, user_id):
        query = """
                SELECT 
                    books.id as bookid,
                    users.publicationsname as publisher,
                    books.bookname,
                    books.authorname,
                    books.translatorname,
                    books.releaseddate,
                    books.bookcoverimage,
                    books.price,
                    books.description,
                    books.numberofpages,
                    languages.name as language
                FROM books
                JOIN userbooks ON books.id = userbooks.bookid
                JOIN users ON books.userid = users.id
                JOIN languages ON books.languageid = languages.id
                WHERE userbooks.userid = %s AND books.isdelete = false;
                """
        return info_dict(query=query, user_id=user_id)

    @classmethod
    def update_user_bookmark(cls, user_id, bookmark_id):
        query = """
                Update public.UserBookMarks 
                SET IsDelete = TRUE
                WHERE UserId = %s AND Id = %s
                """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id, bookmark_id])

    @classmethod
    def get_total_successful_amount(cls, user_id):
        query = """
            SELECT SUM(Amount) AS total_amount
            FROM public.WalletActions
            WHERE UserId = %s AND IsSuccessful = TRUE;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            result = cursor.fetchone()

        total_amount = result[0] if result and result[0] is not None else 0.0

        return total_amount

    @classmethod
    def get_user_wallet_history(cls, self, user_id, request):
        query = """
                SELECT
                     walletactions.id,
                     walletactiontypes.actiontype as actiontype,
                     walletactions.amount,
                     walletactions.issuccessful,
                     walletactions.description,
                     walletactions.createddate
                FROM walletactions 
                JOIN walletactiontypes ON walletactiontypes.id = walletactions.actiontypeid
                WHERE userid = %s AND walletactions.issuccessful = TRUE
                """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            results = cursor.fetchall()

            paginator = self.pagination_class()
            paginated_results = paginator.paginate_queryset(results, request)

            total_pages = paginator.page.paginator.num_pages

            current_page = paginator.page.number

            data = {
                "page_size": 9,
                "page_index": current_page,
                "count": total_pages,
                "data": [dict(zip([col[0] for col in cursor.description], row)) for row in paginated_results]
            }

        return data
