#!/usr/bin/env python3
# ============================================================
# ADVANCED JOKE GENERATOR WITH FILTERING & CACHING
# ============================================================

import requests
import json
import time
import random
from typing import Dict, Optional, List, Set
from datetime import datetime, timedelta
from enum import Enum
import hashlib

class JokeRating(Enum):
    """Joke rating system"""
    TERRIBLE = 1
    BAD = 2
    OKAY = 3
    GOOD = 4
    EXCELLENT = 5

class AdvancedJokeGenerator:
    """
    Advanced Joke Generator with:
    - Caching system
    - Joke filtering
    - Rating system
    - Duplicate detection
    - Multi-source fallback
    """
    
    JOKEAPI_URL = "https://v2.jokeapi.dev/joke"
    OFFICIAL_API_URL = "https://official-joke-api.appspot.com/random_joke"
    
    def __init__(self, cache_duration_hours: int = 24):
        self.cache = {}
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.joke_ratings = {}
        self.seen_jokes: Set[str] = set()
        self.favorites = []
        
    def _get_joke_hash(self, joke_data: Dict) -> str:
        """Generate hash for duplicate detection"""
        joke_text = f"{joke_data.get('setup', '')}{joke_data.get('delivery', '')}"
        return hashlib.md5(joke_text.encode()).hexdigest()
    
    def _is_cached_valid(self, cache_key: str) -> bool:
        """Check if cached item is still valid"""
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key]["timestamp"]
        if datetime.now() - cached_time > self.cache_duration:
            del self.cache[cache_key]
            return False
        
        return True
    
    def _cache_joke(self, cache_key: str, joke_data: Dict):
        """Cache joke data"""
        self.cache[cache_key] = {
            "joke": joke_data,
            "timestamp": datetime.now()
        }
    
    def get_cached_joke(self, cache_key: str) -> Optional[Dict]:
        """Get joke from cache"""
        if self._is_cached_valid(cache_key):
            return self.cache[cache_key]["joke"]
        return None
    
    def fetch_with_fallback(self, primary_source: str = "official") -> Optional[Dict]:
        """
        Fetch joke with fallback to other sources
        
        Args:
            primary_source: Preferred source ("official" or "jokeapi")
            
        Returns:
            Joke data or None
        """
        sources = [primary_source, "jokeapi", "official"]
        sources = list(dict.fromkeys(sources))  # Remove duplicates, keep order
        
        for source in sources:
            try:
                if source == "official":
                    joke = self._fetch_from_official_api()
                elif source == "jokeapi":
                    joke = self._fetch_from_jokeapi()
                else:
                    continue
                
                if joke:
                    return joke
            except Exception as e:
                print(f"⚠️  {source} failed: {e}")
                continue
        
        return None
    
    def _fetch_from_official_api(self) -> Optional[Dict]:
        """Fetch from Official Joke API"""
        try:
            response = requests.get(self.OFFICIAL_API_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            joke_data = {
                "source": "Official Joke API",
                "setup": data.get("setup"),
                "delivery": data.get("punchline"),
                "id": data.get("id"),
                "type": "two-part",
                "timestamp": time.time()
            }
            
            joke_hash = self._get_joke_hash(joke_data)
            
            if joke_hash in self.seen_jokes:
                return None  # Duplicate
            
            self.seen_jokes.add(joke_hash)
            return joke_data
            
        except Exception as e:
            raise e
    
    def _fetch_from_jokeapi(self) -> Optional[Dict]:
        """Fetch from JokeAPI"""
        try:
            categories = ["General", "Programming", "Knock-Knock"]
            category = random.choice(categories)
            
            url = f"{self.JOKEAPI_URL}/{category}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("error"):
                return None
            
            joke_data = {
                "source": f"JokeAPI ({category})",
                "setup": data.get("setup"),
                "delivery": data.get("delivery"),
                "joke": data.get("joke"),
                "category": data.get("category"),
                "type": data.get("type"),
                "timestamp": time.time()
            }
            
            joke_hash = self._get_joke_hash(joke_data)
            
            if joke_hash in self.seen_jokes:
                return None  # Duplicate
            
            self.seen_jokes.add(joke_hash)
            return joke_data
            
        except Exception as e:
            raise e
    
    def rate_joke(self, joke_id: str, rating: JokeRating):
        """Rate a joke"""
        self.joke_ratings[joke_id] = rating
    
    def add_to_favorites(self, joke_data: Dict):
        """Add joke to favorites"""
        self.favorites.append(joke_data)
    
    def get_favorites(self) -> List[Dict]:
        """Get all favorite jokes"""
        return self.favorites
    
    def get_random_favorite(self) -> Optional[Dict]:
        """Get random favorite joke"""
        return random.choice(self.favorites) if self.favorites else None
    
    def get_high_rated_jokes(self, min_rating: JokeRating = JokeRating.GOOD) -> List[str]:
        """Get jokes with high ratings"""
        return [jid for jid, rating in self.joke_ratings.items() 
                if rating.value >= min_rating.value]
    
    def format_joke_detailed(self, joke_data: Dict) -> str:
        """Format joke with detailed information"""
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"📖 Source: {joke_data.get('source', 'Unknown')}")
        output.append(f"📁 Type: {joke_data.get('type', 'Unknown')}")
        
        if joke_data.get('setup') and joke_data.get('delivery'):
            output.append(f"\n❓ {joke_data['setup']}")
            output.append(f"😂 {joke_data['delivery']}")
        elif joke_data.get('joke'):
            output.append(f"\n😂 {joke_data['joke']}")
        
        output.append(f"{'='*60}\n")
        return "\n".join(output)
    
    def generate_joke_batch(self, count: int = 5) -> List[Dict]:
        """Generate multiple jokes"""
        jokes = []
        for _ in range(count):
            joke = self.fetch_with_fallback()
            if joke:
                jokes.append(joke)
            time.sleep(0.5)  # Rate limiting
        return jokes
    
    def print_joke_stats(self):
        """Print statistics"""
        print(f"\n📊 JOKE GENERATOR STATISTICS")
        print(f"{'='*60}")
        print(f"Total Jokes Fetched: {len(self.seen_jokes)}")
        print(f"Favorites: {len(self.favorites)}")
        print(f"Rated Jokes: {len(self.joke_ratings)}")
        print(f"Cached Items: {len(self.cache)}")
        
        if self.joke_ratings:
            avg_rating = sum(r.value for r in self.joke_ratings.values()) / len(self.joke_ratings)
            print(f"Average Rating: {avg_rating:.1f}/5.0")
        
        print(f"{'='*60}\n")

# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎭 ADVANCED JOKE GENERATOR WITH CACHING & FILTERING")
    print("="*60)
    
    generator = AdvancedJokeGenerator(cache_duration_hours=24)
    
    # Generate batch of jokes
    print("\n🔄 Generating 3 jokes with fallback...")
    jokes = generator.generate_joke_batch(count=3)
    
    for i, joke in enumerate(jokes, 1):
        print(f"\nJoke #{i}:")
        print(generator.format_joke_detailed(joke))
        
        # Rate the joke
        rating = random.choice(list(JokeRating))
        joke_id = f"joke_{i}"
        generator.rate_joke(joke_id, rating)
        print(f"Rating: {rating.name} ({rating.value}/5)")
        
        # Add to favorites if good
        if rating.value >= JokeRating.GOOD.value:
            generator.add_to_favorites(joke)
            print("⭐ Added to favorites!")
    
    # Print statistics
    generator.print_joke_stats()
    
    # Show favorites
    if generator.get_favorites():
        print(f"\n❤️  FAVORITE JOKES ({len(generator.get_favorites())})")
        for fav in generator.get_favorites():
            print(generator.format_joke_detailed(fav))
    
    print("="*60)
    print("✨ ADVANCED JOKE GENERATOR READY")
    print("="*60 + "\n")
