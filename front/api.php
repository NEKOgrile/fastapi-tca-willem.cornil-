<?php
header("Content-Type: application/json");

// Récupère l'endpoint depuis la query string
$endpoint = $_GET['endpoint'] ?? '';
$method = $_SERVER['REQUEST_METHOD'];

// Récupérer le token envoyé depuis le front
$headers = [];
$allHeaders = function_exists('getallheaders') ? getallheaders() : [];
if (!empty($allHeaders['Authorization'])) {
    $headers[] = "Authorization: " . $allHeaders['Authorization'];
}

// URL finale de l'API distante
$apiUrl = "http://frontvw.vicode.agency/" . $endpoint;

// Initialiser cURL
$ch = curl_init($apiUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

// Ajouter les headers
$contentType = $_SERVER["CONTENT_TYPE"] ?? "application/x-www-form-urlencoded";
$headers[] = "Content-Type: " . $contentType;
$headers[] = "Accept: application/json";
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

// Pour POST/PUT, envoyer le corps de la requête
if (in_array($method, ['POST', 'PUT'])) {
    $input = file_get_contents("php://input");
    curl_setopt($ch, CURLOPT_POSTFIELDS, $input);
}

// Exécuter la requête
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

// Gestion d'erreur cURL
if ($response === false) {
    $err = curl_error($ch);
    curl_close($ch);
    http_response_code(500);
    echo json_encode(["error" => "Erreur cURL: $err"]);
    exit;
}

curl_close($ch);

// Renvoie la réponse et le code HTTP
http_response_code($httpCode);
echo $response;
?>
