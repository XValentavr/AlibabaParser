class GPTParser:
    def __init__(self, response: dict):
        self.__response = response

    def parse_text_from_response(self):
        print(self.__response)
