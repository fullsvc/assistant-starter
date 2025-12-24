import asyncio
import httpx


async def get_data(url: str) -> str:
    ''' Получаем данные из публичных источников '''
    print(f'Получаем данные из {url}')
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)

        response.raise_for_status()
        print(f'Данные из {url} получены успешно; Status code: {response.status_code}')
        body_text = response.text
        return body_text
    except httpx.HTTPError as error:
        print(f'Сбой получения данных из {url}; Ошибка: {error}')
        return ''
    
    # https://cat-fact.herokuapp.com/facts



async def fetch_many_async():
    services = {
        'cat_facts': 'https://cat-fact.herokuapp.com/facts?amount=3',
        'dog_facts': 'http://dog-api.kinduff.com/api/facts?number=3',
    }

    print(f'Запускаем асинхронные запросы')
    tasks = [get_data(url) for url in services.values()]
    start = asyncio.get_event_loop().time()
    responses = await asyncio.gather(*tasks)
    end_time = asyncio.get_event_loop().time()
    total_time = end_time - start
    print(f'Все запросы выполнились за {total_time:.2f}')
    result = {}
    for service_name, response_body in zip(services.keys(), responses):
        result[service_name] = response_body
        print(f'Сервис {service_name}')
        print(f'Первые символы ответа {response_body[:70]}')

async def async_main() -> None:
    print(f'=====Началась асинхронная обработка HTTP =====')
    summary = await fetch_many_async()

    print(f'=====Завершилась асинхронная обработка HTTP =====')
    if not summary:
        print('Пустой ответ')


if __name__ == '__main__':
    asyncio.run(async_main())