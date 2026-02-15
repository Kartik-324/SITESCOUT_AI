// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const generateBtn = document.getElementById('generateBtn');
const searchQueryInput = document.getElementById('searchQuery');
const maxResultsInput = document.getElementById('maxResults');
const rangeValue = document.getElementById('rangeValue');
const loadingSection = document.getElementById('loadingSection');
const loadingText = document.getElementById('loadingText');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const errorText = document.getElementById('errorText');
const resultsBody = document.getElementById('resultsBody');
const totalLeadsSpan = document.getElementById('totalLeads');
const sendEmailsBtn = document.getElementById('sendEmailsBtn');
const downloadBtn = document.getElementById('downloadBtn');
const viewSheetsBtn = document.getElementById('viewSheetsBtn');
const emailModal = document.getElementById('emailModal');
const modalClose = document.querySelector('.modal-close');
const copyEmailBtn = document.getElementById('copyEmailBtn');
const retryBtn = document.getElementById('retryBtn');

// Stats elements
const withWebsiteSpan = document.getElementById('withWebsite');
const withoutWebsiteSpan = document.getElementById('withoutWebsite');
const withEmailSpan = document.getElementById('withEmail');
const avgRatingSpan = document.getElementById('avgRating');

// State
let currentLeads = [];
let currentSheetId = '1n2SQq5Cf1YPg0CuwLh-GjuX8nCt7HFWXlj73DhupXM0'; // Update with your Sheet ID

// Event Listeners
generateBtn.addEventListener('click', handleGenerateLeads);
sendEmailsBtn.addEventListener('click', handleSendEmails);
downloadBtn.addEventListener('click', handleDownloadJSON);
viewSheetsBtn.addEventListener('click', handleViewSheets);
modalClose.addEventListener('click', closeEmailModal);
copyEmailBtn.addEventListener('click', handleCopyEmail);
retryBtn.addEventListener('click', handleRetry);

// Range slider update
maxResultsInput.addEventListener('input', (e) => {
    rangeValue.textContent = e.target.value;
});

// Close modal when clicking overlay
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('modal-overlay')) {
        closeEmailModal();
    }
});

// Main Functions
async function handleGenerateLeads() {
    const query = searchQueryInput.value.trim();
    const maxResults = parseInt(maxResultsInput.value);

    // Validation
    if (!query) {
        showError('Please enter a search query (e.g., "best cafes in bhopal")');
        return;
    }

    if (maxResults < 5 || maxResults > 25) {
        showError('Number of leads must be between 5 and 25');
        return;
    }

    // Hide previous results/errors
    hideAllSections();
    showLoading('🔍 Searching for businesses...');
    updateLoadingSteps(0);

    try {
        const response = await fetch(`${API_BASE_URL}/generate-leads`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                max_results: maxResults
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate leads');
        }

        updateLoadingSteps(1);
        loadingText.textContent = '🌐 Analyzing websites...';

        const data = await response.json();
       
        if (data.success) {
            currentLeads = data.leads;
            displayResults(data);
           
            if (data.saved_to_sheets) {
                console.log('✅ Data saved to Google Sheets successfully!');
            }
        } else {
            throw new Error(data.message || 'Unknown error occurred');
        }

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred while generating leads. Please try again.');
    } finally {
        hideLoading();
    }
}

async function handleSendEmails() {
    if (currentLeads.length === 0) {
        showError('No leads available to send emails');
        return;
    }

    // Filter leads that have emails
    const leadsWithEmails = currentLeads.filter(lead => 
        lead.email && 
        lead.email !== '' && 
        lead.email !== 'Not found'
    );

    if (leadsWithEmails.length === 0) {
        showError('No leads have valid email addresses');
        return;
    }

    // Create detailed confirmation message
    const confirmSend = confirm(
        `🚀 Ready to send ${leadsWithEmails.length} cold emails?\n\n` +
        `Recipients:\n${leadsWithEmails.map(l => `• ${l.business_name} (${l.email})`).slice(0, 5).join('\n')}` +
        `${leadsWithEmails.length > 5 ? `\n...and ${leadsWithEmails.length - 5} more` : ''}\n\n` +
        '⚠️ Make sure your SMTP settings are configured in backend/.env\n\n' +
        'Click OK to proceed.'
    );

    if (!confirmSend) return;

    showLoading('📧 Sending emails...');

    try {
        const response = await fetch(`${API_BASE_URL}/send-emails`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                leads: leadsWithEmails,
                subject: 'Website Development Opportunity - Grow Your Business Online'
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to send emails');
        }

        const data = await response.json();
       
        hideLoading();
       
        if (data.success) {
            alert(
                `✅ Email Campaign Completed!\n\n` +
                `📨 Successfully sent: ${data.sent}\n` +
                `❌ Failed: ${data.failed}\n\n` +
                `${data.failed > 0 ? `Failed emails:\n${data.errors.slice(0, 3).join('\n')}${data.errors.length > 3 ? '\n...' : ''}` : 'All emails sent successfully!'}`
            );
        } else {
            throw new Error('Email sending failed');
        }

    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showError(error.message || 'An error occurred while sending emails');
    }
}

