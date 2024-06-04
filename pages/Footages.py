import streamlit as st

st.title("Video Player")

video_file = open("cctv_footages/veh2.mp4", 'rb')

video_bytes = video_file.read()

st.video(video_file, format="video/mp4", start_time=0,
         subtitles=None, end_time=None,
         loop=False, autoplay=False, muted=False)