<?php

if($_POST) {
	print_r($_POST);
	$items = explode("&",$_POST['obj']);
	
	if(count($items) > 0){
		$data = array();
		$count = 0;
		foreach($items as $item){
			$e = explode('_',$item);
			$drow = $e[0];
			$dseat = $e[1];
			$dname = $e[2];
			$data[$drow][$dseat] = str_replace('=on','',urldecode($dname));		
			$count++;
		}
	}
	else {
		echo "WARNING: NO ROUTE DETECTED"
	}
	
	/*
	print_r($data);
	
	$arr = array();
	foreach($_POST['obj'] as $key => $obj) {
		if(!is_array($obj)) {
			$obj = array($obj);
		}
		foreach(array_filter($obj) as $key2 => $data) {
			if(!empty($data)) {
				$count++;
			$arr[$key+1][$key2] = $data;
			}
		}
	}*/
	$str = addslashes(json_encode(array_filter($data),JSON_UNESCAPED_SLASHES));
	$str = json_encode(array_filter($data));
	
	//echo shell_exec("sudo bython /home/pi/t21.py '".$str."' ".$count." 2>&1");
	echo "'".$str."' ".$count."";
}
