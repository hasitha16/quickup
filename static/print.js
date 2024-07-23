document.addEventListener('DOMContentLoaded', (event) => {
    const dateInput = document.getElementById('date-input');
    
    dateInput.addEventListener('change', function() {
        if (this.value) {
            this.classList.add('has-value');
        } else {
            this.classList.remove('has-value');
        }
    });
});
