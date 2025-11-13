# Code X Emotion Analyzer - Streamlit Edition

A powerful, easy-to-deploy emotion detection application built with Streamlit. Analyze emotions from voice recordings using advanced deep learning models.

![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?style=flat-square&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python)

## 🎯 Features

### Core Functionality
- **🎙️ Voice Recording & Upload** - Record directly or upload audio files (WAV, MP3, OGG, M4A)
- **🧠 AI Emotion Detection** - Detect 7 emotions using Hugging Face's advanced models
- **📊 Real-time Visualization** - Interactive charts and gauges for emotion analysis
- **🎯 Emotion Breakdown** - Detailed confidence scores for each emotion
- **📈 Frequency Analysis** - Visual frequency spectrum of your voice

### Advanced Features
- **📊 Comparison Tool** - Compare multiple recordings side-by-side
- **📈 Analytics Dashboard** - Track emotion patterns over time
- **💬 Feedback System** - Improve model accuracy by providing corrections
- **🌍 Multi-language Support** - 12 languages including English, Spanish, French, etc.
- **💡 Guided Prompts** - Recording prompts to help generate consistent samples
- **🎚️ Confidence Adjustment** - Fine-tune emotion predictions

### Emotions Detected
- 😠 **Anger** - Aggressive, irritated
- 🤢 **Disgust** - Repulsed, offended
- 😨 **Fear** - Anxious, scared
- 😊 **Happiness** - Joyful, content
- 😐 **Neutral** - Calm, indifferent
- 😢 **Sadness** - Unhappy, melancholic
- 😲 **Surprise** - Astonished, amazed

## Quick Start

### Option 1: Deploy on Streamlit Cloud

1. **Fork this repository** to your GitHub account
2. **Go to Streamlit Cloud**: https://streamlit.io/cloud
3. **Sign in with GitHub**
4. **Click "New app"**
5. **Select your repository**
6. **Set environment variables**:
   - `HUGGING_FACE_API_KEY` - Your Hugging Face API token
7. **Click "Deploy"**

Your app will be live in minutes! 

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/hamzamohee1/code-x-emotion-streamlit.git
cd code-x-emotion-streamlit

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export HUGGING_FACE_API_KEY=your_token_here

# Run the app
streamlit run app.py
```

Your app will be available at: `http://localhost:8501`

## 📋 Requirements

- Python 3.8+
- Hugging Face API key (free at https://huggingface.co/settings/tokens)
- Internet connection for API calls

## 🔧 Installation

### From Source

```bash
git clone https://github.com/hamzamohee1/code-x-emotion-streamlit.git
cd code-x-emotion-streamlit
pip install -r requirements.txt
```

### Docker

```bash
docker build -t code-x-emotion .
docker run -e HUGGING_FACE_API_KEY=your_token -p 8501:8501 code-x-emotion
```

## 📖 Usage

### 1. Record & Analyze
- Choose a guided prompt or record freely
- Upload or record audio directly
- Get instant emotion analysis with confidence scores

### 2. Compare Recordings
- Select multiple recordings
- View side-by-side emotion comparison
- Analyze patterns in your voice

### 3. Analytics
- Track emotion trends over time
- View emotion distribution
- Monitor confidence levels

### 4. Provide Feedback
- Correct misclassified emotions
- Rate prediction helpfulness
- Help improve the model

## 🌍 Supported Languages

- English
- Spanish
- French
- German
- Italian
- Portuguese
- Japanese
- Chinese
- Korean
- Russian
- Arabic
- Hindi


## 📊 Emotion Detection Model

Uses **jihedjabnoun/wavlm-base-emotion** from Hugging Face:
- Trained on multiple emotion datasets
- Supports 7 emotion categories
- High accuracy on diverse voice samples
- Fast inference time


## 🛠️ Configuration

### Environment Variables

```bash
HUGGING_FACE_API_KEY=hf_your_token_here
```

### Streamlit Config

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Font styles
- Server settings
- Logger levels

## 📈 Performance

- **Inference Time**: ~2-5 seconds per audio
- **Memory Usage**: ~500MB
- **Supported Audio Length**: Up to 30 seconds
- **Supported Formats**: WAV, MP3, OGG, M4A



## 📊 Statistics

- **Emotions Detected**: 7
- **Languages Supported**: 12
- **Audio Formats**: 4

## 🎯 Use Cases

- **Mental Health**: Track emotional patterns
- **Speech Therapy**: Monitor voice changes
- **Customer Service**: Analyze customer sentiment
- **Research**: Study emotional expression
- **Education**: Learn about emotions
- **Entertainment**: Fun voice analysis

---

**Made with ❤️ by Code X**

