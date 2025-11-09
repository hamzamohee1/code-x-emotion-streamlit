# Deployment Guide - Code X Emotion Analyzer (Streamlit)

## 🚀 Deployment Options

Choose the easiest option for you:

### 1. **Streamlit Cloud** (Recommended - Easiest)
### 2. **Railway.app** (Full Control)
### 3. **Heroku** (Classic Deployment)
### 4. **Docker** (Self-hosted)

---

## 🎯 Option 1: Streamlit Cloud (Easiest)

**Time to Deploy**: 5 minutes
**Cost**: Free tier available
**Difficulty**: ⭐ Very Easy

### Step 1: Prepare Your Repository

```bash
# Make sure your code is on GitHub
git push origin main
```

### Step 2: Go to Streamlit Cloud

1. Visit https://streamlit.io/cloud
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit to access your GitHub account

### Step 3: Deploy Your App

1. Click **"New app"**
2. Select:
   - **Repository**: `hamzamohee1/code-x-emotion-streamlit`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **"Deploy"**

### Step 4: Add Environment Variables

1. Click **"Settings"** (gear icon)
2. Go to **"Secrets"** tab
3. Add your Hugging Face API key:

```toml
HUGGING_FACE_API_KEY = "hf_your_token_here"
```

4. Click **"Save"**

### Step 5: Your App is Live!

Your app will be available at:
```
https://code-x-emotion-streamlit.streamlit.app
```

**That's it!** Your app is now live and will auto-update when you push to GitHub.

---

## 🚂 Option 2: Railway.app

**Time to Deploy**: 10 minutes
**Cost**: Free tier with $5/month credit
**Difficulty**: ⭐⭐ Easy

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign in with GitHub
3. Create a new project

### Step 2: Deploy from GitHub

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `code-x-emotion-streamlit`
4. Click **"Deploy"**

### Step 3: Add Environment Variables

1. In Railway dashboard, go to **"Variables"**
2. Add:
   ```
   HUGGING_FACE_API_KEY=hf_your_token_here
   ```

### Step 4: Configure Start Command

1. Go to **"Settings"**
2. Set **Start Command**:
   ```bash
   streamlit run app.py --server.port=$PORT
   ```

### Step 5: Your App is Live!

Your app will be available at:
```
https://code-x-emotion-streamlit.up.railway.app
```

---

## 🐳 Option 3: Docker (Self-Hosted)

**Time to Deploy**: 15 minutes
**Cost**: Depends on hosting
**Difficulty**: ⭐⭐⭐ Moderate

### Step 1: Create Dockerfile

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Build Docker Image

```bash
docker build -t code-x-emotion-streamlit .
```

### Step 3: Run Container

```bash
docker run \
  -e HUGGING_FACE_API_KEY=hf_your_token_here \
  -p 8501:8501 \
  code-x-emotion-streamlit
```

### Step 4: Access Your App

Visit: `http://localhost:8501`

---

## 🦸 Option 4: Heroku

**Time to Deploy**: 15 minutes
**Cost**: Paid (free tier discontinued)
**Difficulty**: ⭐⭐ Easy

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Create Procfile

Create a file named `Procfile`:

```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 3: Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create code-x-emotion-streamlit

# Set environment variable
heroku config:set HUGGING_FACE_API_KEY=hf_your_token_here

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Step 4: Your App is Live!

```
https://code-x-emotion-streamlit.herokuapp.com
```

---

## 📋 Environment Variables

All deployment options require:

```
HUGGING_FACE_API_KEY=hf_your_token_here
```

### How to Get Your Token

1. Go to https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Give it a name (e.g., "Code X Emotion Analyzer")
4. Select **"Read"** permission
5. Click **"Create token"**
6. Copy the token
7. Add to your deployment platform

---

## 🔄 Auto-Deploy from GitHub

All platforms support auto-deploy:

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. Your app automatically redeploys!

---

## 🆘 Troubleshooting

### App Crashes on Startup

**Error**: `HUGGING_FACE_API_KEY is not set`

**Solution**: Add the environment variable to your platform

### Slow Performance

**Solution**: 
- Use shorter audio clips (< 30 seconds)
- Upgrade to paid tier for more resources

### Out of Memory

**Solution**:
- Streamlit Cloud: Use free tier (sufficient)
- Railway: Upgrade to paid plan
- Docker: Allocate more memory

### API Rate Limit

**Solution**:
- Hugging Face free tier: 30k requests/month
- Upgrade to Pro for unlimited

---

## 📊 Recommended Deployment

### For Beginners
👉 **Streamlit Cloud** - Easiest, free, no configuration needed

### For Developers
👉 **Railway.app** - More control, affordable, easy setup

### For Production
👉 **Docker + Custom Server** - Full control, scalable

---

## 🎯 Comparison Table

| Feature | Streamlit Cloud | Railway | Docker | Heroku |
|---------|-----------------|---------|--------|--------|
| Ease | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Cost | Free | $5/mo | Variable | Paid |
| Setup Time | 5 min | 10 min | 15 min | 15 min |
| Auto-Deploy | ✅ | ✅ | ❌ | ✅ |
| Custom Domain | ✅ | ✅ | ✅ | ✅ |
| Scaling | Auto | Manual | Manual | Auto |

---

## 🔐 Security Best Practices

1. **Never commit API keys** to GitHub
2. **Use environment variables** for secrets
3. **Keep dependencies updated**:
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```
4. **Monitor logs** for errors
5. **Use HTTPS** (all platforms provide this)

---

## 📈 Monitoring & Logs

### Streamlit Cloud
- View logs in the app menu (⋮)
- Check app health in dashboard

### Railway
- View logs in Deployments tab
- Monitor CPU/Memory usage

### Docker
```bash
docker logs container_id
```

### Heroku
```bash
heroku logs --tail
```

---

## 🚀 Next Steps

1. **Deploy your app** using one of the options above
2. **Test the application** thoroughly
3. **Share your app** with friends
4. **Monitor performance** and logs
5. **Collect user feedback** to improve

---

## 💡 Pro Tips

1. **Custom Domain**: All platforms support custom domains
2. **SSL Certificate**: Automatic HTTPS on all platforms
3. **Analytics**: Add Streamlit analytics for insights
4. **Caching**: Use `@st.cache_data` for performance
5. **Secrets**: Use platform's secret management, not .env files

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Railway Docs**: https://docs.railway.app
- **GitHub Issues**: https://github.com/hamzamohee1/code-x-emotion-streamlit/issues

---

**Your app is ready to go live! Choose your platform and deploy! 🚀**
