
# 🎶 Music Mood Analyzer & Playlist Generator

**Analyze Spotify playlists, classify songs by mood, and generate custom playlists — all in your browser with Streamlit!**

---

## 📌 Overview

The **Music Mood Analyzer & Playlist Generator** is a Streamlit application that uses the **Spotify Web API** (via the `spotipy` library) to analyze playlists and classify tracks based on **audio features** such as valence and energy. It allows users to:

* Analyze **any public Spotify playlist**.
* Classify tracks into moods: **Happy**, **Sad**, **Relaxed**, and **Neutral**.
* View track details with album art and audio previews.
* Generate **mood-specific playlists** with a chosen number of songs.
* Export analyzed data and playlists to CSV.

---

## 📂 Project Structure

```
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## ✨ Features

* **Spotify Playlist Analysis**: Fetch and analyze tracks from any Spotify playlist ID.
* **Mood Classification**: Automatically classify songs based on audio features.
* **Preview & Artwork**: View album covers and listen to 30-second previews.
* **Custom Playlist Generation**: Create playlists for your current mood.
* **Data Export**: Save results as CSV for later use.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Shreya-Reddy2004/MusicMoodAnalyzerAndPlaylistGenerator.git
cd MusicMoodAnalyzerAndPlaylistGenerator
```

### 2️⃣ Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Get Spotify API credentials

* Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
* Create a new application to get your **Client ID** and **Client Secret**.
* Replace `'Your client id'` and `'Your client secret'` in `app.py` with your credentials.

---

## ▶️ Running the Application

Run the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your browser at:

```
http://localhost:8501
```

---

## 🎯 How to Use

### **1. Analyze a Playlist**

* Enter the **Spotify Playlist ID** in the sidebar.
* Click **Analyze Playlist**.
* View:

  * Track mood classification
  * Album artwork
  * Audio previews (if available)

### **2. Generate a Playlist**

* Choose a **Mood** from the sidebar.
* Enter the desired **number of songs**.
* Click **Generate Playlist**.
* View your playlist and export it to CSV.

---

## 🧠 Mood Classification Logic

* **Happy** → valence > 0.5 and energy > 0.5
* **Sad** → valence < 0.5 and energy < 0.5
* **Relaxed** → valence > 0.5 and energy < 0.5
* **Neutral** → all other cases

---

## 📦 Dependencies

* `streamlit`
* `spotipy`
* `pandas`
* `Pillow`
* `requests`
* `time` (built-in)

> 📜 Full list of exact versions is available in `requirements.txt`.

