from streamlit.web.server.websocket_headers import _get_websocket_headers
import streamlit as st
import scrape_songs
import find_neighbors
import database
import os

st.title("Find Similar Songs")

# text box for user to input a link
link = st.text_input("Enter a link to a song on YouTube")
button = st.button("Find Similar Songs")

def validate_yt_link(link):
    print(link)
    if "youtube.com" not in link and "youtu.be" not in link:
        return False
    return True

if button:
    session_id = _get_websocket_headers().get("Sec-Websocket-Key")
    sess_prefix = session_id[0:8]
    if validate_yt_link(link):
        st.write("Downloading song...")
        scrape_songs.temp_scrape_song(link, sess_prefix)
        if os.path.exists(sess_prefix + "temp.mp3"):
            db = database.Database()
            st.write("Finding similar songs...")
            results = find_neighbors.find_neighbors(sess_prefix+"temp.mp3")
            st.write("Results:")
            for result in results:
                st.write(result[0] + " - " + result[1])
                st.audio(db.get_file_by_song_name(result[0]))
            os.remove(sess_prefix + "temp.mp3")
    else:
        st.write("Invalid link")