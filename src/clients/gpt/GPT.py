import re
from typing import List
from uuid import UUID

from ai.gpt.GPT_models import gpt_models
from cruds.product_keywords_cruds import ProductKeywordsCRUDS
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
        response = self.__gpt.key_words_model(income_text=text_to_extract)

        keywords = self.__init_parser(response).parse_text_from_response()
        keywords_list = self.__keywords_str_to_list(keywords)

        self.__keywords_cruds.insert_keywords(list_of_keywords=keywords_list, alibaba_id=product_id)

    def get_keywords_similarity(self, keywords_amazon: List, keywords_alibaba: List) -> str:

        keywords_amazon_str = ', '.join(str(keyword) for keyword in keywords_amazon)
        keywords_alibaba_str = ', '.join(str(keyword) for keyword in keywords_alibaba)

        response = self.__gpt.key_text_similarity(income_text_alibaba=keywords_alibaba_str,
                                                  income_text_amazon=keywords_amazon_str)
        is_text_similar = self.__init_parser(response).parse_text_from_response()
        return is_text_similar

    @staticmethod
    def __keywords_str_to_list(keywords: str) -> List[str]:
        changed_string_from_gpt = re.sub(r"[^a-zA-Z0-9 \n\.]", "", keywords).strip()
        pre_keywords = changed_string_from_gpt.split('\n')

        return [item.strip() for item in pre_keywords]
