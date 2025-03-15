document.addEventListener("DOMContentLoaded", () => {
  const loginTab = document.getElementById("tab-login");
  const registerTab = document.getElementById("tab-register");
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const formWrapper = document.getElementById("form-wrapper");
  const signupButton = document.getElementById('signupbutton');
  
  loginTab.addEventListener("click", () => {
    loginTab.classList.add("border-blue-500", "text-blue-500");
    registerTab.classList.remove("border-blue-500", "text-blue-500");
    loginForm.classList.remove("hidden");
    registerForm.classList.add("hidden");
    formWrapper.style.height = `${loginForm.offsetHeight}px`; // Smooth transition to login form
  });

  registerTab.addEventListener("click", () => {
    registerTab.classList.add("border-blue-500", "text-blue-500");
    loginTab.classList.remove("border-blue-500", "text-blue-500");
    registerForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
    formWrapper.style.height = `${registerForm.offsetHeight}px`; // Smooth transition to register form
  });

  // Set initial height to login form
  formWrapper.style.height = `${loginForm.offsetHeight}px`;
});

async function submit_signup() {
  // Alert to test if the function is triggered
  alert('hey')

  // Get the values from the form inputs using their IDs
  const username = document.getElementById('creationusernmae').value;
  const email = document.getElementById('creationemail').value;
  const password = document.getElementById('creationpass').value;
  const cpassword = document.getElementById('creationcpass').value;

  // Create the data object to send to the backend
  const data = {
      username: username,
      email: email,
      password: password,
      cpassword: cpassword
  };

  try {
      const response = await fetch('/createaccount', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok) {
          // Redirect to the home page if account creation is successful
          window.location.href = '/';
      } else {
          // Show the error message if there's an issue
          alert(result.error || 'An unknown error occurred');
      }
  } catch (error) {
      // Handle any errors that occur during the fetch process
      alert('An error occurred: ' + error.message);
  }
};

async function submit_login() {
  const email = document.getElementById('loginemail').value;
  const password = document.getElementById('loginpass').value;

  const data = {
    email: email,
    pswd: password
  }

  try {
    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
        // Redirect to the home page if account creation is successful
        window.location.href = '/';
    } else {
        // Show the error message if there's an issue
        alert(result.error || 'An unknown error occurred');
    }
  } catch (error) {
      // Handle any errors that occur during the fetch process
      console.error('An error occurred: ' + error.message);
  }
}
