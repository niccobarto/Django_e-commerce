    const input = document.getElementById('front_image');
    const previewBox = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview_img');
    const cancelBtn = document.getElementById('cancel-image-btn');

    input.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImg.src = e.target.result;
                previewBox.style.display = 'flex';

            };
            reader.readAsDataURL(file);
        } else {
            previewBox.style.display = 'none';
            previewImg.src = '';
        }
    });

    cancelBtn.addEventListener('click', function () {
        input.value = '';                 // reset file input
        previewImg.src = '';              // nasconde immagine
        previewBox.style.display = 'none';
    });