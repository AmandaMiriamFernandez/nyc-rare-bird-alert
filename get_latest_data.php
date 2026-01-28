<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Find the most recent JSON file
$files = glob('ny_rare_birds_*.json');
if (empty($files)) {
    http_response_code(404);
    echo json_encode(['error' => 'No data files found']);
    exit;
}

// Sort by modification time, most recent first
usort($files, function($a, $b) {
    return filemtime($b) - filemtime($a);
});

$latestFile = $files[0];
$data = file_get_contents($latestFile);
echo $data;
?>
