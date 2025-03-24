import json
from django.http import JsonResponse

class CustomResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            data = json.loads(response.content.decode("utf-8"))
            formatted_response = {
                "success": response.status_code >= 200 and response.status_code < 400,
                "message": "Request processed successfully." if response.status_code < 400 else "Error occurred.",
                "data": data,
            }
            return JsonResponse(formatted_response, status=response.status_code)

        except Exception:
            return response
