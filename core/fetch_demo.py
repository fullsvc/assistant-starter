import httpx
import asyncio


async def fetch_async(url: str) -> dict:
    '''
    Getting information from the website api
    
    :param url: 
        :lang: language
        :count: number of fact requests
    :type url: str
    :return: json
    '''
    print(f' - Getting data from {url}')
    try:
        async with httpx.AsyncClient(timeout=7.0) as client:
            response = await client.get(url)

        response.raise_for_status()
        print(f'   - Data from {url} received successfully')
        body_json = response.json()
        return body_json
    except httpx.HTTPError as error:
        print(f'Failure to receive data from {url}; Status code: {error}')
        return ''


async def fetch_many_async() -> None:
    ''' Multiple asynchronous requests '''

    services = {
        'Cat facts': 'https://meowfacts.herokuapp.com/?lang=rus&count=3',
        'Useless facts': 'https://uselessfacts.jsph.pl//api/v2/facts/random',
    }
    print(f'Start async requersts')
    tasks = [fetch_async(url=url) for url in services.values()]
    responses = await asyncio.gather(*tasks)
    data = [resp['data'] if 'data' in resp.keys() else resp['text'] for resp in responses]

    if data:
        for service_name, data_info in zip(services.keys(), data):
            print(f'{service_name}: {data_info}')
    else:
        print('No information available')


async def async_main() -> None:
    ''' Main function '''

    print(f'Start Job')
    summary = await fetch_many_async()
    print(f'End job')


if __name__ == '__main__':
    asyncio.run(async_main())

