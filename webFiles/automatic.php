<?php if($_SERVER['SERVER_NAME']!=$_SERVER['SERVER_ADDR']) header('Location: http://'.$_SERVER['SERVER_ADDR']);

$routes_file = "routes.txt";
$routes = array();
//Get Routes file
if(file_exists($routes_file)) {
$file = file_get_contents($routes_file);
if(strlen($file)>0) $routes = json_decode($file, true);
}
else {
	echo "Important! Routes file does not exists.";
}


?>
<html>
	<head>
	<title>Automatic Control</title>
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
		padding-bottom: 75%;
		width: 100%;
		height: 100%;
		margin: 0 auto;
	}
	
	</style>
	<script>
	$(document).ready(function(){

    var WEBSOCKET_ROUTE = ":3500/ws";
		var ip = '<?php echo $_SERVER['SERVER_ADDR'] ?>';

        if(window.location.protocol == "http:"){
            //localhost
            var ws = new WebSocket("ws://" + ip + WEBSOCKET_ROUTE);
            }
        else if(window.location.protocol == "https:"){
            //Dataplicity
            var ws = new WebSocket("wss://" + ip + WEBSOCKET_ROUTE);
            }
				
        ws.onopen = function(evt) {
            $("#ws-status").html(evt.data);
            ws.send(-1);
            };

        ws.onmessage = function(evt) {
            $("#ws-status").html(evt.data);
            };

        ws.onclose = function(evt) {
            $("#ws-status").html("Disconnected");
            };
		

		$(".submit_").click(function(e) {
			e.preventDefault();
			var obj = [];
			/*
			$('input[type=checkbox]:checked').each(function() {
				var drow = parseInt($(this).attr("data-row"));
				var dseat = parseInt($(this).attr("data-seat"));
				var dname = $(this).attr("data-instructor");
				if(!(drow in obj)) {
					var tmp = [];
					tmp[dseat] = dname;
					obj[drow] = tmp;
				}
				else {
					var tmp = [];
					tmp[dseat] = dname;
					obj[drow][dseat] = dname;
				}
			});
			console.log(obj);
			obj = obj.filter(function(el) {
				return el != null;
			});
			*/
			//console.log($("#for1").serialize());
			var g = $(".instructor_list input[type='checkbox']").filter(":checked").length;
			if (g > 0) {
				  $.ajax({
					type:'post',
					url:'automatic_post.php',
					data:{obj:$("#for1").serialize()},
					success:function(response) {
						console.log(response);
					  try {
						// ws.send("go_auto,xyx,"+response);
					  }
					  catch(err) {
						console.log(err);
						alert("Something bad has happened.");
					  }
					},
					error:function(response) {
						console.log(response);
					}
				  });
			}
		});	


		$(".stop_").click(function() {
			 ws.send("stop_auto,xyx,");
		});		
		$(".pause_").click(function() {
			 ws.send("pause_auto,xyx,");
		});		
		$(".play_").click(function() {
			 ws.send("play_auto,xyx,");
		});			
	});
	</script>
	</head>
	<body>
		<div class="container-fluid container h-100">
			<div class="row h-100 justify-content-center align-items-center">
				<div class="col-md-8 d-flex flex-column align-items-center justify-content-center">
					<div style="max-height: 480px; max-width: 640px; margin: 0 auto;">
					<img src='http://<?php echo $_SERVER['SERVER_ADDR'] ?>:8081' width="100%"/>
					</div>
				<div id="ws-status">Connecting...</div>
				</div>
				<div class="col-md-4 d-flex flex-column ">
					<form id="for1" name="sub1">
					<div class="instructor_list">
						<?php foreach($routes as $route): ?>
						<label><input type="checkbox" name="<?php echo $route['data-row']."_".$route['data-seat']."_".$route['data-instructor'] ?>" data-row="<?php echo $route['data-row'] ?>" data-seat="<?php echo $route['data-seat'] ?>" data-instructor="<?php echo $route['data-instructor'] ?>" /><?php echo $route['data-instructor']." [".$route['data-row']."] [".$route['data-seat']."]" ?></label><br/>
						<?php endforeach ?>
					</div>
					</form>
					<button class="btn btn-primary submit_">Submit</button>
					<br>
					<button class="btn btn-primary stop_">Stop</button>
					<br>
					<button class="btn btn-primary pause_">Pause</button>
					<br>
					<button class="btn btn-primary play_">Play</button>
					<br>
					<a href="modify.php" style="color: white; width: 100%;"><button class=" form-control btn btn-primary">Modify Routes</button></a>
				</div>
			</div>
		</div>
	</body>
</html>

