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


			$('button[robo_type=movement]').on('click',function() {
				ws.send($(this).attr('id'));
			});
		
	});
	</script>
	</head>
	<body>
		<div class="container h-100">
		  <div class="row h-100 justify-content-center align-items-center">
			<div class="col-12">
			  <div class="form-group text-center">
					<a href="index.php">Back to options</a>
			  </div>
			  <div class="form-group text-center">
				<div style="max-height: 480px; max-width: 640px; margin: 0 auto;">
				<img src='http://<?php echo $_SERVER['SERVER_ADDR'] ?>:8081' width="100%"/>
				</div>
			  </div>
			  <div class="form-group text-center">
				<button class="btn btn-secondary btn_min secondary_color">TL</button>
				<button robo_type="movement" class="btn btn-primary btn_min" id="go_forward">Forward</button>
				<button class="btn btn-secondary btn_min secondary_color">TR</button>
				<div style="display: block; height: 1px;"></div>
				<button robo_type="movement"  class="btn btn-primary btn_min" id="go_left">Left</button>
				<button robo_type="movement"  class="btn btn-primary btn_min" id="go_stop">Stop</button>
				<button robo_type="movement"  class="btn btn-primary btn_min" id="go_right">Right</button>
				<div style="display: block; height: 1px;"></div>
				<button class="btn btn-secondary btn_min secondary_color">TL</button>
				<button robo_type="movement"  class="btn btn-primary btn_min" id="go_reverse">Reverse</button>
				<button class="btn btn-secondary btn_min secondary_color">TR</button>
			  </div>

				
				<button robo_type="movement"  class="btn btn-primary btn_min" id="go_auto">Reverse</button>

			  <div class="form-group text-center">
				<div id="ws-status">Connecting...</div>
			  </div>
			  
			</div>  
		  </div>
		  
		</div>
	</body>
</html>

