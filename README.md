Installation and Running
--------------------
- Install all requirements with `pip install -r requirements.txt`
- Create a new `.env` file to store your OpenAI and Deepgram API keys, as well as the Livekit URL, secret, and API key
- Run `python src/main.py start` in the terminal
- To join a chat room, log in through `https://agents-playground.livekit.io/` and select the playground that corresponds to your API key

Overview
--------------------
<h3>Technologies Used</h3>
This agent is primarily built using Livekit alongside Silero, OpenAI, and Deepgram. Langchain is used to provide additional functionality to the LLM.

<h3>Voice Pipeline</h3>

- The agent follows a pipeline of VAD -> STT -> LLM -> TTS to communicate to the user. Silero and Deepgram are used for VAD and STT respectively, while OpenAI is used for LLM and TTS.
- Using a callback function in between the STT and LLM stage, the user's query can be modified before entering the LLM.
    - Here, the query is classified, and if needed, relevant documents are retrieved
- The use of a function context object allows the LLM to make function calls for supplementary information.
    - Currently, this is only used to provide the current time

<h3>Functionality</h3>
Through the above pipeline, the agent can:

- Answer questions about the company using classification and RAG
- Handle orders by the customer
- Let the LLM make function calls, providing extra context

Performance
--------------------
<h3>Additional Functionality</h3>

Currently, the pizza center doesn't have any real locations. This could be changed in the future, where there would exist a list of locations. In this case, we would also implement a way to retrieve the user's location. From here, we can add a function to our function context, maybe using an API call to help the LLM find the store location that is closest to the user.

Other features such as chatbot-human handoff could be implemented, for if the user requires human assistance.

<h3>Speed</h3>

Overall, the bot seems to be pretty quick, with there usually being a couple second delay from the end of the user talking to the start of the agent talking. 

<h3>Testing</h3>

Due to the agent interacting through voice and the voice agent pipeline, going from STT -> LLM -> TTS, testing would be a little more difficult than if it was purely a text to text agent. Because of this, I chose to use loggers and manually test my agent. 

If needed, individually testing components such as the speech to text or specific LLM components (classification, document retrieval, etc) shouldn't be difficult, as the models that are used in the pipeline can be used independently.

In the future, I would like to test the speed of individual components, and see how to improve the agent. Additionally, I'd implement stress testing to see how well the speed scales.

<h3>Costs</h3>
The costs on the scale used here are negligible. The Deepgram and Livekit services are free to the extent that it is used here, and the cost of using OpenAI is not high. On a mass scale however, we will incur more costs from API calls such as to OpenAI. And we will have to pay for the increased use of Deepgram and Livekit
