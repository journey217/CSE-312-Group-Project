<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="../static/registration.css">
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <div class='register'>
        <ul>
            <header class="header">PRODUCT NAME</header>
            <div class="register-form">
                <form class="reg-inputs">
                    <header class="formheader">Create New Account</header>
                    <input type="name" placeholder='First Name' name='name' required />
                    <input type="name" placeholder='Last Name' name='name' required />
                    <input type="date" placeholder='Date of Birth' name='name' required />
                    <input type="email" placeholder="Email" name="email" required />
                    <input type="password" placeholder="Password" name="password" required />
                    <input type="password" placeholder="Confirm Password" name="password" required />
                    <button>Register</button>
                </form>
                <button class="create-account-button">
                    <Link to="/login">Have An Account? Click Here</Link>
                </button>
            </div>
        </ul>
    </div>
</body>

</html>