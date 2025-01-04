const usernameField= document.querySelector("#usernameField");
const invalidFeedbackArea = document.querySelector(".invalid-feedback-area");
const checkUsernameOutPut=  document.querySelector(".checkUsernameOutPut");
const submitBtn =document.querySelector(".submit-btn");

usernameField.addEventListener('keyup', (e) =>{
  const userNameVal = e.target.value;
  //console.log("Usrname:", userNameVal);
  checkUsernameOutPut.style.display="block";
  checkUsernameOutPut.innerText= `Checking ${userNameVal}`;
  invalidFeedbackArea.style.display="none";
  usernameField.classList.remove("is-invalid")
  
  if (userNameVal.length>0){
    fetch("/authentication/validate-username", {
      body: JSON.stringify({username:userNameVal}),
      method: "POST"
    })
    .then((res)=>res.json())
    .then((data) =>{
      console.log("data", data);
      checkUsernameOutPut.style.display="none";
      if (data.username_error){
        invalidFeedbackArea.style.display="block";
        usernameField.classList.add("is-invalid")
        invalidFeedbackArea.innerHTML= `<p>${data.username_error}</p>`;
        submitBtn.disabled=true;
      }else{
        submitBtn.removeAttribute("disabled");
      }
    });
  }
});