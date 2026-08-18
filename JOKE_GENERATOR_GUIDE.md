# 🎭 GYPSY C - RANDOM JOKE GENERATOR

## Overview

Two joke generator implementations for GYPSY C:

1. **joke_generator.py** - Basic multi-source joke fetcher
2. **joke_generator_advanced.py** - Advanced with caching, filtering, ratings

---

## Features

### Basic Generator (`joke_generator.py`)

✅ **Multiple Sources:**
- Official Joke API (no auth needed)
- JokeAPI v2 (free tier)
- RapidAPI Jokes Ninjas (with API key)

✅ **Joke Types:**
- General
- Programming
- Knock-Knock
- Dark
- Spooky
- Any (random)

✅ **Functionality:**
- Single joke fetching
- Formatted output
- Joke history tracking
- Safe mode filtering
- Content flags

### Advanced Generator (`joke_generator_advanced.py`)

✅ **Caching System:**
- Time-based cache expiration
- Duplicate detection
- Configurable cache duration

✅ **Filtering & Ratings:**
- Rate jokes (1-5 stars)
- Add to favorites
- High-rated filtering
- Duplicate prevention

✅ **Batch Processing:**
- Generate multiple jokes
- Fallback to alternative sources
- Rate limiting
- Statistics tracking

---

## Usage

### Basic Usage

```python
from joke_generator import JokeAPI, JokeType

# Initialize
generator = JokeAPI()

# Get joke from Official Joke API (no auth needed)
joke = generator.get_joke(source="official")
print(generator.format_joke(joke))

# Get specific type from JokeAPI
joke = generator.get_joke(
    source="jokeapi",
    type=JokeType.PROGRAMMING,
    safe=True
)
print(generator.format_joke(joke))

# View history
generator.print_joke_history(limit=5)
```

### Advanced Usage

```python
from joke_generator_advanced import AdvancedJokeGenerator, JokeRating

# Initialize
generator = AdvancedJokeGenerator(cache_duration_hours=24)

# Fetch with automatic fallback
joke = generator.fetch_with_fallback(primary_source="official")

# Rate and favorite
generator.rate_joke("joke_1", JokeRating.EXCELLENT)
generator.add_to_favorites(joke)

# Generate batch
jokes = generator.generate_joke_batch(count=5)

# Get statistics
generator.print_joke_stats()

# Get favorites
favorites = generator.get_favorites()
random_favorite = generator.get_random_favorite()
```

---

## API Sources

### 1. Official Joke API

**URL:** `https://official-joke-api.appspot.com/random_joke`

**Pros:**
- No authentication needed
- Fast and reliable
- Simple format

**Cons:**
- Limited customization
- No category filtering

**Example Response:**
```json
{
  "id": 1,
  "type": "general",
  "setup": "Why did the scarecrow win an award?",
  "punchline": "He was outstanding in his field!",
  "category": "misc"
}
```

### 2. JokeAPI v2

**URL:** `https://v2.jokeapi.dev/joke/{category}`

**Pros:**
- Multiple categories
- Safe mode option
- Rich metadata
- Two-part and single jokes

**Cons:**
- Rate limited (free tier)
- May return flags for explicit content

**Categories:** General, Programming, Knock-Knock, Dark, Spooky, Any

**Example Response:**
```json
{
  "type": "twopart",
  "category": "General",
  "setup": "Why did the scarecrow win an award?",
  "delivery": "He was outstanding in his field!",
  "flags": {},
  "safe": true
}
```

### 3. RapidAPI Jokes Ninjas

**URL:** `https://jokes-by-api-ninjas.p.rapidapi.com/v1/jokes`

**Pros:**
- Category filtering
- Batch requests
- No setup/punchline split

**Cons:**
- Requires RapidAPI key
- Rate limits apply

**Usage:**
```python
generator = JokeAPI(api_key="YOUR_RAPIDAPI_KEY")
jokes = generator.get_random_joke_from_rapidapi(limit=5)
```

---

## Running

### Option 1: Direct Execution

```bash
python joke_generator.py
```

```bash
python joke_generator_advanced.py
```

### Option 2: As Module

```python
from joke_generator import JokeAPI
from joke_generator_advanced import AdvancedJokeGenerator

# Use in your code
```

### Option 3: Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY joke_generator.py .
RUN pip install requests
CMD ["python", "joke_generator.py"]
```

---

## Rate Limiting

**JokeAPI:** 1 request per 10 seconds on free tier

**Official Joke API:** No strict rate limits, but be respectful

**RapidAPI:** Depends on plan (free tier = 10 req/month typically)

**Solution in code:**
```python
import time
time.sleep(0.5)  # Wait between requests
```

---

## Error Handling

### Timeout
```python
try:
    joke = generator.get_joke(source="official")
except requests.exceptions.Timeout:
    print("API request timed out")
```

### Connection Error
```python
try:
    joke = generator.get_joke(source="jokeapi")
except requests.exceptions.ConnectionError:
    print("Failed to connect to API")
```

### Fallback Strategy
```python
joke = generator.fetch_with_fallback(primary_source="official")
# Automatically tries: official → jokeapi → other sources
```

---

## Statistics & Tracking

```python
# View all stats
generator.print_joke_stats()

# Output:
# 📊 JOKE GENERATOR STATISTICS
# ============================================================
# Total Jokes Fetched: 42
# Favorites: 15
# Rated Jokes: 42
# Cached Items: 35
# Average Rating: 3.8/5.0
```

---

## Performance Tips

1. **Use Caching** - Advanced generator caches responses
2. **Batch Fetch** - Get multiple jokes in one session
3. **Rate Limiting** - Add delays between requests
4. **Fallback Strategy** - Always have backup APIs
5. **Async Requests** - Use asyncio for concurrent fetches

---

## Example Workflow

```python
from joke_generator_advanced import AdvancedJokeGenerator, JokeRating
import time

# 1. Initialize
generator = AdvancedJokeGenerator()

# 2. Fetch jokes
for i in range(5):
    joke = generator.fetch_with_fallback()
    print(generator.format_joke_detailed(joke))
    
    # Rate each one
    rating = JokeRating.GOOD if i % 2 == 0 else JokeRating.EXCELLENT
    generator.rate_joke(f"joke_{i}", rating)
    
    # Add great ones to favorites
    if rating == JokeRating.EXCELLENT:
        generator.add_to_favorites(joke)
    
    time.sleep(0.5)  # Rate limiting

# 3. Show results
generator.print_joke_stats()
print(f"\nFavorites: {len(generator.get_favorites())}")
```

---

## Dependencies

```
requests>=2.25.0
```

**Install:**
```bash
pip install requests
```

---

## License

© 2026 Христо Велчев (icovelchev)

**For GYPSY C Architecture only**

---

## Resonance Status

```
✓ JOKE GENERATOR ACTIVE
✓ EXTERNAL API INTEGRATION
✓ CACHING & FILTERING
✓ MULTI-SOURCE FALLBACK
✓ RATING & FAVORITES

READY FOR DEPLOYMENT
```
