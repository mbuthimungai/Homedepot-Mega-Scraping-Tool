from tools.tools import Response
from graphql_queries.search_model_query_1 import SearchModel

from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.homedepot.com/federation-gateway/graphql?opname=searchModel"

class HomeDepot:
    def __init__(self) -> None:
        pass
        
        
    async def get_products(self, category_code: str, start_index: int,
                           page_size: int) -> dict:
                                
        response = Response(base_url=BASE_URL)
        search_model = SearchModel()
        
        graphql = await search_model.create_search_model_query(
            category_code=category_code, page_size=page_size, start_index=start_index)
        
        content = await response.content_graph(graph_payload=graphql)
        return content
        
    async def extract_user_agents(self, url: str) -> None:
        content = await Response(base_url=url).content_html()
        
        soup = BeautifulSoup(content, "html.parser")        
        
        div_ids = ['most-common-desktop-useragents-json-csv', 'most-common-mobile-useragents-json-csv']
        
        is_delete = True
        
        for div_id in div_ids:
            # find div with user agents
            div_with_json_ua = soup.find('div', id=div_id)
            
            textarea = div_with_json_ua.find('textarea', {'class': 'form-control'})
            
            await self.save_user_agents(textarea=textarea, is_delete=is_delete)
            
            is_delete = False
        
        
        
    async def save_user_agents(self, textarea: list, is_delete: bool) -> None:
        if textarea:
            user_agents = json.loads(textarea.text)            
            try:
                if is_delete:
                    # This deletes content from the user agent.txt file
                    with open("./tools/user-agents.txt", "w") as file:
                        pass
                    
                with open("./tools/user-agents.txt", "a") as file:                    
                    for user_agent in user_agents:                        
                        file.write(f'{user_agent.get("ua")}\n')
            except Exception as e:
                print(e)