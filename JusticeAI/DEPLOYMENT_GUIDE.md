# JusticeAI Deployment Guide

This guide covers deploying your JusticeAI Multi-Agent Legal Assistance Platform to various platforms.

## 🚀 Quick Deployment Options

### Option 1: GitHub Pages (Frontend Only)
Since this is a Flask application, GitHub Pages won't work directly. You'll need a backend service.

### Option 2: Render.com (Recommended - Free)
1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Connect Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the JusticeAI repository

3. **Configure Service**
   - **Name**: `justiceai`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Environment Variables** (Optional)
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `FLASK_ENV`: `production`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete
   - Your app will be available at `https://justiceai.onrender.com`

### Option 3: Heroku (Free Tier Discontinued)
1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create justiceai-app
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

### Option 4: Railway.app (Free Tier Available)
1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your JusticeAI repository
   - Railway will auto-detect Python and deploy

### Option 5: Vercel (Frontend + Serverless)
1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Follow prompts**
   - Link to existing project or create new
   - Deploy automatically

## 🐳 Docker Deployment

### Local Docker
```bash
# Build image
docker build -t justiceai .

# Run container
docker run -p 5001:5001 justiceai

# Access at http://localhost:5001
```

### Docker Hub
```bash
# Tag image
docker tag justiceai yourusername/justiceai

# Push to Docker Hub
docker push yourusername/justiceai

# Pull and run
docker pull yourusername/justiceai
docker run -p 5001:5001 yourusername/justiceai
```

## ☁️ Cloud Platform Deployment

### AWS (Amazon Web Services)
1. **EC2 Instance**
   ```bash
   # Launch Ubuntu instance
   # Install Python and dependencies
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install -r requirements.txt
   
   # Run with gunicorn
   pip3 install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

2. **Elastic Beanstalk**
   - Create `.ebextensions/python.config`
   - Deploy via EB CLI

### Google Cloud Platform
1. **App Engine**
   - Create `app.yaml`
   - Deploy with `gcloud app deploy`

2. **Cloud Run**
   ```bash
   # Build and deploy
   gcloud builds submit --tag gcr.io/PROJECT_ID/justiceai
   gcloud run deploy --image gcr.io/PROJECT_ID/justiceai
   ```

### Microsoft Azure
1. **Azure App Service**
   - Create web app
   - Deploy via Azure CLI or GitHub Actions

## 🔧 Environment Setup

### Required Environment Variables
```bash
# Optional - for enhanced AI features
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key

# Required for production
FLASK_ENV=production
PORT=5001
```

### Database Setup
- SQLite database is created automatically
- For production, consider PostgreSQL or MySQL

## 📊 Monitoring & Logs

### Application Logs
```bash
# View logs on Render
# Dashboard → Your Service → Logs

# View logs on Heroku
heroku logs --tail

# View logs on Railway
railway logs
```

### Health Check
- Endpoint: `/health`
- Returns agent status and system health

## 🔒 Security Considerations

### Production Security
1. **Environment Variables**
   - Never commit API keys to Git
   - Use platform environment variables

2. **HTTPS**
   - Most platforms provide SSL automatically
   - Ensure HTTPS redirects

3. **Rate Limiting**
   - Consider adding rate limiting for API endpoints
   - Monitor usage and abuse

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Issues
```bash
# Check if port is in use
lsof -i :5001

# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

#### 2. Dependencies Issues
```bash
# Update requirements
pip freeze > requirements.txt

# Install specific versions
pip install -r requirements.txt
```

#### 3. Database Issues
```bash
# Check database file
ls -la database/

# Recreate database
rm database/justiceai.db
# Restart application
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h

# Optimize for low memory
# Use requirements-minimal.txt
```

## 📈 Performance Optimization

### For Production
1. **Use Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

2. **Add Caching**
   - Consider Redis for session storage
   - Cache frequently accessed data

3. **Database Optimization**
   - Use connection pooling
   - Index frequently queried fields

## 🔄 Continuous Deployment

### GitHub Actions
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Render
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Render
      uses: johnbeynon/render-deploy-action@v1.0.0
      with:
        service-id: ${{ secrets.RENDER_SERVICE_ID }}
        api-key: ${{ secrets.RENDER_API_KEY }}
```

## 📞 Support

### Platform Support
- **Render**: [docs.render.com](https://docs.render.com)
- **Heroku**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **Railway**: [docs.railway.app](https://docs.railway.app)
- **Vercel**: [vercel.com/docs](https://vercel.com/docs)

### Application Support
- Check logs for error messages
- Test locally before deploying
- Use health check endpoint: `/health`

---

**Recommended Deployment**: Render.com for easiest setup and free tier
**Alternative**: Railway.app for simple deployment
**For Learning**: Local Docker deployment

Happy Deploying! 🚀
