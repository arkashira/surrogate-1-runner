fetch('http://localhost:8080/api/current-rig-performance')
  .then(response => response.json())
  .then(data => {
    // Return performance data
    // ...
  });