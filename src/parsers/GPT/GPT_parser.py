class GPTParser:
    def __init__(self, response: dict):
        self.__response = response

    def parse_text_from_response(self) -> str:
        choices = self.__response.get('choices')
        return choices[0].get('text')
