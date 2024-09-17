<?php
session_start();
$server = "localhost";
$username = "root";
$password = "";
$db = "user_system"; // Replace with your database name

// Create a connection
$conn = new mysqli($server, $username, $password, $db);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Handle registration form submission
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $name = mysqli_real_escape_string($conn, $_POST['name']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $password = mysqli_real_escape_string($conn, $_POST['pass']);

    // Hash the password before saving it
    $hashedPassword = password_hash($password, PASSWORD_BCRYPT);

    // Insert new user data
    $sql = "INSERT INTO users (name, email, password) VALUES ('$name', '$email', '$hashedPassword')";

    if ($conn->query($sql) === TRUE) {
        echo "Registration successful!";
        header('Location: login.html'); // Redirect to login page
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>
