# 🧭 Inference Compass — an opinionated model picker for open-source inference on Featherless AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](#)

## 🚨 Why It Exists

Featherless AI hosts over 30,000 open-source models accessible via an elegant serverless API. However, this massive selection introduces a severe Developer Experience (DX) challenge: **analysis paralysis**. 

When building an application, developers shouldn't have to wade through 50 variations of 7B models or decode dense academic benchmark tables. **Inference Compass** solves this by narrowing the universe down to 20 elite, hand-curated models and matching them to your specific engineering constraints (context length, speed, cost, and task type) instantly.

<!-- Add screenshot here -->

---

## 🛠️ How to Run Locally

You can get Inference Compass running on your local machine in under two minutes.

### 1. Clone the repository
```bash
git clone https://github.com/placeholder/inference_compass.git
cd inference_compass
```

### 2. Configure Environment Variables
Create a `.env` file from the example template:
```bash
cp .env.example .env
```
Open `.env` and add your Featherless AI API key (get one at [Featherless AI](https://featherless.ai)):
```env
FEATHERLESS_API_KEY=your_featherless_api_key_here
```

### 3. Install Dependencies
Ensure you have Python 3.11+ installed.
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
The application will automatically launch in your browser at `http://localhost:8501`.

---

## ☁️ How to Deploy on Streamlit Cloud

Deploying to Streamlit Cloud is completely free and takes under 5 minutes.

1. Push your local `inference_compass` repository to a public GitHub repository.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and select your GitHub repository, branch (`main`), and main file path (`app.py`).
4. Click **Advanced settings** before deploying, and add your API key under the Secrets field:
   ```toml
   FEATHERLESS_API_KEY = "your_featherless_api_key_here"
   ```
5. Click **Deploy!** Your app is now live and shareable on LinkedIn and Twitter.

---

## 🚀 What I'd Build Next

* **Real-time Latency Benchmarking**: Live stream pinging across model tiers to dynamically rank current API throughput.
* **Model Comparison Mode**: Side-by-side prompt output generation from two recommended models simultaneously.
* **Cost Calculator**: Interactive slider to estimate monthly inference spend based on expected input/output token volume.
* **Per-Persona Presets**: One-click configuration profiles tailored for *Indie Hackers*, *Enterprise MLEs*, and *Startup Founders*.

---

## 👨‍💻 Author

**Jaideep Murthy**

* GitHub: [github.com/placeholder](#)
* LinkedIn: [linkedin.com/in/placeholder](#)
* Twitter: [twitter.com/placeholder](#)
