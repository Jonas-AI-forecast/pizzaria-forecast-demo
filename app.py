import streamlit as st
import streamlit.components.v1 as components
import base64
from PIL import Image
from io import BytesIO
import os
import time

# === SETTINGS ===
USERNAME = "Demo"
PASSWORD = "Demo123"

st.set_page_config(page_title="Optimate | Login", layout="wide")

# === Global background & styles ===
st.markdown("""
    <style>
        html, body, .stApp, .block-container, .main, .css-1d391kg, .css-1v3fvcr {
            background-color: #003366 !important;
        }
        .block-container {
            padding-top: 1rem !important;
        }
        input, textarea, .stTextInput > div > input, .stPasswordInput > div > input {
            background-color: #002244 !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            caret-color: #ffffff !important;
        }
        label, .stCheckbox > div, .stCheckbox > div > label, .stCheckbox > div > label > div,
        .stCheckbox > div > label span, .stCheckbox > label > div:nth-child(2),
        .stCheckbox label span, .stCheckbox span, .stCheckbox p {
            color: #ffffff !important;
        }
        input::placeholder {
            color: #bbbbbb !important;
        }
        .stApp {
            color: #f0f0f0 !important;
        }
        button, .stButton>button {
            color: #ffffff !important;
            background-color: #007bff !important;
            border: none;
            border-radius: 6px !important;
            padding: 0.5em 1em;
            font-weight: 600;
        }
        button:disabled, .stButton>button:disabled {
            background-color: #999999 !important;
            color: #ffffff !important;
            opacity: 1.0 !important;
        }
    </style>
""", unsafe_allow_html=True)


# === Load logo ===
logo_path = os.path.join(os.path.dirname(__file__), "logo_optimate.png")
logo_image = Image.open(logo_path)
buffered = BytesIO()
logo_image.save(buffered, format="PNG")
logo_base64 = base64.b64encode(buffered.getvalue()).decode()

# === Session State ===
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

# === Landingpage ===
landing_html = f"""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap" rel="stylesheet">

<!-- Preload logo billede -->
<link rel="preload" as="image" href="data:image/png;base64,{logo_base64}">

<div class="logo-container">
    <img src="data:image/png;base64,{logo_base64}" alt="Optimate Logo" class="logo" />
    <div class="slogan">Forvandl data til forudsigelser med ét klik!</div>
</div>

<style>
    .logo-container {{
        max-width: 800px;
        margin: 20px auto 0 auto;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(6px);
        padding: 40px 30px 50px 30px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        text-align: center;
    }}
    .logo {{
        width: 340px;
        margin-top: 10px;
        margin-bottom: 10px;
        opacity: 0;
        animation: fadeInLogo 2s ease-in-out forwards;
        filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
    }}
    .slogan {{
        font-family: 'Poppins', sans-serif;
        font-size: 26px;
        font-weight: 600;
        color: #ffffff;
        margin-top: 5px;
        opacity: 0;
        animation: fadeInText 2s ease-in-out forwards;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    @keyframes fadeInLogo {{
        0% {{ opacity: 0; transform: scale(0.95); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}
    @keyframes fadeInText {{
        0% {{ opacity: 0; transform: translateY(-10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
</style>
"""

if not st.session_state.authenticated:
    components.html(landing_html, height=500)

# === Login Form ===
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
if not st.session_state.authenticated:
    with st.form("login_form"):
        st.text_input("Brugernavn", key="username")
        st.text_input("Adgangskode", type="password", key="password")
        remember_me = st.checkbox("Husk mig")
        login_button = st.form_submit_button("Log ind")

    if login_button:
        if st.session_state.username == USERNAME and st.session_state.password == PASSWORD:
            st.success("Login lykkedes! Velkommen")
            st.session_state.authenticated = True
            time.sleep(1)
            st.rerun()
        else:
            st.error("Forkert brugernavn eller adgangskode. Prøv igen.")

