# Day 4 — Python: Files, JSON & APIs

## What I did
- Read/wrote files with open() and context managers
- Parsed and created JSON with the json module
- Made live API calls with requests
- Used try/except for error handling
- Built a K8s pod status logger that ties it all together

## What I learned
- (fill in)

## What confused me
- (fill in)

## Code I want to remember
- Context manager: with open("file.json", "r") as f:
- JSON round-trip: json.dump(data, f, indent=2) / json.load(f)
- Memory trick: `s` in loads/dumps = string, no `s` = file
- API call: response = requests.get(url) → response.json()
- Error handling: try: / except SomeError:
