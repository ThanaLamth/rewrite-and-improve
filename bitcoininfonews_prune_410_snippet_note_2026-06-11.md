# BitcoinInfoNews prune 410 snippet

- Target slugs: 526
- Source file: `bitcoininfonews_action_delete_homepage_redirects_after_prune_2026-06-09.csv`
- Purpose: override Rank Math homepage redirects for deleted promo URLs and return `410 Gone` instead.

## Install

1. Paste the PHP file into the existing Code Snippets plugin or into the active theme `functions.php`.
2. Save and activate it.
3. Purge cache.
4. Re-test a few deleted promo URLs.

## Notes

- This snippet only targets the 526 problematic deleted promo URLs.
- It does not touch the separate WordPress redirect that currently points one deleted BlockDAG URL to its `-2/` winner.
- To switch from `410` to `404`, change `status_header(410);` to `status_header(404);` and update the fallback `wp_die` response.
