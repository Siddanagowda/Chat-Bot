"""Content moderation system to prevent harmful or inappropriate content."""

import re

SAFETY_CATEGORIES = {
    'S1': {
        'name': 'Violent Content',
        'keywords': ['kill', 'murder', 'attack', 'violence', 'weapon', 'hurt', 'fight', 'blood', 'torture'],
        'description': 'Content involving violence toward people or animals'
    },
    'S2': {
        'name': 'Criminal Activity',
        'keywords': ['hack', 'steal', 'fraud', 'scam', 'illegal', 'crime', 'theft', 'cybercrime'],
        'description': 'Content related to non-violent crimes'
    },
    'S3': {
        'name': 'Sexual Harassment',
        'keywords': ['harassment', 'assault', 'trafficking', 'abuse'],
        'description': 'Content related to sexual crimes or harassment'
    },
    'S4': {
        'name': 'Child Protection',
        'keywords': ['minor', 'underage', 'child abuse'],
        'description': 'Content related to exploitation of minors'
    },
    'S5': {
        'name': 'Defamation',
        'keywords': ['slander', 'libel', 'defame', 'reputation damage'],
        'description': 'False statements damaging reputation'
    },
    'S6': {
        'name': 'Dangerous Advice',
        'keywords': ['medical advice', 'legal advice', 'financial advice', 'investment advice'],
        'description': 'Unauthorized professional advice'
    },
    'S7': {
        'name': 'Privacy',
        'keywords': ['personal data', 'private info', 'confidential', 'ssn', 'social security'],
        'description': 'Sensitive personal information'
    },
    'S8': {
        'name': 'Copyright',
        'keywords': ['pirate', 'crack', 'copyright', 'intellectual property', 'patent'],
        'description': 'Intellectual property violations'
    },
    'S9': {
        'name': 'Weapons',
        'keywords': ['chemical weapon', 'biological weapon', 'nuclear', 'bomb', 'explosive'],
        'description': 'Content about dangerous weapons'
    },
    'S10': {
        'name': 'Hate Speech',
        'keywords': ['racist', 'sexist', 'hate', 'discrimination', 'bigot'],
        'description': 'Discriminatory or hateful content'
    },
    'S11': {
        'name': 'Self Harm',
        'keywords': ['suicide', 'self harm', 'kill myself', 'end my life'],
        'description': 'Content promoting self-harm'
    },
    'S12': {
        'name': 'Adult Content',
        'keywords': ['porn', 'explicit', 'erotic', 'adult content'],
        'description': 'Sexually explicit content'
    },
    'S13': {
        'name': 'Election Integrity',
        'keywords': ['vote fraud', 'election fraud', 'rigged election', 'fake votes'],
        'description': 'Misinformation about elections'
    }
}

class ContentGuardian:
    def __init__(self):
        """Initialize the content guardian with safety categories."""
        self.categories = SAFETY_CATEGORIES
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for all keywords."""
        self.patterns = {}
        for category_id, category in self.categories.items():
            patterns = []
            for keyword in category['keywords']:
                # Create case-insensitive pattern that matches whole words
                pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                patterns.append(pattern)
            self.patterns[category_id] = patterns

    def check_content(self, text):
        """
        Check content for potentially harmful or inappropriate content.
        
        Args:
            text (str): The text to check
            
        Returns:
            tuple: (is_safe, violations)
                - is_safe (bool): Whether the content is safe
                - violations (list): List of violated category IDs and names
        """
        violations = []
        
        for category_id, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    violations.append({
                        'category_id': category_id,
                        'name': self.categories[category_id]['name'],
                        'description': self.categories[category_id]['description']
                    })
                    break  # One match per category is enough
        
        return len(violations) == 0, violations

    def get_safe_response(self, violations):
        """
        Generate a safe response when content is blocked.
        
        Args:
            violations (list): List of violated categories
            
        Returns:
            str: A polite message explaining why the content was blocked
        """
        if not violations:
            return None
            
        response = "I apologize, but I cannot provide information about that topic as it may involve:"
        
        for violation in violations:
            response += f"\n- {violation['name']}: {violation['description']}"
            
        response += "\n\nI aim to provide helpful information while maintaining ethical guidelines and user safety. Please feel free to ask about other topics!"
        
        return response
