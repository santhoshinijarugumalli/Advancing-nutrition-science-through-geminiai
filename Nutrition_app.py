import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
my_api_key = os.getenv("my_api_key")
genai.configure(api_key=my_api_key)

st.set_page_config(page_title="Advanced Nutrition AI", layout="wide")

# --- Sidebar: Choose Scenario ---
st.sidebar.title("Nutrition AI Scenarios")
scenario = st.sidebar.radio(
    "Choose what you want to do:",
    ("Dynamic Nutritional Insights", "Tailored Meal Planning", "Virtual Nutrition Coaching"),
)

# --- Scenario 1: Tailored Meal Planning ---
if scenario == "Tailored Meal Planning":
    st.title("🍽️ Tailored Meal Planning")
    st.write(
        "Provide your dietary details and preferences. Gemini AI will generate a meal plan!"
    )
    col1, col2 = st.columns(2)
    with col1:
        dietary_restrictions = st.text_area("Dietary restrictions or allergies")
        health_conditions = st.text_area("Health conditions")
    with col2:
        activity_level = st.selectbox(
            "Activity level",
            ["Sedentary", "Lightly active", "Moderately active", "Very active"],
        )
        taste_preferences = st.text_area("Taste preferences")

    submit = st.button("Generate Meal Plan")
    if submit:
        prompt = f"""
        You are a nutrition expert. Create a week-long meal plan with recipes and grocery lists.
        Dietary restrictions: {dietary_restrictions}
        Health conditions: {health_conditions}
        Activity level: {activity_level}
        Taste preferences: {taste_preferences}
        Ensure nutritional balance, variety, and enjoyment.
        """
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        st.subheader("Your Personalized Meal Plan")
        st.write(response.text)

# --- Scenario 2: Dynamic Nutritional Insights ---
elif scenario == "Dynamic Nutritional Insights":
    st.title("📸 Dynamic Nutritional Insights")
    st.write("Upload an image of food or input its name for detailed nutritional analysis.")
    input_text = st.text_input("Food item name (optional)", key="food_input")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    image_data = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        bytes_data = uploaded_file.getvalue()
        image_data = [
            {"mime_type": uploaded_file.type, "data": bytes_data}
        ]

    submit = st.button("Analyze Nutrition")
    if submit:
        prompt = f"""
        You are a nutritionist. Provide a detailed breakdown of macronutrients, micronutrients, and calories
        for this food. Present it clearly.
        """
        model = genai.GenerativeModel("gemini-1.5-flash")
        if image_data:
            response = model.generate_content([prompt, image_data[0], input_text])
        else:
            response = model.generate_content(f"{prompt} Food: {input_text}")
        st.subheader("Nutrition Analysis")
        st.write(response.text)

# --- Scenario 3: Virtual Nutrition Coaching ---
else:
    st.title("💬 Virtual Nutrition Coaching")
    st.write("Ask any nutrition-related question to your AI coach.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Type your question here...")
    if st.button("Ask Coach"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"You are a professional nutrition coach. Answer this user question with empathy and precision: {user_input}"
        )
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Coach", response.text))

    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.write(f"🧑‍💻 **{speaker}:** {message}")
        else:
            st.write(f"🤖 **{speaker}:** {message}")
