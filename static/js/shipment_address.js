const toggleBtn = document.getElementById('toggleAddressBtn');
const icon = document.getElementById('addressIcon');
const collapseTarget = document.getElementById('newAddressForm');

collapseTarget.addEventListener('show.bs.collapse', () => {
    icon.classList.remove('bi-chevron-down');
    icon.classList.add('bi-chevron-up');
});

collapseTarget.addEventListener('hide.bs.collapse', () => {
    icon.classList.remove('bi-chevron-up');
    icon.classList.add('bi-chevron-down');
});
