document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleSidebarButton = document.getElementById('toggleSidebar');

    toggleSidebarButton.addEventListener('click', function() {
      sidebar.classList.toggle('collapsed');
      if (sidebar.classList.contains('collapsed')) {
        toggleSidebarButton.textContent = '>';
      } else {
        toggleSidebarButton.textContent = '<';
      }
    });
});


function toggleTable(tableId) {
  var table = document.getElementById(tableId);
  if (table.style.display === "none") {
    table.style.display = "table";
  } else {
    table.style.display = "none";
  }
};

function addColumn() {
    fetch('/add_column', {
      method: 'POST',
      body: {column_name: 'Новый столбец'},
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (response.ok) {
        alert('Столбец успешно добавлен!');
      } else {
        alert('Ошибка при добавлении столбца!');
      }
    })
    .catch(error => {
      console.error('Ошибка:', error);
    });
  }

function toggleMenu() {
  var menu = document.getElementById("main-menu");
  menu.classList.toggle("menu-open");
}

  document.addEventListener('DOMContentLoaded', function() {
    const authForm = document.getElementById('authForm');
    const registerForm = document.getElementById('registerForm');
    const authButton = document.getElementById('authButton');
    const regButton = document.getElementById('regButton');
    const toggleAuth = document.getElementById('toggleAuth');
    const toggleReg = document.getElementById('toggleReg');

    toggleAuth.addEventListener('click', function(event) {
      event.preventDefault();
      authForm.style.display = 'none';
      registerForm.style.display = 'block';
      authButton.value = 'Зарегистрироваться';
      authForm.action = "{{ url_for('user_routes.register') }}";
    });

    toggleReg.addEventListener('click', function(event) {
      event.preventDefault();
      authForm.style.display = 'block';
      registerForm.style.display = 'none';
      authButton.value = 'Войти';
      authForm.action = "{{ url_for('user_routes.login') }}";
    });
  });

///////////////////
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const mainMenu = document.querySelector('#main-menu ul');

    menuToggle.addEventListener('click', function() {
        // Очищаем содержимое текущего меню
        mainMenu.innerHTML = '';

        // Получаем список ссылок из HTML
        const links = document.querySelectorAll('[data-menu-link]');

        // Создаем новые элементы списка для каждой ссылки и добавляем их в меню
        links.forEach(function(link) {
            const menuItem = document.createElement('li');
            const menuLink = document.createElement('a');
            menuLink.setAttribute('href', link.getAttribute('data-menu-link'));
            menuLink.textContent = link.textContent;
            menuItem.appendChild(menuLink);
            mainMenu.appendChild(menuItem);
        });
    });
});