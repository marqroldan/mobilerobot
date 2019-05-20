<?php if($_SERVER['SERVER_NAME']!=$_SERVER['SERVER_ADDR']) header('Location: http://'.$_SERVER['SERVER_ADDR']);

$routes_file = "routes.txt";
$routes = array();
if(!file_exists($routes_file)) {
	$file = fopen($routes_file,'w+');
	fclose($file);
}

$file = file_get_contents($routes_file);
if(strlen($file)>0) $routes = json_decode($file, true);

$g_data_instructor = '';
$g_data_row = '';
$g_data_seat = '';

if($_POST) {
	if($_POST['data-row']!='' && $_POST['data-seat']!=="" && $_POST['data-instructor']!="") {
		if(@$_POST['modify']!='') { 
			unset($routes[ $_POST['modify']]);
		}
		
		$routes[] = array(
			'data-row' => $_POST['data-row'],
			'data-seat' => $_POST['data-seat'],
			'data-instructor' => $_POST['data-instructor'],
		);
		
		file_put_contents($routes_file, json_encode($routes));
	}
	else {
		echo "Failed to add entry.";
	}
}
else {
	if(@$_GET['del_id']!='') {
		unset($routes[$_GET['del_id']]);
		file_put_contents($routes_file, json_encode($routes));
	}
	elseif(@$_GET['mod_id']!='') {
		$g_data_instructor = $routes[$_GET['mod_id']]['data-instructor'];
		$g_data_row =  $routes[$_GET['mod_id']]['data-row'];
		$g_data_seat =  $routes[$_GET['mod_id']]['data-seat'];
	}
}

?>
<html>
	<head>
	<title>Modify Route</title>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="css/style.css">
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
		

		$(".submit_").click(function() {
			var obj = [];
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
			obj = obj.filter(function(el) {
				return el != null;
			});
			
		  $.ajax({
			type:'post',
			url:'automatic_post.php',
			data:{obj:obj},
			success:function(response) {
				console.log(response);
			  try {
				  ws.send("go_auto,xyx,"+response);
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
		});		

	});
	</script>
	</head>
	<body>
		<div class="wrapper wrapper2">
			<form action="modify.php" method="POST">
				<input type="hidden" name="modify" value="<?php echo ($g_data_row!='') ? @$_GET['mod_id'] : '' ?>" />
				Row: <input type="number" class="form-control" name="data-row" value="<?php echo $g_data_row ?>" required/>
				Seat: <input type="number" class="form-control" name="data-seat" value="<?php echo $g_data_seat ?>" required/>
				Instructor: <input type="text" class="form-control" name="data-instructor" value="<?php echo $g_data_instructor ?>" required/>
				<br/>
				<input type="submit" class="form-control btn btn-primary" value="Add"/>
			</form>
			
			<table class="table table-bordered">
				<thead>
					<tr>
						<td>Row</td>
						<td>Seat</td>
						<td>Instructor</td>
						<td>Action</td>
					</tr>
				</thead>
				<tbody>
					<?php foreach($routes as $route_id => $route): ?>
					<tr class="<?php echo $route_id ?>">
						<td><?php echo $route['data-row'] ?></td>
						<td><?php echo $route['data-seat'] ?></td>
						<td><?php echo $route['data-instructor'] ?></td>
						<td><a href="modify.php?del_id=<?php echo $route_id ?>"><button class="btn btn-danger delete">Delete</button></a><a href="modify.php?mod_id=<?php echo $route_id ?>"><button class="btn btn-primary modify">Modify</button></a></td>
					
					</tr>
					<?php endforeach ?>
				
				</tbody>
			</table>
		</div>
	</body>
</html>

