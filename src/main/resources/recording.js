const streamsToRecord = document.getElementById('streams-to-record');
const recordedStreams = document.getElementById('recorded-streams');
const recordButton = document.getElementById('record-button');

// Fetch available streams and populate the select element
async function fetchStreams() {
  const response = await fetch('api/streams');
  const data = await response.json();
  data.forEach(stream => {
    const option = document.createElement('option');
    option.value = stream.id;
    option.textContent = stream.name;
    streamsToRecord.appendChild(option);
  });
}

fetchStreams();

// Handle recording a stream
recordButton.addEventListener('click', async () => {
  const streamId = streamsToRecord.value;
  const response = await fetch(`api/record/${streamId}`, { method: 'POST' });
  if (response.ok) {
    const stream = await response.json();
    const listItem = document.createElement('li');
    listItem.textContent = stream.name;
    recordedStreams.appendChild(listItem);
  }
});