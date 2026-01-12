// ===== State Management =====
let currentPaper = null;
let currentFile = null;

// ===== DOM Elements =====
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const selectedFile = document.getElementById('selectedFile');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFile');
const analyzeBtn = document.getElementById('analyzeBtn');

const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');

const exportJsonBtn = document.getElementById('exportJson');
const newAnalysisBtn = document.getElementById('newAnalysis');

// ===== File Upload Handling =====
uploadZone.addEventListener('click', () => fileInput.click());

uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'var(--primary)';
    uploadZone.style.background = 'rgba(99, 102, 241, 0.15)';
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.style.borderColor = 'var(--border-light)';
    uploadZone.style.background = 'rgba(99, 102, 241, 0.05)';
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'var(--border-light)';
    uploadZone.style.background = 'rgba(99, 102, 241, 0.05)';

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

removeFileBtn.addEventListener('click', () => {
    currentFile = null;
    fileInput.value = '';
    selectedFile.style.display = 'none';
    uploadZone.style.display = 'block';
    analyzeBtn.disabled = true;
});

// ===== File Selection =====
function handleFileSelect(file) {
    if (!file.name.endsWith('.pdf')) {
        showNotification('Please select a PDF file', 'error');
        return;
    }

    if (file.size > 50 * 1024 * 1024) { // 50MB limit
        showNotification('File size must be less than 50MB', 'error');
        return;
    }

    currentFile = file;
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);

    uploadZone.style.display = 'none';
    selectedFile.style.display = 'flex';
    analyzeBtn.disabled = false;
}

// ===== Analysis =====
analyzeBtn.addEventListener('click', async () => {
    if (!currentFile) return;

    // Show loading
    uploadSection.style.display = 'none';
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('file', currentFile);

        const response = await fetch('http://localhost:8000/api/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to analyze paper');
        }

        const data = await response.json();
        currentPaper = data.paper;

        // Display results
        displayResults(data.paper);

        loadingSection.style.display = 'none';
        resultsSection.style.display = 'block';

    } catch (error) {
        console.error('Error:', error);
        showNotification('Error analyzing paper. Make sure the server is running.', 'error');
        loadingSection.style.display = 'none';
        uploadSection.style.display = 'block';
    }
});

// ===== Display Results =====
function displayResults(paper) {
    // Title and authors
    document.getElementById('paperTitle').textContent = paper.title || 'Untitled';

    const authorsText = paper.authors && paper.authors.length > 0
        ? paper.authors.map(a => a.name).join(', ')
        : 'No authors listed';
    document.getElementById('paperAuthors').textContent = `Authors: ${authorsText}`;

    document.getElementById('paperVenue').textContent = paper.venue
        ? `Venue: ${paper.venue}`
        : '';

    // Abstract
    const abstractSection = document.getElementById('abstractSection');
    const abstractContent = document.getElementById('abstractContent');
    if (paper.abstract) {
        abstractContent.textContent = paper.abstract;
        abstractSection.style.display = 'block';
    } else {
        abstractSection.style.display = 'none';
    }

    // Metadata
    document.getElementById('parserVersion').textContent = paper.parser_version || 'N/A';
    document.getElementById('sectionsCount').textContent = paper.sections?.length || 0;
    document.getElementById('paperDoi').textContent = paper.doi || 'N/A';

    const timestamp = new Date(paper.ingestion_timestamp);
    document.getElementById('ingestionTime').textContent = timestamp.toLocaleString();

    // Sections breakdown
    const sectionsList = document.getElementById('sectionsList');
    sectionsList.innerHTML = '';

    if (paper.sections && paper.sections.length > 0) {
        paper.sections.forEach(section => {
            const sectionItem = document.createElement('div');
            sectionItem.className = 'section-item';

            const sectionInfo = document.createElement('div');
            sectionInfo.className = 'section-item-info';

            const sectionType = document.createElement('div');
            sectionType.className = 'section-type';
            sectionType.textContent = section.section_type.replace('_', ' ');

            const sectionTitle = document.createElement('div');
            sectionTitle.className = 'section-title-text';
            sectionTitle.textContent = section.title || '(no title)';

            sectionInfo.appendChild(sectionType);
            sectionInfo.appendChild(sectionTitle);

            const sectionLength = document.createElement('div');
            sectionLength.className = 'section-length';
            sectionLength.textContent = `${section.content.length} characters`;

            sectionItem.appendChild(sectionInfo);
            sectionItem.appendChild(sectionLength);

            sectionsList.appendChild(sectionItem);
        });
    } else {
        sectionsList.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: var(--spacing-md);">No sections detected</p>';
    }
}

// ===== Export JSON =====
exportJsonBtn.addEventListener('click', () => {
    if (!currentPaper) return;

    const dataStr = JSON.stringify(currentPaper, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${sanitizeFilename(currentPaper.title || 'paper')}.json`;
    link.click();

    URL.revokeObjectURL(url);
    showNotification('JSON exported successfully', 'success');
});

// ===== New Analysis =====
newAnalysisBtn.addEventListener('click', () => {
    currentPaper = null;
    currentFile = null;
    fileInput.value = '';

    resultsSection.style.display = 'none';
    uploadSection.style.display = 'block';
    selectedFile.style.display = 'none';
    uploadZone.style.display = 'block';
    analyzeBtn.disabled = true;
});

// ===== Utility Functions =====
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function sanitizeFilename(filename) {
    return filename
        .replace(/[^a-z0-9]/gi, '_')
        .toLowerCase()
        .substring(0, 50);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'error' ? 'var(--error)' : type === 'success' ? 'var(--success)' : 'var(--primary)'};
        color: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-lg);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        max-width: 300px;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ===== Check Server Health on Load =====
window.addEventListener('load', async () => {
    try {
        const response = await fetch('http://localhost:8000/api/health');
        if (response.ok) {
            console.log('✓ Server is running');
        }
    } catch (error) {
        console.warn('⚠ Server is not running. Please start the server with: python app.py');
        showNotification('Server not running. Start with: python app.py', 'warning');
    }
});
