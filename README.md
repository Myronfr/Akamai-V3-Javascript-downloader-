# Akamai Script for v3 sensor 

Extract Akamai v3 from every site 

## Install

```bash
pip install curl_cffi
```



### Options

- `--url` - Target URL (required)
- `--output` - Output file (default: `akamai_script.js`)

## Features

- curl_cffi still massive 🥺
- Cookie seeds for vm  `data/cookies.txt`
- Request logs in `data/timestamps.txt`
- Auto-detects last script before `</body>` tag

## Example

```bash
python test.py --url https://example.com --output script.js
```

Output:
```
[+] chrome110
[+] /path
[+] 389613 bytes -> akamai_script.js
```

