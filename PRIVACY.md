# Privacy Policy — BOIM Korean Business Finder (Dify plugin)

Last updated: 2026-10-27

## Summary

The plugin itself does not collect, store or log any user data. When a tool runs, it sends only the
search arguments of that call to BOIM (boim.io), the service operated by the plugin's author, and
returns BOIM's public results to Dify. No account, API key or credential is used.

## What is sent, and where

Each tool call sends one HTTPS request to `https://boim.io/api/mcp` containing:

- the tool name (`find_businesses`, `search_vendors` or `find_public_bids`);
- the search arguments filled in by the user or the model: region, industry or item, business name or
  keyword, certification, bid type (each trimmed to 100 characters);
- a fixed result limit (5) and the User-Agent `boim-dify-plugin/<version>`.

No conversation text, user identifiers, files, Dify credentials or other workflow data are sent.
Please do not put personal data (names, phone numbers, email addresses) into the search arguments.

## What BOIM records

As described in the [BOIM privacy policy](https://boim.io/privacy/) (Korean), BOIM keeps an "AI read
log" of MCP tool calls with the client name (here the User-Agent), the tool name, the first part of the
arguments (up to 200 characters) and the time. It does not store IP addresses in this log, keeps it for
180 days and then keeps only aggregate counts. The log is used to count how often AI tools read BOIM data
and to improve the service; it is not used to identify people.

The request comes from the server running your Dify instance, so BOIM sees that server's IP address,
not your end users' addresses. BOIM is hosted on Vercel, which keeps access logs, and BOIM's firewall
keeps a daily summary (IP address, TLS fingerprint, User-Agent, request count) of connections with very
high request volumes to stop bulk scraping, kept for one year. BOIM does not share this data with third
parties except where required by law.

Third parties involved on BOIM's side: Vercel Inc. (hosting, [privacy policy](https://vercel.com/legal/privacy-policy))
and Supabase Inc. (database in Seoul, [privacy policy](https://supabase.com/privacy)).

## What the plugin returns

Results are public information from Korean government open data (business name, industry,
neighborhood, public-procurement records, public bid notices) and details that businesses chose to
publish on BOIM. BOIM does not publish representative names, street addresses or business registration
numbers.

## Contact

Public identity Co., Ltd. (operator of BOIM) — public-id@naver.com · https://boim.io/privacy/
