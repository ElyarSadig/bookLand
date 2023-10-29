from django.http import JsonResponse
from django.db import connection


def ping(request):
    return JsonResponse({"status": "App is running and fully functional!"})


def users(request):
    # Perform the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.Users")
        # Fetch all rows from the result
        results = cursor.fetchall()

    # Convert the results to a list of dictionaries
    # Each dictionary represents a row in the result set
    rows = [dict(zip([col[0] for col in cursor.description], row)) for row in results]

    # Return the result as JSON
    return JsonResponse({'data': rows}, safe=False)
