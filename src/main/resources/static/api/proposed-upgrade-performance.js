fetch('http://localhost:8080/api/proposed-upgrade-performance')
  .then(response => response.json())
  .then(data => {
    // Return performance data
    // ...
  });