    const input = document.getElementById("id_front_image");
    const preview = document.getElementById("image-preview");
    const previewImg = document.getElementById("preview_img");
    const cancelBtn = document.getElementById("cancel-image-btn");

    input.addEventListener("change", function () {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImg.src = e.target.result;
                preview.style.display = "block";
            };
            reader.readAsDataURL(input.files[0]);
        }
    });

    cancelBtn.addEventListener("click", function () {
        input.value = "";  // Clear the file input
        preview.style.display = "none";
    });