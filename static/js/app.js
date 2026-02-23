// API Base URL
const API_BASE = '';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadAPIStatus();
    setupEventListeners();
    initTheme();
    initSearchInput();
    initSkyBackground();
    
    // Check and start tour after everything loads
    if (typeof checkAndStartTour === 'function') {
        checkAndStartTour();
    }
});

// Initialize sky background with dynamic stars, planets, and meteors
function initSkyBackground() {
    const skyBg = document.querySelector('.sky-background');
    if (!skyBg) return;
    
    // Generate stars
    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 60 + '%';
        star.style.animationDelay = Math.random() * 3 + 's';
        skyBg.appendChild(star);
    }
    
    // Generate planets with varied positions
    const planets = [
        { class: 'planet-saturn', top: 15, right: 10 },
        { class: 'planet-mars', top: 60, left: 5 },
        { class: 'planet-jupiter', top: 8, left: 15 },
        { class: 'planet-earth', top: 40, right: 8 },
        { class: 'planet-moon', top: 25, left: 25 },
        { class: 'planet-neptune', top: 70, right: 20 },
        { class: 'planet-venus', top: 45, left: 12 }
    ];
    
    planets.forEach((planetData, index) => {
        const planet = document.createElement('div');
        planet.className = `planet ${planetData.class}`;
        
        // Set position with slight randomization
        if (planetData.top) planet.style.top = (planetData.top + (Math.random() * 5 - 2.5)) + '%';
        if (planetData.left) planet.style.left = (planetData.left + (Math.random() * 5 - 2.5)) + '%';
        if (planetData.right) planet.style.right = (planetData.right + (Math.random() * 5 - 2.5)) + '%';
        
        // Stagger animation delays
        planet.style.animationDelay = `${index * 0.5}s, ${index * 0.7}s`;
        
        skyBg.appendChild(planet);
    });
    
    // Generate shooting stars / meteors
    for (let i = 0; i < 5; i++) {
        const meteor = document.createElement('div');
        meteor.className = 'meteor';
        meteor.style.left = Math.random() * 100 + '%';
        meteor.style.top = Math.random() * 30 + '%';
        meteor.style.animationDelay = (Math.random() * 10 + 5) + 's';
        meteor.style.animationDuration = (Math.random() * 2 + 2) + 's';
        skyBg.appendChild(meteor);
    }
}

// Initialize theme from localStorage
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

// Toggle theme
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    
    // Add animation effect
    const toggleBtn = document.getElementById('themeToggle');
    if (toggleBtn) {
        toggleBtn.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            toggleBtn.style.transform = '';
        }, 300);
    }
}

// Update theme icon
function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (icon) {
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
}

// Initialize search input features
function initSearchInput() {
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearSearch');
    
    if (searchInput && clearBtn) {
        searchInput.addEventListener('input', function() {
            if (this.value.length > 0) {
                clearBtn.classList.add('show');
            } else {
                clearBtn.classList.remove('show');
            }
        });
    }
}

// Clear search
function clearSearch() {
    const searchInput = document.getElementById('searchInput');
    searchInput.value = '';
    document.getElementById('clearSearch').classList.remove('show');
    searchInput.focus();
}

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

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}" 
               style="font-size: 1.5rem; color: var(--${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'warning'}-color);"></i>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
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
        showToast('Please enter a search term', 'warning');
        document.getElementById('searchInput').focus();
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
        showToast('Please select at least one record type', 'warning');
        return;
    }
    
    // Show loading indicator
    showLoading();
    hideResults();
    
    // Scroll to loading indicator
    document.getElementById('loadingIndicator').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'center' 
    });
    
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
            showToast('Search completed successfully!', 'success');
        } else {
            displayError(data.error || 'An error occurred during search');
            showToast('Search failed: ' + (data.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        hideLoading();
        displayError('Network error: ' + error.message);
        showToast('Network error: ' + error.message, 'error');
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
    let cardIndex = 0;
    
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
        cardIndex++;
        const card = document.createElement('div');
        card.className = 'result-card';
        card.style.setProperty('--i', cardIndex);
        
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
    
    // Smooth scroll to results with offset
    setTimeout(() => {
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }, 100);
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
window.toggleTheme = toggleTheme;
window.clearSearch = clearSearch;
