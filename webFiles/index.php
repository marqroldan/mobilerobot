<?php if($_SERVER['SERVER_NAME']!=$_SERVER['SERVER_ADDR']) header('Location: http://'.$_SERVER['SERVER_ADDR']); ?>
<html>
	<head>
	<title>Manual Control</title>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<script src="js/jquery.js"></script>
	<script src="js/bootstrap.js"></script>
	<style type="text/css">
	
	.btn_min {
		width: 100px;
	}
	
	.secondary_color {
		color: #6c757d;
	}
	
	.secondary_color:hover {
		color: #5a6268;
	}
	
	.secondary_color:active {
		color: #545b62 !important;
	}
	
	.showcon {
		max-width: 640px;
		max-height: 480px;
		background: green;
		padding-bottom: 75%;
		width: 100%;
		margin: 0 auto;
	}
	
	</style>
	</head>
	<body>
		<div class="container h-100">
		  <div class="row h-100 justify-content-center align-items-center">
			<div class="col-12">
			  <div class="form-group text-center">
				<a href="manual.php"><button class="btn btn-primary btn_min">Manual</button></a>
				<a href="automatic.php"><button class="btn btn-primary btn_min">Automatic</button></a>
			  </div>
			</div>  
		  </div>
		  
		</div>
	</body>
</html>