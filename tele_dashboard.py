import streamlit as st
import pandas as pd
import altair as alt
import requests
import io
import json

from datetime import datetime
from random import randint
from wordcloud import WordCloud
from streamlit_extras.badges import badge
from PIL import Image


def main():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

    # Create title and header
    col1, col2, col3 = st.columns([0.047, 0.265, 0.035])
    
    with col1:
        url = 'https://github.com/tsu2000/tele_dashboard/raw/main/images/telegram.png'
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        st.image(img, output_format = 'png')

    with col2:
        st.title('&nbsp; Telegram Chat Dashboard')

    with col3:
        badge(type = 'github', name = 'tsu2000/tele_dashboard', url = 'https://github.com/tsu2000/tele_dashboard')

    st.markdown('---')

    # Create sidebar to read files
    with st.sidebar:
        st.title('📤 &nbsp; User Inputs')

        if 'key' not in st.session_state: 
            st.session_state.key = str(randint(1000, 100000000))

        uploaded_files = st.file_uploader('Upload all Telegram chat messages to be processed here (in `.json` format) - View [**instructions**](https://github.com/tsu2000/tele_dashboard/blob/main/instructions.md)', 
                                           accept_multiple_files = True,
                                           key = st.session_state.key,
                                           type = '.json')

        if uploaded_files != []:
            st.markdown('---')
            clear_btn = st.button('Clear All')
            
            if clear_btn and 'key' in st.session_state.keys():
                st.session_state.pop('key')
                st.experimental_rerun()

    # Main page start
    if not uploaded_files:
        st.error('No files have been uploaded. Please upload at least 1 exported Telegram chat file (in `.json` format). If you have multiple `.json` files, upload them in chronological order. However if the file size is too large the app may crash.', icon = '🚨')
    else:
        raw_data_files = []

        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            raw_data_files.append(bytes_data)

        @st.cache
        def days_between(d1, d2):
            d1 = datetime.strptime(d1, "%Y-%m-%d")
            d2 = datetime.strptime(d2, "%Y-%m-%d")
            return abs((d2 - d1).days)

        # Data processing
        days = days_between(json.loads(raw_data_files[0])['messages'][0]['date'][:10], datetime.now().strftime('%Y-%m-%d'))

        # Determing length of JSON object
        init_data = json.loads(raw_data_files[0])

        if len(raw_data_files) > 1:
            for rdf in raw_data_files[1:]:
                more_data = json.loads(rdf)
                init_data['messages'].extend(more_data['messages'])

        # Obtaining statistics about the data
        all_data = init_data

        message_sent = [x['from'] for x in all_data['messages'] if 'from' in x]
        users = list(set(message_sent))

        user_and_message_and_date = [[x['from'], ''.join([y['text'] for y in x['text_entities']]), x['date'][:10]] for x in all_data['messages'] if ('from' in x and 'text_entities' in x and 'date' in x)]
        
        # Main dataframe
        df = pd.DataFrame(data = user_and_message_and_date, columns = ['User', 'Message', 'Date'])

        # Dataframe for bar chart
        msg_counts = df['User'].value_counts()
        d2 = {'User': msg_counts.index, 'Total Message Count': msg_counts.values}
        df2 = pd.DataFrame(data = d2)

        alt_bar_chart = alt.Chart(df2).mark_bar().encode(
            x = alt.X('Total Message Count:Q'),
            y = alt.Y('User:N', sort = alt.EncodingSortField(field = "User", op = "count", order = 'ascending')),
            color = alt.Color('User', sort = '-x')
        )

        # Dataframe for line chart
        dates = df['Date'].value_counts()
        d3 = {'Date': dates.index, 'Daily Messages Sent': dates.values}
        df3 = pd.DataFrame(data = d3)
        df3['Date'] = pd.to_datetime(df3['Date'])

        alt_line_chart = alt.Chart(df3).mark_line(
            point = alt.OverlayMarkDef(color = 'green', shape = 'diamond')
        ).encode(
            x = 'Date:T',
            y = 'Daily Messages Sent',
            color = alt.value('green'),
        ).interactive()

        # APP VISUALISATION START

        # Chat Metrics
        st.markdown(f"### Chat Overview - {all_data['name']}")
        col1, col2, col3 = st.columns(3)
        col1.metric('No. of Users &nbsp; 👥', len(set(users)))
        col2.metric('No. of Messages &nbsp; 💬', len(message_sent))
        col3.metric("Chat group age &nbsp; 🗓️", f'{days} d')

        # Bar chart
        st.markdown('### Most active users')    
        st.altair_chart(alt_bar_chart, use_container_width = True)

        # Line chart
        st.markdown('### Daily no. of messages sent')
        st.altair_chart(alt_line_chart, use_container_width = True)

        # Word cloud
        st.markdown('### Word Cloud')
        all_words = ' '.join(df['Message'])

        wc = WordCloud(mode = "RGBA", background_color = None, width = 800, height = 300, margin = 2)
        fig = wc.generate(all_words)
        
        st.image(fig.to_array(), use_column_width = True)

        st.markdown('---')


if __name__ == "__main__":
    st.set_page_config(page_title = 'Telegram Dashboard', page_icon = '📈')
    main()