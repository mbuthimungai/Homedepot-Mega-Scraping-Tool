import json
import asyncio
import os

class CookieHandler:
    def __init__(self) -> None:
        pass

    async def read_cookie(self) -> str:
        """Reads the cookies.json file and searches the bm_sz cookie and returns it"""
        try:
            with open('cookies.json', 'r') as file:
                cookies = json.load(file)
            
            for cookie in cookies:
                if cookie['name'] == 'bm_sz':
                    return f"bm_sz={cookie['value']};"
        except FileNotFoundError:
            await self.farm_cookies()            
            try:
                with open('cookies.json', 'r') as file:
                    cookies = json.load(file)
                
                for cookie in cookies:
                    if cookie['name'] == 'bm_sz':
                        return f"bm_sz={cookie['value']};"
            except FileNotFoundError:
                print("Failed to generate cookies.")
                return None

    async def farm_cookies(self) -> None:
        """Farms cookies from HD using puppeteer JS"""
        script_path = './cookie_farmer/cookies.js'
        process = await asyncio.create_subprocess_exec(
            'node', script_path, 
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')