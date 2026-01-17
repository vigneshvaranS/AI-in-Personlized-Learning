
# 🎓 Personalized Learning Assistant using Machine Learning & Generative AI

This project is an **AI-powered Personalized Learning Assistant** that adapts learning content based on a learner’s difficulty level.
The system combines **classical Machine Learning**, **real-time web search**, and **Generative AI** to create a complete end-to-end personalized learning experience.

This project was developed as part of my **Minor Degree in Artificial Intelligence**, following proper ML workflow and evaluation practices.

WebApp Url =    [https://ai-in-personlized-learning.streamlit.app/](https://ai-in-personlized-learning.streamlit.app/)

---

## 🚀 Project Overview

Traditional learning systems provide the same content to everyone. However, learners differ in pace, understanding, and effort.
This project aims to solve that problem by:

* Predicting **learner difficulty level** using a trained ML model
* Adapting explanations and study plans accordingly
* Recommending relevant learning resources
* Providing an AI tutor and quiz generation feature

The system works fully end-to-end and demonstrates **real ML usage**, not just API calls.

---

## 🧠 Core Idea

The application predicts whether a learner is likely to find a topic:

* Easy
* Medium
* Hard

based on simple learning signals like:

* Expected quiz score
* Time spent learning
* Number of attempts to understand a topic

Using this prediction, the system generates a **custom learning plan**.

---

## 🛠️ Technologies Used

### Machine Learning

* Logistic Regression (baseline model)
* Random Forest Classifier (final selected model)
* Neural Network (experimented)

### Libraries

* scikit-learn
* numpy
* joblib

### Generative AI

* OpenRouter API
* Model: `meta-llama/llama-3.3-70b-instruct`

### Web & UI

* Streamlit
* Requests
* Pexels API (images)
* Serper.dev (Google Search API)

---

## 📊 Model Training Summary

Three models were trained and evaluated:

| Model               | Purpose        | Result                |
| ------------------- | -------------- | --------------------- |
| Logistic Regression | Baseline       | Good accuracy         |
| Random Forest       | Ensemble model | **Best accuracy**     |
| Neural Network      | Deep model     | Did not outperform RF |

**Final Model Selected:** Random Forest
Reason: Higher accuracy, better generalization on tabular data, and stable performance.

This follows standard ML best practices:
start simple → experiment → compare → select best model.

---

## 🧩 Features

### ✅ Difficulty Prediction (ML-based)

Predicts learner difficulty using trained Random Forest model.

### 📘 Personalized Study Guide

Generates explanations tailored to:

* Difficulty level
* Learning style
* Explanation depth

### 🔗 Resource Recommendations

Fetches and displays learning resources using real Google search results.

### 💬 AI Tutor

Chat-based tutor for follow-up questions on the topic.

### 🧠 Quiz Generator

Generates short quizzes to test understanding.

### 📜 Learning History

Previously generated learning plans can be revisited from the sidebar.

---

## 🏗️ Project Structure

```
.
├── app.py
├── saved_models/
│   ├── random_forest_model.pkl
│   ├── scaler.pkl
│   └── label_encoder.pkl
├── notebooks/
│   ├── data_preprocessing.ipynb
│   ├── logistic_regression.ipynb
│   ├── random_forest.ipynb
│   └── neural_network.ipynb
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run the Project

### 1. Clone the Repository

```
git clone https://github.com/your-username/personalized-learning-assistant.git
cd personalized-learning-assistant
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Add API Keys

Create `.streamlit/secrets.toml`

```
OPENROUTER_API_KEY = "your_openrouter_key"
PEXELS_API_KEY = "your_pexels_key"
SERPER_API_KEY = "your_serper_key"
```

### 4. Run the App

```
streamlit run app.py
```

---

## 🧪 Dataset

A synthetic dataset was created to simulate learner behavior with features such as:

* Quiz score
* Time spent
* Attempts

This dataset was cleaned, scaled, and used to train multiple models.

---

## 📈 Evaluation Metrics

* Accuracy was used since the dataset is balanced
* Random Forest achieved the highest accuracy
* Cross-checking was done using multiple models

---

## 🎯 Learning Outcomes

Through this project, I learned:

* How to design an end-to-end ML system
* Importance of baseline models
* Model comparison and selection
* Integration of ML with real-world applications
* Combining ML with Generative AI effectively

---

## 🔮 Future Improvements

* Use real learner interaction logs
* Add adaptive quizzes based on performance
* Improve dataset size and diversity
* Deploy using cloud services

---

## 👤 Author

**Vignesh S**
AI & Machine Learning Enthusiast

LinkedIn: [https://www.linkedin.com/in/vignesh-s-9b86a7243/](https://www.linkedin.com/in/vignesh-s-9b86a7243/)

Just tell me 👍
