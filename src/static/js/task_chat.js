function sendTaskMessage(taskId) {
    var messageInput = document.getElementById('chat_message_input');
    var messageText = messageInput.value;

    // Отправка сообщения на сервер
    fetch(`/add-chat/${taskId}/messages`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: messageText })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при отправке сообщения');
        }
        return response.json();
    })
    .then(data => {
        // Обновление списка сообщений на странице
        var messagesContainer = document.getElementById('messages');
        var messageElement = document.createElement('p');
        messageElement.textContent = `${data.sender_id}: ${data.text} (${data.timestamp})`;
        messagesContainer.appendChild(messageElement);

        // Очистка поля ввода
        messageInput.value = '';
    })
    .catch(error => console.error('Ошибка:', error));
}
