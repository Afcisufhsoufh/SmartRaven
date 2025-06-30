# Copyright @ISmartDevs
# Channel t.me/TheSmartDev
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
import pycountry
from config import COMMAND_PREFIX, UPDATE_CHANNEL_URL
from utils import LOGGER, get_locale_for_country, notify_admin  # Import LOGGER and notify_admin from utils

# Fixed addresses for Kazakhstan and Algeria
FIXED_ADDRESSES = {
    "KZ": {
        "country": "Kazakhstan",
        "street": "Donetskaya, bld. 8, appt. 106",
        "streetName": "Donetskaya",
        "buildingNumber": "8",
        "city": "Pavlodar",
        "zipcode": "140000",
        "state": "Pavlodarskaya oblast"
    },
    "DZ": [
        {
            "country": "Algeria",
            "street": "Algeria 7e6",
            "streetName": "Algeria 7e6",
            "buildingNumber": "7e6",
            "city": "Algeria",
            "zipcode": "09000"
        },
        {
            "country": "Algeria",
            "street": "3 cours de la Révolution, 23000",
            "streetName": "3 cours de la Révolution",
            "buildingNumber": "23000",
            "city": "Annaba",
            "zipcode": "23000"
        }
    ]
}

def setup_fake_handler(app: Client):
    @app.on_message(filters.command(["fake", "rnd"], prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
    async def fake_handler(client: Client, message: Message):
        if len(message.command) <= 1:
            await client.send_message(message.chat.id, "**❌ Please Provide A Country Code or Name**", parse_mode=ParseMode.MARKDOWN)
            LOGGER.warning(f"Invalid command format: {message.text}")
            return
        
        country_input = message.command[1].upper()
        country = pycountry.countries.get(alpha_2=country_input) or pycountry.countries.get(name=country_input) or pycountry.countries.search_fuzzy(country_input)[0]
        
        if not country:
            await client.send_message(message.chat.id, "**❌ Please Provide A Valid Country Code or Name**", parse_mode=ParseMode.MARKDOWN)
            LOGGER.warning(f"Invalid country input: {country_input}")
            return

        country_code = country.alpha_2
        country_name = country.name
        generating_message = await client.send_message(message.chat.id, "**Generating Fake Address...✨**", parse_mode=ParseMode.MARKDOWN)

        # Handle fixed addresses for Kazakhstan and Algeria
        if country_code in FIXED_ADDRESSES:
            data = FIXED_ADDRESSES[country_code]
            if country_code == "DZ":
                # Randomly select one of the two addresses for Algeria
                import random
                data = random.choice(FIXED_ADDRESSES["DZ"])
        else:
            # Fetch fake address from API for other countries
            locale = get_locale_for_country(country.alpha_2) or f"{country.alpha_2.lower()}_{country.alpha_2.upper()}"
            api_url = f"https://fakerapi.it/api/v2/addresses?_quantity=1&_locale={locale}&_country_code={country.alpha_2}"
            
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, requests.get, api_url)
                response.raise_for_status()  # Raise an exception for non-200 status codes
                data = response.json()['data'][0]
            except (requests.RequestException, ValueError, KeyError) as e:
                LOGGER.error(f"Fake address API error for country '{country_input}': {e}")
                await notify_admin(client, "/fake", e, message)
                await generating_message.edit_text("**❌ Sorry, Fake Address Generator API Failed**", parse_mode=ParseMode.MARKDOWN)
                return

        # Format the output
        address_text = (
            f"**Fake Address For {country_name}**\n"
            f"**━━━━━━━━━━━━━━━━━**\n"
            f"**Street:** `{data['street']}`\n"
            f"**Street Name:** `{data['streetName']}`\n"
            f"**Building Number:** `{data['buildingNumber']}`\n"
            f"**City/Town/Village:** `{data['city']}`\n"
            f"**Postal code:** `{data['zipcode']}`\n"
            f"**Country:** `{data['country']}`\n"
            f"**━━━━━━━━━━━━━━━━━**\n"
            f"**Don't forget to [Join Now]({UPDATE_CHANNEL_URL}) for updates!**"
        )
        await generating_message.edit_text(address_text, parse_mode=ParseMode.MARKDOWN)
        LOGGER.info(f"Sent fake address for {country_input} in chat {message.chat.id}")