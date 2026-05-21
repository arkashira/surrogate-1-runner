import { createVulnerabilitiesFilterController } from "./vulnerabilitiesFilterControllerFactory.js";

const vulnerabilitiesFilterController = createVulnerabilitiesFilterController();

// Initialize the dashboard
document.addEventListener("DOMContentLoaded", function () {
  // Initialize the filter and sort dropdowns
  const filterByVulnerabilitySeveritySelect = document.getElementById("filter-by-vulnerability-severity");
  const sortByVulnerabilityNameSelect = document.getElementById("sort-by-vulnerability-name");

  // Initialize the vulnerabilities list
  const vulnerabilitiesList = document.getElementById("vulnerabilities-list");

  // Initialize the apply filter and sort button
  const applyFilterAndSortButton = document.getElementById("apply-filter-and-sort");

  // Add event listeners to the filter and sort dropdowns
  filterByVulnerabilitySeveritySelect.addEventListener("change", function () {
    const filterValue = this.value;
    const sortValue = sortByVulnerabilityNameSelect.value;

    vulnerabilitiesFilterController.applyFilterAndSort(filterValue, sortValue);
  });

  sortByVulnerabilityNameSelect.addEventListener("change", function () {
    const filterValue = filterByVulnerabilitySeveritySelect.value;
    const sortValue = this.value;

    vulnerabilitiesFilterController.applyFilterAndSort(filterValue, sortValue);
  });

  applyFilterAndSortButton.addEventListener("click", function () {
    const filterValue = filterByVulnerabilitySeveritySelect.value;
    const sortValue = sortByVulnerabilityNameSelect.value;

    vulnerabilitiesFilterController.applyFilterAndSort(filterValue, sortValue);
  });
});