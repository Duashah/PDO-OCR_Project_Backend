# # app/templates/email_templates.py
# def get_reset_password_template(otp: str) -> str:
#     return f"""
#     <html>
#         <body style="font-family: Arial, sans-serif;">
#             <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
#                 <h2 style="color: #333;">Password Reset Request</h2>
#                 <p>Your OTP for password reset is: <strong>{otp}</strong></p>
#                 <p>This OTP will expire in 15 minutes.</p>
#                 <p>If you didn't request this, please ignore this email.</p>
#             </div>
#         </body>
#     </html>
#     """

from app.core.config import settings

def get_reset_password_link_template(reset_link: str) -> str:
    return f"""
    <html>
    <body>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_link}">Reset Password</a>
        <p>This link will expire in {settings.OTP_EXPIRY_MINUTES} minutes.</p>
    </body>
    </html>
    """