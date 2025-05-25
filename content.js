(function () {
  const audioCtx = new AudioContext();
  const streamDest = audioCtx.createMediaStreamDestination();

  const videos = document.querySelectorAll("video, audio");

  videos.forEach(video => {
    const source = audioCtx.createMediaElementSource(video);
    source.connect(streamDest);
    source.connect(audioCtx.destination); // optional
  });

  // Optional: send stream to background script or WebRTC handler
  window.__capturedAudioStream = streamDest.stream;
  console.log("Audio stream captured:", streamDest.stream);
})();