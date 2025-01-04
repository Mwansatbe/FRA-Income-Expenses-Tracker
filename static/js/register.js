const emailField = document.querySelector("#emailField");
const invalidEmailFeedbackArea = document.querySelector(".invalid-email-feedback-area");
const checkUserEmailOutPut = document.querySelector(".checkUserEmailOutPut");

const usernameField = document.querySelector("#usernameField");
const invalidFeedbackArea = document.querySelector(".invalid-feedback-area");
const checkUsernameOutPut = document.querySelector(".checkUsernameOutPut");
const submitBtn = document.querySelector(".submit-btn");
const registerForm = document.querySelector("#registerForm");

let emailValid = false;
let usernameValid = false;

registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    if (emailValid && usernameValid) {
        registerForm.submit();
    }
});

emailField.addEventListener('keyup', (e) => {
    const emailValue = e.target.value;  
    console.log("email", emailValue);
    invalidEmailFeedbackArea.style.display = "none";
    emailField.classList.remove("is-invalid");
    checkUserEmailOutPut.style.display = "block";
    checkUserEmailOutPut.innerHTML = `Checking ${emailValue}`;
    emailValid = false;
    validateForm();

    if (emailValue.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailValue }),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            checkUserEmailOutPut.style.display = "none";
            if (data.email_error) {
                invalidEmailFeedbackArea.style.display = "block";
                emailField.classList.add("is-invalid");
                invalidEmailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                emailValid = false;
            } else {
                emailValid = true;
            }
            validateForm();
        });
    } else {
        checkUserEmailOutPut.style.display = "none";
        emailValid = false;
        validateForm();
    }
});

usernameField.addEventListener('keyup', (e) => {
    const userNameVal = e.target.value;
    checkUsernameOutPut.style.display = "block";
    checkUsernameOutPut.innerText = `Checking ${userNameVal}`;
    invalidFeedbackArea.style.display = "none";
    usernameField.classList.remove("is-invalid");
    usernameValid = false;
    validateForm();
    
    if (userNameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: userNameVal }),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            checkUsernameOutPut.style.display = "none";
            if (data.username_error) {
                invalidFeedbackArea.style.display = "block";
                usernameField.classList.add("is-invalid");
                invalidFeedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                usernameValid = false;
            } else {
                usernameValid = true;
            }
            validateForm();
        });
    } else {
        checkUsernameOutPut.style.display = "none";
        usernameValid = false;
        validateForm();
    }
});

function validateForm() {
    if (emailValid && usernameValid) {
        submitBtn.removeAttribute("disabled");
    } else {
        submitBtn.setAttribute("disabled", "disabled");
    }
}

