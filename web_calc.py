import streamlit as st
import math

# --- ДАННЫЕ ---
rebar_data = {
    "6мм_6м": 1.5, "8мм_6м": 2.5, "10мм_6м": 4, "10мм_11.7м": 7.5,
    "12мм_6м": 6, "12мм_11.7м": 11, "14мм_11.7м": 15, "16мм_11.7м": 19,
    "18мм_11.7м": 24, "20мм_11.7м": 29.5, "22мм_11.7м": 35.5,
    "25мм_11.7м": 46, "28мм_11.7м": 57, "32мм_11.7м": 74,
    "36мм_11.7м": 94, "40мм_11.7м": 116
}

angle_data = {
    "Угол 25 (9м)": 13.5, "Угол 32 (9м)": 17.5, "Угол 40 (11.7м)": 29.0, 
    "Угол 45 (11.7м)": 32.5, "Угол 45 (9м)": 25.0, "Угол 50 (11.7м)": 45.0
}

st.set_page_config(page_title="Калькулятор v3.0", layout="centered")

if 'count' not in st.session_state:
    st.session_state.count = 0

def update_rebar_weight():
    c = st.session_state.count
    key = f"{st.session_state[f'dia_{c}']}_{st.session_state[f'len_{c}']}"
    st.session_state[f"w_r_{c}"] = float(rebar_data.get(key, 0.0))

def update_angle_weight():
    c = st.session_state.count
    st.session_state[f"w_a_{c}"] = float(angle_data.get(st.session_state[f'type_a_{c}'], 0.0))

