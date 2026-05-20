const currentRigData = document.getElementById('current-rig-data');
const proposedUpgradeData = document.getElementById('proposed-upgrade-data');

// Fetch current rig's performance data
fetch('api/current-rig-performance')
  .then(response => response.json())
  .then(data => {
    currentRigData.innerHTML = JSON.stringify(data, null, 2);
  });

// Fetch proposed upgrade's performance data
fetch('api/proposed-upgrade-performance')
  .then(response => response.json())
  .then(data => {
    proposedUpgradeData.innerHTML = JSON.stringify(data, null, 2);
  });