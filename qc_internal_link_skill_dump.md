# QC Internal Link Skill Dump

Source skill path:
`/home/googleupdate/.codex/skills/qc-internal-link/SKILL.md`

Source reference path:
`/home/googleupdate/.codex/skills/qc-internal-link/references/internal-link-rules.md`

## SKILL.md

```md
---
name: qc-internal-link
description: Audit or plan internal linking using a traffic-first, authority-allocation model. Use when the user asks about internal links, link noi bo, topical authority, which pages should link to which pages, or how to improve rankings by linking strong pages to pages ranking around positions 5-10.
---

# QC Internal Link

Use this skill when the task is about:

- auditing an internal linking setup
- deciding which pages should link to which pages
- improving rankings through internal links
- evaluating topical authority and link flow
- reviewing whether a site is wasting internal links

## Core Model

Treat each internal link as an authority allocation decision, not decorative SEO.

Default assumptions:

- more internal links is not automatically better
- weak pages usually have little to pass on
- pages with traffic, rankings, and crawl attention are the main link sources
- the best targets are often pages already ranking around positions `5-10`
- internal linking is iterative and should be updated as rankings change

## Workflow

1. Identify candidate source pages.
Source pages should already have traffic, rankings, and user engagement.

2. Identify candidate target pages.
Prioritize pages close to top positions rather than pages with very low ranking potential.

3. Check whether each target can realistically rank.
Do not recommend pushing impossible head terms for a weak site unless there is clear evidence.

4. Minimize wasted dilution.
If a page links out to too many internal targets, call out authority dilution and suggest prioritization.

5. Evaluate topic fit.
Internal links should strengthen clusters and topical authority, not create random cross-topic jumps.

6. Recommend a dynamic loop.
Once a target page improves and becomes strong, use it as a new source page for the next layer.

## Output

Return:

- verdict: strong / mixed / weak internal linking
- strongest source pages
- best near-win target pages
- wasted links or diluted sections
- topical cluster opportunities
- next linking actions in priority order

## Read This Reference

Read [references/internal-link-rules.md](references/internal-link-rules.md) when you need the detailed operating rules, cautions, and the preferred GSC-driven workflow.
```

## references/internal-link-rules.md

```md
# Internal Link Rules

## Thesis

Internal linking is not free authority. It is a controlled reallocation of existing strength inside the site.

If a page has no traffic, no rankings, and little crawl attention, its internal links usually carry limited SEO value.

## Common Mistake

Many SEOs treat internal links like this:

- publish many blog posts
- point all of them to money pages
- assume every new link adds useful power

This often fails because Google does not value all pages equally. A page that is weak, ignored, or barely crawled is not a meaningful source page.

## Correct Mental Model

Treat each internal link like an investment.

When you add a link, ask:

- does the source page actually have traffic or rankings?
- does Google likely crawl this page often?
- is the target page close enough to benefit from extra authority?
- am I diluting the source page by linking to too many destinations?

## What Google Likely Cares About In Practice

- stronger pages get crawled more often
- pages with traffic and rankings are better link sources
- random links from weak pages are often low-value
- cluster clarity helps Google understand topical authority

Do not assume sitemap coverage means Google meaningfully processes every weak page in the same way.

## Preferred Workflow

### Step 1: Find target pages in Google Search Console

Start with pages ranking around positions `5-10`.

These are often the best internal-link targets because they may only need a modest authority boost to move into top results.

### Step 2: Find strong source pages

Look for pages with:

- stable traffic
- strong rankings
- good crawl attention
- clear topical relevance

Best sources are usually pages already ranking `top 1-3` or pages that consistently attract demand.

### Step 3: Link strong pages to near-win targets

Prioritize:

- strong page -> related page near top
- topically close connections
- limited, intentional links instead of spraying links everywhere

### Step 4: Repeat the loop

Once a target page becomes strong:

- treat it as a new source page
- use it to support the next set of pages

This creates a compounding internal-link growth loop.

## What Not To Do

### Do not over-link

A page with too many internal links spreads attention and authority too thin.

### Do not push impossible targets

If the site is small, do not keep feeding internal links into very difficult head terms with little chance to rank.

### Do not set and forget

Internal linking is not static. Rankings shift. New pages become strong. Old pages lose value. The internal-link map should be reviewed continuously.

### Do not ignore topical fit

Internal links should reinforce subject clusters. Random links weaken semantic clarity.

## Topical Authority Angle

Internal linking helps Google understand that the site covers a topic in depth.

It works best when:

- related pages support each other
- cluster structure is clear
- strong pages transfer relevance to adjacent pages
- the site expands by topic, not by random content accumulation

This matters especially in competitive topics such as finance, real estate, services, and other authority-sensitive verticals.

## Review Checklist

Use this checklist during audits:

- Which pages currently have meaningful traffic?
- Which pages rank in positions `5-10`?
- Which pages are being asked to rank for terms that are too difficult?
- Which source pages link to too many internal targets?
- Which clusters are missing clear hub-to-child or child-to-child support?
- Which pages have become strong enough to start supporting others?

## Recommended Conclusion Style

End with practical actions:

1. Keep only the most strategic internal links from strong pages.
2. Redirect link support toward pages already close to top positions.
3. Remove or de-prioritize links to unrealistic targets.
4. Rebuild internal linking by topical cluster.
5. Re-check the system after rankings shift.
```
