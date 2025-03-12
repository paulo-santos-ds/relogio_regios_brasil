import streamlit as st
import datetime
import pytz
import time
import random

def get_color_palette():
    """Return a list of visually appealing colors that work well on a black background."""
    return [
        '#FF4136',  # Bright Red
        '#2ECC40',  # Bright Green
        '#0074D9',  # Bright Blue
        '#FF851B',  # Orange
        '#B10DC9',  # Purple
        '#39CCCC',  # Teal
        '#01FF70',  # Lime
        '#85144b',  # Maroon
        '#3D9970',  # Olive
        '#F012BE',  # Fuchsia
    ]

def get_localized_times():
    """Retrieve current times for different Brazilian time zones."""
    now = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    return {
        'noronha': now.astimezone(pytz.timezone('America/Noronha')),
        'amazonas': now.astimezone(pytz.timezone('America/Manaus')),
        'acre': now.astimezone(pytz.timezone('America/Rio_branco'))
    }

def format_date(dt):
    """Format date in Brazilian Portuguese."""
    weekdays = {
        'Monday': 'Segunda-Feira',
        'Tuesday': 'Terça-Feira',
        'Wednesday': 'Quarta-Feira',
        'Thursday': 'Quinta-Feira',
        'Friday': 'Sexta-Feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    months = {
        'January': 'Janeiro',
        'February': 'Fevereiro',
        'March': 'Março',
        'April': 'Abril',
        'May': 'Maio',
        'June': 'Junho',
        'July': 'Julho',
        'August': 'Agosto',
        'September': 'Setembro',
        'October': 'Outubro',
        'November': 'Novembro',
        'December': 'Dezembro'
    }
    
    weekday = weekdays.get(dt.strftime("%A"), dt.strftime("%A"))
    month = months.get(dt.strftime("%B"), dt.strftime("%B"))
    
    return f"{weekday}, {dt.day} de {month} de {dt.year}"

def main():
    # Configure page 
    st.set_page_config(page_title="Relógio Brasil", layout="centered", page_icon="⏰")
    
    # Color palette
    color_palette = get_color_palette()
    
    # Placeholder for tracking color change time
    if 'last_color_change' not in st.session_state:
        st.session_state.last_color_change = datetime.datetime.now()
        st.session_state.current_color = color_palette[0]
    
    # Placeholder for storing color index
    if 'color_index' not in st.session_state:
        st.session_state.color_index = 0
    
    # Custom CSS to ensure completely black background and dynamic color
    st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #000000 !important;
    }
    body {
        font-family: Arial, sans-serif;
    }
    .main-time { 
        font-size: 17rem; 
        text-align: center; 
        line-height: 1;
        margin-bottom: -10px;
    }
    .date { 
        font-size: 3rem; 
        text-align: center; 
        margin-bottom: 20px;
    }
    .subscribe { 
        font-size: 1.5rem; 
        text-align: center; 
        margin: 10px 0;
    }
    .time-zones {
        display: flex;
        justify-content: center;
        gap: 50px;
        font-size: 1.5rem;
    }
    .time-zone-name {
        font-size: 1.5rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main app logic
    placeholder = st.empty()
    
    # Real-time clock loop
    while True:
        # Check if 5 minutes have passed to change color
        current_time = datetime.datetime.now()
        if (current_time - st.session_state.last_color_change).total_seconds() >= 100:  # 5 minutes
            st.session_state.color_index = (st.session_state.color_index + 1) % len(color_palette)
            st.session_state.current_color = color_palette[st.session_state.color_index]
            st.session_state.last_color_change = current_time
        
        with placeholder.container():
            # Subscriber count with dynamic color
            st.markdown(f"<div class='subscribe' style='color: {st.session_state.current_color}'>HORARIO DE BRASILIA</div>", unsafe_allow_html=True)
            
            # Get current times
            times = get_localized_times()
            
            # Display main time with dynamic color
            st.markdown(f"<div class='main-time' style='color: {st.session_state.current_color}'>{current_time.strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
            
            # Display formatted date with dynamic color
            st.markdown(f"<div class='date' style='color: {st.session_state.current_color}'>{format_date(current_time)}</div>", unsafe_allow_html=True)
            
            
            # Time zones section with dynamic color in alphabetical order
            st.markdown(f"""
            <div class='time-zones' style='color: {st.session_state.current_color}'>
                <div>
                    <div class='time-zone-name'>ACRE</div>
                    <div>""" + times['acre'].strftime('%H:%M:%S') + """</div>
                </div>
                <div>
                    <div class='time-zone-name'>AMAZONAS</div>
                    <div>""" + times['amazonas'].strftime('%H:%M:%S') + """</div>
                </div>
                <div>
                    <div class='time-zone-name'>FERNANDO DE NORONHA</div>
                    <div>""" + times['noronha'].strftime('%H:%M:%S') + """</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Wait for next update
        time.sleep(1)

# Prevent code from running when imported
if __name__ == "__main__":
    main()