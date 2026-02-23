# Portfolio & Blog Site Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a 5-page portfolio + blog site at theaiagent.github.io with modern gradient design.

**Architecture:** Pure HTML/CSS/JS, zero dependencies. Single `style.css` for all pages. Each page shares nav + footer markup. Blog posts live in `posts/` as standalone HTML files. Deployed via GitHub Pages from `main` branch.

**Tech Stack:** HTML5, CSS3 (custom properties, flexbox, grid), vanilla JS (mobile nav toggle only)

**Design reference:** `docs/plans/2026-02-23-portfolio-blog-site-design.md`

---

### Task 1: Project Setup & Global CSS

**Goal:** Create repo structure and the complete design system in `style.css`.

**Files:**
- Create: `D:/Projects/theaiagent.github.io/assets/css/style.css`
- Create: `D:/Projects/theaiagent.github.io/assets/js/main.js`

**Step 1: Create directory structure**

```bash
mkdir -p D:/Projects/theaiagent.github.io/assets/css
mkdir -p D:/Projects/theaiagent.github.io/assets/js
mkdir -p D:/Projects/theaiagent.github.io/assets/img
mkdir -p D:/Projects/theaiagent.github.io/posts
cd D:/Projects/theaiagent.github.io
git init
```

**Step 2: Write `assets/css/style.css`**

Complete CSS design system:
- CSS custom properties: `--gradient-start: #667eea`, `--gradient-end: #764ba2`, accent colors, font stack
- Reset + base styles (box-sizing, body font, line-height)
- `.nav` — sticky top bar, flexbox, logo left, links right
- `.nav-toggle` — hamburger button, hidden on desktop, shown on mobile
- `.hero` — centered text, gradient heading via `background-clip: text`
- `.card` — white bg, border-radius 12px, box-shadow, hover lift transition
- `.card-grid` — CSS grid, `repeat(auto-fit, minmax(320px, 1fr))`, gap 24px
- `.tag` — small pill-shaped labels for tech stack
- `.btn` — gradient background, white text, border-radius, hover scale
- `.btn-outline` — transparent bg, gradient border
- `.section` — max-width 1100px, margin auto, padding 80px 24px
- `.gradient-text` — `background: linear-gradient(...)`, `-webkit-background-clip: text`
- `.progress-bar` — gradient fill bar for skill levels
- `.footer` — dark bg, centered links
- `code`, `pre` — monospace font, dark bg, rounded, padding
- Media queries: tablet (768px), mobile (480px) — stack nav, single-column grid
- Mobile nav: `.nav-links.active` slide-in

**Step 3: Write `assets/js/main.js`**

Minimal JS:
- Mobile hamburger toggle: querySelector `.nav-toggle`, toggle `.active` on `.nav-links`
- Active page highlight: compare `window.location.pathname` to nav link hrefs, add `.active` class

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: project setup with global CSS design system and nav JS"
```

---

### Task 2: Home Page (index.html)

**Goal:** Hero section + featured projects + skills bar + footer.

**Files:**
- Create: `D:/Projects/theaiagent.github.io/index.html`

**Step 1: Write `index.html`**

Structure:
```
<nav> — logo "AC", links: Home, Projects, Blog, About, Contact, hamburger button
<section class="hero">
  <h1 class="gradient-text">Hi, I'm Aykut</h1>
  <p class="hero-subtitle">Data Scientist & Python Developer</p>
  <p>I clean messy data, build pipelines, and turn raw exports into insights.</p>
  <div> [View Projects btn] [Read Blog btn-outline] </div>
</section>
<section "Featured Projects">
  <h2>Featured Projects</h2>
  <div class="card-grid">
    Card 1: E-commerce Data Cleaning
      - img: assets/img/cleaning_summary.png
      - title, "125K Rows | 8 Issues | Automated"
      - tags: Python, Pandas, NumPy
      - link: projects.html
    Card 2: "Coming Soon" placeholder (subtle dashed border, muted text)
    Card 3: "Coming Soon" placeholder
  </div>
</section>
<section "Skills">
  <h2>Tech Stack</h2>
  <div class="tag-cloud">
    Tags: Python, Pandas, NumPy, SQL, Tableau, PySpark, Airflow, Scikit-learn, Jupyter, Git
  </div>
