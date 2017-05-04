<html>
<head>
  <meta charset="UTF-8">
  <title>Stuco Store - Signup</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=yes">
  
  <link rel='stylesheet prefetch' href='https://fonts.googleapis.com/css?family=Open+Sans'>

      <link rel="stylesheet" href="css/style.css">
</head>

<body>
<?php
if (!isset($_POST['submit'])){
?>
<!-- The HTML login form -->
<form action="<?=$_SERVER['PHP_SELF']?>" method="post" ">
  <div class="cont">
  <div class="signup_demo">
    <div class="login">
      <div class="signup__form">

       <div class="login__row" id ="firstname">
         <input name="First_Name" type="text" autofocus required="required" class="login__input pass" id="First_Name" placeholder="First Name"/>
  </div>
        <div class="login__row" id ="lastname">
          <input name="Last_Name" type="text" required="required" class="login__input pass" id="Last_Name" placeholder="Last Name"/>
        </div>
      
        <div class="login__row" id ="username">
          <input name="username" type="email" required="required" class="login__input name" id="username" placeholder="Email"/>
        </div>
  <div class="login__row" id ="password">
          <input name="password" type="password" required="required" class="login__input pass" id="password" placeholder="Password"/>
        </div>
        <div class="login__row" id ="password_confirm">
          <input name="password_confirm" type="password" required="required" class="login__input pass" id="password_confirm" placeholder="Confirm Password"/>
        </div>
         <div class="login__row" id ="grade">
      <select name = grade required>
  <option selected="selected">Grade</option>
  <option value="1">1</option>
  <option value="2">2</option>
  <option value="3">3</option>
  <option value="4">4</option>
  <option value="5">5</option>
  <option value="6">6</option>
  <option value="7">7</option>
  <option value="8">8</option>
  <option value="9">9</option>
  <option value="10">10</option>
  <option value="11">11</option>
  <option value="12">12</option>
  <option value="Teacher">Teacher</option>
      </select>
  </div> 
       <div class="login__row" id ="gender">
      <select name=gender required>
  <option selected="selected">Gender</option>
  <option value="Female">Female</option>
  <option value="Male">Male</option>
  <option value="Other">Other</option>
</select>
  </div> 
  <input name="submit" type="submit" class="login__submit" value="Sign-Up">
        </form>
        <p class="login__signup"> <a href="index.php">Back to login page</a></p>
      </div>
    </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>

<?php
} else {
	require_once("db_const.php");
	$mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
	# check connection
	if ($mysqli->connect_errno) {
		echo "<p>MySQL error no {$mysqli->connect_errno} : {$mysqli->connect_error}</p>";
		exit();
	}
 
	$username = $_POST['username'];
	$password = $_POST['password'];
	$password_confirm = $_POST['password_confirm'];
	$Last_Name = $_POST['Last_Name'];
	$First_Name = $_POST['First_Name'];
	$grade = $_POST['grade'];
	$gender = $_POST['gender'];
	date_default_timezone_set("Asia/Taipei");
	$date = date("Y-m-d H:i:s");
	$Last_Name = ucfirst(strtolower($Last_Name));
	$First_Name = ucfirst(strtolower($First_Name));
	if($gender == "Gender"){
		echo '<script language="javascript">';
		echo 'alert("You should select your gender!")';
		echo '</script>';
	}
	if($password_confirm != $password){
		echo '<script language="javascript">';
		echo 'alert("Your password does not match!")';
		echo '</script>';
	}
	if($grade == "Grade"){
		echo '<script language="javascript">';
		echo 'alert("You should select your grade!")';
		echo '</script>';
	}
	else{
	
	$sql = "SELECT * from Users WHERE Email LIKE '{$username}' LIMIT 1";
	$result = $mysqli->query($sql);
	if (!$result->num_rows == 1) {
	
	function createSalt()
{
    $text = md5(uniqid(rand(), TRUE));
    return substr($text, 0, 40);
}
	$salt = createSalt();
	
	$passwordencrypt = hash('sha256', $salt . $password);
	$length = 10;
	$randomString = substr(str_shuffle("23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"), 0, $length);
		
			
		 
	  $sql2 = "INSERT INTO Users (First_Name, Last_Name, Date, Grade, Email, Gender, Bonus_Points_Total, 	Bonus_Points_Current, Passcode, Active, Salt, Activation_Code)".
		"VALUES ('$First_Name', '$Last_Name', '$date', '$grade', '$username', '$gender', '0','1000', '$passwordencrypt', '1', '$salt', '$randomString' )";
		if (mysqli_query($mysqli, $sql2)) {


		$sCharset = 'utf8';
		$sMailTo = $username.',stucopas@gmail.com';
		$sMailFrom = 'register@pasestore.com';
		$sSubject = "PAS Stuco - Registration";
		$sMessage = "Hi $First_Name $Last_Name! <br> Welcome to Stuco store face recognition system! Your account has been created. <br> Please contact the nearest STUCO member and use the activation code to activate your account! <bt> Activation Code: <strong>$randomString</strong>";
		$sHeaders = "MIME-Version: 1.0\r\n" .
					"Content-type: text/html; charset=$sCharset\r\n" .
					"From: $sMailFrom\r\n";
		
		mail($sMailTo, $sSubject, $sMessage, $sHeaders);

	
		echo '<script language="javascript">';
		echo 'alert("Registration completed! Please check your email and go to take a photo to activate your account!")';
		echo '</script>';	
		
		header( "refresh:0;url=index.php" );
		} else {
			echo "Error: " . $sql2 . "<br>" . $mysqli->error;
		}
					
	} else {
		echo '<script language="javascript">';
		echo 'alert("You Are Already Registered!")';
		echo '</script>';
	}
}
}
mysqli_close($conn);
	?>
  
