import uuid

class AnonymousSessionMiddleware:
    """
    Middleware to ensure every visitor has a unique 'guest_id' cookie.
    Allows tracking streaks and quiz history without forcing a login.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Check for existing cookie
        guest_id = request.COOKIES.get('guest_id')

        # 2. If missing, generate a new UUID
        if not guest_id:
            guest_id = str(uuid.uuid4())
            request.guest_newly_created = True
        else:
            request.guest_newly_created = False

        # Attach to request for easy access in Views
        request.guest_id = guest_id

        response = self.get_response(request)

        # 3. Set the cookie on the response (expires in 1 year)
        if not request.COOKIES.get('guest_id'):
            response.set_cookie(
                'guest_id', 
                guest_id, 
                max_age=365 * 24 * 60 * 60, # 1 year
                httponly=True, # Secure against XSS
                samesite='Lax'
            )

        return response
