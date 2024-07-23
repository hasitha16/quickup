document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.getElementById('signin-form');
    const phoneNumberInput = document.getElementById('phone-number');
    const passwordInput = document.getElementById('password');
    const rememberMeCheckbox = document.getElementById('remember-me');

    // Check if user data is stored in localStorage
    if (localStorage.getItem('rememberMe') === 'true') {
        phoneNumberInput.value = localStorage.getItem('phoneNumber');
        passwordInput.value = localStorage.getItem('password');
        rememberMeCheckbox.checked = true;
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const phoneNumber = phoneNumberInput.value;
        const password = passwordInput.value;
        const rememberMe = rememberMeCheckbox.checked;

        if (rememberMe) {
            // Save data to localStorage
            localStorage.setItem('phoneNumber', phoneNumber);
            localStorage.setItem('password', password);
            localStorage.setItem('rememberMe', rememberMe);
        } else {
            // Clear data from localStorage
            localStorage.removeItem('phoneNumber');
            localStorage.removeItem('password');
            localStorage.removeItem('rememberMe');
        }

        // Perform sign-in logic (e.g., send data to server for authentication)
        // ...

        // Redirect to choose.html after successful sign-in
        window.location.href = 'choose.html';
    });
});
