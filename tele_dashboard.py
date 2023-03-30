import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import nltk
import requests
import io
import json

from datetime import datetime
from random import randint
from wordcloud import WordCloud
from streamlit_extras.badges import badge
from PIL import Image
from nltk.sentiment import SentimentIntensityAnalyzer
from nlp import sentiment_analysis


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

        with st.expander("View sample Telegram chat file:"):

            # Create downloadable JSON format
            @st.cache
            def initial_json(url):
                data = requests.get(url).json()
                return json.dumps(data)

            st.download_button(
                label = 'Download sample JSON',
                file_name = 'sample_tele_chat_data.json',
                mime = 'application/json',
                help = 'Download sample Telegram JSON file',
                data = initial_json('https://raw.githubusercontent.com/tsu2000/tele_dashboard/main/sample.json')
            )
            
        preloaded_file = open("sample.json", "rb")

        uploaded_files = st.file_uploader('Upload all Telegram chat messages to be processed here (in `.json` format) - View [**instructions**](https://github.com/tsu2000/tele_dashboard/blob/main/instructions.md)', 
                                           accept_multiple_files = True,
                                           key = st.session_state.key,
                                           type = '.json',
                                           value = preloaded_file)

        if uploaded_files != []:
            st.markdown('---')
            clear_btn = st.button('Clear All')
            
            if clear_btn and 'key' in st.session_state.keys():
                st.session_state.pop('key')
                st.experimental_rerun()

    # Main page start
    if not uploaded_files:
        st.error('No files have been uploaded. Please upload at least 1 exported Telegram chat file (in `.json` format). If you have multiple `.json` files, upload them in chronological order. Try not to upload files which are too large (>200MB total), as they ~~may~~ **will** crash the app. You have been warned!', icon = '🚨')
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

        all_data = init_data

        # Obtaining statistics about the data
        message_sent = [x['from'] for x in all_data['messages'] if 'from' in x]
        users = list(set(message_sent))

        user_and_message_and_date = [[x['from'], ''.join([y['text'] for y in x['text_entities']]), x['date'][:10]] for x in all_data['messages'] if ('from' in x and 'text_entities' in x and 'date' in x)]
        
        # MAIN DATAFRAME
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

        # Dataframe for scatter plot
        df['Message word count'] = [len(msg.split()) for msg in df['Message']]
        df4 = df[df['Message word count'] != 0]
        avg_word_count = df4.groupby('User')['Message word count'].mean()
        
        df_scatter = pd.concat([avg_word_count, msg_counts], axis = 1).reset_index()
        df4 = df_scatter.rename(columns = {'index': 'User', 'Message word count': 'Average word count', 'User': 'Total messages sent'})

        alt_scatter_plot = alt.Chart(df4).mark_circle(size = 75, opacity = 0.75).encode(
            x = alt.X('Average word count', title = 'Average word count per message'),
            y = 'Total messages sent',
            color = 'User',
            tooltip = ['User', 'Average word count', 'Total messages sent']
        ).interactive()


        # # # # # # APP VISUALISATION START # # # # # #

        # Chat Metrics
        st.markdown(f"### Chat Overview - {all_data['name']}")
        col1, col2, col3 = st.columns(3)
        col1.metric('No. of Chat Users 👥', f'{len(set(users)):,}')
        col2.metric('No. of Messages &nbsp; 💬', f'{len(message_sent):,}')
        col3.metric("Chat Group Age &nbsp; 🗓️", f'{days:,} d')

        # Bar chart
        st.markdown('### Active users')
        st.altair_chart(alt_bar_chart, use_container_width = True)

        # Line chart
        st.markdown('### Daily no. of messages sent')
        st.altair_chart(alt_line_chart, use_container_width = True)

        # Scatter plot
        st.markdown('#### Average no. of words per message VS Total no. of messages sent')
        st.altair_chart(alt_scatter_plot, use_container_width = True)

        # Word cloud
        st.markdown('### Word Cloud')
        all_words = ' '.join(df['Message'])

        wc = WordCloud(mode = "RGBA", max_words = 100, background_color = None, width = 2000, height = 1000, margin = 2)
        wc_fig = wc.generate(all_words)
        
        st.image(wc_fig.to_array(), use_column_width = True)

        # Sentiment Analysis (Experimental)
        st.markdown('### Sentiment Analysis (Experimental)')
        st.markdown('**Disclaimer**: Sentiment analysis is limited to purely text messages in the chat group, with no support for stickers/emojis.')

        vader = SentimentIntensityAnalyzer()

        all_msg_df = df[df['Message'] != '']
        all_msg_df['Sentiment'] = all_msg_df['Message'].apply(lambda x: vader.polarity_scores(x)['compound'])
        all_msg_df['Sentiment Type'] = all_msg_df['Sentiment'].apply(lambda x: 'Positive' if x > 0 else 'Negative' if x < 0 else 'Neutral')

        summary_df = all_msg_df.groupby(['Sentiment Type']).agg({'Sentiment': 'sum', 'Sentiment Type': 'count'})

        # st.dataframe(summary_df, use_container_width = True)

        series = sentiment_analysis(summary_df)

        source = pd.DataFrame(index = series.index, data = series.values, columns = ['Percentage']).reset_index(names = 'Sentiment Type')

        chart = alt.Chart(source).mark_bar().encode(
            x = alt.X('Percentage', axis=alt.Axis(format='%')),
            y = 'Sentiment Type',
            color = alt.Color('Sentiment Type', scale = alt.Scale(range = ['#48C416', '#CEA200', '#DF2727']), legend = None)
        )

        text = chart.mark_text(align = 'left', dx = 5).encode(
            text = alt.Text('Percentage:Q', format = ',.2%'),
        )

        sentiment_final = (chart + text).properties(
            title = 'Percentage of each type of sentiment in chat group',
            width = 800,
            height = 300
        ).configure_title(
            fontSize = 15,
            offset = 15,
            anchor = 'middle'
        ).configure_axisX(
            titlePadding = 20
        ).configure_axisY(
            titlePadding = 20
        )

        st.altair_chart(sentiment_final, use_container_width = True)

        st.markdown('---')


if __name__ == "__main__":
    nltk.download('vader_lexicon')
    st.set_page_config(page_title = 'Telegram Dashboard', page_icon = '📈')
    main()
