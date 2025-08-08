import os
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI module not available. AI-enhanced responses will be disabled.")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Google Generative AI module not available. AI-enhanced responses will be disabled.")

from datetime import datetime

class LegalAgent:
    """
    Legal Expert Agent: Provides legal advice and suggestions based on case analysis.
    Uses rule-based knowledge and can integrate with AI APIs for enhanced responses.
    """
    
    def __init__(self):
        self.name = "Legal Expert Agent"
        self.description = "Provides legal advice and suggestions using rule-based knowledge and AI"
        
        # Initialize AI clients if API keys are available
        self.openai_client = None
        self.gemini_model = None
        self._initialize_ai_clients()
        
        # Legal knowledge base - rule-based responses
        self.legal_knowledge = {
            'property_dispute': {
                'landlord_tenant': {
                    'deposit_return': {
                        'laws': ['Rent Control Act', 'Tenant Protection Laws'],
                        'advice': [
                            'Landlords must return security deposits within 30 days of lease termination',
                            'Document all communications with your landlord',
                            'Send a formal written notice requesting deposit return',
                            'Consider filing a complaint with local housing authority',
                            'Keep records of property condition when moving out'
                        ],
                        'rights': [
                            'Right to receive deposit back within specified timeframe',
                            'Right to itemized list of deductions',
                            'Right to challenge unreasonable deductions'
                        ]
                    },
                    'eviction': {
                        'laws': ['Eviction Protection Laws', 'Due Process Rights'],
                        'advice': [
                            'Landlords must provide proper notice before eviction',
                            'You have the right to contest eviction in court',
                            'Seek legal aid if facing wrongful eviction',
                            'Document all interactions with landlord'
                        ]
                    }
                }
            },
            'employment_labor': {
                'wage_dispute': {
                    'laws': ['Minimum Wage Laws', 'Fair Labor Standards Act'],
                    'advice': [
                        'Document all hours worked and wages received',
                        'File a complaint with Department of Labor',
                        'Keep copies of pay stubs and employment contracts',
                        'Consider consulting with employment attorney'
                    ]
                },
                'harassment': {
                    'laws': ['Title VII', 'Workplace Harassment Laws'],
                    'advice': [
                        'Document all incidents of harassment',
                        'Report to HR department immediately',
                        'File complaint with EEOC if internal resolution fails',
                        'Consider legal representation for serious cases'
                    ]
                }
            },
            'consumer_rights': {
                'product_defect': {
                    'laws': ['Consumer Protection Laws', 'Product Liability'],
                    'advice': [
                        'Document the defect with photos and videos',
                        'Contact manufacturer for warranty claims',
                        'File complaint with Consumer Protection Agency',
                        'Consider small claims court for damages'
                    ]
                },
                'fraud': {
                    'laws': ['Consumer Fraud Laws', 'Deceptive Trade Practices'],
                    'advice': [
                        'Report fraud to local police and FTC',
                        'Contact your bank to dispute charges',
                        'Document all communications and transactions',
                        'Consider identity theft protection services'
                    ]
                }
            },
            'family_law': {
                'custody': {
                    'laws': ['Family Law Code', 'Child Custody Guidelines'],
                    'advice': [
                        'Focus on child\'s best interests',
                        'Document all interactions with co-parent',
                        'Consider mediation before court proceedings',
                        'Consult with family law attorney'
                    ]
                }
            }
        }
    
    def _initialize_ai_clients(self):
        """Initialize AI clients if API keys are available"""
        try:
            # Initialize OpenAI client
            if OPENAI_AVAILABLE:
                openai_api_key = os.getenv('OPENAI_API_KEY')
                if openai_api_key:
                    openai.api_key = openai_api_key
                    self.openai_client = openai
                    print("✅ OpenAI client initialized")
            
            # Initialize Gemini client
            if GEMINI_AVAILABLE:
                gemini_api_key = os.getenv('GEMINI_API_KEY')
                if gemini_api_key:
                    genai.configure(api_key=gemini_api_key)
                    self.gemini_model = genai.GenerativeModel('gemini-pro')
                    print("✅ Gemini client initialized")
                
        except Exception as e:
            print(f"⚠️ AI client initialization failed: {e}")
    
    def provide_legal_advice(self, case_data):
        """
        Provide legal advice based on case analysis
        
        Args:
            case_data (dict): Case information including issue details
            
        Returns:
            str: Comprehensive legal advice
        """
        try:
            issue_category = case_data.get('issue_category', '')
            issue_description = case_data.get('issue_description', '').lower()
            priority_level = case_data.get('priority_level', 'medium')
            
            # Get rule-based advice
            rule_based_advice = self._get_rule_based_advice(issue_category, issue_description)
            
            # Get AI-enhanced advice if available
            ai_advice = self._get_ai_enhanced_advice(case_data)
            
            # Combine advice
            combined_advice = self._combine_advice(rule_based_advice, ai_advice, priority_level)
            
            return combined_advice
            
        except Exception as e:
            return f"Error providing legal advice: {str(e)}"
    
    def _get_rule_based_advice(self, category, description):
        """
        Get rule-based legal advice from knowledge base
        
        Args:
            category (str): Issue category
            description (str): Issue description
            
        Returns:
            dict: Rule-based advice
        """
        advice = {
            'applicable_laws': [],
            'legal_advice': [],
            'rights': [],
            'next_steps': []
        }
        
        # Get category-specific advice
        if category in self.legal_knowledge:
            category_knowledge = self.legal_knowledge[category]
            
            # Find relevant subcategory based on description
            for subcategory, info in category_knowledge.items():
                if any(keyword in description for keyword in subcategory.split('_')):
                    advice['applicable_laws'].extend(info.get('laws', []))
                    advice['legal_advice'].extend(info.get('advice', []))
                    advice['rights'].extend(info.get('rights', []))
        
        # Add general legal advice
        advice['legal_advice'].extend([
            'Document all relevant communications and interactions',
            'Keep copies of all important documents',
            'Consider consulting with a qualified attorney for complex cases',
            'Be aware of applicable statutes of limitations'
        ])
        
        # Add next steps
        advice['next_steps'] = [
            'Gather all relevant documents and evidence',
            'Document timeline of events',
            'Consider alternative dispute resolution methods',
            'Prepare for potential legal proceedings'
        ]
        
        return advice
    
    def _get_ai_enhanced_advice(self, case_data):
        """
        Get AI-enhanced legal advice if AI clients are available
        
        Args:
            case_data (dict): Case information
            
        Returns:
            str: AI-enhanced advice or empty string
        """
        if not (self.openai_client or self.gemini_model):
            return ""
        
        try:
            prompt = self._create_legal_advice_prompt(case_data)
            
            # Try OpenAI first
            if self.openai_client and OPENAI_AVAILABLE:
                try:
                    response = self.openai_client.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a legal expert providing initial guidance. Provide practical, actionable advice while noting that this is not formal legal counsel."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=500,
                        temperature=0.3
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    print(f"OpenAI API error: {e}")
            
            # Try Gemini if OpenAI fails
            if self.gemini_model and GEMINI_AVAILABLE:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    return response.text
                except Exception as e:
                    print(f"Gemini API error: {e}")
            
        except Exception as e:
            print(f"AI advice generation error: {e}")
        
        return ""
    
    def _create_legal_advice_prompt(self, case_data):
        """
        Create a prompt for AI legal advice
        
        Args:
            case_data (dict): Case information
            
        Returns:
            str: Formatted prompt
        """
        return f"""
        Please provide legal guidance for the following case:
        
        Category: {case_data.get('issue_category', 'Unknown')}
        Description: {case_data.get('issue_description', '')}
        Priority: {case_data.get('priority_level', 'medium')}
        
        Please provide:
        1. Initial legal assessment
        2. Applicable laws or regulations
        3. Recommended next steps
        4. Important considerations
        
        Note: This is for initial guidance only. The person should consult with a qualified attorney for formal legal advice.
        """
    
    def _combine_advice(self, rule_based_advice, ai_advice, priority_level):
        """
        Combine rule-based and AI advice into comprehensive response
        
        Args:
            rule_based_advice (dict): Rule-based advice
            ai_advice (str): AI-enhanced advice
            priority_level (str): Case priority
            
        Returns:
            str: Combined legal advice
        """
        advice_parts = []
        
        # Add priority-based header
        if priority_level in ['high', 'urgent']:
            advice_parts.append("⚠️ HIGH PRIORITY CASE - Immediate attention recommended")
        
        # Add applicable laws
        if rule_based_advice['applicable_laws']:
            advice_parts.append(f"📋 Applicable Laws: {', '.join(rule_based_advice['applicable_laws'])}")
        
        # Add legal advice
        if rule_based_advice['legal_advice']:
            advice_parts.append("💡 Legal Advice:")
            for advice in rule_based_advice['legal_advice']:
                advice_parts.append(f"• {advice}")
        
        # Add rights
        if rule_based_advice['rights']:
            advice_parts.append("⚖️ Your Rights:")
            for right in rule_based_advice['rights']:
                advice_parts.append(f"• {right}")
        
        # Add AI-enhanced advice
        if ai_advice:
            advice_parts.append("🤖 AI-Enhanced Guidance:")
            advice_parts.append(ai_advice)
        
        # Add next steps
        if rule_based_advice['next_steps']:
            advice_parts.append("📝 Recommended Next Steps:")
            for step in rule_based_advice['next_steps']:
                advice_parts.append(f"• {step}")
        
        # Add disclaimer
        advice_parts.append("\n⚠️ DISCLAIMER: This advice is for informational purposes only and does not constitute legal counsel. Please consult with a qualified attorney for formal legal advice.")
        
        return "\n\n".join(advice_parts)
    
    def get_legal_resources(self, category):
        """
        Get legal resources for a specific category
        
        Args:
            category (str): Legal category
            
        Returns:
            dict: Legal resources
        """
        resources = {
            'property_dispute': {
                'organizations': ['Local Housing Authority', 'Tenant Rights Organizations'],
                'websites': ['HUD.gov', 'Local Legal Aid'],
                'helplines': ['Housing Helpline', 'Legal Aid Hotline']
            },
            'employment_labor': {
                'organizations': ['Department of Labor', 'EEOC', 'Local Labor Board'],
                'websites': ['DOL.gov', 'EEOC.gov'],
                'helplines': ['DOL Helpline', 'EEOC Hotline']
            },
            'consumer_rights': {
                'organizations': ['Consumer Protection Agency', 'Better Business Bureau'],
                'websites': ['FTC.gov', 'Consumer.gov'],
                'helplines': ['Consumer Protection Hotline']
            },
            'family_law': {
                'organizations': ['Family Court Services', 'Legal Aid Society'],
                'websites': ['Family Law Resources'],
                'helplines': ['Family Law Helpline']
            }
        }
        
        return resources.get(category, {
            'organizations': ['Local Legal Aid'],
            'websites': ['Legal Resources Directory'],
            'helplines': ['General Legal Helpline']
        })
    
    def validate_legal_advice(self, advice):
        """
        Validate the generated legal advice
        
        Args:
            advice (str): Generated legal advice
            
        Returns:
            bool: Whether advice is valid
        """
        # Check for required components
        required_components = ['Applicable Laws', 'Legal Advice', 'Next Steps']
        
        for component in required_components:
            if component not in advice:
                return False
        
        # Check for disclaimer
        if 'DISCLAIMER' not in advice:
            return False
        
        return True 