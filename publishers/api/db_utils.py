import hashlib
import os
from django.db import connection
from users.api.file_handler import process_and_upload_book, process_and_upload_book_cover_image
from users.api.file_handler import process_and_upload_publications_image

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()


def info_list_dict(query, user_id):
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        results = cursor.fetchall()
        data = [dict(zip([col[0] for col in cursor.description], row)) for row in results]

    return data


def info_dict(query, user_id):
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        result = cursor.fetchone()
        return dict(zip([col[0] for col in cursor.description], result))


class AccountManagementDBUtils:

    @classmethod
    def get_total_successful_amount(cls, user_id):
        query = """
                SELECT
                    SUM(CASE WHEN ActionTypeId = 1 THEN Amount ELSE 0 END) AS total_deposit,
                    SUM(CASE WHEN ActionTypeId = 2 THEN Amount ELSE 0 END) AS total_withdraw
                FROM public.WalletActions
                WHERE UserId = %s AND IsSuccessful = TRUE;
            """

        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            result = cursor.fetchone()

            total_deposit = result[0] if result and result[0] is not None else 0.0
            total_withdraw = result[1] if result and result[1] is not None else 0.0

        total_amount = total_deposit - total_withdraw

        return total_amount

    @classmethod
    def create_book(cls, user_id, data):

        book_cover_image = process_and_upload_book_cover_image(data['book_cover_image'])
        book_demo_file = process_and_upload_book(data['book_demo_file'])
        book_original_file = process_and_upload_book(data['book_original_file'])

        query = """
            INSERT INTO Books 
                    (BookName, AuthorName, TranslatorName, ReleasedDate, 
                       BookCoverImage, Price, Description, NumberOfPages, LanguageId,
                       UserId, IsDelete, CreatedDateTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE, NOW() + INTERVAL '3 hours 30 minutes') RETURNING Id
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [
                    data['book_name'], data['author_name'], data['translator_name'],
                    data['released_date'], book_cover_image, data['price'],
                    data['description'], data['number_of_pages'], data['language_id'],
                    user_id
                ])
            new_book_id = cursor.fetchone()[0]

            query = """
                INSERT INTO BookCategories (CategoryId, BookId, IsDelete) VALUES (%s, %s, FALSE)
            """

            cursor.execute(query, [data["category_id"], new_book_id])

            query = """
                INSERT INTO BookFiles (BookDemoFile, BookOriginalFile, BookId) VALUES (%s, %s, %s)
            """

            cursor.execute(query, [book_demo_file, book_original_file, new_book_id])

            description = f' ایجاد کتاب{data["book_name"]}'

            query = """
                INSERT INTO WalletActions (ActionTypeId, UserId, Amount, IsSuccessful, Description, CreatedDate)
                VALUES (2, %s, 5000, TRUE, %s, NOW() + INTERVAL '3 hours 30 minutes')
            """

            cursor.execute(query, [user_id, description])


    @classmethod
    def delete_publisher_book(cls, user_id, book_id):
        query = """
            UPDATE public.Books 
                SET IsDelete = TRUE
            WHERE (id = %s AND userid = %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [book_id, user_id])

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
    def get_publisher_info(cls, user_id):
        query = """
                SELECT Username, Email, PhoneNumber, PhoneNumber2, 
                Address, IdentityImage, CardNumber, PublicationsName, PublicationsImage FROM public.Users
                WHERE (id = %s)
                """
        return info_dict(query, user_id)


    @classmethod
    def get_books_with_sales_info(cls, user_id):
        query = """
            SELECT
                b.id,
                b.bookname,
                b.authorname,
                b.translatorname,
                b.releaseddate,
                b.bookcoverimage,
                b.price,
                b.numberofpages,
                l.name as language,
                COALESCE(ub.count_of_sold, 0) as count_of_sold,
                COALESCE(ub.income, 0) as income
            FROM books b
            JOIN users u ON b.userid = u.id
            LEFT JOIN languages l ON b.languageid = l.id
            LEFT JOIN (
                SELECT
                    bookid,
                    COUNT(*) as count_of_sold,
                    SUM(b.price) as income
                FROM userbooks ub
                JOIN books b ON ub.bookid = b.id
                GROUP BY bookid
            ) ub ON b.id = ub.bookid
            WHERE u.id = %s AND b.isdelete = FALSE;
        """

        return info_list_dict(query, user_id)

    @classmethod
    def get_publisher_wallet_history(cls, user_id):
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
        return info_list_dict(query, user_id)


    @classmethod
    def get_publisher_wallet_balance(cls, user_id):
        query = """
            SELECT
                SUM(CASE WHEN ActionTypeId = 1 THEN Amount ELSE 0 END) AS deposit,
                SUM(CASE WHEN ActionTypeId = 2 THEN Amount ELSE 0 END) AS withdraw
            FROM public.WalletActions
            WHERE UserId = %s AND IsSuccessful = TRUE;
                """
        return info_dict(query, user_id)


    @classmethod
    def update_publisher_profile(cls, address, phone_number2, publications_image, card_number, user_id):
        # Initialize the SET clause and parameters list
        set_clause = []
        params = []

        # Check each value and add it to the SET clause if not empty
        if address:
            set_clause.append("Address = %s")
            params.append(address)

        if phone_number2:
            set_clause.append("PhoneNumber2 = %s")
            params.append(phone_number2)

        if publications_image:
            response_publications_image = process_and_upload_publications_image(publications_image)
            set_clause.append("PublicationsImage = %s")
            params.append(response_publications_image)

        if card_number:
            set_clause.append("CardNumber = %s")
            params.append(card_number)

        if set_clause:
            # Combine the SET clauses into a single string
            set_clause_str = ", ".join(set_clause)

            # Build the full query
            query = f"""
                        UPDATE public.Users
                        SET {set_clause_str}
                        WHERE Id = %s
                    """

            # Add the user_id parameter
            params.append(user_id)

            with connection.cursor() as cursor:
                cursor.execute(query, params)


