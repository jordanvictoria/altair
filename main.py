import asyncio
import aiohttp
import csv
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_country_data(session, country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return data
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching data for {country}: {e}")
        return None

def print_country_info(country_data):
    country_name = country_data[0]['name']['common']
    currency = country_data[0]['currencies'][list(country_data[0]['currencies'])[0]]['name']
    capital = country_data[0]['capital'][0]
    alternate_spellings = ", ".join(country_data[0]['altSpellings'])

    print(f"Country Name: {country_name}")
    print(f"Currency: {currency}")
    print(f"Capital: {capital}")
    print(f"Alternate Spellings: {alternate_spellings}")

def write_to_csv(country_info_list):
    with open('country_info.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Country Name', 'Currency', 'Capital', 'Alternate Spellings'])
        for country_info in country_info_list:
            writer.writerow(country_info)

async def fetch_and_process_country(session, country):
    country_data = await fetch_country_data(session, country)
    if country_data:
        print_country_info(country_data)
        return (
            country_data[0]['name']['common'],
            country_data[0]['currencies'][list(country_data[0]['currencies'])[0]]['name'],
            country_data[0]['capital'][0],
            ", ".join(country_data[0]['altSpellings'])
        )
    else:
        return None
    
async def main():
    countries = ['united states', 'austria', 'sweden']
    country_info_list = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_process_country(session, country) for country in countries]
        country_info_list = await asyncio.gather(*tasks)

    country_info_list = [info for info in country_info_list if info is not None]

    write_to_csv(country_info_list)

if __name__ == "__main__":
    asyncio.run(main())

