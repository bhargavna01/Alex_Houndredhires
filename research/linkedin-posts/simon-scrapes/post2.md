# LinkedIn Post by Simon Scrapes

- **Profile URL:** https://www.linkedin.com/in/simon-coton-81608b98
- **Post URL:** https://www.linkedin.com/posts/simon-coton-81608b98_youre-using-claude-code-wrong-activity-7429823257048043521-mmCs
- **Date Scraped:** 2026-07-03

## Content

You’re using Claude Code wrong.

Most people treat it like a smarter ChatGPT inside their terminal. They type a prompt, wait for code, and copy-paste.

That’s the manual way. And if you’re building automation systems, manual is the enemy.

Claude Code isn't just a chatbot; it's a configurable environment. If you aren't setting up Agent Teams or custom Slash Commands, you're missing all the potential.

I’ve been digging into the documentation and testing workflows. Here is the difference between a hobbyist setup and a scalable system:

1.  Agent Teams: Don't make one agent do the research, coding, and testing. It creates bottlenecks. Use the new "Agent Teams" feature to run parallel instances. One builds, one reviews.
2.  Point, Don't Dump: Stop pasting your 50-page brand guide into the context window. It burns tokens. Keep your `claude.md` lean and "point" to external skill files.
3.  The Gemini Backdoor: Claude can't access every site. We set up a "fetch skill" that triggers the Gemini CLI to grab the data Claude can't reach.

We don't use AI to write code faster. We use it to build systems that write code for us.

Swipe through for the 5 configuration tips that changed my workflow. 

Which of these did you already know about?
