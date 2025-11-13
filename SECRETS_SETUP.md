# Streamlit Secrets Setup

## Local Development

1. Create `~/.streamlit/secrets.toml`:

```toml
HUGGING_FACE_API_KEY = "hf_your_token_here"
```

2. Get token from: https://huggingface.co/settings/tokens

3. Run: `streamlit run app.py`

## Streamlit Cloud

1. Deploy app
2. Click ⋮ → Settings → Secrets
3. Add:
```toml
HUGGING_FACE_API_KEY = "hf_your_token_here"
```
4. Save

## Railway

1. Go to Variables
2. Add: `HUGGING_FACE_API_KEY=hf_your_token_here`

## Docker

```bash
docker run -e HUGGING_FACE_API_KEY=hf_your_token_here -p 8501:8501 code-x-emotion
```
