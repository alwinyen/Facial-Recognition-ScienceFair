<html>
<head>
  <meta charset="UTF-8">
  <title>Stuco Store - Transaction Record</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=yes">
  
  <link rel='stylesheet prefetch' href='https://fonts.googleapis.com/css?family=Open+Sans'>

      <link rel="stylesheet" href="css/style.css">
</head>
<?php
if (!isset($_POST['submit'])){
	 $errors['sendername'] = '';
?>
<body>
<!-- The HTML login form -->
<form action="<?=$_SERVER['PHP_SELF']?>" method="post" ">
  <div class="cont">
  <div class="signup_demo">
    <div class="login">
      <div class="signup__form">
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
       <div class="login__row" id ="Serial">
         <input name="Serial" type="text" autofocus required="required" class="login__input pass" id="Serial" placeholder="Transaction Number"/>
         <div class="login__input pass">
         <input name="submit" type="submit" class="login__submit" value="Search">
         </form>
 <p class="login__signup"> <a href="index.php">Back to login page</a></p>
         </div>
</div>
      </div>
    </div>
    
<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
<?php
} else {
	require_once("db_const.php");
	$mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
	mysqli_set_charset($mysqli,"utf8");
	# check connection
	if ($mysqli->connect_errno) {
		echo "<p>MySQL error no {$mysqli->connect_errno} : {$mysqli->connect_error}</p>";
		exit();
	}
	 
	$serial = $_POST['Serial'];
	
	$sql = "SELECT * from Log WHERE Transaction_Number LIKE '{$serial}'";
	$result = $mysqli->query($sql);
		
		if ($result->num_rows == 0 ){
			  $current = $_SERVER["PHP_SELF"];
			  $errors['sendername'] = 'Invalid Transaction Number';
			  echo '<form method="post">';
			  echo ' <div class="cont">';
			  echo ' <div class="signup_demo">';
			  echo ' <div class="login">';
			  echo '  <div class="signup__form">';
			  echo '<br>';
			  echo '<br>';
			  echo '<br>';
			  echo '<br>';
			  echo '<br>';
			  echo '<br>';
			  echo '<br>';
			  echo '<br>';
			  echo '<div class="login__row" id ="Serial">';
			  echo ' <input name="Serial" type="text" autofocus required="required" class="login__input pass" id="Serial" placeholder="Transaction Number"/>';
			  echo '<br>';
			  echo '<br>';
			  if(isset($errors['sendername'])) { echo '<strong><font color="red">'.$errors["sendername"].'</font></strong>'; }
			  echo ' <div class="login__input pass">';
			  echo '<input name="submit" type="submit" class="login__submit" value="Search">';
			  echo ' </form>';
			  echo '<p class="login__signup"> <a href="index.php">Back to login page</a></p>';
			  echo '</div>';
			  echo '</div>';
			  echo '</div>';
			  echo '';
			  echo '';
			  echo '';
		}
		else {
			echo '<div class="cont">';	
       		echo '<div class="info_demo">';
			echo '<div class="app__login">';
			while($row = $result->fetch_assoc()) {
			$amount = $row["Amount"];
			$Items_Name = $row["Items_Name"];
			$Balance = $row["Balance"];
			$date = $row["Date"];
			$Single_Transaction_Amount = $row["Single_Transaction_Amount"];
			if ($Items_Name != ''){
				echo '<p class="app__tranText">'.'Item: '.$Items_Name.'</p>';	
				echo '<p class="app__tranText">'.' Amount: '.$amount.' Price: '.$Balance.'</p>';	
				echo '<p class="app__tranText">----------------------------------------</p>';
			
			}
			else if($Single_Transaction_Amount != ''){
				$Transaction_Amount = $Single_Transaction_Amount;
			}
		}
			echo '<p class="app__tranText">'.$Transaction_Amount.'</p>';
			echo '<p class="app__tranText">'.'On'.$date.'</p>';
			echo '<p class="app__tranText">'.'Transaction ID: '.$serial.'</p>';
			echo '<form action="/Transaction.php" method="get">';
  			echo '<input type="submit" value="Back" class="login__submit"' ;
	        echo 'name="Submit" id="frm1_submit" />';
			echo '</form>';
			echo '</div>';	
       		echo '</div>';
			echo '</div>';
		}
		
}
	?>

 </body>
</html>
