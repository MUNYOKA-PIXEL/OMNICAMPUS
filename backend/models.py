# ==================== Feedback Model ====================

class Feedback:
    """Feedback model"""
    
    @staticmethod
    def create(user_id, category, message):
        data = {
            'user_id': user_id,
            'category': category,
            'message': message
        }
        return execute_db('feedback', data, operation='insert')
    
    @staticmethod
    def get_all():
        result = supabase.table('feedback').select(
            '*, user:users(first_name, last_name, student_id, email)'
        ).order('submitted_date', descending=True).execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            user = rec.pop('user')
            if user:
                rec.update(user)
            data.append(rec)
        return data
    
    @staticmethod
    def get_new():
        result = supabase.table('feedback').select(
            '*, user:users(first_name, last_name, student_id, email)'
        ).eq('status', 'new').order('submitted_date').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            user = rec.pop('user')
            if user:
                rec.update(user)
            data.append(rec)
        return data
    
    @staticmethod
    def respond(feedback_id, admin_id, response):
        data = {
            'status': 'replied',
            'admin_response': response,
            'responded_by': admin_id,
            'responded_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('feedback', data, operation='update', filters={'id': feedback_id})
