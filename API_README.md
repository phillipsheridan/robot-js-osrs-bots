# Simple Node.js API for Gemini LLM Image Matching

## Setup

1. Install dependencies:
   ```powershell
   npm install
   ```

2. Set your Gemini API key as an environment variable:
   ```powershell
   $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
   ```

3. Start the API server:
   ```powershell
   npm run api
   ```

## Usage

POST to `http://localhost:3000/find-image-center` with form-data:
- `main_image`: the main image file
- `sub_image`: the image to find inside the main image

The response will be a JSON object with the coordinates of the center of the sub-image within the main image.

---

**Note:**
- Both images should be PNGs for best results.
- The Gemini API key is required for the LLM call.
