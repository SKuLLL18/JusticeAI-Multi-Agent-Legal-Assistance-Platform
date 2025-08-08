import re
from datetime import datetime

class EscalationAgent:
    """
    Escalation Agent: Identifies serious cases and suggests next steps or connects to real-world services.
    Evaluates case severity and provides escalation recommendations.
    """
    
    def __init__(self):
        self.name = "Escalation Agent"
        self.description = "Identifies serious cases and provides escalation recommendations"
        
        # Severity indicators and keywords
        self.severity_indicators = {
            'critical': {
                'keywords': ['emergency', 'urgent', 'immediate', 'danger', 'threat', 'violence', 'assault', 'abuse'],
                'score': 10,
                'requires_immediate_action': True
            },
            'high': {
                'keywords': ['serious', 'important', 'deadline', 'court', 'hearing', 'eviction', 'termination', 'harassment'],
                'score': 7,
                'requires_immediate_action': False
            },
            'medium': {
                'keywords': ['concern', 'issue', 'problem', 'dispute', 'conflict', 'payment', 'deposit'],
                'score': 4,
                'requires_immediate_action': False
            },
            'low': {
                'keywords': ['question', 'inquiry', 'information', 'general', 'advice'],
                'score': 1,
                'requires_immediate_action': False
            }
        }
        
        # Escalation pathways based on category and severity
        self.escalation_pathways = {
            'criminal_law': {
                'critical': {
                    'immediate_actions': [
                        'Contact local police immediately',
                        'File police report',
                        'Seek emergency legal assistance',
                        'Contact victim support services'
                    ],
                    'organizations': ['Local Police Department', 'Victim Support Services', 'Emergency Legal Aid'],
                    'helplines': ['911 (Emergency)', 'National Domestic Violence Hotline', 'Crime Victim Helpline']
                },
                'high': {
                    'immediate_actions': [
                        'File police report',
                        'Document all incidents',
                        'Seek legal representation',
                        'Contact victim advocacy groups'
                    ],
                    'organizations': ['Local Police Department', 'District Attorney Office', 'Legal Aid Society'],
                    'helplines': ['Police Non-Emergency', 'Legal Aid Hotline']
                }
            },
            'family_law': {
                'critical': {
                    'immediate_actions': [
                        'Contact domestic violence hotline',
                        'Seek emergency protection order',
                        'Contact family court immediately',
                        'Document all incidents'
                    ],
                    'organizations': ['Domestic Violence Shelter', 'Family Court Services', 'Emergency Legal Services'],
                    'helplines': ['National Domestic Violence Hotline', 'Family Court Emergency Line']
                },
                'high': {
                    'immediate_actions': [
                        'Consult with family law attorney',
                        'File appropriate court documents',
                        'Contact family mediation services',
                        'Document all interactions'
                    ],
                    'organizations': ['Family Law Attorney', 'Family Mediation Services', 'Child Protective Services'],
                    'helplines': ['Family Law Helpline', 'Child Support Hotline']
                }
            },
            'employment_labor': {
                'critical': {
                    'immediate_actions': [
                        'Document all incidents immediately',
                        'Contact HR department',
                        'File complaint with labor board',
                        'Seek legal representation'
                    ],
                    'organizations': ['Department of Labor', 'EEOC', 'Employment Attorney'],
                    'helplines': ['DOL Helpline', 'EEOC Hotline', 'Workplace Rights Hotline']
                },
                'high': {
                    'immediate_actions': [
                        'Follow company grievance procedures',
                        'Document all workplace incidents',
                        'Contact labor board',
                        'Consult with employment attorney'
                    ],
                    'organizations': ['Department of Labor', 'State Labor Board', 'Employment Attorney'],
                    'helplines': ['DOL Helpline', 'State Labor Helpline']
                }
            },
            'property_dispute': {
                'critical': {
                    'immediate_actions': [
                        'Contact housing authority immediately',
                        'Document all communications',
                        'Seek emergency legal assistance',
                        'Contact tenant rights organizations'
                    ],
                    'organizations': ['Local Housing Authority', 'Tenant Rights Organizations', 'Legal Aid Society'],
                    'helplines': ['Housing Emergency Hotline', 'Tenant Rights Hotline']
                },
                'high': {
                    'immediate_actions': [
                        'Contact housing authority',
                        'Document all interactions',
                        'Seek legal advice',
                        'Contact tenant advocacy groups'
                    ],
                    'organizations': ['Local Housing Authority', 'Tenant Rights Organizations', 'Legal Aid Society'],
                    'helplines': ['Housing Helpline', 'Tenant Rights Hotline']
                }
            }
        }
        
        # General escalation resources
        self.general_resources = {
            'legal_aid': [
                'Local Legal Aid Society',
                'Pro Bono Legal Services',
                'State Bar Association',
                'Community Legal Services'
            ],
            'emergency_contacts': [
                '911 (Emergency Services)',
                'Local Police Department',
                'Emergency Legal Services',
                'Crisis Intervention Services'
            ],
            'helplines': [
                'Legal Aid Hotline',
                'Consumer Protection Hotline',
                'General Legal Information Line'
            ]
        }
    
    def evaluate_case(self, case_data):
        """
        Evaluate case severity and provide escalation recommendations
        
        Args:
            case_data (dict): Case information including issue details
            
        Returns:
            str: Escalation recommendations
        """
        try:
            issue_category = case_data.get('issue_category', '')
            issue_description = case_data.get('issue_description', '').lower()
            priority_level = case_data.get('priority_level', 'medium')
            
            # Assess severity
            severity_assessment = self._assess_severity(issue_description, priority_level)
            
            # Get escalation recommendations
            escalation_recommendations = self._get_escalation_recommendations(
                issue_category, 
                severity_assessment, 
                case_data
            )
            
            # Combine into comprehensive response
            combined_recommendations = self._combine_recommendations(
                severity_assessment, 
                escalation_recommendations
            )
            
            return combined_recommendations
            
        except Exception as e:
            return f"Error evaluating case for escalation: {str(e)}"
    
    def _assess_severity(self, description, priority_level):
        """
        Assess the severity of the case based on description and priority
        
        Args:
            description (str): Issue description
            priority_level (str): User-selected priority level
            
        Returns:
            dict: Severity assessment
        """
        severity_score = 0
        detected_severity = 'low'
        detected_keywords = []
        
        # Calculate base score from priority level
        priority_scores = {'low': 1, 'medium': 3, 'high': 6, 'urgent': 8}
        severity_score += priority_scores.get(priority_level, 1)
        
        # Analyze description for severity indicators
        for severity_level, indicators in self.severity_indicators.items():
            for keyword in indicators['keywords']:
                if keyword in description:
                    severity_score += indicators['score']
                    detected_keywords.append(keyword)
                    if indicators['score'] > self.severity_indicators[detected_severity]['score']:
                        detected_severity = severity_level
        
        # Determine final severity level
        if severity_score >= 15:
            final_severity = 'critical'
        elif severity_score >= 10:
            final_severity = 'high'
        elif severity_score >= 5:
            final_severity = 'medium'
        else:
            final_severity = 'low'
        
        return {
            'severity_level': final_severity,
            'severity_score': severity_score,
            'detected_keywords': detected_keywords,
            'requires_immediate_action': self.severity_indicators[final_severity]['requires_immediate_action'],
            'priority_level': priority_level
        }
    
    def _get_escalation_recommendations(self, category, severity_assessment, case_data):
        """
        Get escalation recommendations based on category and severity
        
        Args:
            category (str): Issue category
            severity_assessment (dict): Severity assessment results
            case_data (dict): Case information
            
        Returns:
            dict: Escalation recommendations
        """
        severity_level = severity_assessment['severity_level']
        
        # Get category-specific recommendations
        if category in self.escalation_pathways and severity_level in self.escalation_pathways[category]:
            category_recommendations = self.escalation_pathways[category][severity_level]
        else:
            # Use general recommendations for unknown categories
            category_recommendations = {
                'immediate_actions': [
                    'Document all relevant information',
                    'Seek legal advice from qualified professionals',
                    'Contact appropriate authorities if necessary',
                    'Follow up on any pending matters'
                ],
                'organizations': self.general_resources['legal_aid'],
                'helplines': self.general_resources['helplines']
            }
        
        # Add emergency contacts if critical
        if severity_level == 'critical':
            category_recommendations['emergency_contacts'] = self.general_resources['emergency_contacts']
        
        return category_recommendations
    
    def _combine_recommendations(self, severity_assessment, escalation_recommendations):
        """
        Combine severity assessment and escalation recommendations into comprehensive response
        
        Args:
            severity_assessment (dict): Severity assessment
            escalation_recommendations (dict): Escalation recommendations
            
        Returns:
            str: Combined recommendations
        """
        recommendations_parts = []
        
        # Add severity assessment header
        severity_level = severity_assessment['severity_level']
        if severity_level == 'critical':
            recommendations_parts.append("🚨 CRITICAL SEVERITY - IMMEDIATE ACTION REQUIRED")
        elif severity_level == 'high':
            recommendations_parts.append("⚠️ HIGH SEVERITY - URGENT ATTENTION NEEDED")
        elif severity_level == 'medium':
            recommendations_parts.append("📋 MEDIUM SEVERITY - STANDARD PROCESSING")
        else:
            recommendations_parts.append("ℹ️ LOW SEVERITY - ROUTINE HANDLING")
        
        # Add severity details
        recommendations_parts.append(f"Severity Score: {severity_assessment['severity_score']}/20")
        if severity_assessment['detected_keywords']:
            recommendations_parts.append(f"Key Indicators: {', '.join(severity_assessment['detected_keywords'])}")
        
        # Add immediate actions
        if 'immediate_actions' in escalation_recommendations:
            recommendations_parts.append("\n🚀 Immediate Actions Required:")
            for action in escalation_recommendations['immediate_actions']:
                recommendations_parts.append(f"• {action}")
        
        # Add organizations
        if 'organizations' in escalation_recommendations:
            recommendations_parts.append("\n🏢 Recommended Organizations:")
            for org in escalation_recommendations['organizations']:
                recommendations_parts.append(f"• {org}")
        
        # Add helplines
        if 'helplines' in escalation_recommendations:
            recommendations_parts.append("\n📞 Available Helplines:")
            for helpline in escalation_recommendations['helplines']:
                recommendations_parts.append(f"• {helpline}")
        
        # Add emergency contacts if critical
        if severity_level == 'critical' and 'emergency_contacts' in escalation_recommendations:
            recommendations_parts.append("\n🚨 Emergency Contacts:")
            for contact in escalation_recommendations['emergency_contacts']:
                recommendations_parts.append(f"• {contact}")
        
        # Add general guidance
        recommendations_parts.append("\n📝 General Guidance:")
        if severity_level in ['critical', 'high']:
            recommendations_parts.append("• Document all interactions and communications")
            recommendations_parts.append("• Keep copies of all relevant documents")
            recommendations_parts.append("• Follow up on all recommended actions")
            recommendations_parts.append("• Consider seeking professional legal representation")
        else:
            recommendations_parts.append("• Follow standard procedures for your issue type")
            recommendations_parts.append("• Document important interactions")
            recommendations_parts.append("• Consider mediation or alternative dispute resolution")
        
        # Add next steps
        recommendations_parts.append("\n🔄 Next Steps:")
        if severity_level == 'critical':
            recommendations_parts.append("1. Take immediate action on emergency recommendations")
            recommendations_parts.append("2. Contact emergency services if safety is at risk")
            recommendations_parts.append("3. Follow up with recommended organizations within 24 hours")
            recommendations_parts.append("4. Document all actions taken")
        elif severity_level == 'high':
            recommendations_parts.append("1. Contact recommended organizations within 48 hours")
            recommendations_parts.append("2. Implement immediate actions")
            recommendations_parts.append("3. Follow up on all recommendations")
            recommendations_parts.append("4. Monitor situation and escalate if needed")
        else:
            recommendations_parts.append("1. Review recommendations and take appropriate action")
            recommendations_parts.append("2. Contact organizations as needed")
            recommendations_parts.append("3. Follow standard procedures for your issue")
            recommendations_parts.append("4. Monitor progress and escalate if situation changes")
        
        return "\n".join(recommendations_parts)
    
    def should_escalate_to_authorities(self, case_data, severity_assessment):
        """
        Determine if case should be escalated to authorities
        
        Args:
            case_data (dict): Case information
            severity_assessment (dict): Severity assessment
            
        Returns:
            bool: Whether case should be escalated
        """
        severity_level = severity_assessment['severity_level']
        category = case_data.get('issue_category', '')
        
        # Critical cases should always be escalated
        if severity_level == 'critical':
            return True
        
        # High severity cases in certain categories should be escalated
        if severity_level == 'high' and category in ['criminal_law', 'family_law']:
            return True
        
        # Check for specific keywords that require escalation
        description = case_data.get('issue_description', '').lower()
        escalation_keywords = ['violence', 'assault', 'abuse', 'threat', 'danger', 'emergency']
        
        if any(keyword in description for keyword in escalation_keywords):
            return True
        
        return False
    
    def get_escalation_timeline(self, severity_assessment):
        """
        Get recommended timeline for escalation actions
        
        Args:
            severity_assessment (dict): Severity assessment
            
        Returns:
            dict: Escalation timeline
        """
        severity_level = severity_assessment['severity_level']
        
        timelines = {
            'critical': {
                'immediate': 'Within 1 hour',
                'short_term': 'Within 24 hours',
                'follow_up': 'Within 48 hours',
                'resolution': '1-2 weeks'
            },
            'high': {
                'immediate': 'Within 24 hours',
                'short_term': 'Within 3 days',
                'follow_up': 'Within 1 week',
                'resolution': '2-4 weeks'
            },
            'medium': {
                'immediate': 'Within 3 days',
                'short_term': 'Within 1 week',
                'follow_up': 'Within 2 weeks',
                'resolution': '1-3 months'
            },
            'low': {
                'immediate': 'Within 1 week',
                'short_term': 'Within 2 weeks',
                'follow_up': 'Within 1 month',
                'resolution': '3-6 months'
            }
        }
        
        return timelines.get(severity_level, timelines['medium'])
    
    def validate_escalation_recommendations(self, recommendations):
        """
        Validate escalation recommendations
        
        Args:
            recommendations (str): Generated recommendations
            
        Returns:
            bool: Whether recommendations are valid
        """
        # Check for required components
        required_components = [
            'Immediate Actions',
            'Recommended Organizations',
            'Next Steps'
        ]
        
        for component in required_components:
            if component not in recommendations:
                return False
        
        # Check for severity level indication
        severity_indicators = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        if not any(indicator in recommendations for indicator in severity_indicators):
            return False
        
        return True 