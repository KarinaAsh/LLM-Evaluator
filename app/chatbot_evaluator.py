"""Chatbot Evaluator."""

import pandas as pd
from helpers import mistral

METRICS_TEXT = """Understanding User Queries, Providing Relevant Information, User Interaction and Engagement,
Personalization and Context Awareness, Overall Satisfaction"""


class MistralJudge:
    """
    A class to evaluate chatbot dialogues based on specified metrics.

    Attributes
    ----------
        metrics_text (str): The text defining the evaluation metrics.
        metrics_schema (dict): The JSON schema for the evaluation metrics.

    """

    def __init__(self, metrics_text=METRICS_TEXT):
        """
        Initialize the ChatbotEvaluator with the specified metrics text.

        Args:
        ----
            metrics_text (str): The text defining the evaluation metrics.

        """
        self.metrics_text = metrics_text
        self.metrics_schema = self.create_metrics_schema(metrics_text)

    def create_metrics_schema(self, metrics_text):
        """
        Create a JSON schema for the evaluation metrics.

        Args:
        ----
            metrics_text (str): The text defining the evaluation metrics.

        Returns:
        -------
            dict: The JSON schema for the evaluation metrics.

        """
        metrics = [metric.strip() for metric in metrics_text.split(',')]
        schema = {
            "type": "object",
            "properties": {"Comment": {"type": "str"}},
            "required": metrics
        }
        for metric in metrics:
            schema["properties"][metric] = {"type": "float"}
        return schema

    def generate_prompt(self, chat):
        """
        Generate the evaluation prompt for a given chat dialogue.

        Args:
        ----
            chat (str): The chat dialogue to be evaluated.

        Returns:
        -------
            str: The evaluation prompt.

        """
        return f"""
        You are a quality assurance specialist evaluating AI assistants.
        Your goal is to assess the user's level of satisfaction with the chat based on the following metrics:
        {self.metrics_text}. For each criterion among these criteria {self.metrics_text} please provide the score between 0 and 5 where 5 is the best score.
        Here is the chat:
        {chat}
        Return JSON format with the following JSON schema where the metric is one of the metrics in the {self.metrics_text} list:
        {self.metrics_schema}
        """

    def evaluate(self, combined_dialogues):
        """
        Evaluate the combined dialogues using the defined metrics.

        Args:
        ----
            combined_dialogues (pd.DataFrame): The DataFrame containing the dialogues to be evaluated.

        Returns:
        -------
            pd.DataFrame: The DataFrame containing the evaluation results.

        """
        results = []
        for i in range(1, 4):
            chat = combined_dialogues.iloc[i, 1]
            prompt = self.generate_prompt(chat)
            response = {'Dialogue': chat}
            response.update(eval(mistral(prompt, model='mistral-large-latest', is_json=True)))
            results.append(response)
        return pd.DataFrame(results)
