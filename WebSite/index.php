<html>
<head>
  <meta charset="UTF-8">
  <title>PAS Stuco Store - Balance Inquiry Login</title>
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
  <div class="demo">
    <div class="login">
      <div class="login__check"></div>
      <div class="login__form">
        <div class="login__row">
          <svg class="login__icon name svg-icon" viewBox="0 0 20 20">
            <path d="M0,20 a10,8 0 0,1 20,0z M10,0 a4,4 0 0,1 0,8 a4,4 0 0,1 0,-8" />
          </svg>
          <input name="username" type="email" autofocus required="required" class="login__input name" id="username" placeholder="Email"/>
        </div>
  <div class="login__row">
          <svg class="login__icon pass svg-icon" viewBox="0 0 20 20">
            <path d="M0,20 20,20 20,8 0,8z M10,13 10,16z M4,8 a6,8 0 0,1 12,0" />
          </svg>
          <input name="password" type="password" required="required" class="login__input pass" id="password" placeholder="Password"/>
        </div>
        <input name="submit" type="submit" class="login__submit" value="Login">
        </form>
        <p class="login__signup">Don't have an account? &nbsp;<a href="Signup.php">Sign Up</a></p>
        <p class="login__signup"> <a href="Transaction.php">Transaction Record</a></p>
      </div>
    </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>

    <script src="js/index.js"></script>
    
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
 
	$sql = "SELECT * from Users WHERE Email LIKE '{$username}' LIMIT 1";
	$result = $mysqli->query($sql);
		while($row = $result->fetch_assoc()) {
			$password = hash('sha256', $row["Salt"].$_POST['password']);	
			$pass_auth = $row["Passcode"];
			$FirstName = $row["First_Name"];
			$LastName = $row["Last_Name"];
			$Grade = $row["Grade"];
			$Balance = $row["Balance"];
			$Bonus = $row["Bonus_Points_Current"];
			$Activate = $row["Active"];
			$Admin = $row["Admin"];
		}
	?>	
	<?php if ($result->num_rows != 1 ){
		 $errors['error'] = 'Password and username do not match!';
		?>
      <form action="<?=$_SERVER['PHP_SELF']?>" method="post" ">
  <div class="cont">
  <div class="demo">
    <div class="login">
      <div class="login__check"></div>
      <div class="login__form">
        <div class="login__row">
          <svg class="login__icon name svg-icon" viewBox="0 0 20 20">
            <path d="M0,20 a10,8 0 0,1 20,0z M10,0 a4,4 0 0,1 0,8 a4,4 0 0,1 0,-8" />
          </svg>
          <input name="username" type="email" autofocus required="required" class="login__input name" id="username" placeholder="Email"/>
        </div>
  <div class="login__row">
          <svg class="login__icon pass svg-icon" viewBox="0 0 20 20">
            <path d="M0,20 20,20 20,8 0,8z M10,13 10,16z M4,8 a6,8 0 0,1 12,0" />
          </svg>
          <input name="password" type="password" required="required" class="login__input pass" id="password" placeholder="Password"/>
          <br>
          <br>
         <?php if(isset($errors['error'])) { echo '<strong><font color="red">'.$errors["error"].'</font></strong>'; }?>
        </div>
        <input name="submit" type="submit" class="login__submit" value="Login">
        </form>
        <p class="login__signup">Don't have an account? &nbsp;<a href="Signup.php">Sign Up</a></p>
        <p class="login__signup"> <a href="Transaction.php">Transaction Record</a></p>
      </div>
    </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>

    <script src="js/index.js"></script>
        
		<?php }
	else if($password==$pass_auth) {
		echo '<script language="javascript">';
		echo 'alert("The System will Logout after 15 seconds!")';
		echo '</script>';
		echo '<div class="cont">';	
        echo '<div class="info_demo">';
		echo '<div class="app__login">';
		echo '<p class="app__hello"> Logged in successfully</p>';	
		if($Admin == '1'){
		echo '<div class="cont_admin">';
		echo '<div class="info_demo_admin">';	
		echo '<p class="app__helloText">'.'Hi!'.'You are admin!'.'</p>';	
			
		}
		else{
			if ($Activate == '1'){
				echo '<p class="app__helloText">'.'You should activate your account! '.'</p>';
			}
		echo '<p class="app__helloText">'.'Hi! '. $FirstName." ".$LastName.'</p>';
        echo '<p class="app__helloText">'.'Grade:'.$Grade.'</p>';
		echo '<p class="app__helloText">'.'Balance: $'.$Balance.'</p>';
		echo '<p class="app__helloText">'.'Bonus Point(s): '.$Bonus.'</p>';
		echo '<p>';
		echo '<form action="index.php" method="post">';
		echo '<input type="submit" class="logout__submit" name="BYLAWS" value="Logout"></form>';
		echo '</p>';
		echo '</div>';	
		echo '</div>';
		echo '</div>';
		header( "refresh:15;url=index.php" );
		
		}
	?>
	<?php }else{
	 $errors['error'] = 'Password and username do not match!';
	 ?>
     
     
      <form action="<?=$_SERVER['PHP_SELF']?>" method="post" ">
  <div class="cont">
  <div class="demo">
    <div class="login">
      <div class="login__check"></div>
      <div class="login__form">
        <div class="login__row">
          <svg class="login__icon name svg-icon" viewBox="0 0 20 20">
            <path d="M0,20 a10,8 0 0,1 20,0z M10,0 a4,4 0 0,1 0,8 a4,4 0 0,1 0,-8" />
          </svg>
          <input name="username" type="email" autofocus required="required" class="login__input name" id="username" placeholder="Email"/>
        </div>
  <div class="login__row">
          <svg class="login__icon pass svg-icon" viewBox="0 0 20 20">
            <path d="M0,20 20,20 20,8 0,8z M10,13 10,16z M4,8 a6,8 0 0,1 12,0" />
          </svg>
          <input name="password" type="password" required="required" class="login__input pass" id="password" placeholder="Password"/>
          <br>
          <br>
         <?php if(isset($errors['error'])) { echo '<strong><font color="red">'.$errors["error"].'</font></strong>'; }?>
        </div>
        <input name="submit" type="submit" class="login__submit" value="Login">
        </form>
        <p class="login__signup">Don't have an account? &nbsp;<a href="Signup.php">Sign Up</a></p>
        <p class="login__signup"> <a href="Transaction.php">Transaction Record</a></p>
      </div>
    </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>

    <script src="js/index.js"></script>
     
	<?php
    }
}

?>	
	
</body>
</html>
