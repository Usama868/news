# خبروں کا تجزیہ کار - Deployment Instructions

## مفت ہوسٹنگ کے لیے آپشنز:

### 1. Railway (تجویز کردہ)
- https://railway.app پر جائیں
- GitHub سے connect کریں
- Repository upload کریں
- Automatic deployment

### 2. Render
- https://render.com پر جائیں
- Free tier available
- GitHub integration

### 3. Vercel (Frontend کے لیے)
- https://vercel.com پر جائیں
- Static sites کے لیے بہترین

## لوکل استعمال:

### Requirements:
- Python 3.11+
- Node.js 18+

### Steps:
1. `cd news-summarizer-backend`
2. `source venv/bin/activate`
3. `python src/main.py`
4. Browser میں `http://localhost:5000` کھولیں

## فائلز:
- Frontend: `/news-summarizer/`
- Backend: `/news-summarizer-backend/`
- Combined: Backend کے static folder میں frontend build موجود ہے

## استعمال:
1. خبر کا متن یا لنک داخل کریں
2. "تجزیہ شروع کریں" پر کلک کریں
3. Lower Thirds، سوالات، اور تجزیہ حاصل کریں
4. Copy buttons سے آسانی سے copy کریں

## Features:
- ✅ Urdu RTL Support
- ✅ Responsive Design
- ✅ Professional LTs Generation
- ✅ Panel Questions
- ✅ Detailed Analysis
- ✅ Copy to Clipboard
- ✅ URL and Text Input Support

