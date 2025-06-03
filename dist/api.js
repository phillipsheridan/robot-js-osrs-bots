"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const multer_1 = __importDefault(require("multer"));
const axios_1 = __importDefault(require("axios"));
const fs_1 = __importDefault(require("fs"));
require("dotenv/config");
const app = (0, express_1.default)();
const upload = (0, multer_1.default)({ dest: 'uploads/' });
// POST /find-image-center
// Expects: main_image, sub_image (both as form-data files)
app.post('/find-image-center', upload.fields([
    { name: 'main_image', maxCount: 1 },
    { name: 'sub_image', maxCount: 1 }
]), async (req, res) => {
    try {
        const mainImagePath = req.files['main_image'][0].path;
        const subImagePath = req.files['sub_image'][0].path;
        // Read images as base64
        const mainImageBase64 = fs_1.default.readFileSync(mainImagePath, { encoding: 'base64' });
        const subImageBase64 = fs_1.default.readFileSync(subImagePath, { encoding: 'base64' });
        // Prepare Gemini LLM prompt
        const prompt = `You are given two images. The first image is the main image. The second image can be found inside the main image, possibly at a different scale. Please return the (x, y) coordinates (in pixels) of the center of the second image's location within the main image. Also return the width/height of the main image. Respond with a JSON object: {\n  \"x\": <number>,\n  \"y\": <number>,\n  \"width\": <number>,\n  \"height\": <number>}.`;
        // Call Gemini LLM API (user must provide API key)
        const GEMINI_API_KEY = process.env.GEMINI_API_KEY || 'YOUR_GEMINI_API_KEY_HERE';
        const geminiUrl = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=' + GEMINI_API_KEY;
        const payload = {
            contents: [
                {
                    parts: [
                        { text: prompt },
                        { inline_data: { mime_type: 'image/png', data: mainImageBase64 } },
                        { inline_data: { mime_type: 'image/png', data: subImageBase64 } }
                    ]
                }
            ],
            config: {
                temperature: 0,
            },
        };
        const response = await axios_1.default.post(geminiUrl, payload);
        // Clean up uploaded files
        fs_1.default.unlinkSync(mainImagePath);
        fs_1.default.unlinkSync(subImagePath);
        // Extract and return the LLM's response
        res.json({ result: response.data });
    }
    catch (err) {
        console.error('Error processing images:', err.message);
        res.status(500).json({ error: err });
    }
});
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`API server running on port ${PORT}`);
});
