# Quick Start: AI Suggestions Feature

## 1-Minute Setup

### Step 1: Get API Key
1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Step 2: Set Environment Variable

**PowerShell (Windows):**
```powershell
$env:GEMINI_API_KEY = "paste_your_key_here"
```

**Command Prompt (Windows):**
```cmd
set GEMINI_API_KEY=paste_your_key_here
```

**Terminal (Linux/Mac):**
```bash
export GEMINI_API_KEY="paste_your_key_here"
```

### Step 3: Install Package
```bash
pip install google-generativeai
```

### Step 4: Restart Server
```bash
python manage.py runserver
```

## Test It

1. Go to: http://localhost:8000/supplies/create/
2. Start typing a supply name (e.g., "keyboard")
3. After 1 second, AI suggestions appear
4. Click buttons to auto-fill fields

## That's It! ✨

The feature is now ready to use. You'll see a blue suggestion box appear as you type supply names.

## What It Suggests

- **Description**: What the item is used for
- **Category**: Best matching category
- **Min Stock Level**: Recommended quantity to keep
- **Unit**: Measurement type (pieces, boxes, etc)

## Need Help?

See `GEMINI_API_SETUP.md` for detailed instructions and troubleshooting.
