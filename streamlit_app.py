import streamlit as st
import cv2
import numpy as np
import requests
from copy import deepcopy
import os

CLASS_NAMES = ["1 cent", "25 cents"]
DIAMETER_MM ={CLASS_NAMES[0]: 19.05, CLASS_NAMES[1]: 24.3, "Unknown coin": 0}


ENDPOINT = os.getenv("ENDPOINT", "http://127.0.0.1:5000/measure")

STATUS_MAP = {
    0: "Success",
    1: "Could not detect hand",
    2: "Could not detect the coin. Replace the coin or adjust camera position",
    3: "More than 1 coin detected",
    4: "Small measurement - Please verify sizes",
    5: "Large measurement - Please verify sizes",
    6: "Could not detect the coin. Replace the coin or adjust camera position",
    7: "Invalid input",
}

def request_image_distance(image):
    files = {'image': image}
    response = requests.post(ENDPOINT, files=files)
    print(response.status_code)
    print(response.text)
    return response.json()


st.title("Hand Measurements")

st.write("This application measures the distance between the thumb and the index finger")

# diameter_mm = st.number_input("Diameter of the coin in mm", value=23)

st.write("Upload an image of your hand with a coin in the frame")

file_upload = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
# use_camera = st.button("Use Camera")
# st.session_state['use_camera'] = st.session_state.get(
#     'use_camera', False) or use_camera

# if st.session_state['use_camera']:
#     img_file_buffer = st.camera_input("Take a picture")
#     if img_file_buffer is not None:
#         # To read image file buffer as bytes:
#         file_upload = img_file_buffer

if file_upload:
    with st.spinner("Measuring..."):
        file_upload_copy = deepcopy(file_upload)
        result = request_image_distance(file_upload)
        st.markdown(f"# Status: {result['status']}")
        st.markdown(f"# {STATUS_MAP[result['status']]}")
        st.markdown(f"# Distance: {result['distance']}")
        st.markdown(f"# Coin: {result['coin_class']}")
        st.markdown(f"# Diameter: {DIAMETER_MM[result['coin_class']]} mm")
        image = cv2.imdecode(np.frombuffer(
            file_upload_copy.read(), np.uint8), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Resize the image to fit the screen
        st.image(image, caption="Uploaded Image", width=300)
