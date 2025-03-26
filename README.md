# Food Detection & Nutrition App

This Streamlit application uses Google's Gemini API to detect food in images and provides nutritional information using the FatSecret API.

## Features

- Upload food images for identification using Google Gemini AI
- Get accurate food detection with advanced AI vision capabilities
- View detailed nutritional information including:
  - Calories
  - Protein
  - Carbohydrates
  - Fat
  - Fiber
  - Sugar
  - Sodium
  - Cholesterol

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Get a Google Gemini API key from [Google AI Studio](https://ai.google.dev/)
4. Add your Gemini API key to the `.env` file:
   ```
   GEMINI_API_KEY="your_api_key_here"
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your browser at `http://localhost:8501` (or whichever port Streamlit provides)

3. Upload a food image using the file uploader

4. The app will automatically detect the food and display its nutritional information

## Technologies Used

- Streamlit for the web interface
- Google Gemini API for advanced food detection
- Python for backend processing

## Tips for Best Results

- Use clear, well-lit images of food
- Try to have only one main food item in the image
- Avoid complex backgrounds that might confuse the AI
- Make sure the food is clearly visible in the center of the image 
