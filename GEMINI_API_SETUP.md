# Gemini API Setup for Supply Suggestions

## Overview
The auto-suggestions feature uses Google's Gemini API to provide AI-powered recommendations for:
- Supply descriptions
- Category suggestions
- Recommended stock levels
- Unit measurements

## Setup Instructions

### 1. Get Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### 2. Set Environment Variable
Create a `.env` file in the project root with:

```bash
GEMINI_API_KEY=your_api_key_here
```

Or set it in your terminal:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Install Required Package
```bash
pip install google-generativeai
```

### 4. Add to requirements.txt
Already included in the project.

## How It Works

When creating/editing a supply:

1. **User enters a supply name** (e.g., "USB Flash Drive 32GB")
2. **After 1 second of typing**, AI suggestions appear showing:
   - Auto-generated description
   - Suggested category
   - Recommended minimum stock level
   - Appropriate unit of measurement
3. **Click "Apply" buttons** to auto-fill those fields
4. **Complete the form** with other details and submit

## Features

✅ **Real-time suggestions** - Triggered after 1 second of typing
✅ **Smart categorization** - Auto-suggests appropriate category
✅ **Stock recommendations** - Based on typical usage patterns
✅ **One-click apply** - Quickly fill form fields
✅ **Error handling** - Graceful fallback if API unavailable

## API Endpoint

- **URL**: `/api/supply-suggestions/`
- **Method**: POST
- **Authentication**: Login required
- **Request**: `{"name": "supply name"}`
- **Response**:
```json
{
  "success": true,
  "description": "...",
  "category": "...",
  "suggested_quantity": 50,
  "unit": "pieces"
}
```

## Troubleshooting

### "API not configured"
- Check if GEMINI_API_KEY environment variable is set
- Restart your Django development server after setting the variable

### "Invalid JSON response"
- The API sometimes returns markdown code blocks
- The code automatically cleans these up

### Slow responses
- Gemini API calls take 2-5 seconds
- This is normal; the UI shows a loading spinner

### Rate limiting
- Google's free tier has rate limits
- For production, upgrade to a paid API plan
