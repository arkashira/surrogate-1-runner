import { useSelector } from 'react-redux';
import { RootState } from '../redux/reducers';

const llmService = {
  getLLMResponse: async (prompt: string) => {
    const currentProvider = useSelector((state: RootState) => state.provider.currentProvider);
    
    let response;
    switch (currentProvider) {
      case 'openai':
        response = await fetch('https://api.openai.com/v1/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          },
          body: JSON.stringify({
            model: 'text-davinci-003',
            prompt,
            max_tokens: 150,
          }),
        });
        break;
      case 'anthropic':
        response = await fetch('https://api.anthropic.com/v1/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': `${process.env.ANTHROPIC_API_KEY}`,
          },
          body: JSON.stringify({
            prompt,
            max_tokens: 150,
          }),
        });
        break;
      case 'custom':
        response = await fetch('https://api.your-custom-llm.com/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.CUSTOM_API_KEY}`,
          },
          body: JSON.stringify({
            prompt,
            max_tokens: 150,
          }),
        });
        break;
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.choices[0].text;
  },
};