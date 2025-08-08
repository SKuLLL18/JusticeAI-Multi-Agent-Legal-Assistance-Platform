from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import sqlite3
from datetime import datetime
import uuid
from agents.user_agent import UserAgent
from agents.legal_agent import LegalAgent
from agents.mediation_agent import MediationAgent
from agents.report_agent import ReportAgent
from agents.escalation_agent import EscalationAgent

# Try to import dotenv, make it optional
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️ python-dotenv not available. Using default environment variables.")
    def load_dotenv():
        pass

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'justiceai-secret-key-2024')

# Initialize database
def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect('database/justiceai.db')
    cursor = conn.cursor()
    
    # Create cases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id TEXT PRIMARY KEY,
            user_name TEXT NOT NULL,
            user_email TEXT,
            issue_category TEXT NOT NULL,
            issue_description TEXT NOT NULL,
            priority_level TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            legal_advice TEXT,
            mediation_suggestions TEXT,
            escalation_recommendations TEXT,
            report_path TEXT
        )
    ''')
    
    # Create agent_logs table for tracking agent interactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT,
            agent_name TEXT,
            action TEXT,
            response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize agents
user_agent = UserAgent()
legal_agent = LegalAgent()
mediation_agent = MediationAgent()
report_agent = ReportAgent()
escalation_agent = EscalationAgent()

@app.route('/')
def index():
    """Main page with the legal issue submission form"""
    return render_template('index.html')

@app.route('/submit_case', methods=['POST'])
def submit_case():
    """Handle case submission and coordinate all agents"""
    try:
        # Extract form data
        user_name = request.form.get('user_name', '').strip()
        user_email = request.form.get('user_email', '').strip()
        issue_category = request.form.get('issue_category', '').strip()
        issue_description = request.form.get('issue_description', '').strip()
        priority_level = request.form.get('priority_level', 'medium')
        
        # Validate required fields
        if not user_name or not issue_category or not issue_description:
            return jsonify({
                'success': False,
                'message': 'Please fill in all required fields.'
            }), 400
        
        # Generate unique case ID
        case_id = str(uuid.uuid4())
        
        # Store case in database
        conn = sqlite3.connect('database/justiceai.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cases (id, user_name, user_email, issue_category, issue_description, priority_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (case_id, user_name, user_email, issue_category, issue_description, priority_level))
        conn.commit()
        conn.close()
        
        # Coordinate agents
        case_data = {
            'id': case_id,
            'user_name': user_name,
            'user_email': user_email,
            'issue_category': issue_category,
            'issue_description': issue_description,
            'priority_level': priority_level
        }
        
        # Step 1: User Agent processes the case
        user_agent_response = user_agent.process_case(case_data)
        log_agent_action(case_id, 'UserAgent', 'process_case', user_agent_response)
        
        # Step 2: Legal Expert Agent provides advice
        legal_advice = legal_agent.provide_legal_advice(case_data)
        log_agent_action(case_id, 'LegalAgent', 'provide_legal_advice', legal_advice)
        
        # Step 3: Mediation Agent suggests resolutions
        mediation_suggestions = mediation_agent.suggest_resolution(case_data)
        log_agent_action(case_id, 'MediationAgent', 'suggest_resolution', mediation_suggestions)
        
        # Step 4: Escalation Agent evaluates severity
        escalation_recommendations = escalation_agent.evaluate_case(case_data)
        log_agent_action(case_id, 'EscalationAgent', 'evaluate_case', escalation_recommendations)
        
        # Step 5: Report Agent generates PDF
        report_path = report_agent.generate_report(case_data, legal_advice, mediation_suggestions, escalation_recommendations)
        if report_path:
            log_agent_action(case_id, 'ReportAgent', 'generate_report', f'Report generated: {report_path}')
        else:
            log_agent_action(case_id, 'ReportAgent', 'generate_report', 'PDF generation disabled - ReportLab not available')
        
        # Update database with agent responses
        conn = sqlite3.connect('database/justiceai.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE cases 
            SET legal_advice = ?, mediation_suggestions = ?, escalation_recommendations = ?, report_path = ?, status = 'completed'
            WHERE id = ?
        ''', (legal_advice, mediation_suggestions, escalation_recommendations, report_path, case_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'case_id': case_id,
            'message': 'Case processed successfully!',
            'legal_advice': legal_advice,
            'mediation_suggestions': mediation_suggestions,
            'escalation_recommendations': escalation_recommendations,
            'report_path': report_path if report_path else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing case: {str(e)}'
        }), 500

@app.route('/download_report/<case_id>')
def download_report(case_id):
    """Download the generated PDF report for a case"""
    try:
        conn = sqlite3.connect('database/justiceai.db')
        cursor = conn.cursor()
        cursor.execute('SELECT report_path FROM cases WHERE id = ?', (case_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            report_path = result[0]
            if os.path.exists(report_path):
                return send_file(report_path, as_attachment=True, download_name=f'justiceai_report_{case_id}.pdf')
            else:
                return jsonify({'error': 'Report file not found'}), 404
        else:
            return jsonify({'error': 'Case not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Error downloading report: {str(e)}'}), 500

@app.route('/case_status/<case_id>')
def case_status(case_id):
    """Get the status and details of a specific case"""
    try:
        conn = sqlite3.connect('database/justiceai.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, user_name, issue_category, issue_description, priority_level, 
                   status, legal_advice, mediation_suggestions, escalation_recommendations, 
                   created_at, report_path
            FROM cases WHERE id = ?
        ''', (case_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            case_data = {
                'id': result[0],
                'user_name': result[1],
                'issue_category': result[2],
                'issue_description': result[3],
                'priority_level': result[4],
                'status': result[5],
                'legal_advice': result[6],
                'mediation_suggestions': result[7],
                'escalation_recommendations': result[8],
                'created_at': result[9],
                'report_path': result[10]
            }
            return jsonify({'success': True, 'case': case_data})
        else:
            return jsonify({'success': False, 'message': 'Case not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error retrieving case: {str(e)}'}), 500

@app.route('/agent_logs/<case_id>')
def agent_logs(case_id):
    """Get the interaction logs for all agents for a specific case"""
    try:
        conn = sqlite3.connect('database/justiceai.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT agent_name, action, response, timestamp
            FROM agent_logs 
            WHERE case_id = ?
            ORDER BY timestamp ASC
        ''', (case_id,))
        results = cursor.fetchall()
        conn.close()
        
        logs = []
        for result in results:
            logs.append({
                'agent_name': result[0],
                'action': result[1],
                'response': result[2],
                'timestamp': result[3]
            })
        
        return jsonify({'success': True, 'logs': logs})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error retrieving logs: {str(e)}'}), 500

def log_agent_action(case_id, agent_name, action, response):
    """Log agent actions for debugging and tracking"""
    try:
        conn = sqlite3.connect('database/justiceai.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO agent_logs (case_id, agent_name, action, response)
            VALUES (?, ?, ?, ?)
        ''', (case_id, agent_name, action, response))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging agent action: {e}")

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'agents': {
            'user_agent': 'active',
            'legal_agent': 'active',
            'mediation_agent': 'active',
            'report_agent': 'active',
            'escalation_agent': 'active'
        }
    })

if __name__ == '__main__':
    # Create database directory if it doesn't exist
    os.makedirs('database', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Initialize database
    init_db()
    
    print("🚀 JusticeAI Platform Starting...")
    print("📋 Multi-Agent Legal Assistance System")
    print("🎯 Supporting SDG Goal 16: Peace, Justice, and Strong Institutions")
    print("🌐 Access the application at: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 