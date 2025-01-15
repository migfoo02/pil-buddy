import streamlit as st
import requests
import ast
import pandas as pd

URL = "http://127.0.0.1:8000/extract_from_doc"

st.title("PillBuddy 💊")

# Option for uploading file or capturing image with the camera
option = st.radio("Choose input method", ("Upload Image", "Capture with Camera"))

file = None
camera_image = None
img = None

if option == "Upload Image":
    file = st.file_uploader("Upload file", type="png")

elif option == "Capture with Camera":
    camera_image = st.camera_input("Capture Image")

# If file or camera image is provided and button is clicked
if (file or camera_image) and st.button("Scan Image", type="primary"):
    # Show progress bar
    progress_bar_placeholder = st.empty()
    bar = progress_bar_placeholder.progress(0)
    
    # Prepare payload for API request
    if file:
        files = [('file', file.getvalue())]
    elif camera_image:
        files = [('file', camera_image.getvalue())]
    
    headers = {}
    
    try:
        # Perform the file upload and processing
        response = requests.post(URL, headers=headers, files=files)
        # Update progress for uploading
        bar.progress(50)
        
        # Parse response
        dict_str = response.content.decode("UTF-8")
        data = ast.literal_eval(dict_str)
        
        # Update progress after processing
        bar.progress(100)
        
        # Hide progress bar
        progress_bar_placeholder.empty()
        
        # Save data to session state
        if data:
            st.session_state.update(data)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")

# If file or camera image is uploaded, display it
if file:
    img = file
elif camera_image:
    img = camera_image

if img:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your Image")
        st.image(img)
    
    with col2:
        if st.session_state:
            st.subheader("Details")
            # Display fields with extracted data
            name = st.text_input(label="Medicine Name", value=st.session_state.get("medicine_name", ""))
            quantity = st.text_input(label="Quantity", value=st.session_state.get("quantity", ""))
            dosage = st.text_input(label="Dosage", value=st.session_state.get("dosage", ""))
            frequency = st.text_input(label="Frequency", value=st.session_state.get("frequency", ""))
            taken_with = st.text_input(label="Taken With", value=st.session_state.get("taken_with", ""))
            not_taken_with = st.text_input(label="Not Taken With", value=st.session_state.get("not_taken_with", ""))
            food = st.text_input(label="Food Instructions", value=st.session_state.get("food", ""))
            reason = st.text_input(label="Reason", value=st.session_state.get("reason", ""))
            side_effects = st.text_input(label="Side Effects", value=st.session_state.get("side_effects", ""))
            prescription_date = st.text_input(label="Prescription Date", value=st.session_state.get("prescription_date", ""))
            
            if 'recorded_data' not in st.session_state:
                st.session_state.recorded_data = []

            if st.button(label="Submit", type="primary"):
                # Record the current session state to the recorded_data list
                st.session_state.recorded_data.append({
                    "Medicine Name": name,
                    "Quantity": quantity,
                    "Dosage": dosage,
                    "Frequency": frequency,
                    "Taken With": taken_with,
                    "Not Taken With": not_taken_with,
                    "Food Instructions": food,
                    "Reason": reason,
                    "Side Effects": side_effects,
                    "Prescription Date": prescription_date
                })
                
                # Clear session state after submission
                for key in list(st.session_state.keys()):
                    if key != 'recorded_data':
                        del st.session_state[key]
                st.success('Details successfully recorded.')

# Display the table of recorded data
if 'recorded_data' in st.session_state and st.session_state.recorded_data:
    st.header("Recorded Details")
    placeholder = "N/A"
    for i, record in enumerate(st.session_state.recorded_data):
        st.subheader(f"Record {i+1}")
        # records_df = pd.DataFrame(record)
        # records_df.replace("", placeholder, inplace=True)
        # st.dataframe(records_df.style.hide())
        for key, value in record.items():
            if value == "":
                value = placeholder
            st.write(f"**{key}:** {value}")
        if st.button("Delete", key=f"delete_{i}"):
            st.session_state.recorded_data.pop(i)
            st.rerun()
