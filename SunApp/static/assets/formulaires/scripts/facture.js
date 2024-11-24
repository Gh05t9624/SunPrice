document.addEventListener('DOMContentLoaded', () => {
    const date = new Date();
    const formattedDate = date.toLocaleDateString('fr-FR');
    document.getElementById('invoice-date').textContent = formattedDate;

    const updateTotals = () => {
        const rows = document.querySelectorAll('tbody tr');
        let grandTotal = 0;

        rows.forEach(row => {
            const quantityInput = row.querySelector('.quantity');
            const priceCell = row.querySelector('td:nth-child(3)');
            const totalCell = row.querySelector('.line-total');

            let quantity = parseFloat(quantityInput.value) || 1;
            const price = parseFloat(priceCell.textContent.replace(' ', '')) || 0;

            // If quantity is less than 1, set it to 1
            if (quantity < 1) {
                quantity = 1;
                quantityInput.value = 1; // Update the input field
            }

            const total = quantity * price;
            totalCell.textContent = `${total} `;

            grandTotal += total;
        });

        document.getElementById('grand-total').textContent = `${grandTotal} `;
    };

    document.querySelectorAll('.quantity').forEach(input => {
        input.addEventListener('input', updateTotals);
    });

    updateTotals();
});
