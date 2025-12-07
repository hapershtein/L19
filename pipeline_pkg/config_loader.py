"""
Configuration loading and validation
"""
import json
import os


class ConfigLoader:
    """Load and validate pipeline configuration"""

    @staticmethod
    def load_config(config_file):
        """
        Load and validate JSON configuration

        Args:
            config_file: Path to JSON configuration file

        Returns:
            Loaded configuration dictionary
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

        with open(config_file, 'r') as f:
            config = json.load(f)

        if 'searches' not in config:
            raise ValueError("Configuration must contain 'searches' array")

        if not isinstance(config['searches'], list):
            raise ValueError("'searches' must be an array")

        if len(config['searches']) == 0:
            raise ValueError("'searches' array cannot be empty")

        for i, search in enumerate(config['searches']):
            if 'query' not in search:
                raise ValueError(f"Search #{i+1} is missing required 'query' field")

        print(f"Loaded configuration with {len(config['searches'])} search(es)")
        return config

    @staticmethod
    def validate_search(search, index):
        """
        Validate a single search configuration

        Args:
            search: Search configuration dictionary
            index: Index of the search in the config

        Returns:
            Dictionary with validated and default values
        """
        validated = {
            'name': search.get('name', f'Search {index + 1}'),
            'query': search['query'],
            'output': search.get('output', f'search_{index + 1}.xlsx'),
            'max_results': search.get('max_results', 100)
        }

        if not isinstance(validated['max_results'], int) or validated['max_results'] < 1:
            print(f"Warning: Invalid max_results for '{validated['name']}', using default 100")
            validated['max_results'] = 100

        return validated
