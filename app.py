import streamlit as st
import openai
import os

# --- Red Flag Keywords ---
red_flag_keywords = [
    "drugs", "weapon", "escape", "stash", "package", "drop", "pickup",
    "meet up", "under the bridge", "box", "spot", "discreet", "don't tell anyone",
    "move it", "hide it", "get rid of", "kill", "threat", "contraband"
]



# --- Page Configuration ---
st.set_page_config(page_title="Jail Informer – Analyst Portal", layout="wide")

# --- Sidebar ---
st.sidebar.title("Jail Informer Analyst Portal")
st.sidebar.markdown("Secure Upload and Analysis System")

# --- Main Section ---
st.title("📥 Upload Jail Calls for Analysis")

# Upload call files
uploaded_files = st.file_uploader(
    "Upload one or more call files (.txt or .mp3)",
    accept_multiple_files=True
)

# API Key Setup (temporary manual input, we'll automate later)
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
openai.api_key = api_key

# Process files
if st.button("Analyze Calls"):
    if uploaded_files and api_key:
        for uploaded_file in uploaded_files:
            st.write(f"Processing file: {uploaded_file.name}")

            # Handle .txt files
            if uploaded_file.name.endswith(".txt"):
                call_text = uploaded_file.read().decode("utf-8")
            else:
                st.warning(f"Unsupported file type: {uploaded_file.name}")
                continue

            # --- AI Summarization ---
# --- AI Summarization ---

if uploaded_files and api_key:
    uploaded_file = uploaded_files[0]
    call_text = uploaded_file.read().decode("utf-8")

    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a jail intelligence analyst who summarizes inmate phone calls for red flags and criminal activity."},
            {"role": "user", "content": f"Summarize this jail call transcript:\n\n{call_text}"}
        ],
        max_tokens=250,
        temperature=0.5
    )
    summary = response.choices[0].message.content.strip()

    # Display Summary
    st.success(f"Summary for {uploaded_file.name}:")
    st.write(summary)

else:
    st.warning("Please upload a call file and enter your OpenAI API Key before analyzing.")



# --- Red Flag Detection ---
found_flags = []

if 'call_text' in locals() and call_text:
    lowered_transcript = call_text.lower()

    for keyword in red_flag_keywords:
    if keyword.lower() in lowered_transcript:
        found_flags.append(keyword)


# Display Found Red Flags
if found_flags:
    st.warning(f"🚨 Red Flags Detected: {', '.join(found_flags)}")
else:
    st.info("✅ No Red Flags Detected.")


 
