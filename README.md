# 🎬 Movie Recommendation System

A Content-Based Movie Recommendation System built using Machine Learning, Python, TMDB API, and Streamlit.

## 📌 Project Overview

This project recommends movies similar to a user's selected movie using Content-Based Filtering.

The recommendation engine analyzes movie features such as:

* Genres
* Keywords
* Cast
* Crew
* Overview

and computes similarity using CountVectorizer and Cosine Similarity.

The application also provides:

* Movie Posters
* Movie Details
* Movie Trailers
* Favorites List
* Search History
* CSV Download of Recommendations

---

## 🚀 Features

### Movie Recommendation Engine

* Content-Based Filtering
* CountVectorizer
* Cosine Similarity
* Top Similar Movies Recommendation

### Movie Information

* Poster Display
* Movie Rating
* Release Year
* Runtime
* Language
* Genres
* Story Overview

### Trailer Integration

* YouTube Trailer Support
* Watch Trailer Directly Inside Application

### User Features

* Add to Favorites
* Recent Search History
* Download Recommendations as CSV

### User Interface

* Netflix Inspired Dark Theme
* Interactive Cards
* Responsive Layout
* Streamlit Dashboard

---

## 🛠️ Tech Stack

### Programming Language

* Python

### Machine Learning

* Pandas
* NumPy
* Scikit-Learn
* NLTK

### Recommendation Algorithm

* Content-Based Filtering
* CountVectorizer
* Cosine Similarity

### Frontend

* Streamlit
* HTML
* CSS

### API

* TMDB API

---

## 📂 Project Structure

```text
recommendation_system/
│
├── artifacts/
│   ├── movies.pkl
│   └── similarity.pkl
│
├── data/
│   ├── tmdb_5000_movies.csv
│   ├── tmdb_5000_credits.csv
│   └── cleaned_movies.csv
│
├── notebook/
│   ├── 1_Recommendation_EDA.ipynb
│   └── 2_Recommendation_Engine.ipynb
│
├── src/
│   ├── components/
│   ├── pipeline/
│   │   ├── train_pipeline.py
│   │   └── predict_pipeline.py
│   │
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
│
├── app.py
├── requirements.txt
├── setup.py
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <your-github-repository-link>
cd recommendation_system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will start at:

```text
http://localhost:8501
```

---

## 🧠 How Recommendation Works

1. Movie metadata is collected.
2. Important features are merged into tags.
3. Text preprocessing is performed.
4. CountVectorizer converts text into vectors.
5. Cosine Similarity calculates similarity scores.
6. Top similar movies are recommended.

---

## 📊 Dataset

TMDB 5000 Movie Dataset

Files Used:

* tmdb_5000_movies.csv
* tmdb_5000_credits.csv

---

## 📸 Application Features

* Movie Search
* Recommendation Engine
* Poster Display
* Trailer Support
* Favorites Management
* Recent Searches
* CSV Export

---


## 👨‍💻 Author

Priyanshi Vishwakarma

Machine Learning & Python Developer

---

## ⭐ If you like this project

Give this repository a star on GitHub.
