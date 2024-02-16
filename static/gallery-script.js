// JavaScript function to delete image
function deleteImage() {
    // Get CSRF token from the form
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    // Get the filename
    const filename = selectedFilename;

    // Send request to delete image with CSRF token included in headers
    fetch(`/delete/${filename}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (response.ok) {
            // Deletion successful, hide confirmation modal
            hideDeleteConfirmation();
            // Optionally, reload the page or update the image gallery
            window.location.reload();
        } else {
            // Handle deletion failure
            console.error('Failed to delete image');
            // Optionally, display an error message to the user
        }
    })
    .catch(error => {
        // Handle network errors
        console.error('Error deleting image:', error);
        // Optionally, display an error message to the user
    });
}

// JavaScript function to update selected file name
function updateFileName(input) {
    const fileName = input.files[0].name;
    document.getElementById('selected-file').textContent = `Selected File: ${fileName}`;
}

// JavaScript code for handling delete confirmation
function showDeleteConfirmation(filename) {
    selectedFilename = filename;
    document.getElementById('delete-confirm').style.display = 'block';
}

// JavaScript function to hide delete confirmation modal
function hideDeleteConfirmation() {
    selectedFilename = '';
    document.getElementById('delete-confirm').style.display = 'none';
}

// JavaScript function to show image zoom modal
// function zoomImage(filename) {
//     console.log('Zoom image function called with filename:', filename);
//     const modal = document.getElementById('image-zoom-modal');
//     const img = document.getElementById('zoomed-image');
//     console.log('Image src:', img.getAttribute('src'));
//     img.src = img.getAttribute('src');
//     modal.style.display = 'block';
// }


// JavaScript function to hide image zoom modal
function hideImageZoom() {
    const modal = document.getElementById('image-zoom-modal');
    modal.style.display = 'none';
}
