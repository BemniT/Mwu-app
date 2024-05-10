// Initialize Firebase
const firebaseConfig = {
    apiKey: "AIzaSyC2rCweoCvXIB9QIIrKo9Kz58TqnZloQnQ",
    authDomain: "muw-app.firebaseapp.com",
    projectId: "muw-app",
    storageBucket: "muw-app.appspot.com",
    messagingSenderId: "656137794361",
    appId: "1:656137794361:web:e7cc46d3760ce47642eee8",
    measurementId: "G-XG54W8C1FQ"
};

firebase.initializeApp(firebaseConfig);

const database = firebase.database();

// Login form submission
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    
    // Firebase authentication
    firebase.auth().signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
        // Signed in
        const user = userCredential.user;
        console.log("Logged in as:", user.email);
        
        // Check if the user is the staff member
        if (user.email === "yohannsgezahegn2@gmail.com") {
            // Redirect to staff member dashboard
            window.location.href = "staffmemberdashboard.html";
        } else {
            // Redirect to regular user dashboard or show a message
            window.location.href = "userdashboard.html"; // Replace with your regular user dashboard URL
        }
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.error(errorMessage);
        // Handle errors, e.g., display error message to the user
    });
});

// Sign-up form submission
document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    
    // Firebase authentication
    firebase.auth().createUserWithEmailAndPassword(email, password)
    .then((userCredential) => {
        // Signed up
        const user = userCredential.user;
        console.log("Signed up as:", user.email);
        // Redirect or show a message to the user
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.error(errorMessage);
        // Handle errors, e.g., display error message to the user
    });
});