</section>
<footer> GitHub | LinkedIn | Email | © 2026 </footer>
```

**Step 2: Copy project screenshot**

```bash
cp D:/Projects/upwork_demo/demo_1/screenshots/cleaning_summary.png D:/Projects/theaiagent.github.io/assets/img/
```

**Step 3: Open in browser, verify layout**

Verify: nav, hero gradient text, project cards, skills tags, footer links, mobile responsiveness.

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: add home page with hero, featured projects, and skills"
```

---

### Task 3: Projects Page (projects.html)

**Goal:** Full project showcase with large cards.

**Files:**
- Create: `D:/Projects/theaiagent.github.io/projects.html`

**Step 1: Write `projects.html`**

Structure:
```
<nav> (same as index.html)
<section>
  <h1 class="gradient-text">Projects</h1>
  <div class="project-card-large">
    Category tag: "Data Cleaning"
    Title: "Large-Scale E-commerce Data Cleaning & Standardization"
    Metrics row: "125,000 Rows" | "8 Issues Fixed" | "5,000 Duplicates Removed"
    Screenshot: assets/img/cleaning_summary.png
    Description: 2-3 sentences about the project
    Tech tags: Python, Pandas, NumPy
    Buttons: [GitHub →] [Case Study PDF →]
      - GitHub: https://github.com/theaiagent/large-scale-data-cleaning-ecommerce-
      - PDF: link to case study (or hosted HTML)
  </div>

  <div class="project-card-large coming-soon">
    Dashed border, muted
    "More projects coming soon..."
  </div>
</section>
<footer>
```

**Step 2: Copy additional screenshots**

```bash
cp D:/Projects/upwork_demo/demo_1/screenshots/before_raw_data.png D:/Projects/theaiagent.github.io/assets/img/
cp D:/Projects/upwork_demo/demo_1/screenshots/after_cleaned_data.png D:/Projects/theaiagent.github.io/assets/img/
cp D:/Projects/upwork_demo/demo_1/screenshots/schema_comparison.png D:/Projects/theaiagent.github.io/assets/img/
```

**Step 3: Verify in browser**

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: add projects page with e-commerce demo card"
```

---

### Task 4: About Page (about.html)

**Goal:** Bio, 6 expertise cards (3x2), tech stack progress bars.

**Files:**
- Create: `D:/Projects/theaiagent.github.io/about.html`

**Step 1: Write `about.html`**

Structure:
```
<nav>
<section "About Me">
  <div class="about-header">
    <div class="avatar-placeholder"> initials "AC" on gradient circle </div>
    <div>
      <h1 class="gradient-text">Aykut Cosgun</h1>
      <p class="hero-subtitle">Data Scientist</p>
      <p>Bio placeholder — 3-4 sentences. [USER FILLS IN]</p>
    </div>
  </div>
</section>

<section "What I Do">
  <h2>What I Do</h2>
  <div class="card-grid" style 3x2>
    1. Data Cleaning — icon/emoji, short description
    2. Analysis & Visualization
    3. Predictive Modelling
    4. Statistical Analysis
    5. Pipeline Building
    6. Workflow Automation
  </div>
</section>

<section "Tech Stack">
  <h2>Tech Stack</h2>
  <div class="skills-list">
    Python      ████████████ 95%
    Pandas      ████████████ 90%
    NumPy       ████████████ 90%
    SQL         ██████████░░ 80%
    Tableau     █████████░░░ 75%
    PySpark     ████████░░░░ 65%
    Airflow     ████████░░░░ 65%
    Scikit-learn ██████████░░ 80%
  </div>
  Each bar: label left, gradient-fill bar, percentage right
</section>
<footer>
```

**Step 2: Verify in browser** — check 3x2 grid, progress bars, avatar, mobile layout

**Step 3: Commit**

```bash
git add -A
git commit -m "feat: add about page with expertise grid and tech stack"
```

---

### Task 5: Contact Page (contact.html)

**Goal:** Simple contact links page.

**Files:**
- Create: `D:/Projects/theaiagent.github.io/contact.html`

**Step 1: Write `contact.html`**

Structure:
```
<nav>
<section class="hero" style="centered">
  <h1 class="gradient-text">Get in Touch</h1>
  <p>"Have a messy dataset or a data project? Let's talk."</p>

  <div class="contact-links">
    Card/row 1: 📧 Email → mailto:h.aykut.cosgun@bozok.edu.tr
    Card/row 2: 🐙 GitHub → https://github.com/theaiagent
    Card/row 3: 💼 LinkedIn → [placeholder URL]
    Card/row 4: 🔗 Upwork → [placeholder URL]
  </div>

  Each link: icon + label + URL, hover gradient underline
