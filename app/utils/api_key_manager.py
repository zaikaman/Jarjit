from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Optional

class APIKeyManager:
    def __init__(self):
        self.api_keys = []
        self.current_index = 0
        self.rate_limited_keys = {}  # Dictionary to store rate-limited keys and their reset times
        self.load_api_keys()

    def load_api_keys(self) -> None:
        api_keys_file = Path(__file__).resolve().parent.parent / 'resources' / 'api_keys.json'
        if api_keys_file.exists():
            with open(api_keys_file, 'r') as f:
                self.api_keys = json.load(f)

    def get_next_available_key(self) -> Optional[str]:
        if not self.api_keys:
            return None

        # Try to find a non-rate-limited key
        attempts = len(self.api_keys)
        while attempts > 0:
            key = self.api_keys[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.api_keys)
            
            # Check if key is rate limited
            if key in self.rate_limited_keys:
                reset_time = self.rate_limited_keys[key]
                if datetime.now() > reset_time:
                    # Key is no longer rate limited
                    del self.rate_limited_keys[key]
                    return key
            else:
                return key
                
            attempts -= 1
            
        return None

    def mark_key_rate_limited(self, key: str) -> None:
        # Mark key as rate limited for 24 hours
        self.rate_limited_keys[key] = datetime.now() + timedelta(hours=24) 