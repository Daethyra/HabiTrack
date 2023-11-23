document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display data when the page loads
    fetchData();

    // Handle form submission
    document.getElementById('new-entry-form').addEventListener('submit', function(event) {
        event.preventDefault();
        addNewEntry();
    });

    // Handle export button click
    document.getElementById('export-button').addEventListener('click', function() {
        exportData();
    });
});

// Function to fetch and display data
function fetchData() {
    fetch('/get_data')
        .then(response => response.json())
        .then(data => updateTable(data))
        .catch(error => console.error('Error:', error));
}

// Function to update the data table
function updateTable(data) {
    let table = '<table id="data-table"><tr><th>Date</th><th>Level</th><th>Emoji</th></tr>';
    data.forEach(row => {
        table += `<tr>
                    <td>${row.date}</td>
                    <td>${row.smoking_level}</td>
                    <td>${row.emoji}</td>
                  </tr>`;
    });
    table += '</table>';
    document.getElementById('data-table').innerHTML = table;
}

// Function to handle new entry form submission
function addNewEntry() {
    const date = document.getElementById('date').value;
    const level = document.getElementById('level').value;
    const data = { date: date, level: level };

    fetch('/add_entry', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status === 'success' ? 'Entry added successfully!' : 'Error adding entry');
        fetchData(); // Refresh data table
    })
    .catch(error => console.error('Error:', error));
}

// Function to export data
function exportData() {
    fetch('/export')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Data exported successfully! Check your server directory for the file.');
            } else {
                alert('Error exporting data');
            }
        })
        .catch(error => console.error('Error:', error));
}
