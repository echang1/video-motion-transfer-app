import streamlit as st
import os
import time

# Streamlit App Configuration
st.title("Image-to-Video Motion Transfer")
st.write("This app serves as a demo for the following paper:")
st.write("Enhancing Bandwidth Efficiency for Video Motion Transfer Applications Using Deep Learning Based Keypoint Prediction")
st.write("written by Xue Bai et al. (2024)")
st.write("To use this demo, first select an image below by pressing the 'Select Image' button. Then, from the available remaining videos below, select a video to transfer onto your image. Finally, press the 'Process' button to view the resulting video. At any time, you may press the 'Reset All' button to start over from the beginning")

file_dir = "files"
files = os.listdir(file_dir)

# Separate still images, driver videos, and transfer videos
still_images = sorted([f for f in files if f.endswith('still.JPG')])
driver_videos = sorted([f for f in files if f.endswith('driver_video.mp4')])

# Manually define a mapping between (still_image, driver_video) -> transfer_video
transfer_video_map = {
    ("1-still.JPG", "1_driver_video.mp4"): "1-transfer-video.mov",
    ("2-still.JPG", "2_driver_video.mp4"): "2-transfer-video.mov",
    ("3-still.JPG", "3_driver_video.mp4"): "3-transfer-video.mov",
    ("4-still.JPG", "4_driver_video.mp4"): "4-transfer-video.mov",
}

# Initialize session state to store selections
if 'selected_still' not in st.session_state:
    st.session_state.selected_still = None
if 'selected_driver' not in st.session_state:
    st.session_state.selected_driver = None

# Reset All button
if st.button("Reset All"):
    st.session_state.selected_still = None
    st.session_state.selected_driver = None
    st.rerun()  # Rerun the script to refresh the state

# Function to check if an image and video are a valid match
def is_valid_match(still, video):
    return (still, video) in transfer_video_map

# Create a grid layout for still images
st.header("Select Still Image")
image_cols = st.columns(4)  # Adjust the number of columns as needed

for col, img in zip(image_cols, still_images):
    with col:
        # Determine whether this image should be disabled based on selection
        if st.session_state.selected_driver and not is_valid_match(img, st.session_state.selected_driver):
            disabled = True
        else:
            disabled = False

        # Display the image
        st.image(os.path.join(file_dir, img), width=155)

        img_number = img.split("-")[0]
        # Create a button for the image, disable if needed
        if st.button(f"Select Image {img_number}", key=img, disabled=disabled):
            st.session_state.selected_still = img

# Create a grid layout for driver videos
st.header("Select Driver Video")
video_cols = st.columns(4)  # Adjust the number of columns as needed

for col, vid in zip(video_cols, driver_videos):
    with col:
        # Determine whether this video should be disabled based on selection
        if st.session_state.selected_still and not is_valid_match(st.session_state.selected_still, vid):
            disabled = True
        else:
            disabled = False

        # Display the video
        st.video(os.path.join(file_dir, vid))

        vid_number = vid.split("_")[0]

        # Create a button for the video, disable if needed
        if st.button(f"Select Video {vid_number}", key=vid, disabled=disabled):
            st.session_state.selected_driver = vid

# Show the Process button when both are selected
if st.session_state.selected_still and st.session_state.selected_driver:
    if st.button("Process"):
        with st.spinner('Processing...'):
            time.sleep(2)  # Simulate loading screen

        # Use the tuple of (selected_still, selected_driver) to get the corresponding transfer video
        transfer_key = (st.session_state.selected_still, st.session_state.selected_driver)
        transfer_video = transfer_video_map.get(transfer_key)

        if transfer_video:
            # Show the transfer video after processing
            st.video(os.path.join(file_dir, transfer_video))
        else:
            st.error("No transfer video found for the selected still image and driver video.")

# Bio section at the bottom
st.header("About Me")
col1, col2 = st.columns([1, 2])
with col1:
    st.image("headshot.JPG", width=120)  # Replace with the actual path to your image
with col2:
    st.markdown("""
    **Name:** Elliot Chang  
    **School:** West Virginia University  
    **Email:** sc00048@mix.wvu.edu  
    **Bio:** I am an undergraduate student at WVU studying Mathematics and Data Science.  
    This app was built as part of the course requirements for DSCI 450 at WVU in Fall 2024. Enjoy!
    """)