import hashlib
from django.db import connection


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def info_dict(query, user_id):
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        results = cursor.fetchall()
        data = [dict(zip([col[0] for col in cursor.description], row)) for row in results]
    connection.close()
    return data


class AccountManagementDBUtils:

    @classmethod
    def get_user_stored_password(cls, user_id):
        query = """
                            SELECT HashedPassword FROM public.Users
                            WHERE (id = %s)
                            """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            stored_password = cursor.fetchone()[0]
        connection.close()
        return stored_password

    @classmethod
    def update_password(cls, new_password, user_id):
        hashed_newpassword = hash_password(new_password)
        query = """
                            UPDATE public.Users 
                            SET HashedPassword = %s
                            WHERE (id = %s)
                            """
        with connection.cursor() as cursor:
            cursor.execute(query, [hashed_newpassword, user_id])
        connection.close()

    @classmethod
    def get_username_email(cls, user_id):
        query = """
                            SELECT Username, Email FROM public.Users
                            WHERE (id = %s)
                                    """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            username, email = cursor.fetchone()
        connection.close()
        return username, email

    @classmethod
    def get_user_bookmarks(cls, user_id):
        query = """
                            SELECT public.Books.*, UserBookMarks.IsDelete AS bookmark_isdelete 
                            FROM public.users 
                            JOIN public.userbookmarks ON users.id = userbookmarks.userid
                            JOIN public.books on userbookmarks.bookid = books.id
                            WHERE users.id = %s
                                            """
        return info_dict(query=query, user_id=user_id)

    @classmethod
    def get_user_books(cls, user_id):
        query = """
                            SELECT books.* 
                            FROM books 
                            JOIN userbooks ON books.id = userbooks.bookid
                            WHERE userbooks.userid = %s
                                                    """
        return info_dict(query=query, user_id=user_id)

    @classmethod
    def update_user_bookmark(cls, user_id, bookmark_id):
        try:
            query = """
                        Update public.UserBookMarks 
                        SET IsDelete = TRUE
                        WHERE UserId = %s AND Id = %s
                                                    """
            with connection.cursor() as cursor:
                cursor.execute(query, [user_id, bookmark_id])

        except Exception:
            raise Exception

    @classmethod
    def get_user_wallet_history(cls, self, user_id, request):
        query = """
                            SELECT * 
                            FROM walletactions 
                            WHERE userid = %s
                                                            """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            results = cursor.fetchall()

            paginator = self.pagination_class()
            paginated_results = paginator.paginate_queryset(results, request)
        connection.close()
        return [dict(zip([col[0] for col in cursor.description], row)) for row in paginated_results]
