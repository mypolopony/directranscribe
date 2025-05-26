# 📡 Directranscribe

**Directranscribe** is a real-time transcription pipeline that captures audio from a Chrome browser tab, transcribes it using OpenAI’s Whisper model, and stores the results in a local SQLite database for later retrieval and analysis. It’s ideal for transcribing streamed content like webinars, meetings, or live TV.

---

## 🔧 Features

- 🎤 **Live Audio Capture** from Chrome tabs (via macOS Loopback + `ffmpeg`)
- 🧠 **Real-Time Transcription** using Whisper via a FastAPI backend
- 💾 **Local Persistence** with SQLite for searchable transcripts
- 🧩 **Chrome Extension** for quick control and integration
- 🐳 **Dockerized** for easy setup and reproducibility

---

## 🏗️ Project Structure

```
directranscribe/
├── app/                   # FastAPI transcription backend
├── sql/                   # SQLite setup and schema
├── img/                   # App icons and static assets
├── main.py                # Launcher for the full pipeline
├── save_to_db.py          # Handles saving transcription chunks
├── background.js          # Chrome extension background script
├── content.js             # Chrome extension tab content script
├── manifest.json          # Chrome extension metadata
├── stream.html            # Extension interface (popup or tab)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Containerized setup
└── README.md              # You’re here!
```

---

## 🚀 Quickstart

### 1. 🐳 Build & Run with Docker

```bash
docker build -t directranscribe .
docker run -p 8000:8000 directranscribe
```

### 2. 🔊 Set Up Loopback Audio (macOS)

To capture browser audio:

- Use [Loopback](https://rogueamoeba.com/loopback/) to create a virtual device that includes Chrome output.
- Set Chrome’s output to this virtual device.
- Confirm with `ffmpeg` that you’re capturing correctly.

### 3. 🧩 Install Chrome Extension

- Load `manifest.json` as an **unpacked extension** in Chrome:
  - Visit `chrome://extensions/`
  - Enable **Developer Mode**
  - Click **"Load unpacked"** and select the project root

### 4. ▶️ Start Transcribing

- Launch the FastAPI backend (`main.py`)
- Use the extension to start capturing
- Transcriptions will be displayed and saved to SQLite automatically

---

## 🧪 Development

### Run Locally (no Docker)

```bash
poetry install  # or `pip install -r requirements.txt`
uvicorn app.main:app --reload
```

### Transcription Output

- Output is saved in a local SQLite DB: `transcripts.db`
- Each record includes timestamped text chunks

---

## 🧠 Future Ideas

- 🔍 **Searchable Web UI** for stored transcripts
- 📤 Export transcripts as `.txt` or `.srt`
- 🌍 OS-agnostic audio capture setup
- 🔐 Authentication for hosted deployments

---

## 🙏 Credits

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Loopback Audio](https://rogueamoeba.com/loopback/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [ffmpeg](https://ffmpeg.org/)

---

## 📜 License

MIT License © 2025 [@mypolopony](https://github.com/mypolopony)

---

## 💬 Feedback

Spotted a bug? Want to contribute? Open an issue or PR! We welcome collaborators.
