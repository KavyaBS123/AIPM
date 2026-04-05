# 🚀 QUICK START GUIDE - AI Product Manager Environment

**Status**: ✅ **FULLY CONFIGURED WITH API KEY**

---

## 📋 Your Setup

- **API Key**: ✅ Configured in `.env`
- **Project Root**: `C:\Users\Kavya\OneDrive\Desktop\AIPM`
- **Python**: 3.8+ required
- **Environment**: Ready to run

---

## ⚡ Quick Start (Choose One)

### **Option 1: Run Demo (Simplest - No Server Needed)**

```powershell
cd C:\Users\Kavya\OneDrive\Desktop\AIPM
python demo.py
```

**What you'll see:**
- Interactive walkthrough of the environment
- Example agent actions and rewards
- Task completion in real-time
- ✅ **No setup required** — runs immediately

**Expected output:**
```
================================================================================
AI Product Manager Environment - Local Demo
================================================================================

[1] Creating environment...
✓ Environment created

[2] Resetting environment...
✓ Environment reset
  Initial observation:
  - Summarized feedback: User complaints about...
  - Available actions: ['prioritize', 'reject', 'delay', 'request_info', 'finalize']

[DEMO] Taking actions...
```

---

### **Option 2: Run Full AI Inference with OpenAI (Recommended)**

**Terminal 1 - Start API Server:**

```powershell
cd C:\Users\Kavya\OneDrive\Desktop\AIPM
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ Server is running! Keep this terminal open.

**Terminal 2 - Run AI Inference:**

```powershell
cd C:\Users\Kavya\OneDrive\Desktop\AIPM
python inference.py task_001 scenario_1_saas_analytics
```

**Expected output:**
```
======================================================================
AI Product Manager Inference
======================================================================

[START] task_id=task_001 scenario_id=scenario_1_saas_analytics
[STEP 1] action=request_info feature=N/A reward=0.00
[STEP 2] action=prioritize feature=F001 reward=0.40
[STEP 3] action=finalize feature=N/A reward=0.10
[END] total_reward=0.50 grader_score=0.67 steps=3

======================================================================
Task Completed Successfully!
======================================================================
```

---

### **Option 3: Use Batch Scripts (Windows)**

**1. Verify setup:**
```powershell
RUN_SETUP.bat
```

**2. Start API server:**
```powershell
start_api.bat
```

**3. In new terminal, run inference:**
```powershell
cd C:\Users\Kavya\OneDrive\Desktop\AIPM
python inference.py task_002 scenario_2_ecommerce
```

---

## 🎯 Try Different Tasks

### Easy Tasks (3 steps)
```powershell
python inference.py task_001 scenario_1_saas_analytics
python inference.py task_001 scenario_2_ecommerce
python inference.py task_001 scenario_3_healthcare
```

### Medium Tasks (6 steps)
```powershell
python inference.py task_002 scenario_2_ecommerce
python inference.py task_002 scenario_4_collaboration
python inference.py task_002 scenario_5_finance
```

### Hard Tasks (10 steps)
```powershell
python inference.py task_003 scenario_3_healthcare
python inference.py task_003 scenario_1_saas_analytics
python inference.py task_003 scenario_5_finance
```

---

## 📊 Available Scenarios

| Scenario | ID | Difficulty Options |
|----------|----|--------------------|
| **SaaS Analytics** | scenario_1_saas_analytics | ✅ task_001, task_002, task_003 |
| **E-Commerce** | scenario_2_ecommerce | ✅ task_001, task_002, task_003 |
| **Healthcare SaaS** | scenario_3_healthcare | ✅ task_001, task_002, task_003 |
| **Collaboration Tool** | scenario_4_collaboration | ✅ task_001, task_002, task_003 |
| **Personal Finance** | scenario_5_finance | ✅ task_001, task_002, task_003 |

---

## 🔍 Verify Everything is Working

### Check Setup:
```powershell
python setup_verify.py
```

### Check API Server Health:
```powershell
curl http://localhost:8000/health
```

### View API Documentation:
Open browser and go to: **http://localhost:8000/docs**

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pydantic'`

**Solution:**
```powershell
pip cache purge
pip install --only-binary :all: -r requirements.txt
```

---

### Issue: API Server won't start

**Solution:**
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# If in use, either:
# 1. Kill the process: taskkill /PID <PID> /F
# 2. Change API_BASE_URL in .env to different port
```

---

### Issue: Inference script says "API not running"

**Solution:**
1. Ensure `python main.py` is running in another terminal
2. Check `API_BASE_URL` in `.env` matches the server URL
3. Wait 2-3 seconds after starting server before running inference

---

### Issue: OpenAI API errors

**Solution:**
```powershell
# Verify API key is set
echo $env:OPENAI_API_KEY

# Or check if it's in .env
type .env
```

---

## 📈 What to Expect: Output Format

All inference runs produce:

```
[START] task_id=<id> scenario_id=<id>
[STEP 1] action=<type> feature=<id> reward=<float>
[STEP 2] action=<type> feature=<id> reward=<float>
[STEP 3] action=<type> feature=<id> reward=<float>
[END] total_reward=<float> grader_score=<float> steps=<int>
```

**Interpret the results:**
- ✅ **High total_reward**: Good decisions (closer to 1.0 is better)
- ✅ **grader_score near 1.0**: Excellent task completion
- ✅ **Fewer steps**: Efficient reasoning
- ✅ **Clear action types**: Valid decision-making

---

## 🎓 Learning Path

1. **Start with demo:** `python demo.py`
2. **Read scenarios:** Check `scenarios/` folder
3. **Understand tasks:** Check `tasks/` folder
4. **Try easy task:** `python inference.py task_001 scenario_1_saas_analytics`
5. **Run multiple scenarios:** Mix different task/scenario combinations
6. **Explore API:** Visit `http://localhost:8000/docs`

---

## 📚 Project Structure

```
AIPM/
├── pm_env/              # Core environment
├── api/                 # FastAPI server
├── tasks/               # Task definitions
├── graders/             # Scoring logic
├── scenarios/           # Scenario data
├── main.py              # Run API server
├── inference.py         # Run AI inference
├── demo.py              # Run demo (no API needed)
├── example_run.py       # Example script
├── .env                 # ✅ Configuration file (with API key)
└── requirements.txt     # Dependencies
```

---

## ✅ Checklist

- [x] `.env` file created with API key
- [x] `setup_verify.py` created for verification
- [x] `start_api.bat` created for easy server start
- [x] Full documentation ready
- [x] Project is **production-ready**

---

## 🚀 Ready to Go!

**Next step:** Choose an option above and run it!

```powershell
# Quickest test:
python demo.py

# Full AI test (2 terminals):
# Terminal 1:
python main.py

# Terminal 2:
python inference.py task_001 scenario_1_saas_analytics
```

---

**Last Updated**: April 4, 2026  
**Status**: ✅ Production Ready
