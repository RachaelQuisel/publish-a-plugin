# PRIVACY.md

Not required. Plugins list without one. It is the cheapest way to answer a data-handling question
before a reviewer asks it, and it is close to obligatory if your plugin touches a browser, reads
account pages, or has a subject matter where its absence would look strange.

Put it in the plugin folder, beside `README.md`.

## What makes one useful

State the architecture plainly, then be specific about the one or two things that actually leave
the user's machine. Reviewers are looking for a straight answer to "where does the data go".

Say, in roughly this order:

1. **What the package is.** "A package of instructions and reference text" if that is what it is.
   "It has no publisher-operated service, account, telemetry, or storage. The publisher does not
   receive or retain content through this plugin."
2. **No code, no credentials, no network** — if true, say it explicitly, and name what is absent:
   no MCP servers, hooks, agents, scripts, `npx`/`uvx` launchers, no reading of environment
   variables or credential stores, no endpoint of its own.
3. **If your reference text quotes other products' command names and environment variables**, say
   so here. This is the sentence that defuses the credential-read false positive: *"Those are
   descriptions of third-party software for the reader, not instructions the package executes."*
4. **What a run actually reads**, including anything the user opts into.
5. **What third parties see** — the requested URL and normal request metadata, under the user's own
   session, governed by their terms.
6. **What the skill instructs Claude not to do**, followed by the honest caveat: *"These are
   instructions; the host's enabled tools and permissions determine what actions are technically
   possible."* Claiming a hard guarantee you cannot enforce is worse than naming the limit.
7. **Where output is written**, and that it is user-initiated.
8. **Where to ask** — the repository issue tracker.

## What to avoid

- Claiming a technical guarantee that is really an instruction to a model.
- Boilerplate about data you do not touch. It makes the parts you do touch harder to find.
- Omitting the browser or filesystem access a reader can see in the skill. The disclosure costs
  nothing; the omission is what looks evasive.
