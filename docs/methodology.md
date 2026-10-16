# Methodology and Data Handling

SKULLTRACE is designed to be explicit about how each result is obtained.

## DNS module

- Accepts a hostname, not a URL or an IP literal.
- Converts internationalized hostnames to their IDNA ASCII form.
- Uses Python's `socket.getaddrinfo` with the operating system's configured name-resolution settings.
- Returns deduplicated A/AAAA-style addresses from the system resolver.
- Does not perform brute force, subdomain enumeration, port scanning, or repeated query loops.
- A lookup can be visible to the configured resolver and its upstream providers. Consider this before querying sensitive names.

## IP module

- Parses an IPv4 or IPv6 literal using Python's standard-library `ipaddress` module.
- Reports standard address classifications and the reverse-DNS name format.
- Does not send the IP address to an external API and does not issue a reverse-DNS query.
- Classification is descriptive metadata, not proof of the identity, location, or behavior of a person or system.

## Reports

Reports are JSON and include a UTC timestamp, tool version, module, target, status, results, and scope note. They are saved only when the user explicitly supplies `--output`. Avoid distributing reports that contain sensitive operational details.

## Adding a module

Before implementing a new source, document the source owner, request method, fields collected, rate limits, error handling, whether target data leaves the machine, retention implications, and expected authorization. Prefer public, minimal data and avoid targeting private individuals.

## URL module

- Parses only `http://` and `https://` URL forms.
- Flags a small set of syntactic warning signs, including unencrypted HTTP, embedded credentials, a non-default port, IP-literal hosts and percent-encoded paths.
- Does not perform DNS lookups, make HTTP requests, follow redirects or load page content.
- Removes credentials, query strings and fragments from the report target to reduce accidental token leakage. The presence of a query string is represented as a boolean.
- Warning flags are heuristic hints, not a verdict that a URL is malicious or safe.

## Email and domain modules

- Validate basic formatting and normalize IDN hostnames to ASCII.
- Do not verify domain registration, mailbox ownership, deliverability or account identity.
- Do not contact a mail server or make a network request.

## File fingerprint module

- Reads a user-selected regular file in fixed-size chunks and calculates hashes locally.
- Does not modify, execute or upload the file.
- SHA-256 is the primary modern fingerprint; SHA-1 and MD5 are included for compatibility with existing evidence systems, not as recommendations for new security designs.

## Local information and case notes

- Local machine snapshot reports the current host/runtime and asks the configured system resolver for the local hostname. Resolver behavior depends on the machine's configuration.
- Case notes are user-authored observations and are not automatically treated as verified evidence. Keep notes factual and minimize sensitive personal data.
