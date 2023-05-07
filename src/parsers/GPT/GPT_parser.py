from typing import Dict


class GPTParser:
    """
    Class to parse GPT-4 response
    """

    def __init__(self, response: Dict):
        self.__response = response

    def parse_text_from_response(self) -> str:
        """
        Extract text from GPT-4 response
        :return: text of response
        """
        choices = self.__response.get("choices")
        return choices[0].get("text")
