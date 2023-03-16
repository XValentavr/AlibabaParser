from parsers.GPT.GPT_parser import GPTParser


class GPT:
    @staticmethod
    def __init_parser(response):
        """
        creates parser to get need data from response
        :param response: income result
        :return: extracted data from income
        """
        gpt_parser = GPTParser(response)
        return gpt_parser

