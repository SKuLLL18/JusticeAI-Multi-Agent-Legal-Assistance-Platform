import re
from datetime import datetime

class UserAgent:
    """
    User Agent: Receives user complaints and initiates agent coordination.
    This agent acts as the entry point and coordinator for the multi-agent system.
    """
    
    def __init__(self):
        self.name = "User Agent"
        self.description = "Receives and processes user complaints, initiates multi-agent coordination"
        
        # Define issue categories and their keywords
        self.issue_categories = {
            'property_dispute': {
                'keywords': ['landlord', 'tenant', 'rent', 'deposit', 'property', 'house', 'apartment', 'eviction'],
                'description': 'Property and rental disputes'
            },
            'employment_labor': {
                'keywords': ['employer', 'employee', 'salary', 'wages', 'termination', 'workplace', 'harassment', 'overtime'],
                'description': 'Employment and labor law issues'
            },
            'family_law': {
                'keywords': ['divorce', 'custody', 'child', 'marriage', 'alimony', 'maintenance', 'domestic'],
                'description': 'Family law and domestic issues'
            },
            'consumer_rights': {
                'keywords': ['consumer', 'product', 'service', 'refund', 'warranty', 'fraud', 'scam', 'purchase'],
                'description': 'Consumer rights and protection'
            },
            'criminal_law': {
                'keywords': ['crime', 'theft', 'assault', 'harassment', 'stalking', 'cybercrime', 'fraud'],
                'description': 'Criminal law matters'
            },
            'civil_dispute': {
                'keywords': ['contract', 'agreement', 'breach', 'damages', 'compensation', 'neighbor', 'noise'],
                'description': 'Civil disputes and contract issues'
            },
            'financial_debt': {
                'keywords': ['loan', 'debt', 'credit', 'bank', 'mortgage', 'foreclosure', 'bankruptcy'],
                'description': 'Financial and debt-related issues'
            },
            'other': {
                'keywords': [],
                'description': 'Other legal matters'
            }
        }
    
    def process_case(self, case_data):
        """
        Process the user's case and prepare it for other agents
        
        Args:
            case_data (dict): Case information including user details and issue description
            
        Returns:
            dict: Processed case data with additional analysis
        """
        try:
            # Extract case information
            issue_description = case_data.get('issue_description', '').lower()
            issue_category = case_data.get('issue_category', '')
            
            # Analyze the case
            analysis = self._analyze_case(issue_description, issue_category)
            
            # Determine priority level
            priority = self._determine_priority(issue_description, analysis)
            
            # Create processed case data
            processed_case = {
                'original_data': case_data,
                'analysis': analysis,
                'priority_level': priority,
                'processing_timestamp': datetime.now().isoformat(),
                'agent_notes': self._generate_agent_notes(analysis, priority)
            }
            
            return f"Case processed successfully. Category: {analysis['detected_category']}, Priority: {priority}, Keywords detected: {', '.join(analysis['detected_keywords'])}"
            
        except Exception as e:
            return f"Error processing case: {str(e)}"
    
    def _analyze_case(self, issue_description, user_category):
        """
        Analyze the case description to extract relevant information
        
        Args:
            issue_description (str): User's description of the issue
            user_category (str): User-selected category
            
        Returns:
            dict: Analysis results
        """
        detected_keywords = []
        detected_category = user_category
        
        # Check if user category matches detected category
        for category, info in self.issue_categories.items():
            for keyword in info['keywords']:
                if keyword in issue_description:
                    detected_keywords.append(keyword)
                    if not detected_category or detected_category == 'other':
                        detected_category = category
        
        # If no specific category detected, use user's selection
        if not detected_keywords and user_category:
            detected_category = user_category
        
        return {
            'detected_category': detected_category,
            'detected_keywords': detected_keywords,
            'user_category': user_category,
            'word_count': len(issue_description.split()),
            'has_contact_info': self._extract_contact_info(issue_description),
            'urgency_indicators': self._detect_urgency(issue_description)
        }
    
    def _determine_priority(self, issue_description, analysis):
        """
        Determine the priority level of the case
        
        Args:
            issue_description (str): Case description
            analysis (dict): Case analysis results
            
        Returns:
            str: Priority level (low, medium, high, urgent)
        """
        urgency_score = 0
        
        # Check for urgency indicators
        urgency_words = ['urgent', 'emergency', 'immediate', 'asap', 'critical', 'serious']
        for word in urgency_words:
            if word in issue_description.lower():
                urgency_score += 3
        
        # Check for time-sensitive issues
        time_indicators = ['today', 'tomorrow', 'deadline', 'court date', 'hearing']
        for indicator in time_indicators:
            if indicator in issue_description.lower():
                urgency_score += 2
        
        # Check for serious legal categories
        serious_categories = ['criminal_law', 'family_law']
        if analysis['detected_category'] in serious_categories:
            urgency_score += 2
        
        # Check for financial impact
        financial_words = ['money', 'payment', 'salary', 'rent', 'deposit', 'loan']
        for word in financial_words:
            if word in issue_description.lower():
                urgency_score += 1
        
        # Determine priority based on score
        if urgency_score >= 5:
            return 'urgent'
        elif urgency_score >= 3:
            return 'high'
        elif urgency_score >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _extract_contact_info(self, text):
        """
        Extract contact information from the text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Extracted contact information
        """
        contact_info = {
            'phone_numbers': [],
            'emails': [],
            'addresses': []
        }
        
        # Extract phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        contact_info['phone_numbers'] = re.findall(phone_pattern, text)
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        contact_info['emails'] = re.findall(email_pattern, text)
        
        return contact_info
    
    def _detect_urgency(self, text):
        """
        Detect urgency indicators in the text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            list: List of urgency indicators found
        """
        urgency_indicators = []
        
        urgency_patterns = [
            r'\b(urgent|emergency|immediate|asap|critical)\b',
            r'\b(deadline|due date|court date|hearing)\b',
            r'\b(today|tomorrow|this week)\b',
            r'\b(serious|severe|dangerous)\b'
        ]
        
        for pattern in urgency_patterns:
            matches = re.findall(pattern, text.lower())
            urgency_indicators.extend(matches)
        
        return list(set(urgency_indicators))
    
    def _generate_agent_notes(self, analysis, priority):
        """
        Generate notes for other agents
        
        Args:
            analysis (dict): Case analysis
            priority (str): Priority level
            
        Returns:
            str: Agent notes
        """
        notes = []
        
        if analysis['detected_keywords']:
            notes.append(f"Key legal areas: {', '.join(analysis['detected_keywords'])}")
        
        if priority in ['high', 'urgent']:
            notes.append("High priority case - requires immediate attention")
        
        if analysis['has_contact_info']['phone_numbers'] or analysis['has_contact_info']['emails']:
            notes.append("Contact information provided - consider direct communication")
        
        if analysis['urgency_indicators']:
            notes.append(f"Urgency indicators detected: {', '.join(analysis['urgency_indicators'])}")
        
        return '; '.join(notes) if notes else "Standard case processing"
    
    def get_issue_categories(self):
        """
        Get available issue categories for the frontend
        
        Returns:
            dict: Issue categories with descriptions
        """
        return {k: v['description'] for k, v in self.issue_categories.items()}
    
    def validate_case_data(self, case_data):
        """
        Validate the case data before processing
        
        Args:
            case_data (dict): Case data to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        required_fields = ['user_name', 'issue_category', 'issue_description']
        
        for field in required_fields:
            if not case_data.get(field, '').strip():
                return False, f"Missing required field: {field}"
        
        # Validate email if provided
        email = case_data.get('user_email', '').strip()
        if email:
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
            if not re.match(email_pattern, email):
                return False, "Invalid email format"
        
        # Validate description length
        description = case_data.get('issue_description', '').strip()
        if len(description) < 10:
            return False, "Issue description must be at least 10 characters long"
        
        if len(description) > 2000:
            return False, "Issue description must be less than 2000 characters"
        
        return True, "Validation successful" 