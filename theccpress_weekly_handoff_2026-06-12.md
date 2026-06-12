# TheCCPress Weekly Handoff

Date: 2026-06-12
Scope: audit execution status, cleanup completed this week, and next-week plan

## Current Read

The main technical and editorial quality problems were real:

1. archive canonical and redirect signals were conflicting
2. many internal links still pointed to dead or redirected URLs
3. duplicate article clusters were splitting signals
4. tag sprawl was oversized
5. a large promo / presale article layer was diluting site quality
6. some trashed URLs were soft-404ing via homepage redirects emitted by Rank Math

The biggest cleanup gain this week was removing a large volume of promo / presale content from live publish status.

## Completed This Week

### 1. Archive Canonical / Redirect Conflict Cleanup

Status: completed at live-site settings level

What changed:

1. category-base behavior and archive canonical conflicts were reviewed and cleaned up
2. problematic archive redirect patterns were checked and several bad rules were disabled earlier in the workflow
3. preferred archive shape was kept consistent with the current WordPress setup

Primary evidence:

- [`/home/qcweb/rewrite-and-improve/theccpress_redirection_priority_batch_2026-06-09.csv`](/home/qcweb/rewrite-and-improve/theccpress_redirection_priority_batch_2026-06-09.csv)
- [`/home/qcweb/rewrite-and-improve/theccpress_redirection_remaining_batch_2026-06-09.csv`](/home/qcweb/rewrite-and-improve/theccpress_redirection_remaining_batch_2026-06-09.csv)

### 2. Duplicate Article Cluster Cleanup

Status: completed for the prepared redirect batch

What changed:

1. duplicate cluster mapping was built from crawl data
2. Rank Math import files were generated for duplicate-to-keeper redirects
3. the imported duplicate redirect batch was verified live earlier and was working after the CSV format fix

Underlying finding:

1. `42` duplicate title clusters among indexable `200` pages
2. `91` indexable URLs inside those clusters
3. `95` suffix-style URLs such as `-2`, `-3`, `-4`, `-5`

Primary evidence:

- [`/home/qcweb/rewrite-and-improve/theccpress_task7_duplicate_clusters_2026-06-11.md`](/home/qcweb/rewrite-and-improve/theccpress_task7_duplicate_clusters_2026-06-11.md)
- [`/home/qcweb/rewrite-and-improve/theccpress_duplicate_cluster_decision_sheet_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_duplicate_cluster_decision_sheet_2026-06-11.csv)
- [`/home/qcweb/rewrite-and-improve/theccpress_duplicate_301_rankmath_import_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_duplicate_301_rankmath_import_2026-06-11.csv)

### 3. Tag Taxonomy Cleanup

Status: completed for the current safe scope

What changed:

1. kept tag archives `noindex`
2. merged `6` obvious synonym pairs live
3. finalized a small editorial core tag set
4. stopped the need for further technical tag work right now beyond editorial discipline

Merged pairs:

1. `btc -> bitcoin`
2. `eth -> ethereum`
3. `ripple -> xrp`
4. `ripple-xrp -> xrp`
5. `crypto -> cryptocurrency`
6. `cryptocurrency-exchange -> crypto-exchange`

Verified keeper counts after merge:

1. `bitcoin = 117`
2. `ethereum = 71`
3. `xrp = 92`
4. `cryptocurrency = 307`
5. `crypto-exchange = 49`

Primary evidence:

- [`/home/qcweb/rewrite-and-improve/theccpress_task8_tag_archives_2026-06-11.md`](/home/qcweb/rewrite-and-improve/theccpress_task8_tag_archives_2026-06-11.md)
- [`/home/qcweb/rewrite-and-improve/theccpress_tag_merge_results_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_tag_merge_results_2026-06-11.csv)

### 4. Promo / Presale Content Prune

Status: major cleanup completed

Phase A:

1. an initial prune sheet of `50` URLs was created
2. those `50` URLs were removed from `publish`
3. result after that pass:
   `33` frontend `404`
   `17` frontend homepage redirects

Phase B:

1. a full live candidate scan was built from current published posts
2. `1140` live promo / presale candidates were identified
3. all `1140` were moved to WordPress `trash`
4. final REST result for the full batch:
   `1140` after `trash`
   `0` after `publish`
   `0` REST errors

Top entities removed in the large batch:

1. `blockdag = 459`
2. `qubetics = 108`
3. `unstaked = 87`
4. `cold wallet = 83`
5. `web3 ai = 79`
6. `btfd = 58`
7. `zkp = 48`

Primary evidence:

- [`/home/qcweb/rewrite-and-improve/theccpress_promo_prune_sheet_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_promo_prune_sheet_2026-06-11.csv)
- [`/home/qcweb/rewrite-and-improve/theccpress_promo_prune_delete_results_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_promo_prune_delete_results_2026-06-11.csv)
- [`/home/qcweb/rewrite-and-improve/theccpress_promo_presale_live_candidates_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_promo_presale_live_candidates_2026-06-11.csv)
- [`/home/qcweb/rewrite-and-improve/theccpress_promo_presale_live_delete_all_2026-06-12.csv`](/home/qcweb/rewrite-and-improve/theccpress_promo_presale_live_delete_all_2026-06-12.csv)
- [`/home/qcweb/rewrite-and-improve/theccpress_promo_presale_live_delete_all_summary_2026-06-12.md`](/home/qcweb/rewrite-and-improve/theccpress_promo_presale_live_delete_all_summary_2026-06-12.md)

