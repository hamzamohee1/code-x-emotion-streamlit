import streamlit as st
import numpy as np
import librosa
import soundfile as sf
from huggingface_hub import InferenceClient
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
from pathlib import Path
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Code X Emotion Analyzer",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    :root {
        --primary-color: #6366f1;
        --secondary-color: #a855f7;
        --background-color: #0f172a;
        --surface-color: #1e293b;
        --text-color: #f1f5f9;
    }
    
    body {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    .main {
        background-color: var(--background-color);
    }
    
    .stApp {
        background-color: var(--background-color);
    }
    
    .emotion-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .emotion-title {
        font-size: 24px;
        font-weight: bold;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-box {
        background: rgba(99, 102, 241, 0.1);
        border-left: 4px solid #6366f1;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recordings' not in st.session_state:
    st.session_state.recordings = []
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'English'
if 'hf_token' not in st.session_state:
    st.session_state.hf_token = os.getenv('HUGGING_FACE_API_KEY', '')

# Emotion colors and metadata
EMOTION_CONFIG = {
    'Anger': {'color': '#ef4444', 'emoji': '😠', 'rgb': (239, 68, 68)},
    'Disgust': {'color': '#22c55e', 'emoji': '🤢', 'rgb': (34, 197, 94)},
    'Fear': {'color': '#8b5cf6', 'emoji': '😨', 'rgb': (139, 92, 246)},
    'Happiness': {'color': '#fbbf24', 'emoji': '😊', 'rgb': (251, 191, 36)},
    'Neutral': {'color': '#94a3b8', 'emoji': '😐', 'rgb': (148, 163, 184)},
    'Sadness': {'color': '#3b82f6', 'emoji': '😢', 'rgb': (59, 130, 246)},
    'Surprise': {'color': '#ec4899', 'emoji': '😲', 'rgb': (236, 72, 153)},
}

LANGUAGES = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Japanese': 'ja',
    'Chinese': 'zh',
    'Korean': 'ko',
    'Russian': 'ru',
    'Arabic': 'ar',
    'Hindi': 'hi'
}

PROMPTS = {
    'Daily Life': [
        'Tell me about your day',
        'What did you have for lunch?',
        'How was your morning?',
        'What are your plans for tomorrow?'
    ],
    'Emotions': [
        'What made you happy today?',
        'Tell me about something that frustrated you',
        'What are you worried about?',
        'What are you grateful for?'
    ],
    'Reflections': [
        'What did you learn today?',
        'How are you feeling right now?',
        'What would you change about today?',
        'What are your goals?'
    ],
    'Quick Reactions': [
        'Say your favorite food',
        'Name a movie you like',
        'What\'s your hobby?',
        'Describe your ideal vacation'
    ]
}

def get_emotion_from_huggingface(audio_path: str) -> dict:
    """Get emotion prediction from Hugging Face Inference API"""
    if not st.session_state.hf_token:
        st.error("❌ Hugging Face API key not configured. Please set HUGGING_FACE_API_KEY environment variable.")
        return None
    
    try:
        client = InferenceClient(api_key=st.session_state.hf_token)
        
        with open(audio_path, 'rb') as f:
            result = client.audio_classification(
                audio=f,
                model="jihedjabnoun/wavlm-base-emotion"
            )
        
        # Convert result to emotion scores
        emotions = {}
        for item in result:
            label = item['label']
            score = item['score']
            # Map common emotion labels
            if 'anger' in label.lower():
                emotions['Anger'] = score
            elif 'disgust' in label.lower():
                emotions['Disgust'] = score
            elif 'fear' in label.lower():
                emotions['Fear'] = score
            elif 'happy' in label.lower() or 'joy' in label.lower():
                emotions['Happiness'] = score
            elif 'neutral' in label.lower():
                emotions['Neutral'] = score
            elif 'sad' in label.lower():
                emotions['Sadness'] = score
            elif 'surprise' in label.lower():
                emotions['Surprise'] = score
        
        # Ensure all emotions are present
        for emotion in EMOTION_CONFIG.keys():
            if emotion not in emotions:
                emotions[emotion] = 0.0
        
        # Normalize scores
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v/total for k, v in emotions.items()}
        
        return emotions
    
    except Exception as e:
        st.error(f"❌ Error analyzing emotion: {str(e)}")
        return None

def preprocess_audio(audio_path: str) -> str:
    """Preprocess audio for better emotion detection"""
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=16000)
        
        # Trim silence
        y, _ = librosa.effects.trim(y, top_db=40)
        
        # Normalize
        y = y / np.max(np.abs(y))
        
        # Save preprocessed audio
        output_path = audio_path.replace('.wav', '_processed.wav')
        sf.write(output_path, y, sr)
        
        return output_path
    except Exception as e:
        st.warning(f"⚠️ Could not preprocess audio: {str(e)}")
        return audio_path

