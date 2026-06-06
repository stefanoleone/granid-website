---
title: Why 64 GB of unified memory is the floor for local legal AI
slug: unified-memory-floor
date: 2026-05-05
author: Granid
excerpt: Running a capable model, a document index, and macOS at once has a hard memory floor. Here is why we recommend 64 GB.
lede: The recommended specs for Granid are not arbitrary. They are the point below which a fully local legal AI stops being comfortable to use.
og_image: /og_image_1200x630.png
hero: /assets/blog/unified-memory-floor/hero.svg
tags: Hardware
---

On a paid tier, every part of Granid runs on your Mac: the AI model that reads
your documents, the searchable record of those documents, and the work of
reading them in. All of it shares Apple Silicon's unified memory.

## Where the memory goes

- The model that reads and reasons over Swiss legal text.
- Your firm's documents, kept ready in memory so answers come back instantly.
- macOS, your browser, and document reading running alongside.

> 64 GB is the floor that lets all of it run together without the system slowing down. More memory makes it faster; less makes every question noticeably slower.

## Mac Mini for most firms, Mac Studio for larger teams

A **Mac Mini** with 64 GB handles Essential and Professional comfortably. A
**Mac Studio** is the recommendation once more than four professionals share one
instance. In every case the hardware is yours. Granid is installed on a Mac you
own and keep in the office.

[See the full recommended specs](/hardware/production/).
