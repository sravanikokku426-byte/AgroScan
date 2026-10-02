# AgroScan 🌱

AI-powered crop health and pesticide detection assistant for farmers.

## 📌 About the Project

AgroScan is an AI vision chatbot that helps farmers analyze images of crops, leaves, fruits, and plants. It identifies visible symptoms and provides possible causes such as pesticide-related damage, pests, diseases, or other crop health problems.

The system also provides recommendations for the next steps and can send a summary of the analysis to the farmer through WhatsApp.

> Note: An image alone cannot accurately measure the exact amount or concentration of pesticide residue. Laboratory testing or an appropriate chemical sensor is required for accurate residue measurement.

## ✨ Features

* 🌱 AI-powered crop image analysis
* 🔍 Detection of visible crop symptoms
* 🧪 Identification of possible pesticide-related damage
* 🐛 Possible pest and disease identification
* 💬 AI chatbot for farmer questions
* 📤 WhatsApp summary of crop analysis
* 📷 Supports crop image uploads

## 🛠️ Technologies Used

* Python
* Streamlit
* Google Gemini AI
* Twilio WhatsApp API

## 📂 Project Structure

```text
AgroScan/
├── app.py
├── prompts.py
├── requirements.txt
└── README.md
```

## ⚙️ Setup

Clone the repository:

```bash
git clone https://github.com/sravanikokku426-byte/AgroScan
cd AgroScan
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables / Secrets

The application requires the following secrets:

```text
GEMINI_API_KEY
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_WHATSAPP_FORM
TWILIO_CONTENT_SID
```

For Streamlit Cloud, add these values under the application's **Secrets** settings.

Do not upload API keys or authentication tokens to GitHub.

## ▶️ Run the Application

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🚀 Live Demo

The live demo link will be added after deployment.

## 👩‍💻 Project Goal

The goal of AgroScan is to make AI-based crop health analysis more accessible to farmers and help them make more informed decisions about crop problems and pesticide use.
