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
  document.getElementById("passwordLable").style.display = "inline"
}
function labelInvisible(){
  document.getElementById("passwordLable").style.display = "none"
}


// comment view button funtionality

function commentVisible(){
  let commentSection = document.getElementById('comment');
  if(commentSection.style.display == "block"){
    commentSection.style.display = "none"
  }else{
    commentSection.style.display = "block"
  }
}