<?php
session_start();

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $user = $_POST['email'];
    $pass = $_POST['pass'];

    $server = "localhost";
    $username = "root";
    $password = "";
    $db = "hbs";

    // Create a database connection
    $con = mysqli_connect($server, $username, $password, $db);

    // Check for connection success
    if (!$con) {
        die("Connection failed: " . mysqli_connect_error());
    }

    // Query to select user
    $sql = "SELECT * FROM user WHERE email='$user'";
    $result = $con->query($sql);

    // Fetch user data
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $dbpassword = $row['user_pass'];
        $isAdmin = $row['is_admin'];

        // Verify password
        if ($dbpassword == $pass) {
            $_SESSION['user'] = $user;
            $msg = "Login successful";

            // Redirect based on user role
            if ($isAdmin == 1) {
                $loc = "admin.php";  // Redirect admin users
            } else {
                $loc = "index.html";  // Redirect regular users
            }

            echo "<script type='text/javascript'>
                    alert('$msg');
                    window.location.href='$loc';
                  </script>";
        } else {
            echo "<script type='text/javascript'>
                    alert('Invalid password');
                    window.location.href='login.html';
                  </script>";
        }
    } else {
        echo "<script type='text/javascript'>
                alert('No user found');
                window.location.href='login.html';
              </script>";
    }

    // Close the connection
    $con->close();
}
else {
    // If request method is not POST
    echo "Invalid request method.";
}
?>
