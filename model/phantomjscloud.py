import requests
import json
from typing import Tuple, List, Union
from llama_index.readers.schema.base import Document


def getDocumentsByUrls(urls: List[Union[str, Tuple[str, Tuple[int, int]]]]) -> str:
    documents = []
    for _, url in enumerate(urls):
        text = scrape_website_by_phantomjscloud(url)
        document = Document(text)
        documents.append(document)
    return documents


def scrape_website_by_phantomjscloud(url: str) -> str:
    endpoint_url = f"https://PhantomJsCloud.com/api/browser/v2/ak-awryp-dbpw8-865fb-vjfxz-cpby3/"
    data = {
        "url": url,
        "renderType": "plainText",
        "requestSettings": {
            "doneWhen": [
                {
                    "event": "domReady"
                },
            ],
        }
    }
    response = requests.post(endpoint_url, data=json.dumps(data))
    if response.status_code == 200:
        try:
            return response.content.decode('utf-8')
        except:
            return "Error: Unable to fetch content"
    else:
        return f"Error: {response.status_code} - {response.reason}"


