// JusticeAI Frontend JavaScript
// Handles form submission, API calls, and UI interactions

class JusticeAI {
    constructor() {
        this.currentCaseId = null;
        this.init();
    }

    init() {
        console.log('JusticeAI init() called');
        this.setupEventListeners();
        this.setupCharacterCounter();
        this.showForm();
        console.log('JusticeAI init() completed');
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('legalIssueForm');
        if (form) {
            console.log('Setting up form submission listener');
            form.addEventListener('submit', (e) => {
                console.log('Form submitted');
                this.handleFormSubmit(e);
            });
        } else {
            console.error('Form not found: legalIssueForm');
        }

        // Download report button
        const downloadBtn = document.getElementById('downloadReportBtn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => this.downloadReport());
        }

        // New case button
        const newCaseBtn = document.getElementById('newCaseBtn');
        if (newCaseBtn) {
            newCaseBtn.addEventListener('click', () => this.showForm());
        }

        // Form reset button
        const resetBtn = document.getElementById('resetBtn');
        if (resetBtn) {
            resetBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.resetForm();
            });
        }
    }

    setupCharacterCounter() {
        const textarea = document.getElementById('issue_description');
        const charCount = document.getElementById('charCount');
        
        if (textarea && charCount) {
            textarea.addEventListener('input', () => {
                const count = textarea.value.length;
                charCount.textContent = count;
                
                // Change color based on character count
                if (count > 1800) {
                    charCount.style.color = '#e53e3e';
                } else if (count > 1500) {
                    charCount.style.color = '#d69e2e';
                } else {
                    charCount.style.color = '#718096';
                }
            });
        }
    }

    async handleFormSubmit(e) {
        console.log('handleFormSubmit called');
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const submitBtn = document.getElementById('submitBtn');
        
        console.log('Form data:', {
            user_name: formData.get('user_name'),
            issue_category: formData.get('issue_category'),
            priority_level: formData.get('priority_level'),
            issue_description: formData.get('issue_description')?.substring(0, 50) + '...'
        });
        
        // Validate form
        if (!this.validateForm(formData)) {
            console.log('Form validation failed');
            return;
        }

        console.log('Form validation passed, starting submission');

        // Disable submit button and show loading
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        
        try {
            // Show loading section
            this.showLoading();
            
            // Simulate agent processing
            await this.simulateAgentProcessing();
            
            // Submit case to backend
            console.log('Submitting case to backend...');
            const response = await this.submitCase(formData);
            console.log('Backend response:', response);
            
            if (response.success) {
                this.currentCaseId = response.case_id;
                this.displayResults(response);
            } else {
                throw new Error(response.message || 'Failed to process case');
            }
            
        } catch (error) {
            console.error('Error submitting case:', error);
            this.showError(error.message);
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Case';
        }
    }

    validateForm(formData) {
        const requiredFields = ['user_name', 'issue_category', 'issue_description', 'priority_level'];
        
        for (const field of requiredFields) {
            const value = formData.get(field);
            if (!value || value.trim() === '') {
                this.showFieldError(field, 'This field is required');
                return false;
            }
        }

        // Validate email if provided
        const email = formData.get('user_email');
        if (email && email.trim() !== '') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                this.showFieldError('user_email', 'Please enter a valid email address');
                return false;
            }
        }

        // Validate description length
        const description = formData.get('issue_description');
        if (description.length < 10) {
            this.showFieldError('issue_description', 'Description must be at least 10 characters long');
            return false;
        }

        if (description.length > 2000) {
            this.showFieldError('issue_description', 'Description must be less than 2000 characters');
            return false;
        }

        return true;
    }

    showFieldError(fieldName, message) {
        const field = document.getElementById(fieldName);
        if (field) {
            // Remove existing error
            const existingError = field.parentNode.querySelector('.field-error');
            if (existingError) {
                existingError.remove();
            }

            // Add error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            errorDiv.style.color = '#e53e3e';
            errorDiv.style.fontSize = '0.8rem';
            errorDiv.style.marginTop = '0.25rem';
            errorDiv.textContent = message;
            
            field.parentNode.appendChild(errorDiv);
            field.style.borderColor = '#e53e3e';
            
            // Focus on the field
            field.focus();
            
            // Remove error after 5 seconds
            setTimeout(() => {
                if (errorDiv.parentNode) {
                    errorDiv.remove();
                    field.style.borderColor = '#e2e8f0';
                }
            }, 5000);
        }
    }

    async simulateAgentProcessing() {
        const agents = [
            { id: 'userAgentStatus', name: 'User Agent', delay: 1000 },
            { id: 'legalAgentStatus', name: 'Legal Expert Agent', delay: 2000 },
            { id: 'mediationAgentStatus', name: 'Mediation Agent', delay: 3000 },
            { id: 'escalationAgentStatus', name: 'Escalation Agent', delay: 4000 },
            { id: 'reportAgentStatus', name: 'Report Agent', delay: 5000 }
        ];

        for (const agent of agents) {
            await this.updateAgentStatus(agent.id, 'processing');
            await this.sleep(agent.delay);
            await this.updateAgentStatus(agent.id, 'completed');
        }
    }

    async updateAgentStatus(agentId, status) {
        const statusElement = document.getElementById(agentId);
        if (statusElement) {
            statusElement.textContent = status === 'processing' ? 'Processing...' : 'Completed';
            statusElement.className = `status-indicator ${status}`;
        }
    }

    async submitCase(formData) {
        try {
            console.log('Making fetch request to /submit_case');
            const response = await fetch('/submit_case', {
                method: 'POST',
                body: formData
            });

            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Response error text:', errorText);
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const jsonResponse = await response.json();
            console.log('JSON response:', jsonResponse);
            return jsonResponse;
        } catch (error) {
            console.error('Error submitting case:', error);
            throw new Error('Failed to submit case. Please try again.');
        }
    }

    displayResults(response) {
        // Hide loading and show results
        this.hideLoading();
        this.showResults();

        // Populate case details
        this.populateCaseDetails(response);

        // Populate agent results
        this.populateAgentResults(response);

        // Add fade-in animation
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.classList.add('fade-in');
    }

    populateCaseDetails(response) {
        const caseDetails = document.getElementById('caseDetails');
        if (caseDetails) {
            const details = [
                { label: 'Case ID', value: response.case_id },
                { label: 'Status', value: 'Completed' },
                { label: 'Priority', value: this.capitalizeFirst(response.priority_level || 'medium') },
                { label: 'Category', value: this.formatCategory(response.issue_category) }
            ];

            caseDetails.innerHTML = details.map(detail => `
                <div class="case-detail-item">
                    <div class="case-detail-label">${detail.label}</div>
                    <div class="case-detail-value">${detail.value}</div>
                </div>
            `).join('');
        }
    }

    populateAgentResults(response) {
        // Legal advice
        const legalContent = document.getElementById('legalAdviceContent');
        if (legalContent && response.legal_advice) {
            legalContent.innerHTML = this.formatAgentResponse(response.legal_advice);
        }

        // Mediation suggestions
        const mediationContent = document.getElementById('mediationContent');
        if (mediationContent && response.mediation_suggestions) {
            mediationContent.innerHTML = this.formatAgentResponse(response.mediation_suggestions);
        }

        // Escalation recommendations
        const escalationContent = document.getElementById('escalationContent');
        if (escalationContent && response.escalation_recommendations) {
            escalationContent.innerHTML = this.formatAgentResponse(response.escalation_recommendations);
        }
    }

    formatAgentResponse(response) {
        if (!response) return '<p>No response available.</p>';

        // Split by double newlines to get paragraphs
        const paragraphs = response.split('\n\n');
        
        return paragraphs.map(paragraph => {
            if (paragraph.trim() === '') return '';
            
            // Check if it's a header (contains emoji or is all caps)
            if (paragraph.includes('🚨') || paragraph.includes('⚠️') || paragraph.includes('📋') || 
                paragraph.includes('💡') || paragraph.includes('⚖️') || paragraph.includes('🤖') ||
                paragraph.includes('📝') || paragraph.includes('💬') || paragraph.includes('🤝') ||
                paragraph.includes('📊') || paragraph.includes('⏱️') || paragraph.includes('🔗') ||
                paragraph.includes('🚀') || paragraph.includes('🏢') || paragraph.includes('📞') ||
                paragraph.includes('🔄') || paragraph.includes('ℹ️')) {
                return `<h4 style="color: #667eea; margin: 1rem 0 0.5rem 0; font-weight: 600;">${paragraph}</h4>`;
            }
            
            // Check if it's a list item
            if (paragraph.trim().startsWith('•')) {
                const items = paragraph.split('\n').filter(item => item.trim().startsWith('•'));
                if (items.length > 0) {
                    const listItems = items.map(item => `<li>${item.substring(1).trim()}</li>`).join('');
                    return `<ul style="margin: 0.5rem 0 1rem 1.5rem;">${listItems}</ul>`;
                }
            }
            
            // Check if it's a numbered list
            if (paragraph.trim().match(/^\d+\./)) {
                const items = paragraph.split('\n').filter(item => item.trim().match(/^\d+\./));
                if (items.length > 0) {
                    const listItems = items.map(item => `<li>${item.replace(/^\d+\.\s*/, '')}</li>`).join('');
                    return `<ol style="margin: 0.5rem 0 1rem 1.5rem;">${listItems}</ol>`;
                }
            }
            
            // Regular paragraph
            return `<p style="margin-bottom: 1rem; line-height: 1.6;">${paragraph}</p>`;
        }).join('');
    }

    async downloadReport() {
        if (!this.currentCaseId) {
            this.showNotification('No case available for download', 'error');
            return;
        }

        try {
            const response = await fetch(`/download_report/${this.currentCaseId}`);
            
            if (!response.ok) {
                throw new Error('Failed to download report');
            }

            // Create blob and download
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `justiceai_report_${this.currentCaseId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            this.showNotification('Report downloaded successfully!', 'success');
        } catch (error) {
            console.error('Error downloading report:', error);
            this.showNotification('Failed to download report. Please try again.', 'error');
        }
    }

    showForm() {
        this.hideAllSections();
        document.getElementById('caseForm').style.display = 'block';
        document.getElementById('caseForm').classList.add('fade-in');
    }

    showLoading() {
        this.hideAllSections();
        document.getElementById('loadingSection').style.display = 'block';
        document.getElementById('loadingSection').classList.add('fade-in');
    }

    hideLoading() {
        document.getElementById('loadingSection').style.display = 'none';
    }

    showResults() {
        this.hideAllSections();
        document.getElementById('resultsSection').style.display = 'block';
    }

    showError(message) {
        this.hideAllSections();
        const errorSection = document.getElementById('errorSection');
        const errorMessage = document.getElementById('errorMessage');
        
        if (errorMessage) {
            errorMessage.textContent = message;
        }
        
        errorSection.style.display = 'block';
        errorSection.classList.add('fade-in');
    }

    hideAllSections() {
        const sections = ['caseForm', 'loadingSection', 'resultsSection', 'errorSection'];
        sections.forEach(sectionId => {
            const section = document.getElementById(sectionId);
            if (section) {
                section.style.display = 'none';
                section.classList.remove('fade-in');
            }
        });
    }

    resetForm() {
        const form = document.getElementById('legalIssueForm');
        if (form) {
            form.reset();
            
            // Reset character counter
            const charCount = document.getElementById('charCount');
            if (charCount) {
                charCount.textContent = '0';
                charCount.style.color = '#718096';
            }
            
            // Remove any field errors
            const fieldErrors = document.querySelectorAll('.field-error');
            fieldErrors.forEach(error => error.remove());
            
            // Reset field borders
            const fields = form.querySelectorAll('input, select, textarea');
            fields.forEach(field => {
                field.style.borderColor = '#e2e8f0';
            });
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            max-width: 300px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        // Set background color based on type
        const colors = {
            success: '#48bb78',
            error: '#e53e3e',
            warning: '#d69e2e',
            info: '#667eea'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        notification.textContent = message;
        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 5 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }

    // Utility functions
    capitalizeFirst(str) {
        if (!str) return '';
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    formatCategory(category) {
        if (!category) return '';
        return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Global functions for onclick handlers
function showForm() {
    if (window.justiceAI) {
        window.justiceAI.showForm();
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing JusticeAI...');
    // Initialize JusticeAI application
    window.justiceAI = new JusticeAI();
    console.log('JusticeAI initialized:', window.justiceAI);
}); 