import os
import re
import certifi
import airportsdata
import pycountry
from dotenv import load_dotenv
load_dotenv()

os.environ["SSL_CERT_FILE"]=certifi.where()
os.environ["REQUEST_CA_BUNDLE"]=certifi.where()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA")

BASE_URL= "https://api.aviationstack.com/v1/flights"

AIRPORTS = airportsdata.load("IATA")

COUNTRY_ALIASES = {
    "usa": "US",
    "us": "US",
    "u.s.a.": "US",
    "u.s.": "US",
    "america": "US",
    "united states": "US",
    "india": "IN",
    "bharat": "IN",
    "ind": "IN",
    "uk": "GB",
    "u.k.": "GB",
    "britain": "GB",
    "great britain": "GB",
    "england": "GB",
    "united kingdom": "GB",
    "canada": "CA",

    "australia": "AU",

    "germany": "DE",
    "deutschland": "DE",

    "france": "FR",

    "italy": "IT",

    "spain": "ES",

    "japan": "JP",

    "china": "CN",
    "prc": "CN",

    "south korea": "KR",
    "korea": "KR",
    "republic of korea": "KR",

    "singapore": "SG",

    "uae": "AE",
    "emirates": "AE",
    "united arab emirates": "AE",

    "thailand": "TH",

    "vietnam": "VN",

    "malaysia": "MY",

    "indonesia": "ID",

    "nepal": "NP",

    "sri lanka": "LK",

    "pakistan": "PK",

    "bangladesh": "BD",

    "bhutan": "BT",

    "maldives": "MV",
}

COUNTRY_MAIN_AIRPORT = {
    # United States
    "usa": "JFK",
    "us": "JFK",
    "u.s.a.": "JFK",
    "u.s.": "JFK",
    "america": "JFK",
    "united states": "JFK",

    # India
    "india": "DEL",
    "bharat": "DEL",
    "ind": "DEL",

    # United Kingdom
    "uk": "LHR",
    "u.k.": "LHR",
    "britain": "LHR",
    "great britain": "LHR",
    "england": "LHR",
    "united kingdom": "LHR",

    # Canada
    "canada": "YYZ",

    # Australia
    "australia": "SYD",

    # Germany
    "germany": "FRA",
    "deutschland": "FRA",

    # France
    "france": "CDG",

    # Italy
    "italy": "FCO",

    # Spain
    "spain": "MAD",

    # Japan
    "japan": "HND",

    # China
    "china": "PEK",
    "prc": "PEK",

    # South Korea
    "south korea": "ICN",
    "korea": "ICN",
    "republic of korea": "ICN",

    # Singapore
    "singapore": "SIN",

    # United Arab Emirates
    "uae": "DXB",
    "emirates": "DXB",
    "united arab emirates": "DXB",

    # Thailand
    "thailand": "BKK",

    # Vietnam
    "vietnam": "SGN",

    # Malaysia
    "malaysia": "KUL",

    # Indonesia
    "indonesia": "CGK",

    # Nepal
    "nepal": "KTM",

    # Sri Lanka
    "sri lanka": "CMB",

    # Pakistan
    "pakistan": "ISB",

    # Bangladesh
    "bangladesh": "DAC",

    # Bhutan
    "bhutan": "PBH",

    # Maldives
    "maldives": "MLE",
}

CITY_MAIN_AIRPORTS = {
    # India
    "lucknow": "LKO",
    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "hyderabad": "HYD",
    "chennai": "MAA",
    "kolkata": "CCU",
    "pune": "PNQ",
    "ahmedabad": "AMD",
    "jaipur": "JAI",
    "kochi": "COK",
    "cochin": "COK",
    "goa": "GOI",
    "varanasi": "VNS",
    "agra": "AGR",
    "amritsar": "ATQ",
    "bhubaneswar": "BBI",
    "indore": "IDR",
    "nagpur": "NAG",
    "patna": "PAT",
    "surat": "STV",
    "guwahati": "GAU",
    "dehradun": "DED",
    "chandigarh": "IXC",

    # USA
    "new york": "JFK",
    "los angeles": "LAX",
    "chicago": "ORD",
    "san francisco": "SFO",
    "washington": "IAD",
    "boston": "BOS",
    "miami": "MIA",
    "las vegas": "LAS",
    "seattle": "SEA",

    # UK
    "london": "LHR",
    "manchester": "MAN",
    "edinburgh": "EDI",

    # France
    "paris": "CDG",

    # Germany
    "frankfurt": "FRA",
    "munich": "MUC",
    "berlin": "BER",

    # UAE
    "dubai": "DXB",
    "abu dhabi": "AUH",

    # Singapore
    "singapore": "SIN",

    # Japan
    "tokyo": "HND",
    "osaka": "KIX",

    # China
    "beijing": "PEK",
    "shanghai": "PVG",

    # South Korea
    "seoul": "ICN",

    # Thailand
    "bangkok": "BKK",
    "phuket": "HKT",

    # Malaysia
    "kuala lumpur": "KUL",

    # Indonesia
    "jakarta": "CGK",
    "bali": "DPS",
    "denpasar": "DPS",

    # Vietnam
    "ho chi minh city": "SGN",
    "saigon": "SGN",
    "hanoi": "HAN",

    # Nepal
    "kathmandu": "KTM",

    # Sri Lanka
    "colombo": "CMB",

    # Pakistan
    "islamabad": "ISB",
    "karachi": "KHI",
    "lahore": "LHE",

    # Bangladesh
    "dhaka": "DAC",

    # Bhutan
    "paro": "PBH",

    # Maldives
    "male": "MLE",

    # Australia
    "sydney": "SYD",
    "melbourne": "MEL",
    "brisbane": "BNE",
    "perth": "PER",

    # Canada
    "toronto": "YYZ",
    "vancouver": "YVR",
    "montreal": "YUL",
}

def clean_text(text:str)->str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    
    stop_words = ["flight","flights","ticket","tickets","trip","travel","plan","complete","days","day","including","hotel","hotels","sightseeing","under","budget","info","information"]
    
    words = [w for w in text.split() if w not in stop_words]
    return " ".join(words).strip()

def country_name_to_code(text:str):
    text = clean_text(text)
    if text in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[text]
    
    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2
    except LookupError:
        pass
    
    for country in pycountry.countries:
        country_name = country.name.lower()
        if country_name in text:
            return country.alpha_2
        
    for alias,code in COUNTRY_ALIASES.items():
        if alias in text:
            return code
    return None

def airport_country_matches(airport: dict, country_code: str) -> bool:
    airport_country = str(airport.get("country", "")).upper().strip()

    if airport_country == country_code:
        return True

    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if country and airport_country.lower() == country.name.lower():
            return True
    except Exception:
        pass

    return False
