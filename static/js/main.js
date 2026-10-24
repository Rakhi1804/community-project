// Sir Kasturchand Daga Bal Sadan - Main JavaScript
document.addEventListener("DOMContentLoaded", function() {
    // 1. Smooth Scroll for hash links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // 2. Auto-dismiss alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 6000);
    });

    // 3. Set minimum date for all date pickers
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(input => {
        if (!input.getAttribute('min')) {
            input.setAttribute('min', today);
        }
    });

    console.log("Sir Kasturchand Daga Bal Sadan platform loaded successfully.");
});

function copyWhatsAppMessage() {
    const textElement = document.getElementById('waMessageText');
    const btnText = document.getElementById('copyBtnText');
    if (textElement) {
        navigator.clipboard.writeText(textElement.innerText).then(() => {
            if (btnText) {
                btnText.textContent = "Copied!";
                setTimeout(() => {
                    btnText.textContent = "Copy Text";
                }, 2500);
            }
        });
    }
}
