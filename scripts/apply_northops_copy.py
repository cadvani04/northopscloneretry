#!/usr/bin/env python3
"""Replace Kharros wording + logo with NorthOps across mirror/*.html (markup/classes unchanged)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIRROR = ROOT / "mirror"

LOGO_SVG_NAV = "/_assets/cdn.prod.website-files.com/68e05d1a944a644eaacd5878/6940a378d1a98f27ba34dbdf_Kharros.svg"
LOGO_ICON_CTA = "/_assets/cdn.prod.website-files.com/68e05d1a944a644eaacd5878/6a017b19cf55218fc00acc24_KharrosIcon.svg"
LOGO_WHITE_DIAGRAM = "/_assets/cdn.prod.website-files.com/68e05d1a944a644eaacd5878/6a018521c817996989d1e034_KharrosIconWhite.svg"
LOGO_PNG = "/northops-logo.png"

CALENDLY_URL = "https://calendly.com/north-ops-info/30min"
CALENDLY_HREF_ATTR = f'href="{CALENDLY_URL}" target="_blank" rel="noopener noreferrer"'

ABOUT_DESC_OLD = (
    "Built by experts on a joint DIU x USSF x AFRL special project, Kharros delivers vendor-neutral T&amp;E products "
    "that certify defense systems before contract award."
)
ABOUT_DESC_NEW = (
    "NorthOps builds custom operational systems for manufacturers and operations-heavy teams—inventory, purchasing, "
    "job tracking, dashboards, and AI automations—implemented around how you actually work."
)

CONTACT_DESC_OLD = (
    "Talk to Kharros about productized test and evaluation for national security. Vendors prove capability, "
    "primes de-risk bids, government offices downselect faster."
)
CONTACT_DESC_NEW = (
    "Book an operational review with NorthOps. Tell us what&apos;s breaking on the floor—we&apos;ll map workflows, "
    "surface bottlenecks, and outline a practical build plan."
)

NEWSROOM_DESC_OLD = (
    "News and analysis from Kharros on defense T&amp;E, PAEs, OTAs, CSOs, procurement reform, and the productized "
    "evaluation layer powering national security acquisition."
)
NEWSROOM_DESC_NEW = (
    "Updates from NorthOps on operational systems, inventory and purchasing workflows, implementation notes, "
    "and how teams escape spreadsheet chaos."
)

INDEX_RAW: list[tuple[str, str]] = [
    (
        "<title>KHARROS - Productized Evaluation Layer for National Security</title>",
        "<title>NorthOps | Operational Systems for Manufacturers</title>",
    ),
    (
        '<meta content="Kharros is the productized evaluation layer for national security. Independent test and evaluation, scoring rubrics, and certifications that prove systems work." name="description"/>',
        '<meta content="NorthOps builds custom AI-powered operational systems for manufacturers and operations-heavy businesses drowning in disconnected software, spreadsheets, and manual workflows." name="description"/>',
    ),
    (
        '<meta content="KHARROS - Productized Evaluation Layer for National Security" property="og:title"/>',
        '<meta content="NorthOps | Operational Systems for Manufacturers" property="og:title"/>',
    ),
    (
        '<meta content="Kharros is the productized evaluation layer for national security. Independent test and evaluation, scoring rubrics, and certifications that prove systems work." property="og:description"/>',
        '<meta content="NorthOps builds custom AI-powered operational systems for manufacturers and operations-heavy businesses drowning in disconnected software, spreadsheets, and manual workflows." property="og:description"/>',
    ),
    (
        '<meta content="KHARROS - Productized Evaluation Layer for National Security" property="twitter:title"/>',
        '<meta content="NorthOps | Operational Systems for Manufacturers" property="twitter:title"/>',
    ),
    (
        '<meta content="Kharros is the productized evaluation layer for national security. Independent test and evaluation, scoring rubrics, and certifications that prove systems work." property="twitter:description"/>',
        '<meta content="NorthOps builds custom AI-powered operational systems for manufacturers and operations-heavy businesses drowning in disconnected software, spreadsheets, and manual workflows." property="twitter:description"/>',
    ),
    (
        "/_assets/cdn.prod.website-files.com/68e05d1a944a644eaacd5878/6a0230842a010916ef988fab_Kharros.png",
        LOGO_PNG,
    ),
    (
        "<title>Kharros | Government Acquisition Office Evaluation Software</title>",
        "<title>NorthOps | Operational Systems &amp; AI Infrastructure</title>",
    ),
    (
        '<meta name="description" content="Kharros helps government acquisition offices evaluate vendors with neutral data, mission-aligned evidence, and productized downselection support for national security programs." />',
        '<meta name="description" content="NorthOps helps operations teams replace duct-taped QuickBooks, spreadsheets, and legacy ERP gaps with custom workflows, inventory truth, and dashboards leadership can trust." />',
    ),
    (
        '<meta property="og:title" content="Kharros | Government Acquisition Office Evaluation Software" />',
        '<meta property="og:title" content="NorthOps | Operational Systems &amp; AI Infrastructure" />',
    ),
    (
        '<meta property="og:description" content="Neutral vendor evaluation products for government acquisition teams, national security offices, and commercial vendors competing on objective performance." />',
        '<meta property="og:description" content="Modern operational infrastructure for manufacturers: inventory, purchasing, job tracking, reporting, and AI automations built around how you actually run." />',
    ),
    (
        """  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Kharros",
    "applicationCategory": "Government acquisition evaluation software",
    "description": "Kharros provides neutral evaluation products for government acquisition offices, national security teams, and vendors throughout the downselection cycle.",
    "audience": [
      { "@type": "Audience", "audienceType": "Government acquisition offices" },
      { "@type": "Audience", "audienceType": "National security program offices" },
      { "@type": "Audience", "audienceType": "Commercial vendors" }
    ],
    "offers": { "@type": "Offer", "category": "Vendor evaluation and evidence-backed certification" }
  }""",
        """  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "NorthOps",
    "applicationCategory": "BusinessApplication",
    "description": "NorthOps delivers custom operational systems and AI-enabled infrastructure for manufacturers and operations-heavy businesses.",
    "audience": [
      { "@type": "Audience", "audienceType": "Operations managers and plant leaders" },
      { "@type": "Audience", "audienceType": "Owners, COOs, and founders" },
      { "@type": "Audience", "audienceType": "Industrial and manufacturing teams" }
    ],
    "offers": { "@type": "Offer", "category": "Custom operational systems and implementation" }
  }""",
    ),
    (
        '  <section class="kharros-hero-section" aria-label="Kharros">',
        '  <section class="kharros-hero-section" aria-label="NorthOps">',
    ),
    (
        '        title="Kharros background video"',
        '        title="NorthOps background video"',
    ),
    (
        "        Kharros is the productized evaluation layer for national security.\n",
        "        NorthOps is the operating system for complex operations\n",
    ),
    (
        "        See how it works <span class=\"cta-arrow\">&rarr;</span>",
        "        See what&apos;s slowing operations down <span class=\"cta-arrow\">&rarr;</span>",
    ),
    (
        '  <section class="kharros-morph-section" aria-label="Who uses Kharros">',
        '  <section class="kharros-morph-section" aria-label="Who NorthOps is for">',
    ),
    (
        '  <section class="kharros-summary-section" aria-label="Kharros summary">',
        '  <section class="kharros-summary-section" aria-label="NorthOps summary">',
    ),
    (
        "<p>Commercial teams use Kharros to prove capability throughout downselection, from pre-bid readiness to evidence-backed certification.</p>",
        "<p>Operations leaders use NorthOps to replace spreadsheet chaos with inventory truth, job visibility, and workflows that match how the floor actually runs.</p>",
    ),
    (
        "<p>Government acquisition offices use Kharros to compare vendors against the same mission requirements and move faster from interest to award.</p>",
        "<p>Owners and COOs use NorthOps for reporting, accountability, and systems that scale without betting the company on another failed ERP rip-and-replace.</p>",
    ),
    (
        "<p>Kharros supports neutral vendor evaluation, evidence-backed certification, acquisition downselection, national security programs, procurement offices, and program offices that need objective performance data.</p>",
        "<p>NorthOps supports inventory, purchasing, production tracking, dashboards, AI automations, and internal tooling—implemented fast, operator-first, without forcing your business into a generic template.</p>",
    ),
    (
        "<p>One evaluation layer: vendors prove capability, government teams compare on the same evidence.</p>",
        "<p>One operational layer: operators get clarity, leadership gets numbers everyone agrees on.</p>",
    ),
    (
        '<p class="hero-headline" id="khHeadline">Kharros is the productized evaluation layer for national security</p>',
        '<p class="hero-headline" id="khHeadline">NorthOps is the operating system for complex operations</p>',
    ),
    (
        """    var STATEMENTS = [
      'Kharros is the productized evaluation layer for national security',
      'Commercial teams use Kharros to prove capability throughout downselection, from pre-bid readiness to evidence-backed certification.',
      'Government acquisition teams use Kharros to compare vendors against the same mission requirements and move faster from interest to award.',
      'One evaluation layer: vendors prove capability, government teams compare on the same evidence.'
    ];""",
        """    var STATEMENTS = [
      'NorthOps is the operating system for complex operations',
      'Operations leaders use NorthOps to replace spreadsheet chaos with inventory truth, job visibility, and workflows that match how the floor actually runs.',
      'Owners and COOs use NorthOps for reporting, accountability, and systems that scale without another failed ERP rip-and-replace.',
      'One operational layer: operators get clarity, leadership gets numbers everyone agrees on.'
    ];""",
    ),
    (
        "<h2>Proof before procurement.</h2>",
        "<h2>Proof before your next software gamble.</h2>",
    ),
    (
        "            Kharros gives government buyers and commercial vendors objective evidence that systems perform against real mission requirements.\n",
        "            NorthOps gives operators and leadership the same operational picture—grounded in workflows, inventory, and execution—not slideware.\n",
    ),
    ("              <span>Government</span>", "              <span>Operators</span>"),
    ("              <span>Commercial</span>", "              <span>Leadership</span>"),
    (
        '              <div class="quote-label">Government</div>',
        '              <div class="quote-label">Operators</div>',
    ),
    (
        '              <div class="quote-label">Commercial</div>',
        '              <div class="quote-label">Leadership</div>',
    ),
    (
        "<blockquote data-quote>Kharros gave us the evidence we needed before making a decision. Instead of relying on vendor claims, we could see who actually performed against the mission requirements.</blockquote>",
        "<blockquote data-quote>NorthOps mapped our real workflow in week one. We stopped firefighting inventory mismatches and finally had one source of truth the floor actually uses.</blockquote>",
    ),
    (
        '<div class="quote-source">Fmr. Program Executive Officer, U.S. Department of War</div>',
        '<div class="quote-source">Director of Operations, precision manufacturing</div>',
    ),
    (
        "<blockquote data-quote>Kharros gave us third-party validation we could actually use. It made our system easier to trust, easier to compare, and much harder for buyers to dismiss.</blockquote>",
        "<blockquote data-quote>We were terrified of another 18-month ERP science project. NorthOps shipped usable systems in sprints—purchasing tied to jobs, dashboards my COO finally trusts.</blockquote>",
    ),
    (
        '<div class="quote-source">Director of Government Affairs, Series D defense AI startup</div>',
        '<div class="quote-source">COO, industrial services company</div>',
    ),
    (
        "          <div class=\"card-title\">Air Superiority</div>\n          <div class=\"card-details\">\n            <p>\n              Accelerate acquisition timelines for UAV programs. We provide the empirical safety data required to move autonomous swarm systems from prototype to Program of Record.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Schedule Air Superiority demo</span>",
        "          <div class=\"card-title\">Inventory &amp; materials</div>\n          <div class=\"card-details\">\n            <p>\n              Real-time inventory, lot and location discipline, and materials visibility so production stops guessing what&apos;s on hand.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Book an operational review</span>",
    ),
    (
        "          <div class=\"card-title\">Maritime Dominance</div>\n          <div class=\"card-details\">\n            <p>\n              Validate unmanned surface and subsurface vessels against NAVSEA compliance standards. Ensure your navigation algorithms are certified for contested waters.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Schedule Maritime Dominance demo</span>",
        "          <div class=\"card-title\">Production &amp; jobs</div>\n          <div class=\"card-details\">\n            <p>\n              Job tracking, WIP, throughput, and bottleneck visibility across your floor—without another dashboard nobody opens.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Book an operational review</span>",
    ),
    (
        "          <div class=\"card-title\">Orbital Command</div>\n          <div class=\"card-details\">\n            <p>\n              Satisfy Space Force resiliency requirements before launch. We benchmark satellite maneuver logic to ensure survivability in high-risk orbital environments.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Schedule Orbital Command demo</span>",
        "          <div class=\"card-title\">Scheduling &amp; planning</div>\n          <div class=\"card-details\">\n            <p>\n              Master schedules, capacity, and commitments tied to real constraints—so sales and ops stop arguing in meetings.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Book an operational review</span>",
    ),
    (
        "          <div class=\"card-title\">Ground Force</div>\n          <div class=\"card-details\">\n            <p>\n              Bridge the gap between R&amp;D and deployment. We certify robotic mule and autonomous convoy logic to meet rigorous Army safety and reliability benchmarks.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Schedule Ground Force demo</span>",
        "          <div class=\"card-title\">Purchasing &amp; vendors</div>\n          <div class=\"card-details\">\n            <p>\n              POs, receipts, and vendor workflows wired into jobs and inventory so buyers and operators stay aligned.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Book an operational review</span>",
    ),
    (
        "          <div class=\"card-title\">Tactical Field</div>\n          <div class=\"card-details\">\n            <p>\n              Prove warfighter utility. We validate edge-compute threat detection models to ensure they deliver actionable intelligence, not false positives.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Schedule Tactical Field demo</span>",
        "          <div class=\"card-title\">Dashboards &amp; alerts</div>\n          <div class=\"card-details\">\n            <p>\n              Operational summaries, exceptions, and alerts your team can act on the same day—not buried in email threads.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Book an operational review</span>",
    ),
    (
        "          <div class=\"card-title\">Special Projects</div>\n          <div class=\"card-details\">\n            <p>\n              Black box verification for classified initiatives. We provide third-party algorithmic assurance within secure, compartmentalized environments.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Schedule Special Projects demo</span>",
        "          <div class=\"card-title\">Custom internal systems</div>\n          <div class=\"card-details\">\n            <p>\n              Internal tools, migrations off spreadsheets, and integrations when off-the-shelf ERP won&apos;t fit how you actually execute.\n            </p>\n            <a href=\"/contact\" class=\"liquid-btn\">\n              <span>Book an operational review</span>",
    ),
    (
        "      <h1>We help your products get to the war fighter.</h1>",
        "      <h1>We help operators run the business on facts—not spreadsheets.</h1>",
    ),
    (
        '<div class="cta_pill">See how KHARROS works</div>',
        '<div class="cta_pill">See how NorthOps works</div>',
    ),
    (
        '<h2 class="heading-style-h5">Partner with the frontier of how defense is built, acquired, and deployed.</h2>',
        '<h2 class="heading-style-h5">Partner with a team that ships operational systems the way your shop actually runs.</h2>',
    ),
    (
        '<div class="button_text">Start now</div>',
        '<div class="button_text">Book an operational review</div>',
    ),
]

HOME_ABOUT_SECTION_NORTHOPS = r'''<section class="section_home-about northops-home-about" aria-label="Operational workflows"><style>
  .northops-home-about .home-about_img-text {
    display: inline-flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.45em 1.1em;
    box-sizing: border-box;
  }
  .northops-home-about .northops-wf-rail {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }
  .northops-home-about .northops-wf-stages {
    display: inline-flex;
    align-items: center;
    gap: 0.2rem;
  }
  .northops-home-about .northops-wf-stages span {
    display: block;
    width: 5px;
    height: 14px;
    border-radius: 1px;
    background: rgba(255, 255, 255, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.35);
    transform-origin: center bottom;
    animation: northopsWfStage 2.4s ease-in-out infinite;
  }
  .northops-home-about .northops-wf-stages span:nth-child(2) {
    animation-delay: 0.25s;
  }
  .northops-home-about .northops-wf-stages span:nth-child(3) {
    animation-delay: 0.5s;
  }
  .northops-home-about .northops-wf-stages span:nth-child(4) {
    animation-delay: 0.75s;
  }
  @keyframes northopsWfStage {
    0%,
    100% {
      opacity: 0.35;
      transform: scaleY(0.55);
      background: rgba(255, 255, 255, 0.18);
    }
    35% {
      opacity: 1;
      transform: scaleY(1);
      background: rgba(255, 255, 255, 0.95);
      box-shadow: 0 0 12px rgba(255, 255, 255, 0.35);
    }
  }
  .northops-home-about .northops-wf-copy {
    position: relative;
    letter-spacing: 0.02em;
  }
  .northops-home-about .northops-wf-copy::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: -0.22em;
    height: 2px;
    border-radius: 1px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(255, 255, 255, 0.15) 20%,
      rgba(255, 255, 255, 0.85) 50%,
      rgba(255, 255, 255, 0.15) 80%,
      transparent 100%
    );
    background-size: 180% 100%;
    animation: northopsWfFlow 2.8s linear infinite;
    opacity: 0.75;
    pointer-events: none;
  }
  @keyframes northopsWfFlow {
    0% {
      background-position: 100% 0;
    }
    100% {
      background-position: -100% 0;
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .northops-home-about .northops-wf-stages span,
    .northops-home-about .northops-wf-copy::after {
      animation: none !important;
    }
    .northops-home-about .northops-wf-stages span {
      opacity: 0.75;
      transform: scaleY(1);
    }
  }
</style><div class="home-about_wrapper"><div class="scroll-note_text">Keep scrolling</div><div class="home-about_sticky"><div class="home-about_component"><h2 class="home-about_heading _1">Stop firefighting</h2><div class="home-about_img-wrap"><div class="div-block"><img src="/_assets/cdn.prod.website-files.com/68e05d1a944a644eaacd5878/68e06d6f34626e38423110ed_Military%20Operations%20Room.png" loading="lazy" alt="" class="home-about_img"/></div><h2 class="home-about_img-text"><span class="northops-wf-rail"><span class="northops-wf-stages" aria-hidden="true"><span></span><span></span><span></span><span></span></span><span class="northops-wf-copy">CONNECT&nbsp;EVERY&nbsp;WORKFLOW</span></span></h2></div><h2 class="home-about_heading _2">across your org</h2></div></div></div></section>'''

_HOME_ABOUT_VANILLA_RE = re.compile(
    r'<section class="section_home-about">\s*<div class="home-about_wrapper">.*?</div>\s*</div>\s*</div>\s*</section>',
    re.DOTALL,
)


def apply_calendly_links(html: str) -> str:
    """Send booking CTAs to Calendly (opens new tab)."""
    html = html.replace(
        'href="/contact" aria-current="page" class="button-2 light-small w-inline-block w--current"',
        f'{CALENDLY_HREF_ATTR} class="button-2 light-small w-inline-block"',
    )
    return html.replace('href="/contact"', CALENDLY_HREF_ATTR)


def inject_northops_home_about(html: str) -> str:
    """Replace vanilla Webflow sticky band with workflow-stage animation + NorthOps copy."""
    if "northops-home-about" in html:
        return html
    m = _HOME_ABOUT_VANILLA_RE.search(html)
    if not m:
        return html
    return html[: m.start()] + HOME_ABOUT_SECTION_NORTHOPS + html[m.end() :]


SHARED: list[tuple[str, str]] = [
    (LOGO_SVG_NAV, LOGO_PNG),
    (LOGO_ICON_CTA, LOGO_PNG),
    (LOGO_WHITE_DIAGRAM, LOGO_PNG),
    (
        "/_assets/cdn.prod.website-files.com/68e05d1a944a644eaacd5878/6939d527aa88eec39831f129_favicon-Kharros.png",
        LOGO_PNG,
    ),
    (
        "/_assets/cdn.prod.website-files.com/68e05d1a944a644eaacd5878/6939d52f77243ebc80dc2f29_Kharros-Webclip.png",
        LOGO_PNG,
    ),
    ("Get Started", "Book an Operational Review"),
    ("© 2026 Kharros, inc.", "© 2026 NorthOps, Inc."),
    ("© 2026 Kharros, Inc.", "© 2026 NorthOps, Inc."),
    ("Prove Effectiveness.", "Operational clarity, implemented fast."),
    ("mailto:contact@kharros.com", "mailto:hello@northops.com"),
    ("contact@kharros.com", "hello@northops.com"),
    (
        "580 California Street, 12th &amp; 16th Floors, <br/>San Francisco, California 94104",
        "Serving manufacturers &amp; operations-heavy teams nationwide.",
    ),
    ('<div class="footer_brand-copy">KHARROS</div>', '<div class="footer_brand-copy">NORTHOPS</div>'),
    ("<title>KHARROS</title>", "<title>NorthOps</title>"),
    ("Kharros", "NorthOps"),
    ("KHARROS", "NORTHOPS"),
]


def apply_shared(html: str) -> str:
    for old, new in SHARED:
        html = html.replace(old, new)
    return html


_NAV_STRIP_PATTERNS = [
    re.compile(
        r'<a href="/newsroom" class="navbar_link-2 w-inline-block"><div class="navbar_link-text _1">Newsroom</div><div class="navbar_link-text _2">Newsroom</div></a>'
    ),
    re.compile(
        r'<a href="/newsroom" aria-current="page" class="navbar_link-2 w-inline-block w--current"><div class="navbar_link-text _1">Newsroom</div><div class="navbar_link-text _2">Newsroom</div></a>'
    ),
    re.compile(
        r'<a href="/app" class="navbar_link-2 w-inline-block"><div class="navbar_link-text _1">Sign In</div><div class="navbar_link-text _2">Sign In</div></a>'
    ),
    re.compile(
        r'<a href="/app" class="footer_link">Sign In</a><a href="/newsroom" class="footer_link">Newsroom</a>'
    ),
]


def strip_newsroom_and_signin(html: str) -> str:
    """Remove Newsroom + Sign In from navbar and footer (not linked site areas)."""
    for p in _NAV_STRIP_PATTERNS:
        html = p.sub("", html)
    return html


def strip_about_team_animation_attr(html: str) -> str:
    """Webflow hides `[animation=scale]` until IX; team placeholders never unhide reliably."""
    if "section_team" not in html or "about-team_img" not in html:
        return html
    return html.replace(' animation="scale"', "")


ABOUT_MEDIA_STYLE = (
    '<style id="northops-about-images">'
    "html.w-mod-js:not(.w-mod-ix3) .section_values img, "
    "html.w-mod-js:not(.w-mod-ix3) .section_team img "
    "{ visibility: visible !important; }\n"
    ".about-team_img-wrap { min-height: 1px; }\n"
    ".about-team_img { display: block; position: absolute; inset: 0; width: 100%; height: 100%; "
    "object-fit: cover; }\n"
    "</style>"
)


def patch_about_page_media(html: str) -> str:
    """Values section imgs: mirrored Webflow URLs break (literal %20 filenames vs encoded paths)."""
    if "northops-about-images" not in html:
        html = html.replace("</head>", ABOUT_MEDIA_STYLE + "</head>", 1)

    m = re.search(
        r'(<section class="section_values">)(.*?)(<section class="section_approach">)',
        html,
        re.DOTALL,
    )
    if not m:
        return html
    inner = m.group(2)
    if "/images/about/values-01.jpg" in inner:
        return html

    tags = re.findall(r"<img\b[^>]*>", inner)
    if len(tags) != 6:
        return html
    replacements = [
        '<img loading="eager" src="/images/about/values-01.jpg" alt="" class="about-values_img _1"/>',
        '<img loading="eager" src="/images/about/values-02.jpg" alt="" class="about-values_img _2"/>',
        '<img loading="eager" src="/images/about/values-03.jpg" alt="" class="about-values_img _3"/>',
        '<img loading="eager" src="/images/about/values-04.jpg" alt="" class="about-values_img-tablet"/>',
        '<img loading="eager" src="/images/about/values-05.jpg" alt="" class="about-values_img-tablet"/>',
        '<img id="w-node-_3e2f36c7-a93b-26f9-3eb0-428f49cd1226-aacd58f7" loading="eager" '
        'src="/images/about/values-06.jpg" alt="" class="about-values_img-tablet"/>',
    ]
    new_inner = inner
    for old, new in zip(tags, replacements):
        new_inner = new_inner.replace(old, new, 1)
    return html[: m.start()] + m.group(1) + new_inner + m.group(3) + html[m.end() :]


def patch_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    html = raw
    rel = path.relative_to(MIRROR).as_posix()

    if rel == "index.html":
        for old, new in INDEX_RAW:
            html = html.replace(old, new)
        html = inject_northops_home_about(html)

    if rel == "about/index.html":
        html = html.replace(ABOUT_DESC_OLD, ABOUT_DESC_NEW)
        html = patch_about_page_media(html)

    if rel == "contact/index.html":
        html = html.replace(CONTACT_DESC_OLD, CONTACT_DESC_NEW)

    if rel == "newsroom/index.html":
        html = html.replace(NEWSROOM_DESC_OLD, NEWSROOM_DESC_NEW)

    if "newsroom/kharros-selected" in rel:
        html = re.sub(
            r"<title>[^<]+</title>",
            "<title>NorthOps | Field notes on operational systems</title>",
            html,
            count=1,
        )
        html = html.replace(
            "Kharros joins Catalyst Campus to accelerate trusted AI adoption for the Space Force through rigorous, independent benchmarking.",
            "NorthOps shares how manufacturers are replacing spreadsheet chaos with inventory truth, purchasing tied to jobs, and dashboards leadership trusts.",
        )
        html = html.replace(
            "NorthOps Selected for Catalyst Campus Mini-Accelerator to Establish New Standard for Space AI Evaluation",
            "NorthOps field notes: operational systems for manufacturers",
        )

    html = apply_shared(html)
    html = apply_calendly_links(html)
    html = strip_newsroom_and_signin(html)
    html = strip_about_team_animation_attr(html)

    if html != raw:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    for path in sorted(MIRROR.rglob("*.html")):
        if patch_file(path):
            n += 1
            print("updated", path.relative_to(ROOT))
    print("done,", n, "files")


if __name__ == "__main__":
    main()
