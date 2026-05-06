import html as html_module
import pickle

import folium
import pandas as pd
import numpy as np
import streamlit as st
from streamlit.components.v1 import html as components_html
import streamlit as st
from streamlit.components.v1 import html as components_html

# —— Layout: main column ratio ≈ 1.618 : 1 (map : control panel) ——
MAP_COL_WEIGHT = 1.618
PANEL_COL_WEIGHT = 1.0
MAP_IFRAME_HEIGHT_PX = 420
MARKER_RADIUS_PX = 9
# Pin matches primary (indigo) so the map does not introduce a second accent hue
MARKER_HEX = "#4338ca"

st.set_page_config(
    page_title="Traffic Accident Risk",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        /* —— Palette: zinc neutrals + indigo accent; risk = same card + semantic stripe only —— */
        :root {
            --ink: #18181b;
            --ink-muted: #52525b;
            --caption: #71717a;
            --line: #e4e4e7;
            --line-strong: #d4d4d8;
            --surface-page: #f4f4f5;
            --surface-elevated: #ffffff;
            --surface-sidebar: #fafafa;
            --sidebar-bg-top: #27272a;
            --sidebar-bg-bottom: #18181b;
            --sidebar-border: #3f3f46;
            --sidebar-text: #f4f4f5;
            --sidebar-muted: #a1a1aa;
            --sidebar-subtle: #71717a;
            --sidebar-input-bg: #3f3f46;
            --sidebar-input-border: #52525b;
            --primary: #4f46e5;
            --primary-hover: #6366f1;
            --primary-active: #4338ca;
            --primary-ink: #fafafa;
            --space-1: 0.25rem;
            --space-2: 0.5rem;
            --space-3: 0.75rem;
            --space-4: 1rem;
            --space-5: 1.25rem;
            --space-6: 1.5rem;
            --space-8: 2rem;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 14px;
            --font-xs: 0.75rem;
            --font-sm: 0.8125rem;
            --font-base: 1rem;
            --font-lg: 1.0625rem;
            --font-xl: clamp(1.5rem, 2.2vw, 1.875rem);
            --font-hero-sub: clamp(0.9375rem, 1.1vw, 1.0625rem);
            --shadow-sm: 0 1px 2px rgba(24, 24, 27, 0.04);
            --shadow-md: 0 4px 14px rgba(24, 24, 27, 0.08);
            /* Risk: shared neutral surface; only accent stripe + label hue shift */
            --risk-card-bg: #fafafa;
            --risk-title: #18181b;
            --risk-body: #52525b;
            --risk-low-stripe: #16a34a;
            --risk-mid-stripe: #d97706;
            --risk-high-stripe: #dc2626;
            --risk-low-soft: rgba(22, 163, 74, 0.08);
            --risk-mid-soft: rgba(217, 119, 6, 0.09);
            --risk-high-soft: rgba(220, 38, 38, 0.08);
        }

        div[data-testid="stAppViewContainer"] > .main {
            background: var(--surface-page);
        }
        .block-container {
            padding-top: var(--space-6);
            padding-bottom: var(--space-8);
            max-width: 1120px;
        }
        section[data-testid="stSidebar"] {
            background: var(--sidebar-bg-bottom);
        }
        section[data-testid="stSidebar"] > div {
            background: linear-gradient(
                180deg,
                var(--sidebar-bg-top) 0%,
                var(--sidebar-bg-bottom) 100%
            ) !important;
            border-right: 1px solid var(--sidebar-border);
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: var(--space-5);
            background-color: transparent !important;
            color: var(--sidebar-text);
        }
        section[data-testid="stSidebar"] .section-label {
            color: var(--sidebar-text) !important;
        }
        section[data-testid="stSidebar"] .section-hint {
            color: var(--sidebar-muted) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] label p {
            color: var(--sidebar-text) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p span {
            color: var(--sidebar-muted) !important;
        }
        section[data-testid="stSidebar"] [data-baseweb="base-input"] input,
        section[data-testid="stSidebar"] [data-testid="stNumberInputField"] {
            background-color: var(--sidebar-input-bg) !important;
            color: var(--sidebar-text) !important;
            border-color: var(--sidebar-input-border) !important;
            caret-color: var(--primary-hover);
        }
        section[data-testid="stSidebar"] [data-baseweb="input"] {
            background-color: var(--sidebar-input-bg) !important;
            border-color: var(--sidebar-input-border) !important;
        }
        section[data-testid="stSidebar"] hr {
            border: none;
            border-top: 1px solid var(--sidebar-border);
            margin: var(--space-4) 0;
        }
        section[data-testid="stSidebar"] [data-testid="stThumbValue"] {
            color: var(--sidebar-text) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
            background-color: var(--primary) !important;
            border: 2px solid #e0e7ff !important;
        }
        section[data-testid="stSidebar"] [data-baseweb="slider"] [data-baseweb="track"] > div {
            background-color: var(--sidebar-input-border) !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stExpander"] details {
            border: 1px solid var(--sidebar-border);
            border-radius: var(--radius-sm);
            background: rgba(39, 39, 42, 0.85);
        }
        section[data-testid="stSidebar"] div[data-testid="stExpander"] summary,
        section[data-testid="stSidebar"] div[data-testid="stExpander"] summary span,
        section[data-testid="stSidebar"] div[data-testid="stExpander"] summary p {
            color: var(--sidebar-text) !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stExpander"] .risk-legend {
            color: var(--sidebar-muted) !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stExpander"] .risk-legend strong {
            color: var(--sidebar-text) !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stExpander"] .risk-legend__swatch {
            border-color: var(--sidebar-input-border) !important;
        }

        .hero-title {
            font-weight: 700;
            letter-spacing: -0.03em;
            color: var(--ink);
            font-size: var(--font-xl);
            line-height: 1.2;
            margin: 0 0 var(--space-2) 0;
        }
        .hero-sub {
            color: var(--ink-muted);
            font-size: var(--font-hero-sub);
            line-height: 1.55;
            max-width: 52ch;
            margin: 0 0 var(--space-6) 0;
        }
        .section-label {
            font-size: var(--font-sm);
            font-weight: 600;
            color: var(--ink);
            letter-spacing: 0.02em;
            margin: 0 0 var(--space-2) 0;
        }
        .section-hint {
            font-size: var(--font-xs);
            color: var(--caption);
            line-height: 1.45;
            margin: 0 0 var(--space-4) 0;
        }

        .stButton > button {
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: var(--font-sm);
            min-height: 48px;
            padding: var(--space-3) var(--space-5);
            border: none;
            background: var(--primary);
            color: var(--primary-ink) !important;
            box-shadow: var(--shadow-sm);
            transition: background 0.15s ease, box-shadow 0.15s ease;
        }
        .stButton > button:hover {
            background: var(--primary-hover) !important;
            color: var(--primary-ink) !important;
            border: none;
            box-shadow: var(--shadow-md);
        }
        .stButton > button:active {
            background: var(--primary-active) !important;
        }
        .stButton > button:focus-visible {
            outline: 2px solid var(--primary-active);
            outline-offset: 2px;
        }

        div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div:has(iframe) {
            border-radius: var(--radius-md);
            overflow: hidden;
            border: 1px solid var(--line);
            box-shadow: var(--shadow-sm);
        }

        [data-testid="stMetricValue"] {
            font-size: 1.35rem !important;
            font-weight: 600 !important;
            color: var(--ink) !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: var(--font-xs) !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--caption) !important;
        }

        .risk-result {
            border-radius: var(--radius-md);
            padding: var(--space-5) var(--space-6);
            margin: var(--space-3) 0 var(--space-5) 0;
            border: 1px solid var(--line);
            border-left: 4px solid var(--risk-stripe, var(--line-strong));
            background: var(--risk-card-bg);
            box-shadow: var(--shadow-sm);
        }
        .risk-result__title {
            font-size: var(--font-lg);
            font-weight: 700;
            margin: 0 0 var(--space-2) 0;
            line-height: 1.3;
            color: var(--risk-title);
        }
        .risk-result__body {
            font-size: var(--font-sm);
            margin: 0;
            line-height: 1.55;
            color: var(--risk-body);
        }
        .risk-result--0 {
            --risk-stripe: var(--risk-low-stripe);
            background: linear-gradient(90deg, var(--risk-low-soft) 0%, var(--risk-card-bg) 14%);
        }
        .risk-result--1 {
            --risk-stripe: var(--risk-mid-stripe);
            background: linear-gradient(90deg, var(--risk-mid-soft) 0%, var(--risk-card-bg) 14%);
        }
        .risk-result--2 {
            --risk-stripe: var(--risk-high-stripe);
            background: linear-gradient(90deg, var(--risk-high-soft) 0%, var(--risk-card-bg) 14%);
        }

        .risk-legend {
            display: flex;
            flex-direction: column;
            gap: var(--space-2);
            font-size: var(--font-sm);
            color: var(--ink-muted);
            margin-top: var(--space-2);
        }
        .risk-legend__row {
            display: flex;
            align-items: center;
            gap: var(--space-3);
        }
        .risk-legend__swatch {
            width: 12px;
            height: 12px;
            border-radius: 3px;
            flex-shrink: 0;
            border: 1px solid var(--line-strong);
        }
        .risk-legend__swatch--0 { background: var(--risk-low-stripe); border-color: #86efac; }
        .risk-legend__swatch--1 { background: var(--risk-mid-stripe); border-color: #fcd34d; }
        .risk-legend__swatch--2 { background: var(--risk-high-stripe); border-color: #fca5a5; }

        .callout-idle {
            font-size: var(--font-sm);
            color: var(--ink-muted);
            background: var(--surface-elevated);
            border: 1px dashed var(--line);
            border-radius: var(--radius-md);
            padding: var(--space-5);
            line-height: 1.55;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    with open("models/model.pkl", "rb") as f:
        return pickle.load(f)

# @st.cache_data
def get_dataset_hierarchy():
    try:
        df = pd.read_csv("data/traffic.csv")
        # Build hierarchy: State -> District -> City -> Mean Coords
        hierarchy = {}
        for state, s_df in df.groupby('state'):
            hierarchy[state] = {}
            for district, d_df in s_df.groupby('district'):
                hierarchy[state][district] = {}
                for city, c_df in d_df.groupby('city'):
                    hierarchy[state][district][city] = {
                        'lat': c_df['latitude'].mean(),
                        'lon': c_df['longitude'].mean()
                    }
        return hierarchy
    except Exception:
        return {}

model = load_model()
location_hierarchy = get_dataset_hierarchy()

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

if "lat" not in st.session_state:
    st.session_state.lat = 20.5937  # Center of India
if "lon" not in st.session_state:
    st.session_state.lon = 78.9629
if "address" not in st.session_state:
    st.session_state.address = "India"

# No longer needed as search box is removed

def reverse_geocode():
    # Reverse geocoding disabled with search box removal to keep app clean
    pass

def update_from_city_dropdown():
    state = st.session_state.state_dropdown
    district = st.session_state.get('district_dropdown', '-- Select District --')
    city = st.session_state.get('city_dropdown', '-- Select City --')
    
    if (state in location_hierarchy and 
        district in location_hierarchy[state] and 
        city in location_hierarchy[state][district]):
        
        coords = location_hierarchy[state][district][city]
        # Update both the main state and the widget keys to force UI refresh
        st.session_state.lat = coords['lat']
        st.session_state.lon = coords['lon']
        st.session_state.lat_input = coords['lat']
        st.session_state.lon_input = coords['lon']
        st.session_state.address = f"{city}, {district}, {state}"

st.markdown(
    '<h1 class="hero-title">Traffic accident risk</h1>'
    "<p class=\"hero-sub\">Adjust time and location in the sidebar, then run a prediction. "
    "The layout uses a fixed spacing scale and a wide main row so the map and results stay balanced.</p>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<p class="section-label">Inputs</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-hint">One row to the model: hour, calendar day, coordinates.</p>',
        unsafe_allow_html=True,
    )
    hour = st.slider(
        "Hour of day",
        0,
        23,
        12,
        help="0 = midnight · 23 = 11 PM",
    )
    day = st.slider("Day of month", 1, 31, 15)
    st.markdown('<p class="section-label">Location</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-hint">Drill down by State → District → City or enter coordinates.</p>',
        unsafe_allow_html=True,
    )

    if location_hierarchy:
        states = sorted(list(location_hierarchy.keys()))
        selected_state = st.selectbox(
            "Select State",
            options=["-- Select State --"] + states,
            key="state_dropdown"
        )
        
        if selected_state != "-- Select State --":
            districts = sorted(list(location_hierarchy[selected_state].keys()))
            selected_district = st.selectbox(
                "Select District",
                options=["-- Select District --"] + districts,
                key="district_dropdown"
            )
            
            if selected_district != "-- Select District --":
                cities = sorted(list(location_hierarchy[selected_state][selected_district].keys()))
                st.selectbox(
                    "Select City/Town",
                    options=["-- Select City --"] + cities,
                    key="city_dropdown",
                    on_change=update_from_city_dropdown
                )
    
    # Search box removed as requested

    col_la, col_lo = st.columns(2)
    with col_la:
        lat = st.number_input(
            "Latitude", 
            value=st.session_state.lat, 
            format="%.4f", 
            key="lat_input",
            on_change=reverse_geocode
        )
    with col_lo:
        lon = st.number_input(
            "Longitude", 
            value=st.session_state.lon, 
            format="%.4f", 
            key="lon_input",
            on_change=reverse_geocode
        )
    
    # Update state from inputs if not already handled by callbacks
    st.session_state.lat = lat
    st.session_state.lon = lon

    with st.expander("Risk scale (model classes)", expanded=False):
        st.markdown(
            '<div class="risk-legend">'
            '<div class="risk-legend__row"><span class="risk-legend__swatch risk-legend__swatch--0"></span>'
            "<span><strong>Low</strong> · class 0</span></div>"
            '<div class="risk-legend__row"><span class="risk-legend__swatch risk-legend__swatch--1"></span>'
            "<span><strong>Medium</strong> · class 1</span></div>"
            '<div class="risk-legend__row"><span class="risk-legend__swatch risk-legend__swatch--2"></span>'
            "<span><strong>High</strong> · class 2</span></div>"
            "</div>",
            unsafe_allow_html=True,
        )

input_data = np.array([[hour, day, lat, lon]])

left, right = st.columns([MAP_COL_WEIGHT, PANEL_COL_WEIGHT], gap="large")

with left:
    st.markdown('<p class="section-label">Map preview</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-hint">Light basemap so the location pin stays easy to see.</p>',
        unsafe_allow_html=True,
    )
    m = folium.Map(location=[lat, lon], zoom_start=6, tiles="CartoDB positron")
    # Halo first (meters) so the point marker draws above it
    folium.Circle(
        location=[lat, lon],
        radius=2200,
        color=MARKER_HEX,
        fill=True,
        fill_opacity=0.08,
        weight=1,
    ).add_to(m)
    folium.CircleMarker(
        location=[lat, lon],
        radius=MARKER_RADIUS_PX,
        color=MARKER_HEX,
        weight=2,
        fill=True,
        fill_color=MARKER_HEX,
        fill_opacity=0.88,
        popup=f"{lat:.4f}, {lon:.4f}",
    ).add_to(m)
    components_html(m._repr_html_(), height=MAP_IFRAME_HEIGHT_PX)

with right:
    st.markdown('<p class="section-label">Prediction</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-hint">Runs the model on the values from the sidebar.</p>',
        unsafe_allow_html=True,
    )
    predict = st.button("Predict accident risk", use_container_width=True)

    if predict:
        st.session_state.last_prediction = int(model.predict(input_data)[0])

    pred = st.session_state.last_prediction

    if pred is None:
        st.markdown(
            '<div class="callout-idle">Set the sidebar inputs, then choose <strong>Predict accident risk</strong> '
            "to see the risk panel and a snapshot of what was sent to the model.</div>",
            unsafe_allow_html=True,
        )
    else:
        risk_copy = {
            0: (
                "Low risk",
                "The model suggests comparatively safer conditions for this time and place.",
            ),
            1: (
                "Medium risk",
                "Elevated versus low-risk cases. Useful as one signal among many.",
            ),
            2: (
                "High risk",
                "The model flags higher risk for this combination. Use for planning, not as sole ground truth.",
            ),
        }
        title, body = risk_copy.get(pred, risk_copy[1])
        safe_title = html_module.escape(title)
        safe_body = html_module.escape(body)
        st.markdown(
            f'<div class="risk-result risk-result--{pred}" role="status">'
            f'<p class="risk-result__title">{safe_title}</p>'
            f'<p class="risk-result__body">{safe_body}</p>'
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown('<p class="section-label">Input snapshot</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-hint">Same numbers the model just used.</p>',
            unsafe_allow_html=True,
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Hour", f"{hour:02d}:00")
        c2.metric("Day", str(day))
        c3.metric("Latitude", f"{lat:.3f}")
        c4.metric("Longitude", f"{lon:.3f}")
