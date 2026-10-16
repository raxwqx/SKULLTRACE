# Security Policy

## Supported versions

Security reports are welcome for the latest development version of SKULLTRACE.

## Reporting a concern

Please do not publish exploitable details, credentials, access tokens, or personal information in a public issue. Open a private security advisory in the hosting platform when available, or contact the project maintainer through a verified repository contact channel.

## Scope and design

SKULLTRACE is designed for transparent, low-impact research. The current DNS module performs hostname resolution through the operating system's configured resolver. The IP module classifies an address locally and does not contact a third-party intelligence service. New modules should document any network requests, data sent, sources used, rate limits, and privacy considerations before implementation.

SKULLTRACE must not be extended to facilitate unauthorized account access, credential theft, stalking, covert tracking, or collection of private personal information.
