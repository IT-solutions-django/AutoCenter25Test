function search_modal() {
	static_backdrop = document.getElementById('staticBackdrop');
	search_car_header = document.getElementById('search-car-header');
		
	if (window.innerWidth <= 576) {
		static_backdrop.classList.add("modal");
		static_backdrop.style.display = "none";
		search_car_header.style.display = "flex";
	}
	else {
		static_backdrop.classList.remove("modal");
		static_backdrop.style.display = "block";
		search_car_header.style.display = "none";
	}
};
function toggleSortDropdown() {
    const sortButton = document.querySelector('.mob-btn-sorting');
    let mobileDropdownMenu = document.getElementById('mobile-dropdown-menu');

    if (!mobileDropdownMenu) {
        mobileDropdownMenu = document.createElement('ul');
        mobileDropdownMenu.id = 'mobile-dropdown-menu';
        mobileDropdownMenu.className = 'dropdown-menu';

        const originalDropdownMenu = document.getElementById('dropdown-menu');
        mobileDropdownMenu.innerHTML = originalDropdownMenu.innerHTML;
        document.body.appendChild(mobileDropdownMenu);
    }

    const rect = sortButton.getBoundingClientRect();
    mobileDropdownMenu.style.position = 'absolute';
    mobileDropdownMenu.style.top = `${rect.bottom + window.scrollY}px`;
    mobileDropdownMenu.style.left = `${rect.left + window.scrollX}px`;
    mobileDropdownMenu.classList.toggle('show');
};

function closeMobileSortDropdown(event) {
    const mobileDropdownMenu = document.getElementById('mobile-dropdown-menu');
    if (mobileDropdownMenu && mobileDropdownMenu.classList.contains('show')) {
        const sortButton = document.querySelector('.mob-btn-sorting');
        if (!mobileDropdownMenu.contains(event.target) && !sortButton.contains(event.target)) {
            mobileDropdownMenu.classList.remove('show');
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
	search_modal();

	const sortButton = document.querySelector('.mob-btn-sorting');
    if (sortButton) {
        sortButton.addEventListener('click', toggleSortDropdown);
    }

    document.addEventListener('click', closeMobileSortDropdown);
});



