from typing import Dict

import openai

from helpers.project_envs import ProjectEnvs


class GPTModels:

    def __init__(self):
        openai.api_key = ProjectEnvs.GPT_API_KEY

    @staticmethod
    def qa_model(income_question: str) -> Dict:
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
        response = openai.Completion.create(
            model=ProjectEnvs.GPT_API_BASE_MODEL,
            prompt=f"Extract keywords from this text:\n\n{income_text}",
            temperature=0.5,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0.8,
            presence_penalty=0
        )
        return response

    @staticmethod
    def key_text_similarity(income_text_alibaba: str, income_text_amazon: str) -> Dict:
        response = openai.Completion.create(
            model=ProjectEnvs.GPT_API_BASE_MODEL,
            prompt=f"Find the similar words from this sentences:\n\n1.{income_text_alibaba}\n\n2.{income_text_amazon}",
            temperature=0.5,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0.8,
            presence_penalty=0
        )
        return response


gpt_models = GPTModels()
