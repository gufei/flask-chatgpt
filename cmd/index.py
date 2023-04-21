from flask import Blueprint
from llama_index import GPTSimpleVectorIndex, LLMPredictor, RssReader, PromptHelper, ServiceContext
from langchain.chat_models import ChatOpenAI
from llama_index.node_parser import SimpleNodeParser
from pathlib import Path
from flask import current_app as app

indexCmdBp = Blueprint('index', __name__)

llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.75, model_name="gpt-3.5-turbo"))

prompt_helper = PromptHelper(max_input_size=4096, num_output=1000, max_chunk_overlap=20)

service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

xueqiu_index_path = Path("./indexdata/xueqiu")


@indexCmdBp.cli.command()
def xueqiu():
    app.logger.info("雪球内容索引开始......")

    urls = ["https://rsshub.app/xueqiu/today", "https://rsshub.app/xueqiu/hots"]

    documents = RssReader(html_to_text=True).load_data(urls=urls)

    parser = SimpleNodeParser()

    nodes = parser.get_nodes_from_documents(documents)

    for node_index, node_item in enumerate(nodes):
        nodes[node_index].doc_id = nodes[node_index].get_doc_hash()

    if xueqiu_index_path.is_file():
        index = GPTSimpleVectorIndex.load_from_disk(xueqiu_index_path, service_context=service_context)
        index.insert_nodes(nodes)
    else:
        index = GPTSimpleVectorIndex(nodes, service_context=service_context)

    index.save_to_disk(xueqiu_index_path)

    app.logger.info("雪球内容索引结束")
