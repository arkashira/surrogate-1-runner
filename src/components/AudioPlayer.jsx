import React, { useState, useEffect, useRef } from 'react';

const AudioPlayer = ({ recordingId, audioUrl }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef(null);
  const seekRef = useRef(null);

  // Load saved position from localStorage
  useEffect(() => {
    const savedPosition = localStorage.getItem(`audioPosition_${recordingId}`);
    if (savedPosition && audioRef.current) {
      audioRef.current.currentTime = parseFloat(savedPosition);
    }
  }, [recordingId]);

  // Save position to localStorage on time update
  useEffect(() => {
    if (audioRef.current) {
      const handleTimeUpdate = () => {
        localStorage.setItem(`audioPosition_${recordingId}`, audioRef.current.currentTime.toString());
      };
      audioRef.current.addEventListener('timeupdate', handleTimeUpdate);
      return () => {
        audioRef.current.removeEventListener('timeupdate', handleTimeUpdate);
      };
    }
  }, [recordingId]);

  // Handle metadata loading
  const handleLoadedMetadata = () => {
    setDuration(audioRef.current.duration);
    const savedPosition = localStorage.getItem(`audioPosition_${recordingId}`);
    if (savedPosition) {
      audioRef.current.currentTime = parseFloat(savedPosition);
    }
  };

  // Handle play/pause toggle
  const togglePlayPause = () => {
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  // Handle seeking
  const handleSeek = (e) => {
    const newTime = parseFloat(e.target.value);
    audioRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  };

  // Format time for display
  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  return (
    <div className="audio-player">
      <audio
        ref={audioRef}
        src={audioUrl}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={() => setIsPlaying(false)}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onTimeUpdate={() => setCurrentTime(audioRef.current.currentTime)}
      />
      
      <div className="controls">
        <button onClick={togglePlayPause}>
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        
        <div className="seek-container">
          <input
            ref={seekRef}
            type="range"
            min="0"
            max={duration || 0}
            value={currentTime}
            onChange={handleSeek}
            className="seek-slider"
          />
        </div>
        
        <div className="time-display">
          {formatTime(currentTime)} / {formatTime(duration)}
        </div>
      </div>
    </div>
  );
};

export default AudioPlayer;