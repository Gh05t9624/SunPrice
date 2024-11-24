// Caption Profile
let uploadimg = document.getElementById("upload-profile");
let choosenimg = document.getElementById("choosen-profile");
// let fileNameimg = document.getElementById("file-name");


uploadimg.onchange = () => {
    let reader = new FileReader();
    reader.readAsDataURL(uploadimg.files[0]);
    reader.onload = () => {
        choosenimg.setAttribute("src", reader.result);
    } 

    fileNameimg.textContent = uploadimg.files[0].name;
}

// Caption Couverture
let uploadVideo = document.getElementById("upload-couverture");
let choosenVideo = document.getElementById("choosen-couverture");
// let fileNameVideo = document.getElementById("file-name_video");


uploadVideo.onchange = () => {
    let reader = new FileReader();
    reader.readAsDataURL(uploadVideo.files[0]);
    reader.onload = () => {
        choosenVideo.setAttribute("src", reader.result);
    } 

    fileNameVideo.textContent = uploadVideo.files[0].name;
}