<form action="<?=$_SERVER['PHP_SELF']?>" method="post" ">
  <div class="cont">
  <div class="signup_demo">
    <div class="login">
      <div class="signup__form">

       <div class="login__row" id ="firstname">
         <input name="First_Name" type="text" autofocus required="required" class="login__input pass" id="First_Name" placeholder="First Name" value="<?php echo isset($_POST["First_Name"]) ? htmlentities($_POST["First_Name"]) : ''; ?>"/>
  </div>
        <div class="login__row" id ="lastname">
          <input name="Last_Name" type="text" required="required" class="login__input pass" id="Last_Name" placeholder="Last Name" value="<?php echo isset($_POST["Last_Name"]) ? htmlentities($_POST["Last_Name"]) : ''; ?>"/>
        </div>
      
        <div class="login__row" id ="username">
          <input name="username" type="email" required="required" class="login__input name" id="username" placeholder="Email" value="<?php echo isset($_POST["username"]) ? htmlentities($_POST["username"]) : ''; ?>"/>
        </div>
  <div class="login__row" id ="password">
          <input name="password" type="password" required="required" class="login__input pass" id="password" placeholder="Password" />
        </div>
        <div class="login__row" id ="password_confirm">
          <input name="password_confirm" type="password" required="required" class="login__input pass" id="password_confirm" placeholder="Confirm Password"/>
        </div>
         <div class="login__row" id ="grade">
      <select name = grade required>
  <option selected='<?php echo $grade?>'><?php echo $grade?></option>
  <option value="1">1</option>
  <option value="2">2</option>
  <option value="3">3</option>
  <option value="4">4</option>
  <option value="5">5</option>
  <option value="6">6</option>
  <option value="7">7</option>
  <option value="8">8</option>
  <option value="9">9</option>
  <option value="10">10</option>
  <option value="11">11</option>
  <option value="12">12</option>
  <option value="Teacher">Teacher</option>
      </select>
  </div> 
       <div class="login__row" id ="gender">
      <select name=gender required>
    <option selected='<?php echo $gender?>'><?php echo $gender?></option>
  <option value="Female">Female</option>
  <option value="Male">Male</option>
  <option value="Other">Other</option>
</select>
  </div> 
  <input name="submit" type="submit" class="login__submit" value="Sign-Up">
        </form>
        <p class="login__signup"> <a href="index.php">Back to login page</a></p>
      </div>
    </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>  
 
    
</body>    
</html>
