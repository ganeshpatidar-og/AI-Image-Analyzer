AI Image Analyzer — Flask + OpenRouter Vision

An AI-powered web application that analyzes images using multimodal vision models.  
Users can upload any image, and the app intelligently inspects it to generate meaningful insights using OpenRouter and advanced AI models

## ✨ Features
| 🔍 Object Recognition | Detects all visible objects and explains their relationships |
| 📝 Text Extraction & Summary (OCR) | Reads text present in the image and summarizes it |
| 🖼 Metadata-Style Analysis | Generates a caption, mood, dominant colors, and scene details |
| 🛒 Product-Style Object Scan | Identifies the main object, category, material, usage, and e-commerce keywords |
| 🌐 Universal Image Support | Backend auto-converts image types (JPG, PNG, AVIF, HEIC, WebP etc.) into JPEG using Pillow |

Tech Stack

 Backend | Python, Flask 
 AI  | OpenRouter (Grok / Gemini / Vision models) 
 Image Processing | Pillow 
 Frontend | HTML, CSS, JavaScript 
 Architecture | REST API + Multimodal Prompt Engineering 

How It Works

1. User uploads an image from the browser  
2. Backend converts non-JPEG images → JPEG (so all formats work seamlessly)  
3. User selects analysis mode  
4. The backend sends the prompt + image (base64) to an OpenRouter vision model  
5. The AI responds with a tailored interpretation  
6. The UI displays the results clearly and instantly  

🖥️ Running the Project Locally

pip install -r requirements.txt
python app.py
The app runs on:
http://127.0.0.1:5000

🔐 Environment Variables (.env setup)
Create a .env file inside the project directory:
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=x-ai/grok-4.1-fast:free
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions

📁 Project Structure

ai-image-analyzer/
│  app.py
│  requirements.txt
│  README.md
│  .gitignore
│  .env (not included in GitHub)
├─ templates/
│    index.html
└─ static/
     style.css

# Future Enhancements (Optional Ideas)
Live camera input (Google Lens-style scanning)

PDF / DOCX export of analysis

Drag-and-drop image upload

User login + analysis history

Deployment on Render / Railway

🎯 Project Purpose
This project demonstrates skills in:
Full-stack development using Flask
API integration
Image understanding using multimodal AI
Prompt engineering
Error handling and file processing
Clean frontend + backend architecture
Perfect for portfolio, internship and job applications.


⭐ Author
Ganesh Patidar
AI & Full Stack Developer
🔗 GitHub • LinkedIn — https://www.linkedin.com/in/ganeshpatidarcse/

If you want, I can now:

- Add **GitHub tags** (like `#AI #Flask #OpenRouter #VisionAI`)
- Add **project description for resume**
- Help you **deploy the project online** so your README has a **Live Demo link**

Just tell me what you want next 🚀
