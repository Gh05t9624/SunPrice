document.addEventListener('DOMContentLoaded', function () {
    const videoFileInput = document.getElementById('videoFile');
    const videoProgress = document.getElementById('videoProgress');
    const videoProgressText = document.getElementById('videoProgressText');
    const videoContainer = document.getElementById('videoContainer');
  
    const imageFileInput = document.getElementById('imageFile');
    const imageProgress = document.getElementById('imageProgress');
    const imageProgressText = document.getElementById('imageProgressText');
    const imageContainer = document.getElementById('imageContainer');
  
    videoFileInput.addEventListener('change', handleMediaSelect.bind(null, videoContainer, videoProgress, videoProgressText));
    imageFileInput.addEventListener('change', handleMediaSelect.bind(null, imageContainer, imageProgress, imageProgressText));
  
    function handleMediaSelect(container, progressElement, progressTextElement, event) {
        const files = event.target.files || [];
  
        if (files.length > 0) {
            displayFiles(files, container, progressElement, progressTextElement);
            simulateUploadProgress(progressElement, progressTextElement);
        }
    }
  
  
    function simulateUploadProgress(progressElement, progressTextElement) {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5; // simulate progress
            progress = Math.min(progress, 100); // ensure progress does not exceed 100
            progressElement.value = progress;
            progressTextElement.innerText = `${progress}%`;
  
            if (progress >= 100) {
                clearInterval(interval);
            }
        }, 200);
    }
  
    function displayFiles(files, container, progressElement, progressTextElement) {
        for (const file of files) {
            const mediaURL = URL.createObjectURL(file);
            const mediaElement = createMediaElement(file.type, mediaURL);
            container.appendChild(mediaElement);
        }
  
        // Réinitialiser la valeur du champ d'entrée de fichier
        progressElement.value = 0;
        progressTextElement.innerText = '0%';
    }
  
    function createMediaElement(type, url) {
        const mediaElement = type.includes('video') ? document.createElement('video') : document.createElement('img');
        mediaElement.src = url;
        mediaElement.controls = true;
  
        // Bouton de suppression
        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-button';
        deleteButton.innerHTML = '&#10006;'; // Unicode pour une croix (X)
        deleteButton.addEventListener('click', () => {
            // Supprimer l'élément média, le bouton de suppression et le conteneur
            const mediaContainerItem = deleteButton.parentElement;
            mediaContainerItem.remove();
            updateFileInput();
        });
  
        // Conteneur pour l'élément média et le bouton de suppression
        const mediaContainerItem = document.createElement('div');
        mediaContainerItem.className = 'media-container-item';
        mediaContainerItem.appendChild(mediaElement);
        mediaContainerItem.appendChild(deleteButton);
  
        return mediaContainerItem;
    }
  
    function updateFileInput() {
        // Réinitialiser la valeur du champ d'entrée de fichier
        videoFileInput.value = '';
        imageFileInput.value = '';
    }
  });
  