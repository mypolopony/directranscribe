# 📡 Directranscribe

**Directranscribe** is a real-time transcription pipeline that captures audio from your system (e.g., a Chrome browser tab via Loopback on macOS), transcribes it using OpenAI’s Whisper model, and stores the results in a local SQLite database for later retrieval and analysis. It’s ideal for transcribing streamed content like webinars, meetings, or live TV using a command-line interface.

---

## 🔧 Features

- 🎤 **Live Audio Capture** from system audio (e.g., Chrome tabs via macOS Loopback + `ffmpeg`)
- 🧠 **Real-Time Transcription** using Whisper via a FastAPI backend
- 💾 **Local Persistence** with SQLite for searchable transcripts
- 命令行 **CLI Control** for starting and managing transcription
- 🔦 **Terminal log preview** via `transcript.log` and direct terminal output
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
├── background.js          # (Optional) Chrome extension background script
├── content.js             # (Optional) Chrome extension tab content script
├── manifest.json          # (Optional) Chrome extension metadata
├── stream.html            # (Optional) Extension interface (popup or tab)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Containerized setup
└── README.md              # You’re here!
```

---

## 🚀 Quickstart (CLI Method)

### 1. 🐳 Build & Run Dockerized Backend

First, build and run the Docker container which hosts the FastAPI transcription backend:
```bash
docker build -t directranscribe .
docker run -p 8000:8000 directranscribe
```
Keep this terminal window open as it runs the server.

### 2. 🔊 Set Up Loopback Audio (macOS)

To capture audio from a specific application like Chrome:
- Use a tool like [Loopback](https://rogueamoeba.com/loopback/) to create a virtual audio device.
- Configure this virtual device to capture audio output from Google Chrome (or your desired audio source).
- Set this virtual device as your system's default input, or identify its input index for `ffmpeg`. You can list devices with `ffmpeg -f avfoundation -list_devices true -i ""`. The CLI script below assumes it's device `:4`.

### 3. 💾 Initialize Database (One-time)

In a new terminal window, in the project directory, initialize the SQLite database if you haven't already:
```bash
sqlite3 transcripts.db < sql/0_init.sql
```
(If the table already exists, this command will show an error, which is fine.)

### 4. ▶️ Start Transcribing via CLI

In a new terminal window (different from the Docker backend and database initialization), navigate to the project directory and run the following script:
```bash
while true; do
  echo "$(date)" >> transcript.log
  # Adjust -i ":4" if your Loopback device has a different index
  ffmpeg -f avfoundation -i ":4" -ac 1 -ar 16000 -t 30 -filter:a "volume=10dB" -y chunk.wav -loglevel quiet
  curl -s -X POST http://localhost:8000/transcribe -F "file=@chunk.wav" \
    | tee -a transcript.log \
    | jq -r .transcript \
    | python3 save_to_db.py "DirectTV" # Label for the transcript source
  echo "---" >> transcript.log
  rm chunk.wav # Clean up the temporary audio file
done
```
- This script will record 30-second audio chunks, send them for transcription, print the transcript to the terminal, and save it to `transcript.log` and the database.
- Press `Ctrl+C` to stop the script.
- The `jq` command is used to extract the transcript text. Ensure `jq` is installed (`brew install jq` on macOS).
- The `python3 save_to_db.py` script saves the transcript to the SQLite database.

---

## 🧪 Development

### Run Locally (no Docker)

```bash
poetry install  # or `pip install -r requirements.txt`
uvicorn app.main:app --reload
```

---

## 🛠️ CLI Transcription Script Details

The primary method for transcription is the following CLI script. It records audio in 30-second chunks, sends them to the local backend for transcription, logs the output, and saves it to a database.

```bash
while true; do
  echo "$(date)" >> transcript.log
  ffmpeg -f avfoundation -i ":4" -ac 1 -ar 16000 -t 30 -filter:a "volume=10dB" -y chunk.wav -loglevel quiet
  curl -s -X POST http://localhost:8000/transcribe -F "file=@chunk.wav" \
    | tee -a transcript.log \
    | jq -r .transcript \
    | python3 save_to_db.py "DirectTV" # Label for the transcript source
  rm chunk.wav # Clean up the temporary audio file
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

![text](img/veryscure.png)

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