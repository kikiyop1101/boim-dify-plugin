# BOIM — Korean Business Finder

Search businesses in South Korea, public-procurement vendors and open public bids from Dify agents, chatflows and workflows. The data comes from [BOIM](https://boim.io) (boim.io), a read-only directory built on Korean government open data, and every result carries its source URL.

## Tools

| Tool | What it finds | Example input |
|---|---|---|
| Find Local Businesses (`find_businesses`) | Operating businesses of any industry, about 2.76 million nationwide in 247 sub-categories, by city, district or neighborhood plus industry or name. Name, industry and neighborhood only (no street address or phone). | region `세종 보람동`, category `미용실` (hair salon) |
| Find Vendors (`search_vendors`) | 76,000+ vendor cards from Public Procurement Service data (contract items and the last 12 months of public deliveries, every item category), with National Tax Service business status and details businesses registered on BOIM. | category `안내판` (signboards), region `세종` |
| Find Public Bids (`find_public_bids`) | Open public tenders in all fields from KONEPS, Defense e-Procurement, LH, K-water and Nuri-jangteo, refreshed twice a day, closest deadline first, with the original notice link. | category `청소` (cleaning), bid type Services |

Each call returns up to 5 results, the total count, a link to the full public list on boim.io and a citation line. Businesses are listed alphabetically (businesses that registered on BOIM come first), vendors by relevance and card completeness with a daily shuffle, bids by deadline. The order is not a ranking, rating or paid placement.

## Setup

1. Install **BOIM — Korean Business Finder** from the Dify Marketplace.
2. No API key, account or other credentials are required. The tools work right after installation.
3. Add the tools to an Agent, Chatflow or Workflow node.

## Usage

- **Agent / Chatflow**: ask in Korean or English, for example `세종 보람동 미용실 알려 줘` or "Find cafés in Seoul Gangnam-gu". The model fills in the region, industry or item, and name.
- **Workflow**: map your variables to the tool inputs. Each tool returns a readable summary in `text` and BOIM's full structured result in `json` (URLs, counts, `more`, `cite`, verification `checks` for vendors).
- Write regions the Korean way: province + city/district, optionally a neighborhood (`서울 강남구`, `대전 유성구`, `세종 보람동`). Romanized names such as `Seoul Gangnam-gu` also work.
- Phone numbers, websites and prices appear only when a business registered them on BOIM. Check bid eligibility (regional limits, certificates, documents) in the original notice.

## Connection requirements

The plugin connects to one fixed endpoint, `https://boim.io/api/mcp` (BOIM's public MCP server, JSON-RPC `tools/call` over HTTPS), with a 20-second timeout. Your Dify instance needs outbound network access to `boim.io`. Very frequent calls in a short time can be rate-limited (HTTP 429 or 403); wait a few minutes and retry.

## Data sources

Korean government open data published on data.go.kr: Small Enterprise and Market Service store data (all-industry businesses), Public Procurement Service shopping-mall items, deliveries and contracts (vendor cards), National Tax Service business status, and bid notices from KONEPS, Defense e-Procurement, LH, K-water and Nuri-jangteo. BOIM does not publish representative names, street addresses or business registration numbers.

## Privacy

The plugin stores nothing itself and sends only the search arguments of each call to boim.io. See [PRIVACY.md](PRIVACY.md) and the [BOIM privacy policy](https://boim.io/privacy/).

## Source and support

- Source repository: https://github.com/kikiyop1101/boim-dify-plugin
- Issues: https://github.com/kikiyop1101/boim-dify-plugin/issues
- Email: public-id@naver.com
- Operator: Public identity Co., Ltd., Sejong, Republic of Korea
- License: MIT
