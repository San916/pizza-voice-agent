from livekit.agents import llm, cli, JobContext, AutoSubscribe, WorkerOptions
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, deepgram
import classification
import assistant_function
from logger_config import logger

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create the vector store containg the information found in company_data.json
import data_handling
data = data_handling.load_data("src/company_data.json")
documents = data_handling.generate_documents(data)
vector_store = data_handling.create_vector_store(documents)

# This function will be called to create a session with the user
async def entrypoint(ctx : JobContext):
    logger.debug("entrypoint() called.")

    # Initial chat context. Will expand as conversation progresses
    chat_ctx = llm.ChatContext().append(
        role = "system",
        text = ("You are a voice agent for Zazzou Pizza Center, a pizza delivery business."
                "You are designed to help users order pizzas and to obtain information about the company"
                "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
                "Avoid responding to general inquiries and focus on providing answers only for relevant queries."
                "If the query is too vague, ask clarifying questions instead of providing a general response."))

    # Interface will be through audio only, no video
    logger.debug("Connecting to the room.")
    await ctx.connect(auto_subscribe = AutoSubscribe.AUDIO_ONLY)

    # Additional functions to be used by the model will be accessed through fnc_ctx
    fnc_ctx = assistant_function.AssistantFnc()

    # Callback function used after STT, but before LLM
    #  Classify user's query and retrieve relevant documents if needed to respond
    async def handle_context(assistant: VoiceAssistant, chat_ctx: llm.ChatContext):
        logger.debug("handle_context() called.")

        # The last message sent is the user's query
        transcribed_text = chat_ctx.messages[-1].content
        intent = classification.classify_intent(transcribed_text)
        logger.debug("Transtribed text: " + transcribed_text)
        logger.debug("Intent: " + intent)
        if intent == "General Query":
            chat_ctx.append(role = "system", 
                            text = ("You are responding to a general query. Respond politely."
                                    "If the query is not relevant to the conversation or to your goals of helping users order pizza, you can say that you can't answer the question"))
        elif intent == "Intent to Leave":
            chat_ctx.append(role = "system", 
                            text = "The user wishes to leave. Create a final response for the user.")
        else:
            retrieved_info = data_handling.query_vector_store(transcribed_text, vector_store)
            chat_ctx.append(role = "system",
                            text = f"Use the following information to help respond to the user's query: {retrieved_info}")

    # Initialize the voice agent pipeline
    logger.debug("Initializing Voice Agent Pipeline.")
    voiceAgent = VoiceAssistant(
        vad = silero.VAD.load(),
        stt = deepgram.STT(model = "nova-2-general"),
        llm = openai.LLM(),
        tts = openai.TTS(),
        chat_ctx = chat_ctx,
        fnc_ctx = fnc_ctx,
        allow_interruptions = True,
        before_llm_cb = handle_context)

    # Begin the chatting with an initial message
    logger.debug("Starting chat room.")
    voiceAgent.start(ctx.room)

    await voiceAgent.say("Hello, I am a voice agent for Zazzou Pizza Center! How can I assist you today?")

if __name__ == "__main__":
    logger.debug("Running App.")
    cli.run_app(WorkerOptions(entrypoint_fnc = entrypoint))