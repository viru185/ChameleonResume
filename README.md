# <p align="center"> NOTE - WORKING ON THIS PROJECT </p>

# 🦎 ChameleonResume

**ChameleonResume** is a smart resume generator that tailors your resume to match any job description using AI (powered by Mistral via Ollama). It adapts your experience just like a chameleon adapts its color.

---

## ✨ Features
- Input job descriptions via text, file, or URL
- Supports rich candidate data from a YAML file
- Uses local AI (Ollama + Mistral) for free, private resume generation
- Exports resume as both HTML and PDF
- Logs all operations for debugging

---

## 🚀 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/ChameleonResume.git
cd ChameleonResume
```

### 2. Set Up Environment
```bash
pip install -r requirements.txt
```

### 3. Start Ollama with Mistral
```bash
ollama run mistral
```

### 4. Add Your Candidate Profile
Place your `candidate.yaml` inside the `private/` folder. Structure reference is in the sample file.

---

## 🛠 Usage
```bash
python main.py
```
Then follow the prompt to input the job description.

---

## 📁 Output
- HTML resume: `output/resume.html`
- PDF resume: `output/resume.pdf`

---

## 🧼 Clean Up / Privacy
Everything sensitive is kept inside:
```
private/
```
and ignored by Git using `.gitignore`.

---

## 📓 Logs
All app activity is logged to:
```
logs/chameleon_resume.log
```

---

## 📬 Contributions
PRs are welcome! Open an issue or submit improvements.

---

## 📄 License
MIT License
