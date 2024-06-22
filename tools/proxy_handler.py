import random

class ProxyHandler:
    def __init__(self) -> None:
        pass
    
    async def rotate_proxies(self, ) -> str:
        proxies = []
        with open("./proxies.txt", "r") as file:
            proxies = file.readlines()
        
        proxies = [proxy.strip() for proxy in proxies]
        return random.choice(proxies)