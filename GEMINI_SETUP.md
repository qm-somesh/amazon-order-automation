# 🤖 Google Gemini Integration Guide

## Overview

This project uses **Google Gemini 2.0 Flash** (instead of OpenAI) for the Browser Use AI implementation. Gemini offers:

- ✅ **Generous Free Tier**: 1,500 requests/day
- ✅ **Fast Performance**: Gemini 2.0 Flash is optimized for speed
- ✅ **High Quality**: Excellent reasoning and vision capabilities
- ✅ **Cost Effective**: Much cheaper than OpenAI (if you exceed free tier)

---

## 🚀 Quick Setup

### Step 1: Get Your FREE Gemini API Key

1. Visit: **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy the generated key (starts with `AIza...`)

### Step 2: Add to `.env` File

Open the `.env` file in your project root and add:

```env
# Amazon India Credentials
AMAZON_EMAIL=your_email@example.com
AMAZON_PASSWORD=your_password

# Google Gemini API Key (get free at https://aistudio.google.com/apikey)
GOOGLE_API_KEY=AIzaSy...your_actual_key_here...
```

### Step 3: Install Dependencies (if not done already)

```bash
pip install langchain-google-genai
```

Or just:
```bash
pip install -r requirements.txt
```

### Step 4: Run Browser Use Implementation

```bash
python run.py --mode browseruse
```

---

## 📊 Gemini Free Tier Limits

| Feature | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Requests/Day** | 1,500 | Unlimited |
| **Requests/Minute** | 15 | Custom |
| **Input Tokens** | 1M/min | Custom |
| **Output Tokens** | 32K/min | Custom |

**For this project**: Each automation run uses approximately 1-3 requests, so you can run the automation **500-1500 times per day** for FREE!

---

## 💰 Cost Comparison

| Provider | Model | Cost per Run | Free Tier |
|----------|-------|--------------|-----------|
| **Google Gemini** | gemini-2.0-flash-exp | **FREE** or $0.01-0.03 | ✅ 1,500 req/day |
| OpenAI | gpt-4o-mini | $0.02-0.06 | ❌ No free tier |
| Anthropic | claude-3-haiku | $0.03-0.08 | ❌ No free tier |

---

## 🔧 Switching Between Models

Want to try different Gemini models? Edit `src/amazon_automation_browseruse.py`:

```python
# Current (fastest, free):
llm=ChatGoogleGenerativeAI(
    model='gemini-2.0-flash-exp',  # Latest & fastest
    api_key=gemini_key,
    temperature=0.1
)

# Alternative models:
# 'gemini-1.5-flash'        - Stable version
# 'gemini-1.5-pro'          - Higher quality, slower
# 'gemini-2.0-flash-exp'    - Experimental, fastest (recommended)
```

---

## 🆚 Why Gemini Over OpenAI?

### Advantages of Gemini:
1. **FREE Tier**: 1,500 requests/day vs OpenAI's $5 minimum credit
2. **Faster**: Gemini 2.0 Flash is optimized for speed
3. **Great Vision**: Excellent screenshot/page understanding
4. **Lower Cost**: Even if you exceed free tier, it's cheaper
5. **No Phone Required**: OpenAI requires phone verification

### When to Use OpenAI Instead:
- If you already have OpenAI credits
- If you need specific GPT-4 capabilities
- If you're already familiar with OpenAI API

---

## 🔐 Security Best Practices

1. **Never commit `.env` to Git** (already in `.gitignore`)
2. **Rotate API keys** every 3-6 months
3. **Use environment-specific keys** (dev vs prod)
4. **Monitor usage** at https://aistudio.google.com

---

## 📞 Troubleshooting

### Error: "GOOGLE_API_KEY not found"
- Ensure `.env` file exists in project root
- Verify the key is spelled exactly: `GOOGLE_API_KEY`
- Restart your terminal/IDE after adding the key

### Error: "Quota exceeded"
- You've hit the 1,500 requests/day limit
- Wait 24 hours or upgrade to paid tier
- Check usage at https://aistudio.google.com

### Error: "Invalid API key"
- Verify key is correct (should start with `AIza`)
- Regenerate key at https://aistudio.google.com/apikey
- Check for extra spaces in `.env` file

---

## 🎯 Next Steps

1. ✅ Get your FREE Gemini API key
2. ✅ Add it to `.env` file
3. ✅ Run: `python run.py --mode browseruse`
4. ✅ Compare with Playwright: `python run.py --mode both`

**Need help?** Open an issue on GitHub!

---

## 📚 Resources

- **Get API Key**: https://aistudio.google.com/apikey
- **Gemini Pricing**: https://ai.google.dev/pricing
- **Gemini Docs**: https://ai.google.dev/docs
- **LangChain Gemini**: https://python.langchain.com/docs/integrations/chat/google_generative_ai

---

**Made with ❤️ by qm-somesh**
