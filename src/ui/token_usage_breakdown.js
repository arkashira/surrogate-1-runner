const tokenUsageTableBody = document.getElementById('tokenUsageBody');

async function fetchTokenUsage() {
  const response = await fetch('/api/token-usage');
  const data = await response.json();
  tokenUsageTableBody.innerHTML = '';
  data.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.apiCall}</td>
      <td>${item.tokensUsed}</td>
    `;
    tokenUsageTableBody.appendChild(row);
  });
}

setInterval(fetchTokenUsage, 5000); // Fetch token usage every 5 seconds
fetchTokenUsage(); // Initial fetch