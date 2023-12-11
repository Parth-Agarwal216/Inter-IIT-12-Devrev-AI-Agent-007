from imports import *
from prompts import *


os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"
os.environ['OPENAI_API_KEY'] = "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"
# ENV_HOST = "https://cloud.langfuse.com"
# ENV_SECRET_KEY = userdata.get('LF-SECRET')
# ENV_PUBLIC_KEY = userdata.get('LF-PUBLIC')

system_prompt_classifier = PromptTemplate(
    input_variables=["QUERY", "PREV_QUERY"], template= system_prompt_classifier_template,
    output_key="cassification"
)

system_memory_prompt = PromptTemplate(
    input_variables=["QUERY", "API_LIST", "RAG", "PAST_QUERY", "PAST_RESPONSE"], template= system_prompt_memory_template
)

system_prompt = PromptTemplate(
    input_variables=["QUERY", "API_LIST", "RAG"], template= system_prompt_template
)

follow_up_prompt = PromptTemplate(
    input_variables=["QUERY", "chat_history"], template= follow_up_prompt_template
)
generation_prompt = PromptTemplate(
    input_variables = ["API_LIST", "FEW_SHOT", "APIS", "TOOL_NAME"],template = generation_prompt_template
  )

memory = ConversationBufferWindowMemory(
    memory_key="chat_history", input_key = "QUERY", k = 1,
    return_messages=True
)
llm = ChatOpenAI(temperature = 0.0, model =  "gpt-3.5-turbo-1106")


mem_chain = LLMChain(llm=llm,
                     prompt=system_prompt_classifier,
                     memory = memory,
                     verbose=True)

query_chain_memory = LLMChain(llm=llm,
                        prompt=system_memory_prompt,
                        memory = memory,
                        verbose=True)

query_chain = LLMChain(llm=llm,
                       prompt=system_prompt,
                       memory = memory,
                       verbose=True)

format_chain = LLMChain(llm=llm,
                        prompt=follow_up_prompt,
                        memory = memory,
                        verbose=True)

generation_chain = LLMChain(llm= ChatOpenAI(temperature = 0.7, model =  "gpt-3.5-turbo-1106"),
                        prompt=generation_prompt,
                        output_key = 'QUERY',
                        verbose=False)
reprompt = PromptTemplate(
    input_variables=["QUERY", "API_LIST", "CORRECTION_PROMPT", "chat_history"], template= reprompt_template
)

reprompt_chain = LLMChain(llm=llm,
                        prompt=reprompt,
                        output_key = 'new_response',
                        memory = memory,
                        verbose=True)