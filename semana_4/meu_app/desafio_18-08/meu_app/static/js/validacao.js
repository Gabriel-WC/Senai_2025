const checkbox = document.querySelector('input[type="checkbox"]');
const submitBtn = document.getElementById('submit-btn');

submitBtn.disabled = true;

checkbox.addEventListener('change', () => {
    submitBtn.disabled = !checkbox.checked;
});
