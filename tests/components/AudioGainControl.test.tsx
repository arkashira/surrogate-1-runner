import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import AudioGainControl from '../../src/components/AudioGainControl';
import { AudioProcessor } from '../../src/audio_processing';

describe('AudioGainControl', () => {
    let audioProcessor: AudioProcessor;

    beforeEach(() => {
        audioProcessor = new AudioProcessor();
    });

    it('renders correctly', () => {
        const { getByText } = render(<AudioGainControl audioProcessor={audioProcessor} />);
        expect(getByText('Audio Gain Control')).toBeInTheDocument();
    });

    it('toggles gain boost when checkbox is clicked', () => {
        const { getByLabelText } = render(<AudioGainControl audioProcessor={audioProcessor} />);
        const checkbox = getByLabelText('Audio Gain Control') as HTMLInputElement;

        fireEvent.click(checkbox);
        expect(audioProcessor.gain_boost_enabled).toBe(true);

        fireEvent.click(checkbox);
        expect(audioProcessor.gain_boost_enabled).toBe(false);
    });

    it('shows gain indicator when enabled', () => {
        const { getByText, queryByText } = render(<AudioGainControl audioProcessor={audioProcessor} />);
        const checkbox = getByText('Audio Gain Control') as HTMLInputElement;

        expect(queryByText('🎤 Boost')).not.toBeInTheDocument();

        fireEvent.click(checkbox);
        expect(getByText('🎤 Boost')).toBeInTheDocument();
    });
});