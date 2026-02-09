import asyncio

import aiohttp


async def check_ban(uid: str) -> dict | None:
    api_url = f"http://raw.thug4ff.com/check_ban/check_ban/{uid}"
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(api_url) as response:
                response.raise_for_status()
                response_data = await response.json()

                if response_data.get("status") == 200:
                    data = response_data.get("data")
                    if data:
                        return {
                            "is_banned": data.get("is_banned", 0),
                            "nickname": data.get("nickname", ""),
                            "period": data.get("period", 0),
                            "region": data.get("region", "N/A"),
                        }

                return None
    except aiohttp.ClientError as error:
        print(f"API request failed for UID {uid}: {error}")
        return None
    except asyncio.TimeoutError:
        print(f"API request timed out for UID {uid}.")
        return None
    except Exception as error:
        print(f"An unexpected error occurred for UID {uid}: {error}")
        return None
