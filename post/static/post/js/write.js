autosize($("textarea"));

const uploads = document.querySelectorAll("input.upload");
const thumbnails = document.querySelectorAll("label.attach img.thumbnail");
const checkAgree = document.querySelector("input[name='agree']");

function checkLength(textarea, max){
    let value = textarea.value
    let length = value.length > max ? max : value.length;
    max = max.toLocaleString('ko-KR'); //한국 숫자 표기법(끝 3자리 마다 콤마 삽입)
    textarea.nextElementSibling.innerText = `${length}/${max}`;
}

checkAgree.addEventListener("change", (e) => {
    let isChecked = e.target.checked;
    isChecked ? checkedSaveId() : notCheckedSaveId();
});

function checkedSaveId(){
    document.querySelector("#check-agree span.checkbox").style.borderColor = "rgb(235 124 120)";
    document.querySelector("#check-agree span.checkbox").style.backgroundColor = "rgb(235 124 120)";
}

function notCheckedSaveId(){
    document.querySelector("#check-agree span.checkbox").style.borderColor = "";
    document.querySelector("#check-agree span.checkbox").style.backgroundColor = "";
}

uploads.forEach((upload, i) => {
    upload.addEventListener("change", (e) => {
        let reader = new FileReader();
        reader.readAsDataURL(e.target.files[0]);
        reader.addEventListener("load", (e) => {
            let url = e.target.result;
            if(url.includes('image')) {
                document.querySelectorAll("label.attach")[i].lastElementChild.style.display = "none"
                document.querySelectorAll("label.attach")[i].lastElementChild.previousElementSibling.style.display = "none"
                document.querySelectorAll("div.x")[i].style.display = "block"
                thumbnails[i].style.display = "block"
                thumbnails[i].src = url;
            }else{
                let modalMessage = "<span>이미지 파일만 등록 가능합니다.</span>"
                showWarnModal(modalMessage);
            }
        });
    });
});

document.querySelectorAll("div.x").forEach((cancel, i) => {
    cancel.addEventListener("click", (e) => {
        e.preventDefault();
        uploads[i].value = "";
        document.querySelectorAll("label.attach")[i].lastElementChild.style.display = "block"
        document.querySelectorAll("label.attach")[i].lastElementChild.previousElementSibling.style.display = "block"
        document.querySelectorAll("div.x")[i].style.display = "none"
        thumbnails[i].src = "";
        thumbnails[i].style.display = "none"
    });
});

document.write.ok.addEventListener("click", (e) => {
    if(!document.write['post-title'].value){
        return;
    }
    if(!document.write['post-content'].value){
        return;
    }
    document.write.submit();
});













