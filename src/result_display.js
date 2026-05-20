
const table = require('cli-table3');

function displayResults(results) {
  const tableData = [];

  results.forEach((result) => {
    tableData.push([
      result.importPath,
      result.isError ? 'Error' : 'OK',
      result.errorMessage || '',
    ]);
  });

  const tableInstance = new table({
    head: ['Import Path', 'Status', 'Error Message'],
    colWidths: [50, 7, 50],
  });

  tableInstance.push(tableData);
  console.log(tableInstance.toString());
}

module.exports = { displayResults };