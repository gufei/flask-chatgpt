from flask_restful import Resource
from flask import request
from flask import current_app as app
from urlextract import URLExtract

from model import phantomjscloud
from llama_index import GPTSimpleVectorIndex

extractor = URLExtract()


class ChatGPT(Resource):
    """
    通过继承 Resource 来实现调用 GET/POST 等动作方法
    """

    def post(self):
        # 参数数据
        body = request.get_json()
        # print(json_data["url"])

        app.logger.info(body['prompt'])

        prompt = body['prompt']

        urls = extractor.find_urls(body['prompt'], with_schema_only=True)

        if urls:
            for _, url in enumerate(urls):
                prompt = prompt.replace(url, "")
            documents = phantomjscloud.getDocumentsByUrls(urls)

            index = GPTSimpleVectorIndex.from_documents(documents)
            app.logger.info(index)

            response = index.query(prompt)

            app.logger.info(response)

            answer = "ok"

        else:
            answer = "no url in prompt!"

        return {'code': 200, 'msg': 'ok', 'data': answer}