def create_emotion_gauge(emotion: str, score: float) -> go.Figure:
    """Create a gauge chart for emotion"""
    config = EMOTION_CONFIG[emotion]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score * 100,
        title={'text': f"{emotion} {config['emoji']}"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': config['color']},
            'steps': [
                {'range': [0, 33], 'color': "rgba(100, 100, 100, 0.1)"},
                {'range': [33, 66], 'color': "rgba(100, 100, 100, 0.2)"},
                {'range': [66, 100], 'color': "rgba(100, 100, 100, 0.3)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(15, 23, 42, 0)',
        plot_bgcolor='rgba(30, 41, 59, 0.5)',
        font=dict(color='#f1f5f9', size=12)
    )
    
    return fig

def create_emotion_radar(emotions: dict) -> go.Figure:
    """Create a radar chart for all emotions"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(emotions.values()),
        theta=list(emotions.keys()),
        fill='toself',
        name='Emotions',
        line_color='#6366f1',
        fillcolor='rgba(99, 102, 241, 0.3)',
        marker=dict(size=8, color='#a855f7')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(emotions.values()) * 1.2],
                tickcolor='#475569',
                gridcolor='#334155'
            ),
            angularaxis=dict(tickcolor='#475569'),
            bgcolor='rgba(30, 41, 59, 0.3)'
        ),
        height=500,
        margin=dict(l=80, r=80, t=80, b=80),
        paper_bgcolor='rgba(15, 23, 42, 0)',
        font=dict(color='#f1f5f9', size=12),
        showlegend=False
    )
    
    return fig

def create_frequency_visualization(audio_path: str) -> go.Figure:
    """Create frequency spectrum visualization"""
    try:
        y, sr = librosa.load(audio_path, sr=16000)
        
        # Compute STFT
        D = librosa.stft(y)
        S = np.abs(D)
        
        # Convert to dB
        S_db = librosa.power_to_db(S**2, ref=np.max)
        
        # Create spectrogram
        fig = go.Figure(data=go.Heatmap(
            z=S_db,
            colorscale='Viridis',
            colorbar=dict(title="Magnitude (dB)")
        ))
        
        fig.update_layout(
            title="Frequency Spectrum",
            xaxis_title="Time",
            yaxis_title="Frequency",
            height=400,
            paper_bgcolor='rgba(15, 23, 42, 0)',
            plot_bgcolor='rgba(30, 41, 59, 0.5)',
            font=dict(color='#f1f5f9', size=12)
        )
        
        return fig
    except Exception as e:
        st.warning(f"⚠️ Could not create frequency visualization: {str(e)}")
        return None

def save_recording(emotions: dict, audio_path: str, intensity: float = 1.0):
    """Save recording to session state"""
    recording = {
        'timestamp': datetime.now().isoformat(),
        'emotions': emotions,
        'dominant_emotion': max(emotions, key=emotions.get),
        'confidence': max(emotions.values()),
        'intensity': intensity,
        'audio_path': audio_path,
        'language': st.session_state.selected_language
    }
    st.session_state.recordings.append(recording)

def display_header():
    """Display application header"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div class="emotion-title">
            🎙️ Code X Emotion Analyzer
        </div>
        """, unsafe_allow_html=True)
        st.markdown("*Detect emotions from your voice using AI*")
    
    with col2:
        st.session_state.selected_language = st.selectbox(
            "Language",
            list(LANGUAGES.keys()),
            key='language_select'
        )

def main():
    """Main application"""
    display_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "Hugging Face API Key",
            value=st.session_state.hf_token,
            type="password",
            help="Get your API key from https://huggingface.co/settings/tokens"
        )
        if api_key:
            st.session_state.hf_token = api_key
        
        st.markdown("---")
        
        # Information
        st.markdown("### 📊 About")
        st.info("""
        **Code X Emotion Analyzer** uses advanced deep learning to detect 7 emotions:
        - 😠 Anger
        - 🤢 Disgust
        - 😨 Fear
        - 😊 Happiness
        - 😐 Neutral
        - 😢 Sadness
        - 😲 Surprise
        """)
        
        st.markdown("---")
        
        # Statistics
        if st.session_state.recordings:
            st.markdown("### 📈 Statistics")
            
            df = pd.DataFrame([
                {
                    'Emotion': r['dominant_emotion'],
                    'Confidence': r['confidence'],
                    'Time': r['timestamp']
                }
                for r in st.session_state.recordings
            ])
            
            emotion_counts = df['Emotion'].value_counts()
            
            fig = px.pie(
                values=emotion_counts.values,
                names=emotion_counts.index,
                title="Emotion Distribution"
            )
            fig.update_layout(
                height=300,
                paper_bgcolor='rgba(15, 23, 42, 0)',
                font=dict(color='#f1f5f9')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎤 Record & Analyze",
        "📊 Comparison",
        "📈 Analytics",
        "💬 Feedback"
    ])
    
    with tab1:
        st.markdown("### Record Your Voice")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Prompt selection
            prompt_category = st.selectbox(
                "Choose a prompt category",
                list(PROMPTS.keys())
            )
            prompt = st.selectbox(
                "Guided prompt",
                PROMPTS[prompt_category]
            )
            st.info(f"💡 **Prompt**: {prompt}")
        
        with col2:
            # Intensity slider
            intensity = st.slider(
                "Emotion Intensity",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.1,
                help="Adjust predicted emotion confidence"
            )
        
        # Audio recording
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            audio_file = st.file_uploader(
                "Upload audio file",
                type=['wav', 'mp3', 'ogg', 'm4a'],
                help="Supported formats: WAV, MP3, OGG, M4A"
            )
        
        with col2:
            st.markdown("**Or record directly:**")
            audio_data = st.audio_input("Record audio")
        
        # Process audio
        if audio_file or audio_data:
            st.markdown("---")
            
            # Save audio temporarily
            if audio_file:
                audio_bytes = audio_file.read()
                audio_path = f"/tmp/{audio_file.name}"
            else:
                audio_bytes = audio_data.getvalue()
                audio_path = "/tmp/recorded_audio.wav"
            
            with open(audio_path, 'wb') as f:
                f.write(audio_bytes)
            
            # Preprocess
            with st.spinner("🔄 Preprocessing audio..."):
                processed_path = preprocess_audio(audio_path)
            
            # Analyze emotion
            with st.spinner("🧠 Analyzing emotion..."):
                emotions = get_emotion_from_huggingface(processed_path)
            
            if emotions:
                # Save recording
                save_recording(emotions, audio_path, intensity)
                
                # Display results
                st.success("✅ Analysis Complete!")
                
                st.markdown("### 🎯 Emotion Detection Results")
                
                # Dominant emotion
                dominant_emotion = max(emotions, key=emotions.get)
                config = EMOTION_CONFIG[dominant_emotion]
                
                st.markdown(f"""
                <div class="emotion-card">
                    <h2>{config['emoji']} {dominant_emotion}</h2>
                    <p style="font-size: 24px; color: {config['color']};">
                        {emotions[dominant_emotion]*100:.1f}% Confidence
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Emotion gauges
                st.markdown("### 📊 Detailed Breakdown")
                
                cols = st.columns(4)
                for idx, (emotion, score) in enumerate(emotions.items()):
                    with cols[idx % 4]:
                        fig = create_emotion_gauge(emotion, score)
                        st.plotly_chart(fig, use_container_width=True)
                
                # Radar chart
                st.markdown("### 🎯 Emotion Radar")
                fig = create_emotion_radar(emotions)
                st.plotly_chart(fig, use_container_width=True)
                
                # Frequency visualization
                st.markdown("### 📈 Frequency Spectrum")
                fig = create_frequency_visualization(processed_path)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Intensity adjustment
                st.markdown("### 🎚️ Adjust Confidence")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📈 Increase Confidence"):
                        st.session_state.recordings[-1]['confidence'] *= 1.1
                        st.rerun()
                
                with col2:
                    if st.button("📉 Decrease Confidence"):
                        st.session_state.recordings[-1]['confidence'] *= 0.9
                        st.rerun()
                
                with col3:
                    if st.button("🔄 Reset"):
                        st.session_state.recordings[-1]['confidence'] = max(emotions.values())
                        st.rerun()
    
    with tab2:
        st.markdown("### 📊 Compare Recordings")
        
        if len(st.session_state.recordings) < 2:
            st.info("📝 Record at least 2 samples to compare")
        else:
            # Select recordings to compare
            indices = st.multiselect(
                "Select recordings to compare",
                range(len(st.session_state.recordings)),
                default=[len(st.session_state.recordings)-2, len(st.session_state.recordings)-1]
            )
            
            if indices:
                # Create comparison data
                comparison_data = []
                for idx in indices:
                    recording = st.session_state.recordings[idx]
                    comparison_data.append({
                        'Recording': f"#{idx+1} - {recording['dominant_emotion']}",
                        **recording['emotions']
                    })
                
                df = pd.DataFrame(comparison_data)
                
                # Radar comparison
                fig = go.Figure()
                
                for idx, row in df.iterrows():
                    emotions_list = list(EMOTION_CONFIG.keys())
                    values = [row[e] for e in emotions_list]
                    
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=emotions_list,
                        fill='toself',
                        name=row['Recording'],
                        opacity=0.7
                    ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 1]),
                        bgcolor='rgba(30, 41, 59, 0.3)'
                    ),
                    height=500,
                    paper_bgcolor='rgba(15, 23, 42, 0)',
                    font=dict(color='#f1f5f9'),
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Comparison table
                st.markdown("### 📋 Detailed Comparison")
                st.dataframe(df, use_container_width=True)
    
    with tab3:
        st.markdown("### 📈 Analytics Dashboard")
        
        if not st.session_state.recordings:
            st.info("📝 No recordings yet. Start recording to see analytics!")
        else:
            # Create analytics dataframe
            df = pd.DataFrame([
                {
                    'Timestamp': r['timestamp'],
                    'Emotion': r['dominant_emotion'],
                    'Confidence': r['confidence'],
                    'Language': r['language']
                }
                for r in st.session_state.recordings
            ])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Recordings", len(st.session_state.recordings))
            
            with col2:
                avg_confidence = df['Confidence'].mean()
                st.metric("Avg Confidence", f"{avg_confidence*100:.1f}%")
            
            with col3:
                most_common = df['Emotion'].mode()[0]
                st.metric("Most Common Emotion", most_common)
            
            st.markdown("---")
            
            # Emotion distribution pie chart
            col1, col2 = st.columns(2)
            
            with col1:
                emotion_counts = df['Emotion'].value_counts()
                fig = px.pie(
                    values=emotion_counts.values,
                    names=emotion_counts.index,
                    title="Emotion Distribution"
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(15, 23, 42, 0)',
                    font=dict(color='#f1f5f9')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Confidence trend
                fig = px.line(
                    df,
                    x=range(len(df)),
                    y='Confidence',
                    title="Confidence Trend",
                    markers=True
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(15, 23, 42, 0)',
                    plot_bgcolor='rgba(30, 41, 59, 0.5)',
                    font=dict(color='#f1f5f9'),
                    xaxis_title="Recording #",
                    yaxis_title="Confidence"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Recording history
            st.markdown("### 📜 Recording History")
            st.dataframe(df, use_container_width=True)
    
    with tab4:
        st.markdown("### 💬 Feedback & Improvement")
        
        if not st.session_state.recordings:
            st.info("📝 No recordings to provide feedback on yet!")
        else:
            # Select recording to provide feedback
            recording_idx = st.selectbox(
                "Select a recording to provide feedback",
                range(len(st.session_state.recordings)),
                format_func=lambda i: f"#{i+1} - {st.session_state.recordings[i]['dominant_emotion']} ({st.session_state.recordings[i]['timestamp'][:10]})"
            )
            
            recording = st.session_state.recordings[recording_idx]
            
            # Display current prediction
            st.markdown(f"""
            <div class="emotion-card">
                <h3>Current Prediction</h3>
                <p><strong>Emotion:</strong> {recording['dominant_emotion']}</p>
                <p><strong>Confidence:</strong> {recording['confidence']*100:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Feedback form
            st.markdown("### ✏️ Provide Feedback")
            
            col1, col2 = st.columns(2)
            
            with col1:
                correct_emotion = st.selectbox(
                    "What is the correct emotion?",
                    list(EMOTION_CONFIG.keys()),
                    index=list(EMOTION_CONFIG.keys()).index(recording['dominant_emotion'])
                )
            
            with col2:
                is_correct = st.radio(
                    "Was the prediction correct?",
                    ["Yes", "No"],
                    horizontal=True
                )
            
            # Additional feedback
            feedback_text = st.text_area(
                "Additional comments (optional)",
                placeholder="Help us improve by sharing your thoughts...",
                height=100
            )
            
            # Helpfulness rating
            helpfulness = st.slider(
                "How helpful was this analysis?",
                min_value=1,
                max_value=5,
                value=3,
                step=1
            )
            
            # Submit feedback
            if st.button("📤 Submit Feedback", use_container_width=True):
                feedback = {
                    'recording_idx': recording_idx,
                    'predicted_emotion': recording['dominant_emotion'],
                    'correct_emotion': correct_emotion,
                    'is_correct': is_correct == "Yes",
                    'feedback_text': feedback_text,
                    'helpfulness': helpfulness,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save feedback to file
                feedback_file = Path("feedback.jsonl")
                with open(feedback_file, 'a') as f:
                    f.write(json.dumps(feedback) + '\n')
                
                st.success("✅ Feedback submitted! Thank you for helping us improve.")
            
            # Feedback statistics
            st.markdown("---")
            st.markdown("### 📊 Feedback Statistics")
            
            feedback_file = Path("feedback.jsonl")
            if feedback_file.exists():
                feedback_data = []
                with open(feedback_file, 'r') as f:
                    for line in f:
                        feedback_data.append(json.loads(line))
                
                df_feedback = pd.DataFrame(feedback_data)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    accuracy = (df_feedback['is_correct'].sum() / len(df_feedback)) * 100
                    st.metric("Model Accuracy", f"{accuracy:.1f}%")
                
                with col2:
                    avg_helpfulness = df_feedback['helpfulness'].mean()
                    st.metric("Avg Helpfulness", f"{avg_helpfulness:.1f}/5")
                
                with col3:
                    st.metric("Total Feedback", len(df_feedback))

if __name__ == "__main__":
    main()
