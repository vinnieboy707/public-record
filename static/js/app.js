// API Base URL
const API_BASE = '';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadAPIStatus();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    
    searchBtn.addEventListener('click', performSearch);
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

// Toggle all filter checkboxes
function toggleAllFilters(checkbox) {
    const recordTypeCheckboxes = document.querySelectorAll('.record-type');
    recordTypeCheckboxes.forEach(cb => {
        cb.checked = checkbox.checked;
    });
}

// Select specific record type
function selectRecordType(type) {
    // Uncheck "All Records"
    document.querySelector('input[value="all"]').checked = false;
    
    // Uncheck all record types
    document.querySelectorAll('.record-type').forEach(cb => {
        cb.checked = false;
    });
    
    // Check the selected record type
    document.querySelector(`input[value="${type}"]`).checked = true;
    
    // Focus on search input
    document.getElementById('searchInput').focus();
}

// Perform search
async function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    
    if (!query) {
        alert('Please enter a search term');
        return;
    }
    
    // Get selected record types
    const recordTypes = [];
    const allChecked = document.querySelector('input[value="all"]').checked;
    
    if (allChecked) {
        recordTypes.push('all');
    } else {
        document.querySelectorAll('.record-type:checked').forEach(cb => {
            recordTypes.push(cb.value);
        });
    }
    
    if (recordTypes.length === 0) {
        alert('Please select at least one record type');
        return;
    }
    
    // Show loading indicator
    showLoading();
    hideResults();
    
    try {
        const response = await fetch(`${API_BASE}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                record_types: recordTypes
            })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            displayResults(data);
        } else {
            displayError(data.error || 'An error occurred during search');
        }
    } catch (error) {
        hideLoading();
        displayError('Network error: ' + error.message);
    }
}

// Show loading indicator
function showLoading() {
    document.getElementById('loadingIndicator').style.display = 'block';
}

// Hide loading indicator
function hideLoading() {
    document.getElementById('loadingIndicator').style.display = 'none';
}

// Show results section
function showResults() {
    document.getElementById('resultsSection').style.display = 'block';
}

// Hide results section
function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

// Display search results
function displayResults(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = '';
    
    const results = data.results;
    let hasResults = false;
    
    // Icon mapping for record types
    const icons = {
        'court_records': 'fa-gavel',
        'property_records': 'fa-home',
        'business_registration': 'fa-building',
        'government_data': 'fa-landmark',
        'background_check': 'fa-user-check',
        'vehicle_records': 'fa-car'
    };
    
    // Display name mapping
    const displayNames = {
        'court_records': 'Court Records',
        'property_records': 'Property Records',
        'business_registration': 'Business Registration',
        'government_data': 'Government Data',
        'background_check': 'Background Check',
        'vehicle_records': 'Vehicle Records'
    };
    
    for (const [recordType, result] of Object.entries(results)) {
        const card = document.createElement('div');
        card.className = 'result-card';
        
        const hasError = result.error !== undefined;
        const icon = icons[recordType] || 'fa-file';
        const displayName = displayNames[recordType] || recordType;
        
        let badgeClass = 'badge-success';
        let badgeText = 'Results Found';
        
        if (hasError) {
            badgeClass = 'badge-error';
            badgeText = 'Error';
        } else if (result.message && result.message.includes('Mock implementation')) {
            badgeClass = 'badge-warning';
            badgeText = 'Demo Mode';
        }
        
        card.innerHTML = `
            <div class="result-header">
                <div class="result-title">
                    <i class="fas ${icon}"></i>
                    <h4>${displayName}</h4>
                </div>
                <span class="result-badge ${badgeClass}">${badgeText}</span>
            </div>
            <div class="result-content">
                <pre>${JSON.stringify(result, null, 2)}</pre>
            </div>
        `;
        
        resultsContainer.appendChild(card);
        hasResults = true;
    }
    
    if (!hasResults) {
        resultsContainer.innerHTML = '<div class="no-results">No results found</div>';
    }
    
    showResults();
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

// Display error message
function displayError(message) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = `
        <div class="result-card">
            <div class="result-header">
                <div class="result-title">
                    <i class="fas fa-exclamation-circle" style="color: var(--danger-color);"></i>
                    <h4>Error</h4>
                </div>
                <span class="result-badge badge-error">Failed</span>
            </div>
            <div class="result-content">
                <p style="color: var(--danger-color);">${message}</p>
            </div>
        </div>
    `;
    showResults();
}

// Load API status
async function loadAPIStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        const data = await response.json();
        
        if (data.success) {
            displayAPIStatus(data.status);
        }
    } catch (error) {
        console.error('Failed to load API status:', error);
    }
}

// Display API status
function displayAPIStatus(status) {
    const statusContainer = document.getElementById('apiStatusContainer');
    statusContainer.innerHTML = '';
    
    const displayNames = {
        'court_records': 'Court Records',
        'property_records': 'Property Records',
        'business_registration': 'Business Registration',
        'government_data': 'Government Data',
        'background_check': 'Background Check',
        'vehicle_records': 'Vehicle Records'
    };
    
    for (const [api, isConfigured] of Object.entries(status)) {
        const statusItem = document.createElement('div');
        statusItem.className = 'status-item';
        
        const iconClass = isConfigured ? 'active' : 'inactive';
        const displayName = displayNames[api] || api;
        
        statusItem.innerHTML = `
            <div class="status-icon ${iconClass}"></div>
            <span>${displayName}</span>
        `;
        
        statusContainer.appendChild(statusItem);
    }
}

// Export functions for HTML onclick handlers
window.toggleAllFilters = toggleAllFilters;
window.selectRecordType = selectRecordType;
