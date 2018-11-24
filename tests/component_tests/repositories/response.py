class ReponseRepository:
    def __init__(self):
        self._responses = {}

    def get_response(self, response_id):
        if response_id in self._responses:
            return self._responses[response_id]
