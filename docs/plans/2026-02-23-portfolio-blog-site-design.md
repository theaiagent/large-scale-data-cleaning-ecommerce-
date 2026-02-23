# Portfolio & Blog Site Design

**Date:** 2026-02-23
**Domain:** theaiagent.github.io
**Tech:** Pure HTML/CSS/JS (zero dependencies, zero build step)
**Language:** English

---

## Purpose

Dual-purpose site:
1. **Upwork portfolio** — showcase projects, case studies, results to clients
2. **Educational content** — blog posts on data science, Python, pipelines for students

## Architecture

```
theaiagent.github.io/
├── index.html              # Home (hero + featured projects + skills)
├── projects.html           # Portfolio grid
├── blog.html               # Blog index (post cards)
├── about.html              # Bio + what I do + tech stack
├── contact.html            # Direct links (email, GitHub, LinkedIn, Upwork)
├── posts/
│   └── 2026-02-23-ecommerce-data-cleaning.html  # First blog post
├── assets/
│   ├── css/style.css       # Single global stylesheet
│   ├── img/                # Screenshots, avatar, project images
│   └── js/main.js          # Mobile nav toggle, minimal interactions
└── README.md
```

No CNAME file (using theaiagent.github.io directly).

## Design System

**Style:** Modern gradient
- Gradient headings and accent elements
- Card-based layouts with subtle shadows
- Vibrant color palette (blues/purples/teals)
- Responsive (mobile-first)
- Sans-serif body font, clean whitespace

## Pages

### 1. Home (index.html)

- **Hero:** "Hi, I'm Aykut" + "Data Scientist & Python Developer"
  - Gradient text on title
  - 1-2 sentence tagline
  - CTA buttons: [View Projects] [Read Blog]
- **Featured Projects:** 2-3 cards with image, title, description, tech tags, link
  - demo_1 as first card: "125K Rows | 8 Issues | Automated"
- **Skills bar:** Python, Pandas, SQL, NumPy, Tableau, PySpark, Airflow, Scikit-learn
- **Footer:** GitHub | LinkedIn | Email

### 2. Projects (projects.html)

- Large cards, one per project
- Each card: category tag, title, metrics, screenshot, tech tags, links ([GitHub] [Case Study])
- demo_1: full card with cleaning_summary.png screenshot
- "Coming Soon" placeholder cards for future projects

### 3. Blog (blog.html + posts/)

- Blog index: list of post cards
  - Each card: date, title, tags, reading time, [Read ->]
- Individual posts: `posts/YYYY-MM-DD-slug.html`
  - Shared layout (nav + footer from template)
  - Code snippets with syntax highlighting (inline CSS, no lib)
  - Screenshots as visuals

**First post:** "Cleaning 125K Rows of Messy E-commerce Data"
- Derived from demo_1 case study
- ~800-1000 words
- Problem -> approach -> results structure
- Key code snippets (2-3 blocks)
- Screenshots from existing screenshots/ folder

### 4. About (about.html)

- **Avatar area** (placeholder circle or real photo)
- **Bio:** 3-4 sentences (placeholder text, user fills in)
- **What I Do:** 3x2 grid of cards:
  1. Data Cleaning
  2. Analysis & Visualization
  3. Predictive Modelling
  4. Statistical Analysis
  5. Pipeline Building
  6. Workflow Automation
- **Tech Stack:** gradient progress bars with skill levels
  - Advanced: Python, Pandas, NumPy
  - Proficient: SQL, Tableau
  - Intermediate: PySpark, Airflow

### 5. Contact (contact.html)

- Tagline: "Have a messy dataset or a data project? Let's talk."
- Direct links (no form):
  - Email
  - LinkedIn
  - GitHub (theaiagent)
  - Upwork profile
- Icon + label for each link

## Shared Components

- **Nav:** sticky top bar, logo/name left, links right, mobile hamburger toggle
- **Footer:** compact, links + copyright
- **style.css:** single file, CSS custom properties for colors, responsive breakpoints

## Deployment

1. Create `theaiagent.github.io` repo on GitHub
2. Push all files to `main` branch
3. GitHub Pages auto-deploys from main
4. Remove existing CNAME redirect to aykutcosgun.me

## Content Plan

| Post # | Topic | Source |
|--------|-------|--------|
| 1 | Cleaning 125K Rows of E-commerce Data | demo_1 case study |
| 2+ | Future posts as new projects are built | — |
