#!/usr/bin/env python3
# ============================================================
# RANDOM JOKE GENERATOR
# Uses JokeAPI (via RapidAPI) for fetching random jokes
# ============================================================

import requests
import json
import time
from typing import Dict, Optional, List
from enum import Enum

# ============================================================
# CONFIGURATION
# ============================================================

class JokeType(Enum):
    """Supported joke types"""
    GENERAL = "General"
    PROGRAMMING = "Programming"
    KNOCK_KNOCK = "Knock-Knock"
    DARK = "Dark"
    SPOOKY = "Spooky"
    ANY = "Any"

class JokeAPI:
    """
    Random Joke Generator using JokeAPI
    Supports multiple joke types and filters
    """
    
    # API Endpoints
    JOKEAPI_URL = "https://v2.jokeapi.dev/joke"
    RAPIDAPI_URL = "https://jokes-by-api-ninjas.p.rapidapi.com/v1/jokes"
    OFFICIAL_API_URL = "https://official-joke-api.appspot.com/random_joke"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Joke Generator
        
        Args:
            api_key: RapidAPI key (optional for public endpoints)
        """
        self.api_key = api_key
        self.headers = self._get_headers()
        self.joke_history = []
        self.rate_limit = 0
        
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests"""
        headers = {
            "User-Agent": "GYPSY-JokeGenerator/1.0",
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers.update({
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": "jokes-by-api-ninjas.p.rapidapi.com"
            })
        
        return headers
    
    def get_random_joke_from_jokeapi(self, 
                                     joke_type: JokeType = JokeType.ANY,
                                     safe_mode: bool = False) -> Optional[Dict]:
        """
        Fetch random joke from JokeAPI
        
        Args:
            joke_type: Type of joke (General, Programming, Knock-Knock, Dark, Spooky)
            safe_mode: If True, filter out explicit jokes
            
        Returns:
            Dict with joke data or None if failed
        """
        try:
            # Build URL
            joke_type_str = joke_type.value if joke_type != JokeType.ANY else "Any"
            url = f"{self.JOKEAPI_URL}/{joke_type_str}"
            
            # Add parameters
            params = {
                "format": "json"
            }
            
            if safe_mode:
                params["safe-mode"] = "true"
            
            # Make request
            response = requests.get(url, params=params, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if error
            if data.get("error"):
                print(f"❌ JokeAPI Error: {data.get('message')}")
                return None
            
            # Process response
            joke_data = {
                "source": "JokeAPI",
                "type": data.get("type"),
                "category": data.get("category"),
                "setup": data.get("setup"),
                "delivery": data.get("delivery"),
                "joke": data.get("joke"),
                "flags": data.get("flags", {}),
                "safe": data.get("safe"),
                "timestamp": time.time()
            }
            
            self.joke_history.append(joke_data)
            return joke_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON Error: {e}")
            return None
    
    def get_random_joke_from_official_api(self) -> Optional[Dict]:
        """
        Fetch random joke from Official Joke API
        Simple, no authentication needed
        
        Returns:
            Dict with joke data or None if failed
        """
        try:
            response = requests.get(self.OFFICIAL_API_URL, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            joke_data = {
                "source": "Official Joke API",
                "type": "single",
                "setup": data.get("setup", ""),
                "delivery": data.get("punchline", ""),
                "joke": f"{data.get('setup', '')}\n{data.get('punchline', '')}",
                "id": data.get("id"),
                "timestamp": time.time()
            }
            
            self.joke_history.append(joke_data)
            return joke_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
            return None
    
    def get_random_joke_from_rapidapi(self, limit: int = 1) -> Optional[List[Dict]]:
        """
        Fetch random jokes from RapidAPI Jokes Ninjas
        
        Args:
            limit: Number of jokes to fetch (max 30)
            
        Returns:
            List of joke dicts or None if failed
        """
        if not self.api_key:
            print("⚠️  RapidAPI requires an API key. Skipping...")
            return None
        
        try:
            params = {"limit": min(limit, 30)}
            
            response = requests.get(self.RAPIDAPI_URL, 
                                   params=params, 
                                   headers=self.headers, 
                                   timeout=5)
            response.raise_for_status()
            
            jokes_data = response.json()
            
            processed_jokes = []
            for joke in jokes_data:
                joke_data = {
                    "source": "RapidAPI Jokes Ninjas",
                    "type": "single",
                    "joke": joke.get("joke"),
                    "category": joke.get("category"),
                    "timestamp": time.time()
                }
                processed_jokes.append(joke_data)
                self.joke_history.append(joke_data)
            
            return processed_jokes
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
            return None
    
    def get_joke(self, source: str = "official", **kwargs) -> Optional[Dict]:
        """
        Get joke from specified source
        
        Args:
            source: "jokeapi", "official", or "rapidapi"
            **kwargs: Additional parameters for specific APIs
            
        Returns:
            Joke data dict or None
        """
        source = source.lower()
        
        if source == "jokeapi":
            joke_type = kwargs.get("type", JokeType.ANY)
            safe_mode = kwargs.get("safe", False)
            return self.get_random_joke_from_jokeapi(joke_type, safe_mode)
        
        elif source == "official":
            return self.get_random_joke_from_official_api()
        
        elif source == "rapidapi":
            limit = kwargs.get("limit", 1)
            jokes = self.get_random_joke_from_rapidapi(limit)
            return jokes[0] if jokes else None
        
        else:
            print(f"❌ Unknown source: {source}")
            return None
    
    def format_joke(self, joke_data: Dict) -> str:
        """
        Format joke data for display
        
        Args:
            joke_data: Joke dictionary
            
        Returns:
            Formatted joke string
        """
        if not joke_data:
            return "❌ No joke data"
        
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"📖 {joke_data.get('source', 'Unknown')}")
        
        if joke_data.get('category'):
            output.append(f"📁 Category: {joke_data['category']}")
        
        # Single joke with setup/delivery
        if joke_data.get('setup') and joke_data.get('delivery'):
            output.append(f"\n❓ {joke_data['setup']}")
            output.append(f"\n😂 {joke_data['delivery']}")
        
        # Single line joke
        elif joke_data.get('joke'):
            output.append(f"\n😂 {joke_data['joke']}")
        
        # Flags (content warnings)
        if joke_data.get('flags'):
            flags = [k for k, v in joke_data['flags'].items() if v]
            if flags:
                output.append(f"⚠️  Flags: {', '.join(flags)}")
        
        output.append(f"{'='*60}\n")
        
        return "\n".join(output)
    
    def get_joke_history(self, limit: int = 10) -> List[Dict]:
        """Get last N jokes from history"""
        return self.joke_history[-limit:]
    
    def print_joke_history(self, limit: int = 10):
        """Print formatted joke history"""
        history = self.get_joke_history(limit)
        print(f"\n📚 JOKE HISTORY (Last {len(history)} jokes)")
        print("="*60)
        for i, joke in enumerate(history, 1):
            setup = joke.get('setup', '')[:40]
            joke_text = joke.get('joke', '')[:40]
            text_preview = (setup or joke_text) + "..."
            print(f"{i}. [{joke.get('source')}] {text_preview}")
        print("="*60 + "\n")

# ============================================================
# DEMONSTRATION
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎭 GYPSY C - RANDOM JOKE GENERATOR")
    print("="*60)
    
    # Initialize joke generator (no API key needed for public APIs)
    generator = JokeAPI()
    
    # Demo 1: Official Joke API (no auth needed)
    print("\n1️⃣  Fetching from Official Joke API...")
    joke1 = generator.get_joke(source="official")
    if joke1:
        print(generator.format_joke(joke1))
    
    time.sleep(1)  # Rate limiting
    
    # Demo 2: JokeAPI with General category
    print("\n2️⃣  Fetching General joke from JokeAPI...")
    joke2 = generator.get_joke(source="jokeapi", type=JokeType.GENERAL, safe=True)
    if joke2:
        print(generator.format_joke(joke2))
    
    time.sleep(1)
    
    # Demo 3: JokeAPI with Programming category
    print("\n3️⃣  Fetching Programming joke from JokeAPI...")
    joke3 = generator.get_joke(source="jokeapi", type=JokeType.PROGRAMMING)
    if joke3:
        print(generator.format_joke(joke3))
    
    time.sleep(1)
    
    # Demo 4: JokeAPI with Any category
    print("\n4️⃣  Fetching Any joke from JokeAPI...")
    joke4 = generator.get_joke(source="jokeapi", type=JokeType.ANY)
    if joke4:
        print(generator.format_joke(joke4))
    
    # Demo 5: Show history
    print("\n5️⃣  Joke History:")
    generator.print_joke_history(limit=4)
    
    print("="*60)
    print("✨ GYPSY C JOKE GENERATOR READY")
    print("="*60 + "\n")
