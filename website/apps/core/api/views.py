from django.http import JsonResponse


def health(request) -> JsonResponse:
    return JsonResponse({"status": "ok"})
