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
    app.logger.info("金融内容索引开始......")

    urls = [
        # AI 财经社
        "https://rsshub.app/aicaijing/latest",  # 最新文章
        "https://rsshub.app/aicaijing/recommend",  # 推荐文章
        "https://rsshub.app/aicaijing/cover",  # 封面文章

        # BigQuant
        "https://rsshub.app/bigquant/collections",  # 专题报告

        # DT 财经
        "https://rsshub.app/dtcj/datainsight",  # 数据洞查

        # FX Markets
        "https://rsshub.app/fx-markets/trading",

        # TokenInsight
        "https://tokeninsight.com/rss/news/zh",

        # 北京证券交易所
        "https://rsshub.app/bse",  # 本所要闻

        # 财经网
        "https://rsshub.app/caijing/roll",  # 滚动新闻

        # 财联社
        "https://rsshub.app/cls/telegraph",  # 电报
        "https://rsshub.app/cls/depth/1000",  # 深度-头条
        "https://rsshub.app/cls/hot",  # 热门文章

        # 第一财经杂志
        "https://rsshub.app/cbnweek",

        # 东方财富
        "https://rsshub.app/eastmoney/search/web3",  # 搜索web3
        "https://rsshub.app/eastmoney/search/A股",  # 搜索A股

        # 法布财经
        "https://rsshub.app/fastbull/news",  # 新闻

        # 格隆汇
        "https://rsshub.app/gelonghui/home",  # 首页
        "https://rsshub.app/gelonghui/hot-article",  # 最热文章
        "https://rsshub.app/gelonghui/live",  # 实时快讯

        # 国家金融与发展实验室
        "https://rsshub.app/nifd/research/3333d2af-91d6-429b-be83-28b92f31b6d7",  # 研究评价

        # 麦肯锡
        "https://rsshub.app/mckinsey/cn",  # 洞见

        # 每经网
        "https://rsshub.app/nbd",  # 要闻

        # 前瞻网
        "https://rsshub.app/qianzhan/analyst/column/all",  # 文章列表

        # 上海证券交易所
        "https://rsshub.app/sse/renewal",  # 科创板项目动态

        # 深圳证券交易所
        "https://rsshub.app/szse/notice",  # 上市公告 - 可转换债券
        "https://rsshub.app/szse/projectdynamic",  # 创业板项目动态

        # 首席经济学家论坛
        "https://rsshub.app/chinacef",  # 最新更新
        "https://rsshub.app/chinacef/portal/hot",  # 金融热点

        # 新浪财经
        "https://rsshub.app/sina/finance",  # 新浪财经－国內

        # 有知有行
        "https://rsshub.app/youzhiyouxing/materials",  # 有知文章

        # 证券时报网
        "https://rsshub.app/stcn/yw",  # 要闻
        "https://rsshub.app/stcn/kx",  # 快讯
        "https://rsshub.app/stcn/gs",  # 股市
        "https://rsshub.app/stcn/company",  # 公司
        "https://rsshub.app/stcn/data",  # 数据
        "https://rsshub.app/stcn/fund",  # 基金
        "https://rsshub.app/stcn/finance",  # 金融
        "https://rsshub.app/stcn/comment",  # 评论
        "https://rsshub.app/stcn/cj",  # 产经
        "https://rsshub.app/stcn/ct",  # 创投
        "https://rsshub.app/stcn/kcb",  # 科创板
        "https://rsshub.app/stcn/xsb",  # 新三板
        "https://rsshub.app/stcn/tj",  # 投教
        "https://rsshub.app/stcn/zk",  # ESG
        "https://rsshub.app/stcn/gd",  # 滚动
        "https://rsshub.app/stcn/gsyl",  # 股市一览
        "https://rsshub.app/stcn/djjd",  # 独家解读
        "https://rsshub.app/stcn/gsxw",  # 公司新闻
        "https://rsshub.app/stcn/gsdt",  # 公司动态
        "https://rsshub.app/stcn/djsj",  # 独家数据
        "https://rsshub.app/stcn/kd",  # 看点数据
        "https://rsshub.app/stcn/zj",  # 资金流向
        "https://rsshub.app/stcn/sj_kcb",  # 科创板
        "https://rsshub.app/stcn/zl",  # 专栏
        "https://rsshub.app/stcn/author",  # 作者
        "https://rsshub.app/stcn/cjhy",  # 行业
        "https://rsshub.app/stcn/cjqc",  # 汽车

        # 智通财经网
        "https://rsshub.app/zhitongcaijing/recommend",  # 推荐
        "https://rsshub.app/zhitongcaijing/hkstock",  # 港股
        "https://rsshub.app/zhitongcaijing/meigu",  # 美股
        "https://rsshub.app/zhitongcaijing/agu",  # 沪深
        "https://rsshub.app/zhitongcaijing/ct",  # 创投
        "https://rsshub.app/zhitongcaijing/esg",  # esg
        "https://rsshub.app/zhitongcaijing/aqs",  # 券商
        "https://rsshub.app/zhitongcaijing/ajj",  # 基金
        "https://rsshub.app/zhitongcaijing/focus",  # 要闻
        "https://rsshub.app/zhitongcaijing/announcement",  # 公告
        "https://rsshub.app/zhitongcaijing/research",  # 研究
        "https://rsshub.app/zhitongcaijing/shares",  # 新股
        "https://rsshub.app/zhitongcaijing/bazaar",  # 市场
        "https://rsshub.app/zhitongcaijing/company",  # 公司

        # 中证网
        "https://rsshub.app/cs/news/zzkx",  # 中证快讯

        # 雪球
        "https://rsshub.app/xueqiu/today",
        "https://rsshub.app/xueqiu/hots"

    ]

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

    app.logger.info("金融内容索引结束")
