from tools.tools import Response

from bs4 import BeautifulSoup
import json


class HomeDepot:
    def __init__(self) -> None:
        pass
    
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