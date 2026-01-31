#!/usr/bin/env node
/**
 * Accessibility Audit Script
 *
 * This script provides instructions for running accessibility audits
 * using Lighthouse and axe-core. Run this after starting the development server.
 *
 * Usage:
 *   npm run dev                    # Start the dev server in one terminal
 *   npx lighthouse http://localhost:3000 --only-categories=accessibility --output=html --output-path=./a11y-report.html
 *
 * Or use the Chrome DevTools Lighthouse panel for a GUI-based audit.
 */

console.log(`
╔════════════════════════════════════════════════════════════════════════════╗
║                    ACCESSIBILITY AUDIT INSTRUCTIONS                        ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  This project implements WCAG 2.1 AA accessibility standards.              ║
║                                                                            ║
║  AUTOMATED TESTING:                                                        ║
║  ─────────────────                                                         ║
║  1. Start the development server:                                          ║
║     npm run dev                                                            ║
║                                                                            ║
║  2. Run Lighthouse accessibility audit:                                    ║
║     npx lighthouse http://localhost:3000 --only-categories=accessibility   ║
║         --output=html --output-path=./a11y-report.html                     ║
║                                                                            ║
║  3. Or install axe DevTools browser extension for real-time testing        ║
║                                                                            ║
║  MANUAL TESTING CHECKLIST:                                                 ║
║  ────────────────────────                                                  ║
║  □ Tab through all interactive elements - focus should be visible          ║
║  □ Press ESC to close modals                                               ║
║  □ Use screen reader (VoiceOver on Mac, NVDA on Windows)                   ║
║  □ Test with keyboard only (no mouse)                                      ║
║  □ Verify skip link works (Tab on page load)                               ║
║  □ Check mobile menu focus trap                                            ║
║  □ Test with reduced motion preference enabled                             ║
║  □ Verify all images have alt text                                         ║
║  □ Check color contrast with browser devtools                              ║
║                                                                            ║
║  PAGES TO TEST:                                                            ║
║  ──────────────                                                            ║
║  • http://localhost:3000 (Homepage)                                        ║
║  • http://localhost:3000/blog (Blog listing)                               ║
║  • http://localhost:3000/blog/[slug] (Blog post with images)               ║
║  • http://localhost:3000/projects (Projects gallery)                       ║
║  • http://localhost:3000/projects/[slug] (Project with popup images)       ║
║  • http://localhost:3000/about (About page)                                ║
║  • http://localhost:3000/contact (Contact page)                            ║
║                                                                            ║
║  ACCESSIBILITY FEATURES IMPLEMENTED:                                       ║
║  ───────────────────────────────────                                       ║
║  ✓ Skip to main content link                                               ║
║  ✓ Semantic HTML (main, nav, article, section, header, footer)             ║
║  ✓ ARIA labels on interactive elements                                     ║
║  ✓ Focus trap in modals and mobile menu                                    ║
║  ✓ Keyboard navigation (Tab, Shift+Tab, ESC)                               ║
║  ✓ Visible focus states (focus-visible ring)                               ║
║  ✓ Reduced motion support (prefers-reduced-motion)                         ║
║  ✓ Alt text required in Sanity CMS schemas                                 ║
║  ✓ External links marked for screen readers                                ║
║  ✓ Decorative elements hidden from screen readers                          ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
`);

// Exit with success
process.exit(0);