</section>
<footer>
```

**Step 2: Verify in browser**

**Step 3: Commit**

```bash
git add -A
git commit -m "feat: add contact page with direct links"
```

---

### Task 6: Blog Index + First Post

**Goal:** Blog listing page and first blog post derived from demo_1 case study.

**Files:**
- Create: `D:/Projects/theaiagent.github.io/blog.html`
- Create: `D:/Projects/theaiagent.github.io/posts/2026-02-23-ecommerce-data-cleaning.html`

**Step 1: Write `blog.html`**

Structure:
```
<nav>
<section>
  <h1 class="gradient-text">Blog</h1>
  <p class="hero-subtitle">Notes on data science, Python, and lessons from real-world projects.</p>

  <div class="blog-list">
    <article class="blog-card">
      <span class="blog-date">February 23, 2026</span>
      <h2><a href="posts/2026-02-23-ecommerce-data-cleaning.html">
        Cleaning 125K Rows of Messy E-commerce Data
      </a></h2>
      <div class="tags"> Data Cleaning • Python • Pandas </div>
      <p>A walkthrough of how I built an automated pipeline to fix 8 different
         data quality issues in a large Shopify export...</p>
      <span class="read-time">8 min read</span>
      <a href="..." class="read-more">Read →</a>
    </article>
  </div>
</section>
<footer>
```

**Step 2: Write first blog post**

File: `posts/2026-02-23-ecommerce-data-cleaning.html`

Content structure (~800-1000 words):
```
<nav>
<article class="blog-post">
  <header>
    <a href="../blog.html">← Back to Blog</a>
    <h1 class="gradient-text">Cleaning 125K Rows of Messy E-commerce Data</h1>
    <div class="post-meta">February 23, 2026 • 8 min read</div>
    <div class="tags">Data Cleaning • Python • Pandas</div>
  </header>

  <section "The Problem">
    E-commerce exports arrive messy: encoding corruption, mixed date formats,
    currency symbols, duplicate rows...
    Image: ../assets/img/before_raw_data.png
  </section>

  <section "The Approach">
    Built a 10-step automated pipeline:
    1. Drop empty columns
    2. Remove duplicates
    3. Standardize dates → ISO 8601
    ...
    Code snippet: date parsing example (5-6 lines of pandas)
    Code snippet: encoding fix example (3-4 lines)
  </section>

  <section "Results">
    Image: ../assets/img/after_cleaned_data.png
    Before/after comparison table (from design)
    Image: ../assets/img/cleaning_summary.png
    "Processing time: ~15 seconds"
  </section>

  <section "Key Takeaways">
    3-4 bullet points about lessons learned
    Link to GitHub repo
  </section>
</article>
<footer>
```

Source material for writing: read `case_study.html` and `README.md` from demo_1 for stats and context.

**Step 3: Verify in browser** — blog index card links to post, post renders with images and code blocks

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: add blog page and first post on e-commerce data cleaning"
```

---

### Task 7: Cross-Page Polish & Responsive Testing

**Goal:** Ensure all pages are consistent and mobile-ready.

**Files:**
- Modify: all HTML files + `style.css`

**Step 1: Verify nav active states** — each page highlights current link

**Step 2: Test mobile layout** — resize browser to 375px, verify:
- Hamburger menu works
- Cards stack to single column
- Hero text scales down
- Progress bars fit
- Blog post readable

**Step 3: Check all cross-page links** — nav links, project links, blog post back link, footer links

**Step 4: Commit any fixes**

```bash
git add -A
git commit -m "fix: responsive polish and cross-page link verification"
```

---

### Task 8: Deploy to GitHub Pages

**Goal:** Push to `theaiagent.github.io` repo and verify live site.

**Step 1: Create GitHub repo**

User creates `theaiagent.github.io` repo on GitHub (public, empty, no README).

**Step 2: Add remote and push**

```bash
cd D:/Projects/theaiagent.github.io
git remote add origin https://github.com/theaiagent/theaiagent.github.io.git
git push -u origin main
```

**Step 3: Verify** — open https://theaiagent.github.io in browser, check all pages load.

**Step 4: Remove old CNAME** — if GitHub settings show a custom domain (aykutcosgun.me), remove it in repo Settings → Pages.
