import ollama
import re
import sys

from generation.gemini import Gemini
from generation.ollama import Ollama

class TweetGenerator:

    thread_limit = 5

    def __init__(self, model='gemini-pro', model_type='gemini'):
        self.model = model
        self.model_type = model_type

    def generate_tweets(self, prompt, iteration=1):
        text = self.generate_response(prompt)
        tweets = self.create_tweet_array(text)
        if len(tweets) > self.thread_limit:
            if iteration > 5:
                raise Exception("Error: Response is too long")
            new_prompt = f"""Make this body of text shorter:
                             {text}
                          """
            return self.generate_tweets(new_prompt, iteration=iteration + 1)
        return tweets

    def generate_response(self, prompt):
        if self.model_type == 'ollama':
            ollama_model = Ollama(model=self.model)
            return ollama_model.ollama_generate(prompt=prompt)
        
        elif self.model_type == 'gemini':
            gemini_model = Gemini(model_name=self.model)
            return gemini_model.gemini_generate(prompt)
        
        else:
            raise Exception("The model specified is not supported.")


    def create_tweet_array(self, text):
        max_length = 140
        words = re.split(r"\s|\n", text)
        tweets = [""]
        index = 0
        for word in words:
            if len(tweets[index]) + len(word) < max_length:
                tweets[index] += f" {word}"
            else:
                index += 1
                tweets.append(word)
        tweets[0] = tweets[0].strip()
        return tweets
