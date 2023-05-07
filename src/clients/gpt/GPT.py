from typing import List
from uuid import UUID

from ai.gpt.GPT_models import gpt_models
from cruds.product_keywords_cruds import ProductKeywordsCRUDS
from helpers.validators.remove_special_symbols import remove_special_symbols
from parsers.GPT.GPT_parser import GPTParser


class GPTClient:
    def __init__(self):
        self.__gpt = gpt_models
        self.__keywords_cruds = ProductKeywordsCRUDS()

    @staticmethod
    def __init_parser(response) -> GPTParser:
        """
        creates parser to get need data from response
        :param response: income result
        :return: extracted data from income
        """
        gpt_parser = GPTParser(response)
        return gpt_parser

    def get_keywords(self, product_id: UUID, text_to_extract: str) -> None:
        # response = self.__gpt.key_words_model(income_text=text_to_extract)

        # keywords = self.__init_parser(text_to_extract).parse_text_from_response()
        keywords_list = self.__keywords_str_to_list(text_to_extract)

        self.__keywords_cruds.insert_keywords(
            list_of_keywords=keywords_list, alibaba_id=product_id
        )

    @staticmethod
    def __keywords_str_to_list(keywords: str) -> List[str]:
        """
        Create list of keywords
        :param keywords: keywords as sentence
        :return: list of keywords
        """
        changed_string_from_gpt = remove_special_symbols(keywords)
        pre_keywords = changed_string_from_gpt.split("\n")

        return [item.strip() for item in pre_keywords]
