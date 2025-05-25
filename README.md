# 📡 Directranscribe

**Directranscribe** is a real-time transcription pipeline that captures audio from a Chrome browser tab, transcribes it using OpenAI’s Whisper model, and stores the results in a local SQLite database for later retrieval and analysis. It’s ideal for transcribing streamed content like webinars, meetings, or live TV.

---

## 🔧 Features

- 🎤 **Live Audio Capture** from Chrome tabs (via macOS Loopback + `ffmpeg`)
- 🧠 **Real-Time Transcription** using Whisper via a FastAPI backend
- 💾 **Local Persistence** with SQLite for searchable transcripts
- 🧩 **Chrome Extension** for quick control and integration
- 🔦 **Terminal log preview** via `transcript.log`
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

---

## 🛠️ Advanced CLI Usage

Record from Chrome → transcribe → log every 30 seconds:

```bash
while true; do
  echo "$(date)" >> transcript.log
  ffmpeg -f avfoundation -i ":4" -ac 1 -ar 16000 -t 30 -filter:a "volume=10dB" -y chunk.wav -loglevel quiet
  curl -s -X POST http://localhost:8000/transcribe -F "file=@chunk.wav"     | tee -a transcript.log     | jq -r .transcript     | python3 save_to_db.py "DirectTV"
  echo "---" >> transcript.log
done
```

---

## 💾 Database Schema

Initialize with:

```bash
sqlite3 transcripts.db < sql/0_init.sql
```

Example schema:

```sql
CREATE TABLE transcripts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  label TEXT,
  transcript TEXT
);
```

Query with:

```bash
sqlite3 transcripts.db "SELECT timestamp, label, transcript FROM transcripts ORDER BY id DESC LIMIT 10;"
```

---

## 🧠 Future Ideas

- 🔍 **Searchable Web UI** for stored transcripts
- 📤 Export transcripts as `.txt` or `.srt`
- 🌍 OS-agnostic audio capture setup
- 🔐 Authentication for hosted deployments
- 🏷️ Auto-tagging and show detection
- 🤖 Full-text search or LLM summarization

---

## 📸 Examples

![example](img/example.png)
![example](img/another_example.png)
---

## Example Text

```
Sun May 25 04:53:34 PDT 2025
 We all work so hard. It's so funny how, like, the racing 
 world and dairy farmers have so much in common. I mean, 
 I feel like we have a pit crew that helps run our farm. I
 mean, it takes a bunch of people just like an Indie car 
 driver does. You know, we're the fourth generation raising 
 the fifth generation. I have two daughters. So to be, this 
 is only the second time two women have been milk presenters
 at the Indianapolis 500. So to be a role model and help 
 inspire our children. We're hoping for that and we're a 
 robot dairy. So we have robots at milk our cows. So we're
 our cow, now.
```

## Another example

![text](img/another_example.png)

```
---
Sun May 25 06:40:15 PDT 2025
 Right before baking you take the dough and you make a couple 
 of slashes or scores on the top of the bread now You can use
  a very sharp knife to do this But why not use the right tool
   for the job and that tool is a baker's lawn and Adam's here 
   He's gonna tell us more exactly as he said you can get away 
   with a paring knife You can get away with the utility knife 
   if you want but the right tool is a baker's lawn Let's back 
   up for a second the reason you do this is because when bread 
   bakes the moisture in the
---
Sun May 25 06:40:53 PDT 2025
 your ruptures, it can cause mis-shape and load. If you make 
 those slashes scoring it, you control the weak spot where 
 the moisture escapes. Engineering the vents. Yeah, you're 
 engineering the vents, exactly. That's the perfect way to 
 put it. And this loaf shows that. There were a couple of 
 scores. And so it was predictable how the bread was going to 
 expand. Another reason to do it is to put ears in a loaf. 
 That's very typical in a baguette. That's the little flap 
 that sticks up. And that's the mark of a well-made baguette.
---
Sun May 25 06:41:33 PDT 2025
 They're great. Yeah, you'd expect to buy that but you can 
 actually do that at home. You can do that at home if you h
 ave the right Lomb and that's what we're going to talk 
 about. Lomb is French for Blade. We tested seven 
 breadloms. They were priced between seven dollars and a 
 little over 29 dollars and testers use them to score 10 
 loaves of penneleve and eight baguettes and then the 
 baguettes in particular they put in those slashes that 
 will make the ears. Of course. These are basically raised
---
```

## 🙏 Credits

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Loopback Audio](https://rogueamoeba.com/loopback/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [ffmpeg](https://ffmpeg.org/)