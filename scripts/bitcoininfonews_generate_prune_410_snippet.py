from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path("/home/qcweb/rewrite-and-improve")
INPUT_PATH = ROOT / "bitcoininfonews_action_delete_homepage_redirects_after_prune_2026-06-09.csv"
OUTPUT_PATH = ROOT / "bitcoininfonews_prune_410_snippet_2026-06-11.php"
NOTE_PATH = ROOT / "bitcoininfonews_prune_410_snippet_note_2026-06-11.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def php_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def main() -> None:
    rows = read_rows(INPUT_PATH)
    slugs = sorted({row["slug"] for row in rows if row.get("slug")})

    php_lines: list[str] = []
    php_lines.append("<?php")
    php_lines.append("/**")
    php_lines.append(" * BitcoinInfoNews prune override snippet.")
    php_lines.append(" *")
    php_lines.append(" * Returns 410 Gone for deleted promo URLs before Rank Math can")
    php_lines.append(" * redirect them to the homepage.")
    php_lines.append(" */")
    php_lines.append("")
    php_lines.append("if (!defined('ABSPATH')) {")
    php_lines.append("    exit;")
    php_lines.append("}")
    php_lines.append("")
    php_lines.append("function bitcoininfonews_prune_410_slug_map(): array")
    php_lines.append("{")
    php_lines.append("    static $slug_map = null;")
    php_lines.append("")
    php_lines.append("    if ($slug_map !== null) {")
    php_lines.append("        return $slug_map;")
    php_lines.append("    }")
    php_lines.append("")
    php_lines.append("    $slug_map = [")
    for slug in slugs:
        php_lines.append(f"        '{php_quote(slug)}' => true,")
    php_lines.append("    ];")
    php_lines.append("")
    php_lines.append("    return $slug_map;")
    php_lines.append("}")
    php_lines.append("")
    php_lines.append("function bitcoininfonews_prune_410_current_slug(): string")
    php_lines.append("{")
    php_lines.append("    $request_uri = $_SERVER['REQUEST_URI'] ?? '';")
    php_lines.append("    $path = (string) wp_parse_url($request_uri, PHP_URL_PATH);")
    php_lines.append("    $path = trim(rawurldecode($path), '/');")
    php_lines.append("")
    php_lines.append("    return $path;")
    php_lines.append("}")
    php_lines.append("")
    php_lines.append("function bitcoininfonews_prune_410_matches_request(): bool")
    php_lines.append("{")
    php_lines.append("    $slug = bitcoininfonews_prune_410_current_slug();")
    php_lines.append("")
    php_lines.append("    if ($slug === '') {")
    php_lines.append("        return false;")
    php_lines.append("    }")
    php_lines.append("")
    php_lines.append("    return isset(bitcoininfonews_prune_410_slug_map()[$slug]);")
    php_lines.append("}")
    php_lines.append("")
    php_lines.append("add_filter('redirect_canonical', function ($redirect_url, $requested_url) {")
    php_lines.append("    if (bitcoininfonews_prune_410_matches_request()) {")
    php_lines.append("        return false;")
    php_lines.append("    }")
    php_lines.append("")
    php_lines.append("    return $redirect_url;")
    php_lines.append("}, -9999, 2);")
    php_lines.append("")
    php_lines.append("add_action('template_redirect', function () {")
    php_lines.append("    if (!bitcoininfonews_prune_410_matches_request()) {")
    php_lines.append("        return;")
    php_lines.append("    }")
    php_lines.append("")
    php_lines.append("    status_header(410);")
    php_lines.append("    nocache_headers();")
    php_lines.append("")
    php_lines.append("    global $wp_query;")
    php_lines.append("    if ($wp_query instanceof WP_Query) {")
    php_lines.append("        $wp_query->set_404();")
    php_lines.append("    }")
    php_lines.append("")
    php_lines.append("    $template = get_404_template();")
    php_lines.append("    if ($template) {")
    php_lines.append("        include $template;")
    php_lines.append("    } else {")
    php_lines.append("        wp_die('410 Gone', '410 Gone', ['response' => 410]);")
    php_lines.append("    }")
    php_lines.append("")
    php_lines.append("    exit;")
    php_lines.append("}, -9999);")
    php_lines.append("")

    OUTPUT_PATH.write_text("\n".join(php_lines) + "\n", encoding="utf-8")

    note_lines = [
        "# BitcoinInfoNews prune 410 snippet",
        "",
        f"- Target slugs: {len(slugs)}",
        "- Source file: `bitcoininfonews_action_delete_homepage_redirects_after_prune_2026-06-09.csv`",
        "- Purpose: override Rank Math homepage redirects for deleted promo URLs and return `410 Gone` instead.",
        "",
        "## Install",
        "",
        "1. Paste the PHP file into the existing Code Snippets plugin or into the active theme `functions.php`.",
        "2. Save and activate it.",
        "3. Purge cache.",
        "4. Re-test a few deleted promo URLs.",
        "",
        "## Notes",
        "",
        "- This snippet only targets the 526 problematic deleted promo URLs.",
        "- It does not touch the separate WordPress redirect that currently points one deleted BlockDAG URL to its `-2/` winner.",
        "- To switch from `410` to `404`, change `status_header(410);` to `status_header(404);` and update the fallback `wp_die` response.",
        "",
    ]
    NOTE_PATH.write_text("\n".join(note_lines), encoding="utf-8")

    print(OUTPUT_PATH)
    print(NOTE_PATH)
    print(len(slugs))


if __name__ == "__main__":
    main()
