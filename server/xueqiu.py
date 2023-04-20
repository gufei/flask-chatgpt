from flask_restful import Resource
from flask import request
from flask import current_app as app
from llama_index import GPTSimpleVectorIndex, LLMPredictor, RssReader, PromptHelper, ServiceContext

from cmd.index import xueqiu_index_path,service_context

from llama_index.prompts.prompts import QuestionAnswerPrompt

QUESTION_ANSWER_PROMPT_TMPL_CN = (
    "你是一个经济学专家，对二级市场投资非常精通，以下是雪球热贴和话题： \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "除非在问题中明确指出使用其他语言，都请用中文回答我的问题。我的问题是：{query_str}\n"
)


class XueQiu(Resource):
    def post(self):
        body = request.get_json()
        app.logger.info(body['prompt'])
        prompt = body['prompt']
        index = GPTSimpleVectorIndex.load_from_disk(xueqiu_index_path, service_context=service_context)
        answer = index.query(prompt, service_context=service_context,
                             text_qa_template=QuestionAnswerPrompt(QUESTION_ANSWER_PROMPT_TMPL_CN))

        return {'code': 200, 'msg': 'ok', 'data': answer.response}

