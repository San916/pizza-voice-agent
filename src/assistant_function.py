from livekit.agents import llm
from datetime import datetime
from logger_config import logger

# Extention of FunctionContext class
# Functions here will allow models to obtain additional context, such as the current time
class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        logger.debug("Initializing AssistantFnc class")
        super().__init__()

    @llm.ai_callable(description = "This function returns the current time. This can be used to help answer user questions.")
    async def get_time(self):
        current_time = datetime.now().strftime("%m-%d-%Y %T:%M%p")
        logger.debug("get_time() called. Returning " + current_time)
        return current_time