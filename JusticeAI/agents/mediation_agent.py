import random
from datetime import datetime

class MediationAgent:
    """
    Mediation Agent: Recommends non-legal peaceful resolutions using past case-based reasoning.
    Focuses on alternative dispute resolution methods and conflict resolution strategies.
    """
    
    def __init__(self):
        self.name = "Mediation Agent"
        self.description = "Recommends peaceful resolutions and alternative dispute resolution methods"
        
        # Case-based reasoning database - past successful resolutions
        self.case_database = {
            'property_dispute': {
                'landlord_tenant_deposit': [
                    {
                        'scenario': 'Deposit not returned after vacating',
                        'successful_resolutions': [
                            'Direct communication with landlord via email/letter',
                            'Mediation through housing authority',
                            'Small claims court as last resort',
                            'Documentation of property condition',
                            'Third-party escrow service for future deposits'
                        ],
                        'success_rate': 0.85,
                        'avg_resolution_time': '30 days'
                    }
                ],
                'rent_increase': [
                    {
                        'scenario': 'Unreasonable rent increase',
                        'successful_resolutions': [
                            'Negotiation with landlord',
                            'Review of local rent control laws',
                            'Mediation through tenant association',
                            'Documentation of market rates',
                            'Gradual increase proposal'
                        ],
                        'success_rate': 0.75,
                        'avg_resolution_time': '45 days'
                    }
                ]
            },
            'employment_labor': {
                'wage_dispute': [
                    {
                        'scenario': 'Unpaid overtime or wages',
                        'successful_resolutions': [
                            'Direct discussion with supervisor/HR',
                            'Internal grievance procedure',
                            'Mediation through labor board',
                            'Documentation of hours worked',
                            'Payment plan negotiation'
                        ],
                        'success_rate': 0.80,
                        'avg_resolution_time': '60 days'
                    }
                ],
                'workplace_conflict': [
                    {
                        'scenario': 'Interpersonal workplace conflicts',
                        'successful_resolutions': [
                            'Direct communication with colleague',
                            'HR mediation session',
                            'Conflict resolution training',
                            'Department transfer if necessary',
                            'Professional counseling referral'
                        ],
                        'success_rate': 0.90,
                        'avg_resolution_time': '30 days'
                    }
                ]
            },
            'consumer_rights': {
                'product_issue': [
                    {
                        'scenario': 'Defective product or poor service',
                        'successful_resolutions': [
                            'Direct contact with customer service',
                            'Escalation to management',
                            'Social media complaint',
                            'Better Business Bureau complaint',
                            'Alternative dispute resolution program'
                        ],
                        'success_rate': 0.70,
                        'avg_resolution_time': '15 days'
                    }
                ]
            },
            'family_law': {
                'custody_communication': [
                    {
                        'scenario': 'Co-parenting communication issues',
                        'successful_resolutions': [
                            'Family mediation sessions',
                            'Co-parenting counseling',
                            'Communication apps for coordination',
                            'Neutral third-party involvement',
                            'Structured parenting plan'
                        ],
                        'success_rate': 0.85,
                        'avg_resolution_time': '90 days'
                    }
                ]
            }
        }
        
        # General mediation strategies
        self.general_strategies = {
            'communication': [
                'Active listening techniques',
                'I-message communication',
                'Scheduled discussion times',
                'Written communication for clarity',
                'Third-party facilitation'
            ],
            'negotiation': [
                'Interest-based negotiation',
                'Win-win solution seeking',
                'Compromise identification',
                'Alternative option exploration',
                'Future-focused discussions'
            ],
            'documentation': [
                'Written agreements',
                'Action item tracking',
                'Progress monitoring',
                'Follow-up scheduling',
                'Outcome documentation'
            ]
        }
    
    def suggest_resolution(self, case_data):
        """
        Suggest peaceful resolution strategies based on case analysis
        
        Args:
            case_data (dict): Case information including issue details
            
        Returns:
            str: Comprehensive mediation suggestions
        """
        try:
            issue_category = case_data.get('issue_category', '')
            issue_description = case_data.get('issue_description', '').lower()
            priority_level = case_data.get('priority_level', 'medium')
            
            # Get case-based suggestions
            case_based_suggestions = self._get_case_based_suggestions(issue_category, issue_description)
            
            # Get general mediation strategies
            general_strategies = self._get_general_strategies(priority_level)
            
            # Get escalation prevention tips
            escalation_prevention = self._get_escalation_prevention_tips(issue_category, priority_level)
            
            # Combine all suggestions
            combined_suggestions = self._combine_suggestions(
                case_based_suggestions, 
                general_strategies, 
                escalation_prevention,
                priority_level
            )
            
            return combined_suggestions
            
        except Exception as e:
            return f"Error generating mediation suggestions: {str(e)}"
    
    def _get_case_based_suggestions(self, category, description):
        """
        Get case-based resolution suggestions from past successful cases
        
        Args:
            category (str): Issue category
            description (str): Issue description
            
        Returns:
            dict: Case-based suggestions
        """
        suggestions = {
            'relevant_cases': [],
            'recommended_approaches': [],
            'success_rates': [],
            'timeframes': []
        }
        
        if category in self.case_database:
            category_cases = self.case_database[category]
            
            # Find relevant subcategories
            for subcategory, cases in category_cases.items():
                if any(keyword in description for keyword in subcategory.split('_')):
                    for case in cases:
                        suggestions['relevant_cases'].append(case['scenario'])
                        suggestions['recommended_approaches'].extend(case['successful_resolutions'])
                        suggestions['success_rates'].append(case['success_rate'])
                        suggestions['timeframes'].append(case['avg_resolution_time'])
        
        return suggestions
    
    def _get_general_strategies(self, priority_level):
        """
        Get general mediation strategies based on priority level
        
        Args:
            priority_level (str): Case priority level
            
        Returns:
            dict: General mediation strategies
        """
        strategies = {
            'communication': self.general_strategies['communication'],
            'negotiation': self.general_strategies['negotiation'],
            'documentation': self.general_strategies['documentation']
        }
        
        # Adjust strategies based on priority
        if priority_level in ['high', 'urgent']:
            strategies['communication'].insert(0, 'Immediate direct communication')
            strategies['negotiation'].insert(0, 'Expedited negotiation process')
        
        return strategies
    
    def _get_escalation_prevention_tips(self, category, priority_level):
        """
        Get tips to prevent escalation of the dispute
        
        Args:
            category (str): Issue category
            priority_level (str): Priority level
            
        Returns:
            list: Escalation prevention tips
        """
        general_tips = [
            'Maintain calm and professional communication',
            'Avoid emotional responses in written communication',
            'Focus on facts rather than personal attacks',
            'Seek common ground and mutual interests',
            'Consider the other party\'s perspective'
        ]
        
        category_specific_tips = {
            'property_dispute': [
                'Document all property-related communications',
                'Maintain property in good condition',
                'Follow lease terms and local regulations',
                'Consider mediation before legal action'
            ],
            'employment_labor': [
                'Follow company grievance procedures',
                'Document all workplace incidents',
                'Maintain professional relationships',
                'Seek HR guidance before escalation'
            ],
            'consumer_rights': [
                'Keep all receipts and documentation',
                'Follow company complaint procedures',
                'Be specific about desired resolution',
                'Consider alternative products/services'
            ],
            'family_law': [
                'Focus on children\'s best interests',
                'Maintain civil communication',
                'Consider family counseling',
                'Document all agreements in writing'
            ]
        }
        
        tips = general_tips.copy()
        if category in category_specific_tips:
            tips.extend(category_specific_tips[category])
        
        # Add urgency-specific tips
        if priority_level in ['high', 'urgent']:
            tips.insert(0, 'Consider immediate third-party intervention')
            tips.insert(1, 'Document all interactions for potential escalation')
        
        return tips
    
    def _combine_suggestions(self, case_based, general_strategies, escalation_prevention, priority_level):
        """
        Combine all mediation suggestions into comprehensive response
        
        Args:
            case_based (dict): Case-based suggestions
            general_strategies (dict): General mediation strategies
            escalation_prevention (list): Escalation prevention tips
            priority_level (str): Priority level
            
        Returns:
            str: Combined mediation suggestions
        """
        suggestions_parts = []
        
        # Add priority-based header
        if priority_level in ['high', 'urgent']:
            suggestions_parts.append("🚨 URGENT - Immediate mediation recommended")
        else:
            suggestions_parts.append("🤝 Mediation and Conflict Resolution Suggestions")
        
        # Add case-based suggestions
        if case_based['relevant_cases']:
            suggestions_parts.append("📋 Based on Similar Cases:")
            for i, case in enumerate(case_based['relevant_cases']):
                suggestions_parts.append(f"• {case}")
                if i < len(case_based['recommended_approaches']):
                    approaches = case_based['recommended_approaches'][i*5:(i+1)*5]  # Group by case
                    for approach in approaches:
                        suggestions_parts.append(f"  - {approach}")
        
        # Add general strategies
        suggestions_parts.append("💬 Communication Strategies:")
        for strategy in general_strategies['communication']:
            suggestions_parts.append(f"• {strategy}")
        
        suggestions_parts.append("🤝 Negotiation Approaches:")
        for approach in general_strategies['negotiation']:
            suggestions_parts.append(f"• {approach}")
        
        suggestions_parts.append("📝 Documentation Recommendations:")
        for doc in general_strategies['documentation']:
            suggestions_parts.append(f"• {doc}")
        
        # Add escalation prevention
        suggestions_parts.append("⚠️ Escalation Prevention Tips:")
        for tip in escalation_prevention:
            suggestions_parts.append(f"• {tip}")
        
        # Add success rates if available
        if case_based['success_rates']:
            avg_success_rate = sum(case_based['success_rates']) / len(case_based['success_rates'])
            suggestions_parts.append(f"📊 Success Rate: {avg_success_rate:.1%} for similar cases")
        
        # Add timeframes if available
        if case_based['timeframes']:
            suggestions_parts.append(f"⏱️ Average Resolution Time: {case_based['timeframes'][0]}")
        
        # Add mediation resources
        suggestions_parts.append("🔗 Mediation Resources:")
        suggestions_parts.append("• Local mediation centers")
        suggestions_parts.append("• Online dispute resolution platforms")
        suggestions_parts.append("• Professional mediators")
        suggestions_parts.append("• Community dispute resolution programs")
        
        return "\n\n".join(suggestions_parts)
    
    def get_mediation_resources(self, category):
        """
        Get mediation resources for a specific category
        
        Args:
            category (str): Issue category
            
        Returns:
            dict: Mediation resources
        """
        resources = {
            'property_dispute': {
                'organizations': ['Housing Mediation Services', 'Tenant-Landlord Mediation'],
                'services': ['Property Dispute Mediation', 'Rental Agreement Mediation'],
                'contact': ['Local Housing Authority', 'Community Mediation Center']
            },
            'employment_labor': {
                'organizations': ['Workplace Mediation Services', 'Labor Dispute Mediation'],
                'services': ['Employment Conflict Resolution', 'Workplace Mediation'],
                'contact': ['HR Department', 'Labor Relations Board']
            },
            'consumer_rights': {
                'organizations': ['Consumer Mediation Services', 'Better Business Bureau'],
                'services': ['Consumer Dispute Resolution', 'Product Issue Mediation'],
                'contact': ['Consumer Protection Agency', 'Business Mediation Services']
            },
            'family_law': {
                'organizations': ['Family Mediation Services', 'Co-Parenting Mediation'],
                'services': ['Family Conflict Resolution', 'Parenting Plan Mediation'],
                'contact': ['Family Court Services', 'Family Counseling Centers']
            }
        }
        
        return resources.get(category, {
            'organizations': ['General Mediation Services'],
            'services': ['Conflict Resolution Services'],
            'contact': ['Community Mediation Center']
        })
    
    def calculate_mediation_success_probability(self, case_data):
        """
        Calculate the probability of successful mediation based on case characteristics
        
        Args:
            case_data (dict): Case information
            
        Returns:
            float: Success probability (0.0 to 1.0)
        """
        base_probability = 0.75  # Base success rate
        
        # Adjust based on category
        category = case_data.get('issue_category', '')
        if category in ['family_law', 'employment_labor']:
            base_probability += 0.10  # Higher success rate for these categories
        elif category in ['criminal_law']:
            base_probability -= 0.20  # Lower success rate for criminal matters
        
        # Adjust based on priority
        priority = case_data.get('priority_level', 'medium')
        if priority == 'urgent':
            base_probability -= 0.15  # Urgent cases may be harder to mediate
        elif priority == 'low':
            base_probability += 0.05  # Low priority cases may be easier to resolve
        
        # Ensure probability is within bounds
        return max(0.0, min(1.0, base_probability))
    
    def suggest_mediation_timeline(self, case_data):
        """
        Suggest a timeline for mediation process
        
        Args:
            case_data (dict): Case information
            
        Returns:
            dict: Suggested timeline
        """
        category = case_data.get('issue_category', '')
        priority = case_data.get('priority_level', 'medium')
        
        # Base timeline
        timeline = {
            'initial_contact': '1-3 days',
            'mediation_setup': '1-2 weeks',
            'mediation_sessions': '2-4 sessions',
            'agreement_drafting': '1-2 weeks',
            'total_duration': '4-8 weeks'
        }
        
        # Adjust based on priority
        if priority == 'urgent':
            timeline['initial_contact'] = 'Same day'
            timeline['mediation_setup'] = '3-5 days'
            timeline['total_duration'] = '2-4 weeks'
        elif priority == 'low':
            timeline['total_duration'] = '6-12 weeks'
        
        # Adjust based on category
        if category == 'consumer_rights':
            timeline['total_duration'] = '2-4 weeks'  # Faster for consumer issues
        elif category == 'family_law':
            timeline['total_duration'] = '8-16 weeks'  # Longer for family matters
        
        return timeline 