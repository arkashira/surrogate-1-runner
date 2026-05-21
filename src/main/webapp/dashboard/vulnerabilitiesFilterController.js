import { applyFilterAndSort } from "./vulnerabilitiesFilter.js";

export class VulnerabilitiesFilterController {
  constructor() {
    this.filterByVulnerabilitySeveritySelect = document.getElementById("filter-by-vulnerability-severity");
    this.sortByVulnerabilityNameSelect = document.getElementById("sort-by-vulnerability-name");
    this.applyFilterAndSortButton = document.getElementById("apply-filter-and-sort");

    this.applyFilterAndSortButton.addEventListener("click", () => {
      const filterValue = this.filterByVulnerabilitySeveritySelect.value;
      const sortValue = this.sortByVulnerabilityNameSelect.value;

      applyFilterAndSort(filterValue, sortValue);
    });
  }
}