function handleDownloadJSON() {
    if (currentLeads.length === 0) {
        showError('No leads available to download');
        return;
    }

    const dataStr = JSON.stringify(currentLeads, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
   
    const timestamp = new Date().toISOString().split('T')[0];
    const link = document.createElement('a');
    link.href = url;
    link.download = `leads_${timestamp}_${currentLeads.length}_results.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

function handleViewSheets() {
    const sheetUrl = `https://docs.google.com/spreadsheets/d/${currentSheetId}`;
    window.open(sheetUrl, '_blank');
}

function handleRetry() {
    hideAllSections();
    searchQueryInput.focus();
}

function handleCopyEmail() {
    const emailContent = document.getElementById('emailContent').textContent;
    navigator.clipboard.writeText(emailContent).then(() => {
        copyEmailBtn.textContent = '✅ Copied!';
        setTimeout(() => {
            copyEmailBtn.textContent = '📋 Copy to Clipboard';
        }, 2000);
    });
}

// Display Functions
function displayResults(data) {
    resultsSection.classList.remove('hidden');
    totalLeadsSpan.textContent = data.total_leads;
   
    // Calculate stats
    const withWebsite = data.leads.filter(l => l.website_exists).length;
    const withoutWebsite = data.leads.filter(l => !l.website_exists).length;
    const withEmail = data.leads.filter(l => l.email && l.email !== '').length;
    const ratings = data.leads.filter(l => l.rating && l.rating !== '').map(l => parseFloat(l.rating));
    const avgRating = ratings.length > 0 ? (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(1) : 'N/A';
   
    // Update stats
    withWebsiteSpan.textContent = withWebsite;
    withoutWebsiteSpan.textContent = withoutWebsite;
    withEmailSpan.textContent = withEmail;
    avgRatingSpan.textContent = avgRating;
   
    // Clear previous results
    resultsBody.innerHTML = '';
   
    // Populate table
    data.leads.forEach((lead, index) => {
        const row = document.createElement('tr');
       
        // Priority highlight for businesses without websites
        if (!lead.website_exists) {
            row.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)';
        }
       
        const websiteCell = lead.website_exists && lead.website !== 'N/A'
            ? `<a href="${escapeHtml(lead.website)}" target="_blank" style="color: var(--primary); text-decoration: none; font-weight: 600;">Visit Site</a>`
            : `<span class="badge badge-warning">N/A</span>`;
       
        const statusBadge = !lead.website_exists
            ? `<span class="badge badge-priority">🎯 PRIORITY</span>`
            : `<span class="badge badge-success">✓ Has Website</span>`;
       
        const emailDisplay = lead.email && lead.email !== ''
            ? `<div style="font-size: 13px; word-break: break-all;">${escapeHtml(lead.email)}</div>`
            : `<span class="badge badge-danger">Not found</span>`;
       
        const phoneDisplay = lead.phone && lead.phone !== ''
            ? `<div style="font-size: 13px; color: var(--gray-900); font-weight: 500; margin-top: 6px;">${escapeHtml(lead.phone)}</div>`
            : `<span class="badge badge-danger" style="margin-top: 6px; display: inline-block;">Not found</span>`;
       
        const ratingDisplay = lead.rating
            ? `<span style="color: var(--warning); font-weight: 600;">⭐ ${escapeHtml(lead.rating)}</span>`
            : `<span style="color: var(--gray-700);">-</span>`;
       
        const addressDisplay = lead.address && lead.address !== ''
            ? `<div style="font-size: 12px; color: var(--gray-700); max-width: 200px;">${escapeHtml(lead.address)}</div>`
            : `<span style="color: var(--gray-700);">-</span>`;
       
        row.innerHTML = `
            <td style="font-weight: 600; color: var(--gray-700);">${index + 1}</td>
            <td>
                <div style="font-weight: 600; color: var(--gray-900);">
                    ${escapeHtml(lead.business_name)}
                </div>
            </td>
            <td>${emailDisplay}</td>
            <td>${phoneDisplay}</td>
            <td>${ratingDisplay}</td>
            <td>${websiteCell}</td>
            <td>${addressDisplay}</td>
            <td>${statusBadge}</td>
            <td>
                <button class="btn-view-email" onclick="viewEmail(${index})">
                    📧 View Email
                </button>
            </td>
        `;
        resultsBody.appendChild(row);
    });
}

function viewEmail(index) {
    const lead = currentLeads[index];
    if (!lead || !lead.cold_email) {
        alert('No email available for this lead');
        return;
    }
   
    const emailContent = document.getElementById('emailContent');
    emailContent.textContent = lead.cold_email;
    emailModal.classList.remove('hidden');
}

function closeEmailModal() {
    emailModal.classList.add('hidden');
}

// UI Helper Functions
function showLoading(message = 'Processing...') {
    loadingText.textContent = message;
    loadingSection.classList.remove('hidden');
}

function hideLoading() {
    loadingSection.classList.add('hidden');
}

function updateLoadingSteps(activeIndex) {
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        if (index === activeIndex) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}

function showError(message) {
    errorText.textContent = message;
    errorSection.classList.remove('hidden');
   
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorSection.classList.add('hidden');
    }, 5000);
}

function hideAllSections() {
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    loadingSection.classList.add('hidden');
}

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.toString().replace(/[&<>"']/g, m => map[m]);
}

// Make viewEmail globally accessible
window.viewEmail = viewEmail;

// Auto-focus search input on load
window.addEventListener('load', () => {
    searchQueryInput.focus();
});