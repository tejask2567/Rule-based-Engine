from flask import Blueprint, request, jsonify, render_template
from app.models import Rule
from app.rule_engine import RuleEngine
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Render main page."""
    return render_template('index.html')

@bp.route('/api/rules', methods=['GET'])
def get_rules():
    """Get all rules."""
    rules = Rule.query.all()
    return jsonify([rule.to_dict() for rule in rules])

@bp.route('/api/rules', methods=['POST'])
def create_rule():
    """Create new rule."""
    data = request.get_json()
    
    if not data or 'rule_string' not in data or 'name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        ast = RuleEngine.create_rule(data['rule_string'])
        rule = Rule(
            name=data['name'],
            rule_string=data['rule_string'],
            ast_json=ast.to_dict()
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({'message': 'Rule created successfully', 'id': rule.id}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/api/rules/evaluate', methods=['POST'])
def evaluate_rule():
    """Evaluate rule against provided data."""
    data = request.get_json()
    
    if not data or 'rule_id' not in data or 'data' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    rule = Rule.query.get(data['rule_id'])
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404
    
    try:
        result = RuleEngine.evaluate_rule(rule.ast_json, data['data'])
        return jsonify({'result': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/api/rules/combine/preview', methods=['POST'])
def preview_combined_rules():
    """Preview combined rules without saving."""
    data = request.get_json()
    
    if not data or 'rule_ids' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        rules = Rule.query.filter(Rule.id.in_(data['rule_ids'])).all()
        if len(rules) != len(data['rule_ids']):
            return jsonify({'error': 'One or more rules not found'}), 404
        
        rule_strings = [rule.rule_string for rule in rules]
        combined_ast = RuleEngine.combine_rules(rule_strings)
        combined_rule_string = RuleEngine.ast_to_string(combined_ast)
        
        return jsonify({
            'combined_rule_string': combined_rule_string
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/api/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    """Delete a rule."""
    rule = Rule.query.get(rule_id)
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404
    
    db.session.delete(rule)
    db.session.commit()
    return jsonify({'message': 'Rule deleted successfully'}), 200

@bp.route('/api/rules/combine', methods=['POST'])
def combine_rules():
    """Combine multiple rules into a new rule."""
    data = request.get_json()
    
    if not data or 'rule_ids' not in data or 'name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        rules = Rule.query.filter(Rule.id.in_(data['rule_ids'])).all()
        if len(rules) != len(data['rule_ids']):
            return jsonify({'error': 'One or more rules not found'}), 404
        
        rule_strings = [rule.rule_string for rule in rules]
        combined_ast = RuleEngine.combine_rules(rule_strings)
        combined_rule_string = RuleEngine.ast_to_string(combined_ast)
        
        new_rule = Rule(
            name=data['name'],
            rule_string=combined_rule_string,
            ast_json=combined_ast.to_dict()
        )
        
        db.session.add(new_rule)
        db.session.commit()
        
        return jsonify({
            'message': 'Rules combined successfully',
            'id': new_rule.id
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400