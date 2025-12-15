# 📸 Screenshot Checklist for Submission

## Required Screenshots (Take these in order)

### ✅ 1. Project Folder Structure
**Location:** `C:\Users\balar\Downloads\music project`
**How to take:**
1. Open File Explorer
2. Navigate to the folder
3. Press `Windows + Shift + S` (Snipping Tool)
4. Select the entire folder view showing all files
5. Save as: `01_folder_structure.png`

**Files that should be visible:**
- app.py
- index.html
- requirements.txt
- README.md
- Procfile
- render.yaml
- run.py
- test_api.py
- test_endpoints.py
- spotify_millsongdata.csv (if visible)

---

### ✅ 2. GitHub Repository
**URL:** https://github.com/BalaKrishnan1708/Music-recommendation
**How to take:**
1. Open the repository in browser
2. Make sure you're on the main branch
3. Take screenshot showing:
   - Repository name
   - File list (app.py, index.html, README.md, etc.)
   - Commit history (optional)
4. Save as: `02_github_repo.png`

---

### ✅ 3. API Health Check
**URL:** `https://your-render-url.onrender.com/api/health`
**How to take:**
1. Open the URL in browser
2. Should show JSON response like:
   ```json
   {
     "status": "healthy",
     "dataset_loaded": true,
     "model_loaded": true,
     "total_songs": 20000
   }
   ```
3. Save as: `03_health_check.png`

---

### ✅ 4. Swagger UI Documentation
**URL:** `https://your-render-url.onrender.com/docs`
**How to take:**
1. Open the URL in browser
2. Should show all API endpoints:
   - GET /
   - GET /api/health
   - GET /api/search
   - POST /api/recommend
3. Take full page screenshot
4. Save as: `04_swagger_ui.png`

---

### ✅ 5. Search Endpoint Test
**URL:** `https://your-render-url.onrender.com/docs`
**Steps:**
1. Go to `/docs`
2. Find `/api/search` endpoint
3. Click "Try it out"
4. Enter query: `love`
5. Enter limit: `5`
6. Click "Execute"
7. Screenshot showing:
   - Request parameters
   - Response code (200)
   - Response body with results
8. Save as: `05_search_endpoint.png`

---

### ✅ 6. Recommendations Endpoint Test
**URL:** `https://your-render-url.onrender.com/docs`
**Steps:**
1. Go to `/docs`
2. Find `/api/recommend` endpoint
3. Click "Try it out"
4. Enter song_name: `Gonna Sing You My Lovesong` (or any song from your dataset)
5. Enter num_recommendations: `10`
6. Click "Execute"
7. Screenshot showing:
   - Request parameters
   - Response code (200)
   - Response body with recommendations and similarity scores
8. Save as: `06_recommendations_endpoint.png`

---

### ✅ 7. Frontend Interface - Before Search
**URL:** `https://your-render-url.onrender.com`
**How to take:**
1. Open the frontend URL
2. Take screenshot showing:
   - Header with title
   - Stats bar (Total Songs, Artists, etc.)
   - Search box
   - "How It Works" section
3. Save as: `07_frontend_before.png`

---

### ✅ 8. Frontend Interface - With Recommendations
**URL:** `https://your-render-url.onrender.com`
**Steps:**
1. Open the frontend URL
2. Enter a song name (e.g., "Gonna Sing You My Lovesong")
3. Click "Get Recommendations"
4. Wait for results to load
5. Screenshot showing:
   - Selected song card (at top)
   - Recommendations header
   - Multiple recommendation cards with:
     - Song names
     - Artist names
     - Similarity scores
6. Save as: `08_frontend_results.png`

---

## 📝 Screenshot Tips

1. **Use Snipping Tool:** Windows + Shift + S
2. **Full Page:** Use browser's full page screenshot (F12 → Cmd/Ctrl + Shift + P → "Capture full size screenshot")
3. **High Quality:** Ensure text is readable
4. **Clean:** Close unnecessary tabs/windows
5. **Consistent:** Use same browser for all screenshots
6. **Naming:** Use descriptive names (01_, 02_, etc.)

---

## ✅ Verification Checklist

Before including in PDF, verify:
- [ ] All screenshots are clear and readable
- [ ] Text in screenshots is not blurry
- [ ] URLs are visible (if showing browser)
- [ ] API responses show actual data
- [ ] Frontend shows the enhanced UI
- [ ] All 8 screenshots are taken

---

## 📦 Organizing Screenshots

Create a folder: `submission_screenshots/`
- 01_folder_structure.png
- 02_github_repo.png
- 03_health_check.png
- 04_swagger_ui.png
- 05_search_endpoint.png
- 06_recommendations_endpoint.png
- 07_frontend_before.png
- 08_frontend_results.png

