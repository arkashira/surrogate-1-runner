export function applyFilterAndSort(filterValue, sortValue) {
  return fetch("/api/vulnerabilities?filter=" + filterValue + "&sort=" + sortValue)
    .then(response => response.json())
    .then(data => {
      const vulnerabilitiesList = document.getElementById("vulnerabilities-list");
      vulnerabilitiesList.innerHTML = "";

      data.forEach(vulnerability => {
        const vulnerabilityListItem = document.createElement("li");
        vulnerabilityListItem.textContent = vulnerability.name + " (" + vulnerability.severity + ")";
        vulnerabilitiesList.appendChild(vulnerabilityListItem);
      });
    });
}