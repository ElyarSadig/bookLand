from django.http import JsonResponse


def ping(request):
    return JsonResponse({"status": "App is running and fully functional!"})


