document.getElementById('filterBtn').addEventListener('click', function () {
    document.getElementById('filterDropdown').classList.toggle('show');
});

window.addEventListener('click', function (event) {
    if (!event.target.matches('.filter-btn')) {
        const dropdown = document.getElementById('filterDropdown');
        if (dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const taskCards = document.querySelectorAll('.task-card');
    const modals = document.querySelectorAll('.modal-overlay');
    const closeButtons = document.querySelectorAll('.modal-close');

    taskCards.forEach((card, index) => {
        card.addEventListener('click', () => {
            modals.forEach(modal => modal.style.display = 'none');
            if (modals[index]) {
                modals[index].style.display = 'flex';
            }
        });
    });

    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            modals.forEach(modal => modal.style.display = 'none');
        });
    });

    document.querySelectorAll('.modal-btn-open-status').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            const taskId = this.getAttribute('data-task-id');
            document.querySelector(`#modal-${taskId}`).style.display = 'none';
            document.querySelector(`#status-modal-${taskId}`).style.display = 'flex';
        });
    });

    document.querySelectorAll('.status-modal-close').forEach(btn => {
        btn.addEventListener('click', function () {
            this.closest('.status-modal-overlay').style.display = 'none';
        });
    });

    document.querySelectorAll('.status-modal-overlay').forEach(modal => {
        modal.addEventListener('click', function (e) {
            if (e.target === this) {
                this.style.display = 'none';
            }
        });
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay, .status-modal-overlay').forEach(modal => {
                modal.style.display = 'none';
            });
        }
    });
});