### 5. Search Visibility Diagnosis

Status: diagnosis completed, not yet solved

What the GSC export showed:

1. query clicks in export: `37`
2. branded clicks: `37 / 37`
3. homepage clicks in page export: `64 / 65`
4. non-home organic visibility was extremely weak

Interpretation:

1. the site was not showing broad non-brand search reach in the supplied export
2. historical archive / legacy URL signals were still hanging around
3. durable educational and newsroom hubs need to be strengthened after cleanup

Primary evidence:

- [`/home/qcweb/rewrite-and-improve/theccpress_task6_search_visibility_2026-06-11.md`](/home/qcweb/rewrite-and-improve/theccpress_task6_search_visibility_2026-06-11.md)
- [`/home/qcweb/rewrite-and-improve/theccpress_durable_hubs_and_evergreen_shortlist_2026-06-11.md`](/home/qcweb/rewrite-and-improve/theccpress_durable_hubs_and_evergreen_shortlist_2026-06-11.md)

## Still Open

### 1. Soft-404 Homepage Redirect Problem

Status: confirmed, not fixed yet

The problem:

1. some trashed promo URLs still `301` to homepage
2. response header shows `X-Redirect-By: Rank Math`
3. that means the redirect is being emitted by Rank Math runtime, not by the exported Redirection plugin file

Why this matters:

1. deleted low-quality URLs should usually die as real `404`
2. homepage soft-404 behavior wastes crawl and muddies signals

Primary evidence:

- [`/home/qcweb/rewrite-and-improve/theccpress_soft404_rankmath_trace_checklist_2026-06-11.md`](/home/qcweb/rewrite-and-improve/theccpress_soft404_rankmath_trace_checklist_2026-06-11.md)

### 2. Internal Broken-Link Cleanup Is Not Finished

Status: partly addressed, still open at scale

Underlying finding from the audit:

1. `437` internal URLs returned `404`
2. `431` of those still had internal inlinks
3. many broken links were inside article body content, not only in menus

What has been done:

1. top broken URLs were identified
2. early redirect batches were prepared and imported

What is still needed:

1. export remaining high-inlink `404` targets
2. choose `301` or leave `404` case by case
3. update internal source links in body content for the highest-value broken targets

Primary evidence:

- [`/home/qcweb/rewrite-and-improve/theccpress_duplicate_internal_link_fix_summary_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_duplicate_internal_link_fix_summary_2026-06-11.csv)
- [`/home/qcweb/rewrite-and-improve/theccpress_duplicate_internal_link_fix_source_sheet_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_duplicate_internal_link_fix_source_sheet_2026-06-11.csv)

### 3. Crawl Efficiency / Bot Stability Still Needs Dev Review

Status: diagnosed, not fixed yet

Why it remains important:

1. prior crawl evidence showed many bad responses and unstable access
2. cleanup reduces crawl waste, but server-side bot handling still needs review
3. Cloudflare, LiteSpeed, WAF, and origin behavior still need to be checked against crawler sessions

## Recommended Plan For Next Week

### Priority 1: Fix Soft-404 Redirect Behavior For Trashed Posts

Owner: dev / WP admin

Goal:

1. trashed promo URLs should return normal `404`
2. they should not redirect to homepage

Actions:

1. inspect Rank Math redirect logic using the checklist doc
2. review Rank Math redirection, links, 404 monitor, and deleted-content behavior
3. check custom plugins or snippets if UI rules do not explain the redirect
4. re-test a sample set of trashed promo URLs after the fix

### Priority 2: Run Frontend Verification On The Large Prune Batch

Owner: audit / dev

Goal:

1. measure what the `1140` trashed URLs now do at frontend level
2. split them into:
   real `404`
   redirect to homepage
   redirect to other URL

Actions:

1. sample-check first
2. then bulk-verify the full deleted batch
3. export a follow-up status file

### Priority 3: Finish Internal Broken-Link Cleanup

Owner: audit + editor

Goal:

1. reduce internal equity waste to dead URLs

Actions:

1. sort remaining broken URLs by unique internal inlinks
2. decide `301` vs leave dead
3. update article-body links for top offenders first

### Priority 4: Rebuild Durable Non-Brand Landing Support

Owner: editor

Goal:

1. improve non-brand search reach after the quality cleanup

Actions:

1. build or strengthen a small set of evergreen landing pages
2. apply the internal linking plan from strong hubs
3. route authority from homepage, `latest-news`, `crypto-101`, and other stable hubs into those pages

Primary planning doc:

- [`/home/qcweb/rewrite-and-improve/theccpress_internal_link_plan_2026-06-11.md`](/home/qcweb/rewrite-and-improve/theccpress_internal_link_plan_2026-06-11.md)

### Priority 5: Dev-Side Crawl Stability Review

Owner: dev

Goal:

1. make sure bots can recrawl the cleaner site without unstable failures

Actions:

1. inspect Cloudflare / WAF / rate-limit settings
2. compare server logs for Googlebot and test crawlers
3. confirm no crawler-specific blocking or flaky origin behavior remains

## Practical Bottom Line

This week removed a large amount of low-value indexable clutter and cleaned several structural SEO problems.

The main thing not to miss next week is this:

1. make deleted URLs die cleanly as `404`
2. finish the remaining broken-link cleanup
3. shift effort from pruning into durable hub / evergreen growth
