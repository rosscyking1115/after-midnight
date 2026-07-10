# Security Policy

## Supported versions

This is a personal, capped-scope project. Security fixes, if any are needed,
land on `main`; there are no long-lived release branches.

## Reporting a vulnerability

Please report suspected vulnerabilities privately rather than opening a public
issue. Email **rosscyking@gmail.com** with:

- what you found and where (file, endpoint, or request),
- how to reproduce it, and
- the impact you think it has.

I'll acknowledge as soon as I can and aim to confirm or resolve reasonable
reports within a couple of weeks. There is no bug-bounty programme.

## Scope

The public API (`api/`) is keyless and serves only public UK grid data; it
holds no user accounts or personal data. The tool gives planning advice only and
never controls appliances. Please don't run load, stress, or automated scanning
tests against the hosted API — reproduce against a local instance instead
(see the [Quickstart](README.md#quickstart)).
