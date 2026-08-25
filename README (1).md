# OUT OF ORDER — The Internet's Court of Petty Disputes

> **File suit over life's smallest injustices. $3 per filing. Judge verdicts FREE. The public jury costs $5.**

OUT OF ORDER sells small, dramatic legal proceedings to the extremely online. Unpaid Uber fares, roommate food crimes, criminal movie takes: plaintiffs pay **$3 to sue**, a Judge-Judy-style bench delivers a **FREE voiced verdict video** plus an engraved digital verdict card, and the defendant is served a summons link. The accused pays **$3 to respond**. Losers appeal ($3). Losers counter-sue ($3). **Conflict is the revenue engine.**

## Why this wins (the viral mechanics, engineered in)

| Lever | Mechanic |
|---|---|
| **Recipient-becomes-sender** | Every case creates 2+ users. The defendant *must* respond to the summons link — with engagement ($3 response) or with a counter-suit ($3). |
| **Broadcast artifacts** | Verdict videos + engraved cards are share-by-design content ("I was found GUILTY"). Every ruling is an ad. |
| **Public docket** | Voyeur feed of strangers' disputes = watch-time, plus $3 "pin my case" boost revenue. |
| **Escalation economics** | Filing → appeal → counter-sue → jury trial. The loop monetizes the argument itself, repeatedly. |
| **Free acquisition hook** | The Courtroom Studio daguerreotypes anyone's photo + issues a free instant ruling. Zero-friction, shareable, and it demos the product. |

## Unit economics (as filed)

- **Sue someone (filing)** — $3; the judge verdict is **FREE** (the verdict is the ad — every free ruling markets the court)
- **Defendant response** — $3 (they pay to be heard; monetizes BOTH sides of every beef)
- **Sponsored Response** — +$3 (filer covers the accused's reply — "they can't plead poverty")
- **Jury Trial** — $5 (the public becomes the jury for a day: vote-by-link, tally broadcast)
- **Appeals & counter-suits** — $3 each, recurring per dispute
- **Make It Famous** — $3 docket pin
- **Merch** — GUILTY tee $24 / OBJECTION! cap $19 / Framed Verdict $34 (print-on-demand, ~55% margin)

Target: AOV ~$7 (filing + response + jury upgrades per dispute). Every free judge verdict doubles as content marketing — COGS ≈ $1/case (TTS + render + email).

## Payments — live wiring (PayPal JavaScript SDK)

Checkout runs on PayPal **Smart Buttons** (JS SDK, no backend required): the SDK loads from `paypal.com` at checkout with the app's public **Client ID** (`PAYPAL_CLIENT_ID` in `index.html`), creates + captures an order client-side with line items from the cart, then issues the case number. The app **Secret is never used or stored** in the codebase — keep it offline; if you ever add server-side capture/verification (recommended at scale), that's where it belongs, behind an endpoint.

- Current app: `Mcsmithandco` — **LIVE** (real money, as of launch). Client ID configured in `index.html`. The old sandbox app still exists for safe testing — use it for any experiments, never for production.
- Payouts route to the PayPal account that owns the app; in SA, withdraw via FNB. Currency: USD.

## What's real vs. mocked in this preview

**Working now, fully client-side:** verdict broadcast player with synced typewriter rulings, live docket, courtroom studio (photo → daguerreotype/gild → instant bench ruling, share-copy), 4-step filing checkout (wizard), famous-rulings marquee, referral-ready summons links (served by link, viral by design).

**Mocked / to wire for production:**
1. ~~Payments~~ → ✅ **DONE** — PayPal JS SDK live (sandbox app `Mcsmithandco`; swap client ID for live at launch). Stripe/Paystack remain good ZA-local alternatives.
2. **Verdict video pipeline** → TTS voice (the judge's voice in `audio/`) + ffmpeg/canvas render over the exhibit card, or HeyGen/Synthesia talking-judge clips. ~30–90s per ruling, fully scriptable.
3. ~~Public jury mechanics~~ → ✅ **BUILT** — `vote.html?case=XXXX`: vote-by-link jury page with live tally bar, real countdown, rolling juror commentary, verdict-at-zero state, and a downloadable **Juror Badge** share card (canvas-rendered). Demo ledger is client-side persistence; swap the `oo_tally_*` localStorage calls for a serverless tally endpoint at launch — the page contract is already URL-parameterized per case.
4. **Fulfillment** → Printful/Prodigi for merch + framed verdicts. Print-on-demand, zero inventory.

## Launch playbook (30 days)

- **Week 1:** Post verdict videos daily to TikTok/Reels/Shorts. Format: 3s cold open on the photo ("EXHIBIT A"), verdict readout, guilty stamp. Pin "file your case" link.
- **Week 2:** Seed 20 free cases in big group chats/campuses — the summons mechanic does distribution for you.
- **Week 3:** Launch **Jury Trials** + weekly "Court is in session" livestream where the judge rules the best filings live. Boost winners with $50/day Spark ads.
- **Week 4:** Drop merch + "appeal day" promo (appeals $3). Ship an email digest: *This Week in Petty.*

**KPIs:** filing→appeal rate ≥ 35%, summons-link open rate ≥ 70%, verdict-video shares ≥ 15% of viewers, CAC < $3.

## Running the preview

```bash
cd out-of-order && python3 -m http.server 8080
# open http://localhost:8080
```

Files: `index.html` (entire storefront, self-contained) · `images/` (judge, exhibits, generated art) · `audio/` (voiced verdicts for the broadcast player).