# --- ФИНАЛЬНЫЙ CSS (БЛОКИРОВКА ЛИШНИХ ПОЛЕЙ ВВОДА) ---
st.markdown("""
    <style>
    .stApp { background-color: #dee2e6; }
    
    /* 1. Скрываем стандартные заголовки */
    [data-testid="stWidgetLabel"] { display: none !important; }

    /* 2. СКРЫВАЕМ ПОЛЕ ПОИСКА ВНУТРИ SELECTBOX (те самые лишние поля) */
    div[data-baseweb="select"] input {
        position: absolute !important;
        width: 1px !important;
        height: 1px !important;
        padding: 0 !important;
        margin: -1px !important;
        overflow: hidden !important;
        clip: rect(0,0,0,0) !important;
        border: 0 !important;
    }
    
    /* 3. Обычные поля ввода (числовые) оставляем с рамками */
    input[type="number"] {
        border: 2px solid #6c757d !important;
        border-radius: 5px !important;
        background-color: white !important;
    }

    /* Настройка обертки выпадающего списка */
    div[data-baseweb="select"] {
        border: 2px solid #6c757d !important;
        border-radius: 5px !important;
        background-color: white !important;
    }

    .custom-label {
        font-size: 1.1rem !important;
        font-weight: bold !important;
        color: #212529 !important;
        margin: 10px 0px 2px 0px !important;
    }

    div.stButton > button { 
        background-color: #ff8c00 !important; 
        color: white !important; 
        font-weight: bold !important; 
    }
    
    .sub-title { 
        font-size: 1.5rem !important; 
        font-weight: 800; 
        color: #343a40; 
        text-align: center; 
    }

    [data-testid="stVerticalBlockBorderWrapper"] { 
        background-color: #f8f9fa !important; 
        border: 1px solid #adb5bd !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="sub-title">Предварительный расчет</p>', unsafe_allow_html=True)

if st.button("🔄 ОЧИСТИТЬ ВСЕ", use_container_width=True):
    st.session_state.count += 1
    st.rerun()

c = st.session_state.count

# --- АРМАТУРА ---
st.subheader("АРМАТУРА")
with st.container(border=True):
    if f"w_r_{c}" not in st.session_state: st.session_state[f"w_r_{c}"] = 1.5
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="custom-label">Диаметр</p>', unsafe_allow_html=True)
        st.selectbox("D", ["6мм","8мм","10мм","12мм","14мм","16мм","18мм","20мм","22мм","25мм","28мм","32мм","36мм","40мм"], 
                     key=f"dia_{c}", on_change=update_rebar_weight, label_visibility="collapsed")
    with col2:
        st.markdown('<p class="custom-label">Длина</p>', unsafe_allow_html=True)
        st.selectbox("L", ["6м", "11.7м"], key=f"len_{c}", on_change=update_rebar_weight, label_visibility="collapsed")
    
    st.markdown('<p class="custom-label">Вес 1 прутка (кг)</p>', unsafe_allow_html=True)
    st.number_input("W", step=0.1, key=f"w_r_{c}", label_visibility="collapsed")
    cur_w_r = st.session_state[f"w_r_{c}"]
    
    st.write(f"Текущий вес: **:blue[{cur_w_r} кг]**")
    
    st.markdown('<p class="custom-label">Ввести тонн</p>', unsafe_allow_html=True)
    t_r = st.number_input("T", min_value=0.0, step=0.001, format="%.3f", key=f"t_r_{c}", label_visibility="collapsed")
    
    if cur_w_r > 0:
        c_ex = (t_r * 1000) / cur_w_r
        sug = math.ceil(c_ex) if (c_ex - int(c_ex)) >= 0.3 else math.floor(c_ex)
        st.write(f"Шт точно: `{c_ex:.1f}`")
        st.info(f"**ПРЕДЛАГАЕМ: {sug} шт**")
        st.success(f"**ИТОГО: {(sug * cur_w_r) / 1000:.3f} тонн**")

    st.markdown('<p class="custom-label">Ввести кол-во шт (заказ)</p>', unsafe_allow_html=True)
    p_r = st.number_input("P", min_value=0, step=1, key=f"p_r_{c}", label_visibility="collapsed")
    if p_r > 0:
        st.warning(f"**Результат: {(p_r * cur_w_r) / 1000:.3f} тонн**")

# --- УГОЛОК ---
st.subheader("УГОЛОК")
with st.container(border=True):
    if f"w_a_{c}" not in st.session_state: st.session_state[f"w_a_{c}"] = 13.5

    st.markdown('<p class="custom-label">Тип уголка</p>', unsafe_allow_html=True)
    st.selectbox("A", list(angle_data.keys()), key=f"type_a_{c}", on_change=update_angle_weight, label_visibility="collapsed")
    
    st.markdown('<p class="custom-label">Вес 1 шт (кг)</p>', unsafe_allow_html=True)
    st.number_input("WA", step=0.1, key=f"w_a_{c}", label_visibility="collapsed")
    cur_w_a = st.session_state[f"w_a_{c}"]
    
    st.write(f"Текущий вес: **:blue[{cur_w_a} кг]**")
    
    st.markdown('<p class="custom-label">Ввести тонн</p>', unsafe_allow_html=True)
    t_a = st.number_input("TA", min_value=0.0, step=0.001, format="%.3f", key=f"t_a_{c}", label_visibility="collapsed")
    
    if cur_w_a > 0:
        c_ex_a = (t_a * 1000) / cur_w_a
        sug_a = math.ceil(c_ex_a) if (c_ex_a - int(c_ex_a)) >= 0.3 else math.floor(c_ex_a)
        st.write(f"Шт точно: `{c_ex_a:.1f}`")
        st.info(f"**ПРЕДЛАГАЕМ: {sug_a} шт**")
        st.success(f"**ИТОГО: {(sug_a * cur_w_a) / 1000:.3f} тонн**")
    
    st.markdown('<p class="custom-label">Ввести кол-во шт (заказ)</p>', unsafe_allow_html=True)
    p_a = st.number_input("PA", min_value=0, step=1, key=f"p_a_{c}", label_visibility="collapsed")
    if p_a > 0:
        st.warning(f"**Результат: {(p_a * cur_w_a) / 1000:.3f} тонн**")
