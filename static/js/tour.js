// Custom Tour Implementation
class CustomTour {
    constructor() {
        this.steps = [];
        this.currentStep = 0;
        this.overlay = null;
        this.tooltip = null;
    }

    addStep(step) {
        this.steps.push(step);
    }

    start() {
        if (this.steps.length === 0) return;
        
        this.createOverlay();
        this.currentStep = 0;
        this.showStep(this.currentStep);
    }

    createOverlay() {
        // Create modal overlay
        this.overlay = document.createElement('div');
        this.overlay.className = 'tour-overlay';
        this.overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 9998;
            animation: fadeIn 0.3s ease;
        `;
        document.body.appendChild(this.overlay);

        // Create tooltip container
        this.tooltip = document.createElement('div');
        this.tooltip.className = 'tour-tooltip';
        this.tooltip.style.cssText = `
            position: fixed;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 24px;
            max-width: 400px;
            z-index: 9999;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
            animation: slideUp 0.3s ease;
        `;
        document.body.appendChild(this.tooltip);
    }

    showStep(index) {
        if (index < 0 || index >= this.steps.length) {
            this.end();
            return;
        }

        const step = this.steps[index];
        
        // Highlight target element
        if (step.element) {
            this.highlightElement(step.element);
        }

        // Update tooltip content
        this.tooltip.innerHTML = `
            <div class="tour-header" style="margin-bottom: 16px;">
                <h3 style="font-size: 1.25rem; font-weight: 700; color: #1e293b; margin: 0;">
                    ${step.title}
                </h3>
            </div>
            <div class="tour-content" style="color: #64748b; line-height: 1.6; margin-bottom: 20px;">
                ${step.text}
            </div>
            <div class="tour-footer" style="display: flex; gap: 12px; justify-content: flex-end;">
                ${index > 0 ? `<button class="tour-btn tour-btn-secondary" onclick="window.customTour.previous()">Back</button>` : ''}
                <button class="tour-btn tour-btn-secondary" onclick="window.customTour.skip()">Skip Tour</button>
                <button class="tour-btn tour-btn-primary" onclick="window.customTour.next()">
                    ${index === this.steps.length - 1 ? 'Finish' : 'Next'}
                </button>
            </div>
        `;

        // Position tooltip
        this.positionTooltip(step.element);

        // Add step indicator
        const indicator = document.createElement('div');
        indicator.style.cssText = 'text-align: center; margin-top: 12px; color: #94a3b8; font-size: 0.85rem;';
        indicator.textContent = `Step ${index + 1} of ${this.steps.length}`;
        this.tooltip.appendChild(indicator);
    }

    highlightElement(selector) {
        // Remove previous highlights
        document.querySelectorAll('.tour-highlight').forEach(el => {
            el.classList.remove('tour-highlight');
        });

        const element = document.querySelector(selector);
        if (element) {
            element.classList.add('tour-highlight');
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    positionTooltip(selector) {
        if (!selector) {
            // Center tooltip
            this.tooltip.style.top = '50%';
            this.tooltip.style.left = '50%';
            this.tooltip.style.transform = 'translate(-50%, -50%)';
            return;
        }

        const element = document.querySelector(selector);
        if (!element) {
            this.positionTooltip(null);
            return;
        }

        const rect = element.getBoundingClientRect();
        const tooltipRect = this.tooltip.getBoundingClientRect();

        // Position below element by default
        let top = rect.bottom + 20;
        let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);

        // Adjust if out of viewport
        if (top + tooltipRect.height > window.innerHeight) {
            top = rect.top - tooltipRect.height - 20;
        }

        if (left < 20) left = 20;
        if (left + tooltipRect.width > window.innerWidth - 20) {
            left = window.innerWidth - tooltipRect.width - 20;
        }

        this.tooltip.style.top = top + 'px';
        this.tooltip.style.left = left + 'px';
        this.tooltip.style.transform = 'none';
    }

    next() {
        this.currentStep++;
        if (this.currentStep >= this.steps.length) {
            this.complete();
        } else {
            this.showStep(this.currentStep);
        }
    }

    previous() {
        this.currentStep--;
        if (this.currentStep >= 0) {
            this.showStep(this.currentStep);
        }
    }

    skip() {
        this.end();
    }

    complete() {
        localStorage.setItem('tourCompleted', 'true');
        this.end();
    }

    end() {
        if (this.overlay) {
            this.overlay.remove();
        }
        if (this.tooltip) {
            this.tooltip.remove();
        }
        document.querySelectorAll('.tour-highlight').forEach(el => {
            el.classList.remove('tour-highlight');
        });
    }
}

// Initialize tour
function initCustomTour() {
    const tour = new CustomTour();

    tour.addStep({
        title: '👋 Welcome to Public Records!',
        text: 'Let me show you around! This platform gives you access to 30+ public record APIs all in one place. Take a moment to explore the beautiful animated sky background!',
        element: null
    });

    tour.addStep({
        title: '🔍 Powerful Search',
        text: 'Enter any search term here - names, addresses, business names, VINs, or any identifier. Our system will search across all connected databases.',
        element: '#search-box'
    });

    tour.addStep({
        title: '🎯 Smart Filtering',
        text: 'Choose which record types to search. You can search all at once or target specific categories like Court Records, Property Records, or Business Data.',
        element: '.record-filters'
    });

    tour.addStep({
        title: '⚡ Quick Access Cards',
        text: 'Click any of these cards to quickly filter your search to a specific record type. Hover over them to see the beautiful animations!',
        element: '.quick-access'
    });

    tour.addStep({
        title: '🌤️ Animated Sky',
        text: 'Notice the beautiful sky background? It continuously morphs through different times of day - from dawn to day to sunset to night. Watch it change as you use the app!',
        element: '#header'
    });

    tour.addStep({
        title: '🎉 You\'re All Set!',
        text: 'You can take this tour again anytime by clicking the "Take Tour" button in the top right. Enjoy searching through public records!',
        element: null
    });

    return tour;
}

// Global tour instance
window.customTour = null;

// Start tour function
window.startTour = function() {
    if (!window.customTour) {
        window.customTour = initCustomTour();
    }
    window.customTour.start();
};

// Auto-start tour on first visit
window.checkAndStartTour = function() {
    const tourCompleted = localStorage.getItem('tourCompleted');
    if (!tourCompleted) {
        setTimeout(() => {
            window.customTour = initCustomTour();
            window.customTour.start();
        }, 1500);
    }
};
