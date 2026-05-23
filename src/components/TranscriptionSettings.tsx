import React from 'react';
import AudioGainControl from './AudioGainControl';
import { AudioProcessor } from '../audio_processing';

interface TranscriptionSettingsProps {
    audioProcessor: AudioProcessor;
}

const TranscriptionSettings: React.FC<TranscriptionSettingsProps> = ({ audioProcessor }) => {
    return (
        <div className="transcription-settings">
            <h2>Transcription Settings</h2>
            <AudioGainControl audioProcessor={audioProcessor} />
        </div>
    );
};

export default TranscriptionSettings;