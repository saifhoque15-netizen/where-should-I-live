import pycountry
import streamlit as st

def get_iso_code(name):
    try:
        return pycountry.countries.get(name=name).alpha_2.lower()
    except:
        return None

import pycountry

def flag_from_country(name):
    try:
        if name != 'UnitedKingdom':
            match = pycountry.countries.search_fuzzy(name)[0]
            code = match.alpha_2.lower()
            return f"https://flagcdn.com/h60/{code}.png"
        else:
            return f"https://flagcdn.com/h60/gb.png"
    except:
        return None