# === Mellempage ===
if st.session_state.authenticated and not st.session_state.show_dashboard:
    # Glasmorphic boks med logo og slogan
    st.markdown(f"""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap" rel="stylesheet">
        <div style="max-width: 700px; margin: 30px auto 10px auto; background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(6px); padding: 30px 20px; border-radius: 15px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" alt="Optimate Logo" style="width: 440px; margin-bottom: 8px; animation: fadeInLogo 1.5s ease-in-out; filter: drop-shadow(0 0 10px rgba(255,255,255,0.4));" />
            <div style="font-family: 'Poppins', sans-serif; font-size: 24px; font-weight: 600; color: #ffffff; animation: fadeInText 2s ease-in-out; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                Forvandl data til forudsigelser med ét klik!
            </div>
        </div>

        <style>
        @keyframes fadeInText {{
            0% {{ opacity: 0; transform: translateY(-10px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes fadeInLogo {{
            0% {{ opacity: 0; transform: scale(0.95); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
        </style>
    """, unsafe_allow_html=True)

    # Systemstatus
    st.markdown("<h3 style='color: #cccccc; margin-top: 30px;'>Systemstatus:</h3>", unsafe_allow_html=True)

    progress_bar = st.progress(0)
    percentage_display = st.empty()

    for percent_complete in range(101):
        time.sleep(0.02)
        progress_bar.progress(percent_complete)
        percentage_display.markdown(
            f"<p style='color: #ffffff; font-size:18px;'>Initialiserer AI-system... {percent_complete}%</p>",
            unsafe_allow_html=True
        )

    percentage_display.markdown(
        "<p style='color: #00FFAA; font-size:20px; font-weight:bold;'>100% - Forudsigelsesmodul klar</p>",
        unsafe_allow_html=True
    )

    # Glow-effekt til knappen
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: #007bff;
        color: white;
        font-weight: 600;
        padding: 0.6em 1.3em;
        border-radius: 10px;
        border: none;
        animation: pulseGlow 1.8s infinite alternate;
        transform-origin: center;
        transition: all 0.3s ease-in-out;
    }

    div.stButton > button:hover {
        background-color: #0088ff;
        box-shadow: 0 0 20px rgba(0, 200, 255, 0.9), 0 0 30px rgba(0, 200, 255, 0.6);
        transform: scale(1.08);
        cursor: pointer;
    }

    @keyframes pulseGlow {
        0% {
            transform: scale(1);
            box-shadow: 0 0 8px rgba(0, 123, 255, 0.5);
        }
        100% {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0, 123, 255, 0.9), 0 0 40px rgba(0, 123, 255, 0.5);
        }
    }
    </style>
""", unsafe_allow_html=True)




    # Knap til dashboard
    if st.button("Åbn Dashboard"):
        st.session_state.show_dashboard = True
        st.rerun()

    # Forecast + Vejrdata bokse i bunden
    st.markdown("""
        <div style='margin-top: 40px; display: flex; justify-content: center; gap: 30px;'>
            <div style='background: #002244; padding: 20px; border-radius: 12px; width: 200px;'>
                <h4 style='color: white;'>Forecast</h4>
                <p style='color: #88ccff;'>Dagens salg: 124 enheder</p>
            </div>
            <div style='background: #002244; padding: 20px; border-radius: 12px; width: 200px;'>
                <h4 style='color: white;'>Vejrdata</h4>
                <p style='color: #88ccff;'>Solrigt, 22°C</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.stop()





# === Dummy Dashboard ===
if st.session_state.show_dashboard:
    st.markdown("""
    <style>
        .stMarkdown h1, .stMarkdown p, .stMarkdown div, .stMarkdown span, .stMarkdown label {
            color: #f0f0f0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    st.title("📊 Optimate Demo Dashboard")
    st.success("Du er nu logget ind som demo-bruger!")
    st.write("(Her kan vi senere bygge et rigtigt dashboard med forecast, grafer osv.)")
    if st.button("Log ud"):
        st.session_state.authenticated = False
        st.session_state.show_dashboard = False
        st.rerun()
