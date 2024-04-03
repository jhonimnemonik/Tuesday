//Slide sidebar
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

//Slide list
function toggleTable(tableId) {
  var table = document.getElementById(tableId);
  if (table.style.display === "none") {
    table.style.display = "table";
  } else {
    table.style.display = "none";
  }
};

//Ajax link
function addColumn() {
    // Выполняем AJAX-запрос на сервер
    fetch('/add_column', {
      method: 'POST',
      body: JSON.stringify({ column_name: 'Новый столбец' }), // Отправляем данные на сервер
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
