import React, { useState } from 'react';
import { AudioProcessor } from '../audio_processing';

interface AudioGainControlProps {
    audioProcessor: AudioProcessor;
}

const AudioGainControl: React.FC<AudioGainControlProps> = ({ audioProcessor }) => {
    const [isEnabled, setIsEnabled] = useState(audioProcessor.gain_boost_enabled);

    const handleToggle = () => {
        const newState = !isEnabled;
        setIsEnabled(newState);
        audioProcessor.toggle_gain_boost(newState);
    };

    return (
        <div className="audio-gain-control">
            <label>
                <input
                    type="checkbox"
                    checked={isEnabled}
                    onChange={handleToggle}
                />
                Audio Gain Control
            </label>
            {isEnabled && <span className="gain-indicator">🎤 Boost</span>}
        </div>
    );
};

export default AudioGainControl;