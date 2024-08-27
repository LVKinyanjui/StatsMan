from litellm import completion

from typing import Protocol, Optional, List, Union, Dict

# PROTOCOL CLASS
# Defines an OpenAI response interface
class ModelClientResponseProtocol(Protocol):
    class Choice(Protocol):
        class Message(Protocol):
            content: Optional[str]

        message: Message

    choices: List[Choice]
    model: str

# MODEL CLASS
class CustomModelClient:
    """
    A client class must implement the following methods:
    - create must return a response object that implements the ModelClientResponseProtocol
    - cost must return the cost of the response
    - get_usage must return a dict with the following keys:
        - prompt_tokens
        - completion_tokens
        - total_tokens
        - cost
        - model

    This class is used to create a client that can be used by OpenAIWrapper.
    The response returned from create must adhere to the ModelClientResponseProtocol but can be extended however needed.
    The message_retrieval method must be implemented to return a list of str or a list of messages from the response.
    """
    def __init__(self, config) -> None:
        self.model = config.get("model", "gemini/gemini-pro") 

    def create(self, params) -> ModelClientResponseProtocol:
        ## Get messages from agents
                
        response = completion(
            model=self.model, 
            messages=params["messages"]
        )
        
        return response

    def message_retrieval(
        self, response: ModelClientResponseProtocol
    ) -> Union[List[str], List[ModelClientResponseProtocol.Choice.Message]]:
        """
        Retrieve and return a list of strings or a list of Choice.Message from the response.

        NOTE: if a list of Choice.Message is returned, it currently needs to contain the fields of OpenAI's ChatCompletion Message object,
        since that is expected for function or tool calling in the rest of the codebase at the moment, unless a custom agent is being used.
        """
        choices = response.choices
        return [choice.message.content for choice in choices]

    def cost(self, response: ModelClientResponseProtocol) -> float:
        return 0

    @staticmethod
    def get_usage(response: ModelClientResponseProtocol) -> Dict:
        """Return usage summary of the response using RESPONSE_USAGE_KEYS."""
        return dict(response.usage)
