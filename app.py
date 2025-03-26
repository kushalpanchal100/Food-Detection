import streamlit as st
import numpy as np
from PIL import Image
import io
import requests
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pandas as pd
import re

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Food Detection App",
    page_icon="🍔",
    layout="centered"
)

# Google Gemini API Key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if Gemini API key is available
if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Please add your API key to the .env file as GEMINI_API_KEY='your_key_here'")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Enhanced prompt for detailed food identification
FOOD_PROMPT = """
Analyze this food image and provide the following information in JSON format:
{
  "food_item": "The main food item you see (be very specific)",
  "state": "liquid or solid",
  "approximate_amount": "estimated quantity (e.g., '1 cup', '200g', etc.)",
  "ingredients": ["list up to 5 main visible ingredients"],
  "description": "brief description of the food",
  "preparation_method": "how the food appears to be prepared (e.g., baked, fried, raw, etc.)"
}

Be very precise in your detection. If you cannot identify the food clearly, respond with:
{
  "food_item": "unknown food item",
  "state": "unknown",
  "approximate_amount": "unknown",
  "ingredients": [],
  "description": "Could not identify the food in the image",
  "preparation_method": "unknown"
}
"""
 
# Function to identify food using Gemini Vision API
def identify_food_with_gemini(image):
    try:
        # Convert PIL Image to bytes for Gemini
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Get Gemini vision model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create a prompt with the image
        response = model.generate_content([FOOD_PROMPT, {"mime_type": "image/jpeg", "data": img_byte_arr}])
        
        # Extract the food information
        food_info_text = response.text.strip()
        
        # Try to parse the JSON response
        try:
            # Find and extract just the JSON part from the response
            json_match = re.search(r'({[\s\S]*})', food_info_text)
            if json_match:
                food_info_json = json.loads(json_match.group(1))
                return food_info_json
            else:
                return {
                    "food_item": food_info_text,
                    "state": "unknown",
                    "approximate_amount": "unknown",
                    "ingredients": [],
                    "description": food_info_text,
                    "preparation_method": "unknown"
                }
        except json.JSONDecodeError:
            # If JSON parsing fails, return simple format
            return {
                "food_item": food_info_text,
                "state": "unknown",
                "approximate_amount": "unknown",
                "ingredients": [],
                "description": food_info_text,
                "preparation_method": "unknown"
            }
    except Exception as e:
        st.error(f"Error identifying food with Gemini: {e}")
        return None

# Streamlit UI
st.title("Food Detection 🍽️")
# Create tabs for different modes
tab1 = st.tabs(["Image Upload"])[0]  # Get the first tab from the tuple

with tab1:
    # Image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Process the image with Gemini API
        with st.spinner("Analyzing your food with Google Gemini AI..."):
            food_info = identify_food_with_gemini(image)
            
            if food_info and food_info.get("food_item", "").lower() != "unknown food item":
                with col2:
                    st.subheader("Detected Food:")
                    food_item = food_info.get('food_item', 'Unknown')
                    st.write(f"**Food Item:** {food_item}")
                    st.write(f"**State:** {food_info.get('state', 'Unknown')}")
                    st.write(f"**Approximate Amount:** {food_info.get('approximate_amount', 'Unknown')}")
                    st.write(f"**Preparation Method:** {food_info.get('preparation_method', 'Unknown')}")
                    
                    ingredients = food_info.get('ingredients', [])
                    if ingredients:
                        st.write("**Ingredients:**")
                        for ingredient in ingredients:
                            st.write(f"- {ingredient}")
                    
                    description = food_info.get('description', '')
                    if description:
                        st.write(f"**Description:** {description}")

