document.addEventListener('DOMContentLoaded', function () {
    const categoryField = document.querySelector('#id_category');
    const sizeFieldRow = document.querySelector('.form-row.field-size');
    const genderFieldRow = document.querySelector('.form-row.field-gender');
    const colorFieldRow = document.querySelector('.form-row.field-color');

    function toggleFields() {
        if (!categoryField) return;

        const selectedOption = categoryField.options[categoryField.selectedIndex];
        if (!selectedOption) return;

        const selected = selectedOption.text.trim().toLowerCase();
        console.log("Selected Category:", selected);

        const isPerfume = selected === 'perfumes';

        sizeFieldRow.style.display = isPerfume ? 'none' : '';
        genderFieldRow.style.display = isPerfume ? 'none' : '';
        colorFieldRow.style.display = isPerfume ? 'none' : '';
    }

    if (categoryField) {
        categoryField.addEventListener('change', toggleFields);
        // 🔥 Call once initially
        toggleFields();
    }
});
