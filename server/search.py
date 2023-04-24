from flask_restful import Resource
from flask import request
from flask import current_app as app
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain import LLMMathChain
from langchain.agents import AgentType, Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent

search = GoogleSerperAPIWrapper(gl="cn", hl="zh-cn")

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.75, request_timeout=600, max_tokens=3000)

llm_math_chain = LLMMathChain(llm=llm, verbose=False)

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
        return_direct=True,
    )
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory,
                         max_iterations=5, max_execution_time=600, early_stopping_method="generate", verbose=True)


class Search(Resource):
    def post(self):
        body = request.get_json()
        app.logger.info(body['prompt'])
        prompt = body['prompt']

        res = agent.run(prompt)

        return {'code': 200, 'msg': 'ok', 'data': res}
