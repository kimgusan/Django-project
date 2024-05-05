if(!check){
    let modalMessage = "<span>비밀번호를</span><span>확인해주세요!</span>";
    showWarnModal(modalMessage)
}

const button = document.querySelector("button[type=button]")
const passwordNumberRegex = /[0-9]/g;
const passwordEnglishRegex = /[a-z]/gi;
const passwordSpecialCharacterRegex = /[`~!@@#$%^&*|\\\'\";:\/?]/gi;

const passwordInput = document.getElementById("password");
const passwordCheckInput = document.getElementById("password-check");

let passwordCheck = false;

passwordInput.addEventListener("blur", (e) => {
    if(!e.target.value){
        e.target.nextElementSibling.nextElementSibling.innerText = "비밀번호를 입력하세요.";
        showHelp(e.target, "error.png");
        passwordCheck = false;
        return;
    }

    passwordCheck = e.target.value.length > 9 &&
                    e.target.value.length < 21 &&
                    passwordNumberRegex.test(e.target.value) &&
                    passwordEnglishRegex.test(e.target.value) &&
                    passwordSpecialCharacterRegex.test(e.target.value) &&
                    !/\s/g.test(e.target.value);

    if(passwordCheck){
        e.target.nextElementSibling.nextElementSibling.innerText = "";
        showHelp(e.target, "pass.png");
    }else{
        e.target.nextElementSibling.nextElementSibling.innerText = "공백 제외 영어 및 숫자, 특수문자 모두 포함하여 10~20자로 입력해주세요.";
        showHelp(e.target, "error.png");
        passwordCheck = false;
    }
});

passwordCheckInput.addEventListener("blur", (e) => {
    if(!passwordCheck){
        e.target.nextElementSibling.nextElementSibling.innerText = "비밀번호를 다시 확인해주세요.";
        showHelp(e.target, "error.png");
        return;
    }

    if(!e.target.value){
        e.target.nextElementSibling.nextElementSibling.innerText = "비밀번호 확인을 위해 한번 더 입력하세요.";
        showHelp(e.target, "error.png");
        passwordCheck = false;
        return;
    }
    passwordCheck = passwordInput.value === e.target.value
    if(passwordCheck) {
        e.target.nextElementSibling.nextElementSibling.innerText = "";
        showHelp(e.target, "pass.png");
    }else{
        e.target.nextElementSibling.nextElementSibling.innerText = "위 비밀번호와 일치하지 않습니다. 다시 입력해주세요.";
        showHelp(e.target, "error.png");
        passwordCheck = false;
    }
});

const showHelp = (input, fileName) => {
    input.nextElementSibling.style.display = "block";
    input.nextElementSibling.setAttribute("src", "/static/public/images/" + fileName);

    if (fileName === "pass.png") {
        input.style.border = "1px solid rgba(0, 0, 0, 0.1)";
        input.style.background = "rgb(255, 255, 255)";
        input.nextElementSibling.setAttribute("width", "18px");
    } else {
        input.style.border = "1px solid rgb(255, 64, 62)";
        input.style.background = "rgb(255, 246, 246)";
    }
}

button.addEventListener("click", (e) => {
    if(!passwordCheck){
        return;
    }
    const passhash = CryptoJS.SHA256(passwordInput.value);
    passwordInput.value = passhash.toString(CryptoJS.enc.Hex);

    const passCheckhash = CryptoJS.SHA256(passwordCheckInput.value);
    passwordCheckInput.value =  passCheckhash.toString(CryptoJS.enc.Hex);

    document.mypage.submit();
});

//썸네일
const input = document.querySelector("input[name=profile]");
const thumbnail = document.querySelector(".basic-info-container img");
const cancel = document.querySelector("div.cancel");

input.addEventListener("change", (e) => {
    const [file] = e.target.files;
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.addEventListener("load", (e) => {
        const path = e.target.result;
        if (path.includes("image")) {
            cancel.style.display = "block";
            thumbnail.src = path;
        } else {
            let modalMessage = "<span>이미지 파일만 가능합니다.</span>";
            showWarnModal(modalMessage);
            input.value = "";
        }
    });
});

cancel.addEventListener("click", (e) => {
    thumbnail.src = `/static/public/images/default-profile.png`;
    e.target.style.display = "none";
    input.value = "";
});