import aiohttp

from secrets import token_urlsafe

from typing import Dict, Any, Optional


class ServiceError(Exception):
    pass


class JsonBox:
    session: aiohttp.ClientSession
    api_link: str
    headers: Dict[str, str]

    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        """
        :param session:
        :return: None
        """
        self.api_link: str = "https://jsonbox.io/"
        self.headers: Dict[str, str] = {
            'content-type': 'application/json'
        }
        if session is None:
            self.session = aiohttp.ClientSession()
            return
        self.session = session

    async def close(self) -> None:
        """
        :return:  None
        """
        await self.session.close()

    async def create_box(self, text: str, url: Optional[str] = None) -> str:
        """
        :param url:
        :param text:
        :return: str
        """
        if url is None:
            len_text = len(text)
            if 20 < len_text < 64:
                url = self.api_link + token_urlsafe(len_text)
            else:
                url = self.api_link + (token_urlsafe(29))
            url = url.replace("-", "")

        async with self.session.post(url=url, headers=self.headers, data=text) as response:
            if response.status == 200:
                return url
            raise ServiceError(f"jsonbox responses have status {response.status} => {await response.text()} ")

    async def delete_box(self, url: str) -> None:
        """
        :param url:
        :return:
        """
        async with self.session.delete(url=url) as response:
            if response.status == 200:
                return
            raise ServiceError(f"jsonbox responses have status {response.status} => {await response.text()} ")

    async def edit_data_link(self, url: str, text: str) -> None:
        """

        :param url:
        :param text:
        :return:
        """
        if "https://jsonbox.io/" in url:
            async with self.session.get(url=url, headers=self.headers, data=text) as response:
                if response.status == 200:
                    return
                raise ServiceError(f"jsonbox responses have status {response.status} => {await response.text()}")
        async with self.session.put(url=f"https://jsonbox.io/{url}", headers=self.headers, data=text) as response:
            if response.status == 200:
                return
            raise ServiceError(f"jsonbox responses have status {response.status} => {await response.text()}")

    async def get_data_link(self, url: str) -> str:
        """
        :param url:
        :return: str
        """
        if "https://jsonbox.io/" in url:
            async with self.session.get(url=url) as response:
                return await response.text()
        async with self.session.get(url=f"https://jsonbox.io/{url}") as response:
            return await response.text()

    async def create_protected_box(self, text: str, x_api_key: str, url: Optional[str] = None) -> str:
        """

        :param text:
        :param x_api_key:
        :param url:
        :return:
        """
        self.headers["x-api-key"] = x_api_key
        if url is None:
            len_text = len(text)
            if 20 < len_text < 64:
                url = self.api_link + token_urlsafe(len_text)
            else:
                url = self.api_link + (token_urlsafe(29))
            url = url.replace("-", "")

        async with self.session.post(url=url, headers=self.headers, data=text) as response:
            if response.status == 200:
                return url
            raise ServiceError(f"jsonbox responses have status {response.status} => {await response.text()} ")

    async def get_box_metadata(self, box_id: str, encoding: str = "UTF-8") -> Dict[str, Any]:
        """

        :param box_id:
        :param encoding:
        :return:
        """
        link: str = f"https://jsonbox.io/_meta/{box_id}"
        async with self.session.get(url=link) as response:
            if response.status == 200:
                return await response.json(encoding=encoding)
            raise ServiceError(f"jsonbox responses have status {response.status} => {await response.text()} ")

