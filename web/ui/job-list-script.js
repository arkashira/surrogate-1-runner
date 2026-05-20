document.addEventListener('DOMContentLoaded', function () {
    const jobListTable = document.getElementById('job-list');

    // Simulate fetching job data (replace with actual API call)
    const jobs = [
        { id: '1', status: 'Completed', creationTime: '2023-10-01T12:00:00Z' },
        { id: '2', status: 'Running', creationTime: '2023-10-01T13:00:00Z' },
        { id: '3', status: 'Failed', creationTime: '2023-10-01T14:00:00Z' }
    ];

    jobs.forEach(job => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${job.id}</td>
            <td>${job.status}</td>
            <td>${new Date(job.creationTime).toLocaleString()}</td>
        `;
        jobListTable.appendChild(row);
    });
});