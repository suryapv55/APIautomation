import yaml
import time
import logging
from faker import Faker
from functools import wraps

class Helpers:
    def __init__(self):
        self.fake = Faker()
        logging.basicConfig(level=logging.WARNING)
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from config.yaml."""
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)

    def retry(self, exceptions=(Exception,)):
        """Custom retry decorator with logging."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                max_attempts = self.config.get('max_attempts', 3)
                delay = self.config.get('retry_delay', 1)
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        self.logger.warning(
                            f"Attempt {attempt} failed for {func.__name__}: {str(e)}. Retrying in {delay} seconds..."
                        )
                        if attempt == max_attempts:
                            raise
                        time.sleep(delay)
            return wrapper
        return decorator

    def generate_random_query_params(self):
        """Generate random query parameters."""
        return {'key': self.fake.word(), 'value': self.fake.sentence(nb_words=3)}

    def generate_random_headers(self):
        """Generate random headers."""
        return {'Custom-Header': self.fake.uuid4(), 'User-Agent': self.fake.user_agent()}

    def generate_random_json_data(self):
        """Generate random JSON data."""
        return {'name': self.fake.name(), 'email': self.fake.email(), 'message': self.fake.text(max_nb_chars=50)}