<?php 
if($_REQUEST['type'] == "recibir"){
		$body = '{
		  
		}';
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, "https://api.telegram.org/bot233165205:AAESTFmQfhUQv8xs-yez2HqFzJxHyIAwQ_g/getUpdates");
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: application/json","Authorization: OAuth 2.0 token here"));
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
		$result = curl_exec($ch);

		$k = json_decode($result);

		$k1 = (array)$k;
		$last = (array)$k1["result"][strval(count($k1["result"])-1)];
		$ide = (array)$last["update_id"];
		$dump = strval($ide["0"] -1);
		$body = '{
					"offset": '.$dump.'
		}';
		curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
		$result = curl_exec($ch);

		$k = json_decode($result);
		$k1 = (array)$k;
		$last = (array)$k1["result"][strval(count($k1["result"])-1)];
		
		//var_dump($last);
		
		$last = (array)$last["message"];
		$from = (array)$last["from"];
		$from = (array)$from["first_name"];
		$res = isset($last["text"]) ? $last["text"] : "Not text" ;
		$id_data = (array)$last["from"];
		$id = $id_data["id"];
		echo '{ "message":"'.$res.'",
				"id":"'.$id.'",
				"name":"'.$from["0"].'"
		}';
}else if(!empty($_REQUEST["message"])){
		
		$body = '{
				"chat_id":'.$_REQUEST["id"].',
				"text":"'.$_REQUEST["message"].'"
		}';
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, "https://api.telegram.org/bot233165205:AAESTFmQfhUQv8xs-yez2HqFzJxHyIAwQ_g/sendMessage");
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: application/json","Authorization: OAuth 2.0 token here"));
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
		$result = curl_exec($ch);
		echo($result);


}
?>