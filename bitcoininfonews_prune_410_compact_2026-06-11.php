<?php
add_action('init', function () {
    $path = trim((string) wp_parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH), '/');

    if ($path === '' || str_contains($path, '/')) {
        return;
    }

    if ($path === 'secure-95x-instant-roi-with-blockdag-s-limited-time-0-0000061-offer-xrp-eyes-enterprise-growth-and-shib-dips') {
        return;
    }

    $needles = [
        'blockdag',
        'bdag',
        'cold-wallet',
        'qubetics',
        'web3-ai',
        'unstaked',
        'btfd',
    ];

    $matched = false;
    foreach ($needles as $needle) {
        if (str_contains($path, $needle)) {
            $matched = true;
            break;
        }
    }

    if (!$matched) {
        return;
    }

    $public_types = get_post_types(['public' => true]);
    if (get_page_by_path($path, OBJECT, $public_types)) {
        return;
    }

    status_header(410);
    nocache_headers();
    wp_die('410 Gone', '410 Gone', ['response' => 410]);
}, -9999);
