
# 📚 Personalized Learning Assistant

An interactive AI-powered web app built with **Streamlit** that provides customized learning recommendations and topic explanations based on your preferred learning style and knowledge level.

![App Screenshot](https://user-images.githubusercontent.com/placeholder/image.png)

---

## 🚀 Features

* 🔍 **Personalized Content**: Get tailored explanations and curated resources for any topic.
* 🎨 **Learning Styles**: Choose your preferred style — visual, auditory, kinesthetic, reading/writing, or mixed.
* 📈 **Difficulty Levels**: Beginner, Intermediate, or Advanced.
* 🖼️ **Inspiring Images**: Automatically fetches topic-relevant images from Pexels.
* 📜 **Learning History**: View and revisit your past topic explorations.
* 🧠 **Powered by LLMs**: Uses DeepSeek Chat via OpenRouter API.

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **APIs**:

  * OpenRouter AI (for language model responses)
  * Pexels (for fetching topic-related images)
* **Language**: Python

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/personalized-learning-assistant.git
cd personalized-learning-assistant
```

### 2. Install dependencies

Make sure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

### 3. Set up your API keys

Create a `.streamlit/secrets.toml` file and add your keys:

```toml
OPENROUTER_API_KEY = "your-openrouter-api-key"
PEXELS_API_KEY = "your-pexels-api-key"
```

If `.streamlit` doesn't exist, create the directory manually.

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📂 File Structure

```
├── app.py                   # Main Streamlit app
├── requirements.txt         # Python dependencies
├── .streamlit/
│   └── secrets.toml         # API keys (user-provided)
├── test1.png                # Sidebar image
└── README.md                # Project documentation
```

---

## 🧪 Example Prompt

> Topic: **Linear Algebra**
> Learning Style: **Visual**
> Difficulty: **Beginner**

The app generates:

* A simple explanation of linear algebra.
* Curated videos, articles, or tools for visual learners.
* Topic image fetched from Pexels.

---

## 🧑‍💻 Developer

Made with ❤️ by **[Vignesh S](https://www.linkedin.com/in/vignesh-s-9b86a7243/)**

---

## 📄 License

This project is licensed under the MIT License.

---

Would you also like me to generate a `requirements.txt` for this project?
