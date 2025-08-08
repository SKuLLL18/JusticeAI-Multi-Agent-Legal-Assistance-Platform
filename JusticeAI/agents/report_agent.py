import os
from datetime import datetime

# Try to import reportlab, make it optional
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️ ReportLab module not available. PDF generation will be disabled.")

class ReportAgent:
    """
    Report Agent: Generates comprehensive PDF reports summarizing case analysis and agent responses.
    Creates professional, well-formatted documents for users and legal professionals.
    """
    
    def __init__(self):
        self.name = "Report Agent"
        self.description = "Generates comprehensive PDF reports with case summaries and recommendations"
        
        # Report templates and styling
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Report configuration
        self.report_config = {
            'page_size': A4,
            'margin_top': 1 * inch,
            'margin_bottom': 1 * inch,
            'margin_left': 1 * inch,
            'margin_right': 1 * inch,
            'include_header': True,
            'include_footer': True
        }
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'CustomSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        )
        
        # Subsection style
        self.subsection_style = ParagraphStyle(
            'CustomSubsection',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.darkgreen
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        # Highlight style for important information
        self.highlight_style = ParagraphStyle(
            'CustomHighlight',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.darkred,
            alignment=TA_JUSTIFY
        )
    
    def generate_report(self, case_data, legal_advice, mediation_suggestions, escalation_recommendations):
        """
        Generate a comprehensive PDF report for the case
        
        Args:
            case_data (dict): Case information
            legal_advice (str): Legal advice from Legal Agent
            mediation_suggestions (str): Mediation suggestions from Mediation Agent
            escalation_recommendations (str): Escalation recommendations from Escalation Agent
            
        Returns:
            str: Path to the generated PDF report
        """
        if not REPORTLAB_AVAILABLE:
            print("⚠️ PDF generation disabled - ReportLab not available")
            return ""
            
        try:
            # Create reports directory if it doesn't exist
            os.makedirs('reports', exist_ok=True)
            
            # Generate unique filename
            case_id = case_data.get('id', 'unknown')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"reports/justiceai_report_{case_id}_{timestamp}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filename,
                pagesize=self.report_config['page_size'],
                topMargin=self.report_config['margin_top'],
                bottomMargin=self.report_config['margin_bottom'],
                leftMargin=self.report_config['margin_left'],
                rightMargin=self.report_config['margin_right']
            )
            
            # Build report content
            story = []
            
            # Add header
            story.extend(self._create_header(case_data))
            
            # Add case summary
            story.extend(self._create_case_summary(case_data))
            
            # Add legal analysis
            story.extend(self._create_legal_analysis(legal_advice))
            
            # Add mediation recommendations
            story.extend(self._create_mediation_recommendations(mediation_suggestions))
            
            # Add escalation assessment
            story.extend(self._create_escalation_assessment(escalation_recommendations))
            
            # Add action plan
            story.extend(self._create_action_plan(case_data, legal_advice, mediation_suggestions))
            
            # Add resources and contacts
            story.extend(self._create_resources_section(case_data))
            
            # Add footer
            story.extend(self._create_footer())
            
            # Build PDF
            doc.build(story)
            
            print(f"✅ Report generated: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return ""
    
    def _create_header(self, case_data):
        """Create the report header"""
        story = []
        
        # Title
        title = Paragraph("JusticeAI Legal Assistance Report", self.title_style)
        story.append(title)
        
        # Subtitle
        subtitle = Paragraph("Multi-Agent Legal Analysis and Recommendations", self.section_style)
        story.append(subtitle)
        
        # Report metadata
        metadata_data = [
            ['Report Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
            ['Case ID:', case_data.get('id', 'N/A')],
            ['Client Name:', case_data.get('user_name', 'N/A')],
            ['Issue Category:', case_data.get('issue_category', 'N/A').replace('_', ' ').title()],
            ['Priority Level:', case_data.get('priority_level', 'N/A').title()]
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        
        story.append(metadata_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_case_summary(self, case_data):
        """Create the case summary section"""
        story = []
        
        # Section header
        story.append(Paragraph("Case Summary", self.section_style))
        
        # Issue description
        story.append(Paragraph("Issue Description:", self.subsection_style))
        description = case_data.get('issue_description', 'No description provided.')
        story.append(Paragraph(description, self.body_style))
        story.append(Spacer(1, 12))
        
        # Case details table
        details_data = [
            ['Field', 'Information'],
            ['Client Name', case_data.get('user_name', 'N/A')],
            ['Contact Email', case_data.get('user_email', 'N/A')],
            ['Issue Category', case_data.get('issue_category', 'N/A').replace('_', ' ').title()],
            ['Priority Level', case_data.get('priority_level', 'N/A').title()],
            ['Submission Date', datetime.now().strftime('%B %d, %Y')]
        ]
        
        details_table = Table(details_data, colWidths=[2*inch, 4*inch])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.whitesmoke),
        ]))
        
        story.append(details_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_legal_analysis(self, legal_advice):
        """Create the legal analysis section"""
        story = []
        
        # Section header
        story.append(Paragraph("Legal Analysis and Advice", self.section_style))
        
        # Legal advice content
        if legal_advice:
            # Split advice into paragraphs and format
            advice_paragraphs = legal_advice.split('\n\n')
            for paragraph in advice_paragraphs:
                if paragraph.strip():
                    # Check if it's a header (contains emoji or is all caps)
                    if any(emoji in paragraph for emoji in ['📋', '💡', '⚖️', '🤖', '📝', '⚠️']):
                        story.append(Paragraph(paragraph, self.subsection_style))
                    elif 'DISCLAIMER' in paragraph:
                        story.append(Paragraph(paragraph, self.highlight_style))
                    else:
                        story.append(Paragraph(paragraph, self.body_style))
                    story.append(Spacer(1, 6))
        else:
            story.append(Paragraph("No legal advice available for this case.", self.body_style))
        
        story.append(Spacer(1, 20))
        return story
    
    def _create_mediation_recommendations(self, mediation_suggestions):
        """Create the mediation recommendations section"""
        story = []
        
        # Section header
        story.append(Paragraph("Mediation and Conflict Resolution", self.section_style))
        
        # Mediation suggestions content
        if mediation_suggestions:
            # Split suggestions into paragraphs and format
            suggestion_paragraphs = mediation_suggestions.split('\n\n')
            for paragraph in suggestion_paragraphs:
                if paragraph.strip():
                    # Check if it's a header
                    if any(emoji in paragraph for emoji in ['📋', '💬', '🤝', '📝', '⚠️', '📊', '⏱️', '🔗']):
                        story.append(Paragraph(paragraph, self.subsection_style))
                    else:
                        story.append(Paragraph(paragraph, self.body_style))
                    story.append(Spacer(1, 6))
        else:
            story.append(Paragraph("No mediation suggestions available for this case.", self.body_style))
        
        story.append(Spacer(1, 20))
        return story
    
    def _create_escalation_assessment(self, escalation_recommendations):
        """Create the escalation assessment section"""
        story = []
        
        # Section header
        story.append(Paragraph("Escalation Assessment", self.section_style))
        
        # Escalation recommendations content
        if escalation_recommendations:
            story.append(Paragraph(escalation_recommendations, self.body_style))
        else:
            story.append(Paragraph("No escalation recommendations available for this case.", self.body_style))
        
        story.append(Spacer(1, 20))
        return story
    
    def _create_action_plan(self, case_data, legal_advice, mediation_suggestions):
        """Create the action plan section"""
        story = []
        
        # Section header
        story.append(Paragraph("Recommended Action Plan", self.section_style))
        
        # Immediate actions
        story.append(Paragraph("Immediate Actions (Next 24-48 hours):", self.subsection_style))
        immediate_actions = [
            "Document all relevant communications and interactions",
            "Gather supporting documents and evidence",
            "Review the legal advice provided in this report",
            "Consider the mediation suggestions for peaceful resolution",
            "Contact relevant authorities if immediate action is required"
        ]
        
        for action in immediate_actions:
            story.append(Paragraph(f"• {action}", self.body_style))
        
        story.append(Spacer(1, 12))
        
        # Short-term actions
        story.append(Paragraph("Short-term Actions (Next 1-2 weeks):", self.subsection_style))
        short_term_actions = [
            "Follow up on any pending communications",
            "Implement recommended mediation strategies",
            "Consult with legal professionals if needed",
            "Monitor the situation and document any changes",
            "Prepare for potential escalation if necessary"
        ]
        
        for action in short_term_actions:
            story.append(Paragraph(f"• {action}", self.body_style))
        
        story.append(Spacer(1, 12))
        
        # Long-term considerations
        story.append(Paragraph("Long-term Considerations:", self.subsection_style))
        long_term_considerations = [
            "Evaluate the effectiveness of implemented solutions",
            "Consider preventive measures for future similar situations",
            "Maintain documentation for potential future reference",
            "Follow up on any agreements or settlements reached"
        ]
        
        for consideration in long_term_considerations:
            story.append(Paragraph(f"• {consideration}", self.body_style))
        
        story.append(Spacer(1, 20))
        return story
    
    def _create_resources_section(self, case_data):
        """Create the resources and contacts section"""
        story = []
        
        # Section header
        story.append(Paragraph("Resources and Contacts", self.section_style))
        
        # General resources
        story.append(Paragraph("General Legal Resources:", self.subsection_style))
        general_resources = [
            "Local Legal Aid Society",
            "State Bar Association",
            "Community Legal Services",
            "Pro Bono Legal Services",
            "Court Self-Help Centers"
        ]
        
        for resource in general_resources:
            story.append(Paragraph(f"• {resource}", self.body_style))
        
        story.append(Spacer(1, 12))
        
        # Emergency contacts
        story.append(Paragraph("Emergency Contacts:", self.subsection_style))
        emergency_contacts = [
            "Local Police Department",
            "Emergency Legal Services",
            "Domestic Violence Hotline (if applicable)",
            "Crisis Intervention Services"
        ]
        
        for contact in emergency_contacts:
            story.append(Paragraph(f"• {contact}", self.body_style))
        
        story.append(Spacer(1, 12))
        
        # Online resources
        story.append(Paragraph("Online Resources:", self.subsection_style))
        online_resources = [
            "Legal Information Institute (LII)",
            "FindLaw Legal Resources",
            "Nolo Legal Encyclopedia",
            "State-specific legal websites"
        ]
        
        for resource in online_resources:
            story.append(Paragraph(f"• {resource}", self.body_style))
        
        story.append(Spacer(1, 20))
        return story
    
    def _create_footer(self):
        """Create the report footer"""
        story = []
        
        # Disclaimer
        disclaimer_text = """
        <b>IMPORTANT DISCLAIMER:</b><br/>
        This report is generated by JusticeAI, a multi-agent legal assistance platform. 
        The information provided is for informational purposes only and does not constitute 
        formal legal advice. This report should not be used as a substitute for consultation 
        with qualified legal professionals. JusticeAI is not a law firm and does not provide 
        legal representation. For formal legal advice, please consult with a licensed attorney 
        in your jurisdiction.
        """
        
        disclaimer = Paragraph(disclaimer_text, self.highlight_style)
        story.append(disclaimer)
        
        story.append(Spacer(1, 12))
        
        # Footer information
        footer_text = f"""
        <b>Report Generated by JusticeAI</b><br/>
        Supporting SDG Goal 16: Peace, Justice, and Strong Institutions<br/>
        Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
        For technical support or questions, please contact the JusticeAI development team.
        """
        
        footer = Paragraph(footer_text, self.body_style)
        story.append(footer)
        
        return story
    
    def generate_summary_report(self, case_data, agent_responses):
        """
        Generate a brief summary report for quick reference
        
        Args:
            case_data (dict): Case information
            agent_responses (dict): Responses from all agents
            
        Returns:
            str: Path to the summary report
        """
        if not REPORTLAB_AVAILABLE:
            print("⚠️ PDF generation disabled - ReportLab not available")
            return ""
            
        try:
            # Create reports directory if it doesn't exist
            os.makedirs('reports', exist_ok=True)
            
            # Generate unique filename
            case_id = case_data.get('id', 'unknown')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"reports/justiceai_summary_{case_id}_{timestamp}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filename,
                pagesize=self.report_config['page_size'],
                topMargin=self.report_config['margin_top'],
                bottomMargin=self.report_config['margin_bottom'],
                leftMargin=self.report_config['margin_left'],
                rightMargin=self.report_config['margin_right']
            )
            
            # Build summary content
            story = []
            
            # Add header
            story.append(Paragraph("JusticeAI Case Summary", self.title_style))
            
            # Add case info
            story.append(Paragraph(f"Case ID: {case_id}", self.subsection_style))
            story.append(Paragraph(f"Client: {case_data.get('user_name', 'N/A')}", self.body_style))
            story.append(Paragraph(f"Category: {case_data.get('issue_category', 'N/A')}", self.body_style))
            story.append(Paragraph(f"Priority: {case_data.get('priority_level', 'N/A')}", self.body_style))
            
            story.append(Spacer(1, 20))
            
            # Add agent summaries
            for agent_name, response in agent_responses.items():
                story.append(Paragraph(f"{agent_name} Summary:", self.subsection_style))
                # Truncate response for summary
                summary = response[:200] + "..." if len(response) > 200 else response
                story.append(Paragraph(summary, self.body_style))
                story.append(Spacer(1, 12))
            
            # Add disclaimer
            disclaimer = Paragraph("This is a summary report. For full details, see the complete report.", self.highlight_style)
            story.append(disclaimer)
            
            # Build PDF
            doc.build(story)
            
            return filename
            
        except Exception as e:
            print(f"❌ Error generating summary report: {e}")
            return "" 