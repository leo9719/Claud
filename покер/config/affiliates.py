"""Affiliate link storage and URL building."""

_TRACKING = "sub_id={user_id}&lang={lang}&source=telegram_bot"


def build_link(base: str, user_id: int, lang: str) -> str:
    separator = "&" if "?" in base else "?"
    tracking = _TRACKING.format(user_id=user_id, lang=lang)
    return f"{base}{separator}{tracking}"


AFFILIATE_LINKS: dict[str, dict[str, str]] = {
    "ru": {
        "smartlink": "https://smart.ggpartners.com/ru",
        "pokerok": "https://pokerok.com/ru/register",
        "ggpoker": "https://ggpoker.com/ru/register",
        "pokerstars": "https://pokerstars.ru/register",
        "partypoker": "https://partypoker.com/ru/register",
        "888poker": "https://888poker.ru/register",
    },
    "en": {
        "smartlink": "https://smart.ggpartners.com/en",
        "pokerok": "https://pokerok.com/en/register",
        "ggpoker": "https://ggpoker.com/en/register",
        "pokerstars": "https://pokerstars.com/register",
        "partypoker": "https://partypoker.com/en/register",
        "888poker": "https://888poker.com/register",
    },
    "es": {
        "smartlink": "https://smart.ggpartners.com/es",
        "pokerok": "https://pokerok.com/es/register",
        "ggpoker": "https://ggpoker.com/es/register",
        "pokerstars": "https://pokerstars.es/register",
        "partypoker": "https://partypoker.com/es/register",
        "888poker": "https://888poker.es/register",
    },
    "pt": {
        "smartlink": "https://smart.ggpartners.com/pt",
        "pokerok": "https://pokerok.com/pt/register",
        "ggpoker": "https://ggpoker.com/pt/register",
        "pokerstars": "https://pokerstars.com/pt/register",
        "partypoker": "https://partypoker.com/pt/register",
        "888poker": "https://888poker.com/pt/register",
    },
    "fr": {
        "smartlink": "https://smart.ggpartners.com/fr",
        "pokerok": "https://pokerok.com/fr/register",
        "ggpoker": "https://ggpoker.com/fr/register",
        "pokerstars": "https://pokerstars.fr/register",
        "partypoker": "https://partypoker.com/fr/register",
        "888poker": "https://888poker.fr/register",
    },
    "de": {
        "smartlink": "https://smart.ggpartners.com/de",
        "pokerok": "https://pokerok.com/de/register",
        "ggpoker": "https://ggpoker.com/de/register",
        "pokerstars": "https://pokerstars.de/register",
        "partypoker": "https://partypoker.com/de/register",
        "888poker": "https://888poker.de/register",
    },
}

_FALLBACK_LANG = "en"

ROOM_DISPLAY_NAMES: dict[str, str] = {
    "smartlink": "🌐 Best Room for You",
    "pokerok": "♠️ PokerOK",
    "ggpoker": "♦️ GGPoker",
    "pokerstars": "⭐ PokerStars",
    "partypoker": "🎉 PartyPoker",
    "888poker": "8️⃣ 888poker",
}


def get_link(room: str, user_id: int, lang: str) -> str:
    lang_links = AFFILIATE_LINKS.get(lang) or AFFILIATE_LINKS[_FALLBACK_LANG]
    base = lang_links.get(room) or lang_links["smartlink"]
    return build_link(base, user_id, lang)
