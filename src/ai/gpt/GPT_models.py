from typing import Dict

import openai

from helpers.project_envs import ProjectEnvs


class GPTModels:
    """
    Class to work with GPT-4
    """

    def __init__(self):
        openai.api_key = ProjectEnvs.GPT_API_KEY

    @staticmethod
    def qa_model(income_question: str) -> Dict:
        """
        QA model from GPT-4
        :param income_question: question to ask GPT
        :return: response from GPT
        """
        response = openai.Completion.create(
            model=ProjectEnvs.GPT_API_BASE_MODEL,
            prompt=income_question,
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response

    @staticmethod
    def key_words_model(income_text: str) -> Dict:
        """
        Sentence to get keywords by GPT-4
        :param income_text: sentence to extract data
        :return: response from GPT
        """
        response = openai.Completion.create(
            model=ProjectEnvs.GPT_API_BASE_MODEL,
            prompt=f"Extract keywords from this text:\n\n{income_text}",
            temperature=0.5,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0.8,
            presence_penalty=0,
        )
        return response


gpt_models = GPTModels()
