# Frankfurter — Foreign Exchange Rates API

## Summary

Frankfurter is a free foreign-exchange API that aggregates rates from central banks and other official sources. Its v2 API supports date-specific and historical queries, currency filters, and provider filters.

By default, the API returns blended mid-market rates. These are useful for broad daily currency coverage, but they are not necessarily identical to the official rate published by a particular African central bank. Where a specific provider is required, use the provider filter and verify that the provider publishes the requested currency and date.

## Owner

- **Service:** Frankfurter
- **Documentation:** https://frankfurter.dev/
- **Currency catalogue:** https://frankfurter.dev/currencies/
- **API base URL:** https://api.frankfurter.dev/

## Documentation

- **Main documentation:** https://frankfurter.dev/
- **Currency catalogue:** https://frankfurter.dev/currencies/
- **API endpoint family:** `/v2/rates`

## Domain

Daily foreign-exchange reference rates, historical rates, and currency/provider coverage.

## Access method

REST API over HTTPS.

Example request:

```bash
curl -sS \
  "https://api.frankfurter.dev/v2/rates?base=USD&quotes=NGN,KES,EGP,ZAR,CDF"