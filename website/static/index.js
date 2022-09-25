// Registration form validation

var password = document.registration.password;
var repeat_password = document.registration.repeat_password;
var username = document.registration.username;
var email = document.registration.email;


function formValidation() {

  if (ValidateEmail(email)) {
    if (allLetter(username)) {
      if (password_validation(password, 7, 12)) {
        if (matchPassword(password, repeat_password)) {

        }
      }
    }

  }

  return false;



  function password_validation(password, minimum, maximum) {
    var password_length = password.value.length;
    if (password_length == 0 || password_length > maximum || password_length < minimum) {
      alert("Password should not be empty / length be between " + minimum + " to " + maximum);
      password.focus();
      return false;
    }
    return true;
  }
 
  function allLetter(username) {
  var letters =   /^[A-Za-z]+/ ;
    if (username.value.match(letters)) {
      return true;
    }
    else {
      alert('Username must have alphabet characters only');
      username.focus();
      return false;
    }
  }

  
  function ValidateEmail(email) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (email.value.match(mailformat)) {
      return true;
    }
    else {

      alert("Enter valid email id", "error");

    }
  }
  
}
// ----------------------------------------------------------------

// registration password condditioned label 

function labelVisible(){
  document.getElementById("passwordLable").style.display = "inline";
}
function labelInvisible(){
  document.getElementById("passwordLable").style.display = "none";
}



// 
function categoryInput(){
  form = document.getElementById('category-form');
  if(form.style.display == "block"){
    form.style.display = "none";
  }else{
    form.style.display = "block";
  }
}




function like(postId) {
  const likeCount = document.getElementById(`likes-count-${postId}`);
  console.log(likeCount)
  const likeButton = document.getElementById(`like-button-${postId}`);
  console.log(likeButton)

 
  fetch(`/likepost/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {console.log(data)
      likeCount.innerHTML = data["likes"];
      if (data["liked"] === true) {
        likeButton.className = "fa-solid fa-hands-clapping text-primary fa-lg";
      } else {
        likeButton.className = "fa-solid fa-hands-clapping fa-lg";
      }
    })
}
