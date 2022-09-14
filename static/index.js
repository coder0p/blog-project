var password1 = document.registration.password1;
  var confirm_password = document.registration.confirm_password;
  var uname = document.registration.username;
  var uemail = document.registration.email;
  
 

function formValidation() {
  

  if (ValidateEmail(uemail)) {
    if (allLetter(uname)) {
      if (password_validation(password1, 7, 12)) {
        if (matchPassword(password1, confirm_password)) {
          
        }
      }
    }
  }
  return false;

  /////////////////////////////////////////
  function password_validation(password1, minimum, maximum) {
    var password_length = password1.value.length;
    if (password_length == 0 || password_length >= maximum || password_length < minimum) {
      swal("Password should not be empty / length be between " + minimum + " to " + maximum);
      password1.focus();
      return false;
    }
    return true;
  }

  /////////////////////////////////////////
  function allLetter(uname) {
    var letters = /^[A-Za-z]+$/;
    if (uname.value.match(letters)) {
      return true;
    }
    else {
      swal('Username must have alphabet characters only');
      uname.focus();
      return false;
    }
  }
  /////////////////////////////////////////
  function ValidateEmail(uemail) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (uemail.value.match(mailformat)) {
      return true;
    }
    else {
      
        swal("Enter valid email id", "error"); 
      
      
       
      }
    }
    /////////////////////////////////////////
    
    function matchPassword() {
      if (password1.value != confirm_password.value) {
        swal("Passwords did not match");
      }
  
    }
    
    
  }
    