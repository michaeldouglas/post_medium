from logging import Filter
from library.request_context import request_id_ctx


class RequestIdFilter(Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get()
        return True
