function loadAndShowModal(element) {
    var url = element.getAttribute('data-url');
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(html => {
        document.getElementById('file-upload-modal').innerHTML = html;
        document.getElementById('modal-backdrop').classList.add('modal-show');
    })
    .catch(error => {
        console.error('There was a problem with fetching the file upload page:', error);
    });
}

function closeModal() {
  document.getElementById('modal-backdrop').classList.remove('modal-show');
}