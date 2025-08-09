document.addEventListener('DOMContentLoaded', function() {
    const downloadBtn = document.getElementById('download-btn');
    const videoUrlInput = document.getElementById('video-url');
    const qualitySelect = document.getElementById('quality');
    const statusDiv = document.getElementById('status');
    const statusMessage = document.getElementById('status-message');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const resultDiv = document.getElementById('result');
    const filenameSpan = document.getElementById('filename');
    const downloadLink = document.getElementById('download-link');
    const newDownloadBtn = document.getElementById('new-download');

    downloadBtn.addEventListener('click', startDownload);
    newDownloadBtn.addEventListener('click', resetForm);

    function startDownload() {
        const url = videoUrlInput.value.trim();
        const quality = qualitySelect.value;

        if (!url) {
            showError('Please enter a video URL');
            return;
        }

        if (!isValidUrl(url)) {
            showError('Please enter a valid URL starting with http:// or https://');
            return;
        }

        // Show loading state
        downloadBtn.disabled = true;
        downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        statusDiv.classList.add('visible');
        statusMessage.textContent = 'Preparing download...';
        updateProgress(0);

        // Start the download
        fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                quality: quality
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message) });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                completeDownload(data.filename, data.filepath);
            } else {
                throw new Error(data.message);
            }
        })
        .catch(error => {
            showError(error.message);
        })
        .finally(() => {
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = '<i class="fas fa-download"></i> Download';
        });

        // Simulate progress (in real app, you'd use WebSockets for real progress)
        simulateProgress();
    }

    function simulateProgress() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress > 90) clearInterval(interval);
            updateProgress(Math.min(progress, 90));
        }, 500);
    }

    function updateProgress(percent) {
        progressBar.style.width = percent + '%';
        progressText.textContent = Math.round(percent) + '%';
        
        if (percent < 30) {
            statusMessage.textContent = 'Preparing download...';
        } else if (percent < 60) {
            statusMessage.textContent = 'Downloading video...';
        } else {
            statusMessage.textContent = 'Processing video...';
        }
    }

    function completeDownload(filename, filepath) {
        statusDiv.classList.remove('visible');
        resultDiv.classList.add('visible');
        filenameSpan.textContent = filename;
        
        // Set up download link
        downloadLink.href = `/downloads/${filename}`;
        downloadLink.download = filename;
        
        // Complete progress to 100%
        updateProgress(100);
    }

    function showError(message) {
        statusDiv.classList.add('visible');
        statusMessage.textContent = message;
        statusMessage.style.color = 'var(--danger)';
        progressBar.style.backgroundColor = 'var(--danger)';
        
        setTimeout(() => {
            statusDiv.classList.remove('visible');
            statusMessage.style.color = '';
            progressBar.style.backgroundColor = 'var(--primary)';
        }, 5000);
    }

    function resetForm() {
        resultDiv.classList.remove('visible');
        videoUrlInput.value = '';
        videoUrlInput.focus();
        updateProgress(0);
    }

    function isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }
});