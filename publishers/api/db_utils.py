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
                WHERE b.isdelete = FALSE
                GROUP BY bookid
            ) ub ON b.id = ub.bookid
            WHERE u.id = %s;
        """

        return info_dict(query, user_id)

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
        return info_dict(query, user_id)


    @classmethod
    def get_publisher_wallet_balance(cls, user_id):
        query = """
            SELECT
                SUM(CASE WHEN ActionTypeId = 1 THEN Amount ELSE 0 END) AS deposit,
                SUM(CASE WHEN ActionTypeId = 2 THEN Amount ELSE 0 END) AS withdraw
            FROM public.WalletActions
            WHERE UserId = %s AND IsSuccessful = TRUE;
                """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            results = cursor.fetchone()
            data = {
                "deposit": results[0],
                "withdraw": results[1]
            }
            return data


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
            set_clause.append("PublicationsImage = %s")
            params.append(publications_image)

        if card_number:
            set_clause.append("CardNumber = %s")
            params.append(card_number)

        # Check if there's anything to update
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


