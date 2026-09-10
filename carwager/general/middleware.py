import time
import uuid

from django.http import HttpRequest, HttpResponse

from general.logging_context import request_id_var


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        request_id = request.headers.get("X-Request-ID")

        if not request_id:
            request_id = str(uuid.uuid4())

        token = request_id_var.set(request_id)
        request.request_id = request_id

        try:
            start_time = time.perf_counter()

            response = self.get_response(request)

            duration = time.perf_counter() - start_time

            response["X-Request-ID"] = request_id
            response["duration"] = duration
            return response

        finally:
            request_id_var.reset(token)
