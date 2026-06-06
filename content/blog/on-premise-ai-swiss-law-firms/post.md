---
title: Why on-premise AI is the only defensible choice for Swiss law firms
slug: on-premise-ai-swiss-law-firms
date: 2026-06-05
author: Granid
excerpt: Cloud AI asks Swiss lawyers to send privileged client data to servers they do not control. On-premise AI removes the question entirely.
lede: Every cloud AI tool a firm adopts reopens the same question under Art. 321 StGB: where did the client's data go, and who can reach it? On-premise AI answers it once, structurally, and never asks again.
og_image: /og_image_1200x630.png
hero: /assets/blog/on-premise-ai-swiss-law-firms/hero.svg
tags: Data sovereignty, On-premise AI
---

The fastest way to lose a privilege argument is to make it depend on a vendor's
promise. Cloud AI tools are built on exactly that: your client's documents leave
the building, land on infrastructure you do not own, and your defence becomes a
contract clause and a trust assertion. For a Swiss law firm bound by
**Art. 321 StGB** and the revised **nDSG**, that is a structural liability, not a
configuration detail.

## The problem is architectural, not contractual

Most "secure" cloud AI products address data privacy with encryption,
region pinning, and a data-processing agreement. None of that changes the core
fact: the data is processed somewhere you cannot see, by a system you cannot
inspect, on hardware you do not control. The competitor white papers in this
space concede the risk openly, then offer no architectural answer to it.

> If your compliance story depends on a third party honouring a contract, you
> do not have a compliance story. You have a counterparty.

On-premise inverts the model. The AI runs on a Mac the firm owns and keeps in
its own office. Documents are imported, understood, indexed, and queried without
a single byte reaching an outside service.

![On-premise data flow: client files and AI processing stay inside the office while the external cloud stays unreachable.](/assets/blog/on-premise-ai-swiss-law-firms/figure-architecture.svg "Client files and AI processing stay inside the firm. Nothing crosses to the cloud.")

## What this looks like in practice

A partner drops a matter's documents onto the device. The system reads them in
all four national languages, extracts deadlines and `Fristen`, and answers
cross-document questions with citations checked against the source text. A short
Legal Intelligence demo is shown below.

{% video src="/assets/blog/on-premise-ai-swiss-law-firms/demo.mp4" poster="/assets/blog/on-premise-ai-swiss-law-firms/demo-poster.png" caption="Legal Intelligence demo (preview)." %}

The difference a senior partner cares about is simple:

- **No data leaves the building.** Not for processing, not for analytics, not for telemetry.
- **Verified citations.** Every legal reference is checked against source material. No hallucinated law.
- **Human in the Loop.** The AI assists; the lawyer decides, with full visibility into every recommendation.

## The bottom line

Cloud AI asks you to accept a residual risk you cannot fully quantify and cannot
fully control. On-premise AI removes the risk at its source. For a profession
whose entire value rests on confidentiality, that is not a feature. It is the
only defensible default.

[See the recommended hardware](/hardware/production/) or
[start a two-week trial](/trial/) on a Mac you already own.
