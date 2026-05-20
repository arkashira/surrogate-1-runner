async function fetchTransactions() {
  const response = await fetch('/api/history');
  const data = await response.json();
  return data.slice(-100);
}

async function renderTransactions(transactions) {
  const transactionList = document.getElementById('transaction-list');
  transactions.forEach((transaction) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${transaction.status}</td>
      <td>${transaction.chain}</td>
      <td>${transaction.latency}</td>
    `;
    transactionList.appendChild(row);
  });
}

(async () => {
  const transactions = await fetchTransactions();
  renderTransactions(transactions);
})();