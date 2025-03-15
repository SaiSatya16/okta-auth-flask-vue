import asyncio
from flask import Flask, jsonify, request, session, redirect, url_for
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_oidc import OpenIDConnect
from okta.client import Client as OktaClient
import os
from dotenv import load_dotenv
import json
from flask_session import Session
# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:8080", "http://localhost:5000"], 
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     expose_headers=["Content-Type", "Authorization"],
     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])




api = Api(app)

# Configure Okta
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False  # Set to True in production
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "a-very-secret-key")  # Ensure this is set
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
app.config["OIDC_INTROSPECTION_AUTH_METHOD"] = "client_secret_post"
app.config["OIDC_RESOURCE_SERVER_ONLY"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # Set to True in production
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

Session(app)








# Initialize OpenIDConnect
oidc = OpenIDConnect(app)

# Initialize Okta Client
okta_client = OktaClient({
    'orgUrl': os.getenv("OKTA_ORG_URL"),
    'token': os.getenv("OKTA_API_TOKEN")
})

# Helper functions
def get_mfa_factors_by_subscription(subscription):
    factors = {
        "basic": ["oktaverify"],
        "premium": ["oktaverify", "google"],
        "premium+": ["oktaverify", "phone", "google"]
    }
    return factors.get(subscription, ["oktaverify"])


class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        
        try:
            # Create user in Okta
            user_profile = {
                "firstName": data["firstName"],
                "lastName": data["lastName"],
                "email": data["email"],
                "login": data["email"],
                "subscription": data.get("subscription", "basic"),
                "source": request.headers.get("Origin", "direct"),
                "appAccess": True
            }
            
            user_credentials = {
                "password": {"value": data["password"]}
            }
            
            user = {
                "profile": user_profile,
                "credentials": user_credentials
            }
            
            # Pass activate as a query parameter
            query_params = {"activate": "true"}
            
            # Use asyncio to run the coroutine
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            created_user, resp, err = loop.run_until_complete(
                okta_client.create_user(user, query_params)
            )
            
            if err:
                return {"error": str(err)}, 400
            
            
                
            return {"message": "User created successfully", "id": created_user.id}, 201
            
        except Exception as e:
            return {"error": str(e)}, 400



class UserProfileResource(Resource):
    @oidc.require_login
    def get(self):
        try:
            user_info = oidc.user_getinfo(["sub", "name", "email"])
            okta_id = user_info.get("sub")
            
            # Get full user profile from Okta
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            user, resp, err = loop.run_until_complete(
                okta_client.get_user(okta_id)
            )
            
            if err:
                return {"error": str(err)}, 400
            
            # Get user's subscription and other profile attributes
            subscription = user.profile.subscription if hasattr(user.profile, 'subscription') else "basic"
            source = user.profile.source if hasattr(user.profile, 'source') else "direct"
            
            # Get additional profile attributes if they exist
            mobilePhone = user.profile.mobilePhone if hasattr(user.profile, 'mobilePhone') else ""
            secondEmail = user.profile.secondEmail if hasattr(user.profile, 'secondEmail') else ""
            city = user.profile.city if hasattr(user.profile, 'city') else ""
            state = user.profile.state if hasattr(user.profile, 'state') else ""
            countryCode = user.profile.countryCode if hasattr(user.profile, 'countryCode') else ""
            
            # Get available factors based on subscription
            available_factors = get_mfa_factors_by_subscription(subscription)
            
            # Get enrolled factors
            enrolled_factors = []
            # In a real implementation, you would get enrolled factors from Okta API
            
            return {
                "profile": {
                    "id": okta_id,
                    "firstName": user.profile.firstName,
                    "lastName": user.profile.lastName,
                    "email": user.profile.email,
                    "subscription": subscription,
                    "source": source,
                    "mobilePhone": mobilePhone,
                    "secondEmail": secondEmail,
                    "city": city,
                    "state": state,
                    "countryCode": countryCode
                },
                "mfa": {
                    "available": available_factors,
                    "enrolled": enrolled_factors
                }
            }
        except Exception as e:
            app.logger.error(f"Profile error: {str(e)}")
            return {"error": str(e)}, 400

    @oidc.require_login
    def put(self):
        try:
            data = request.get_json()
            user_info = oidc.user_getinfo(["sub"])
            okta_id = user_info.get("sub")
            
            # Update user in Okta
            user_data = {
                "profile": {
                    "email": user_info.get("email"),
                    "login": user_info.get("email"),
                    "firstName": data.get("firstName"),
                    "lastName": data.get("lastName"),
                    "subscription": data.get("subscription"),
                    "appAccess": True
                }
            }
            
            # Add additional fields if they are provided
            if "mobilePhone" in data:
                user_data["profile"]["mobilePhone"] = data.get("mobilePhone")
            if "secondEmail" in data:
                user_data["profile"]["secondEmail"] = data.get("secondEmail")
            if "city" in data:
                user_data["profile"]["city"] = data.get("city")
            if "state" in data:
                user_data["profile"]["state"] = data.get("state")
            if "countryCode" in data:
                user_data["profile"]["countryCode"] = data.get("countryCode")
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            _, resp, err = loop.run_until_complete(
                okta_client.update_user(okta_id, user_data)
            )
            
            if err:
                app.logger.error(f"Update error: {str(err)}")
                return {"error": str(err)}, 400
                
            return {"message": "Profile updated successfully"}
        except Exception as e:
            app.logger.error(f"Update exception: {str(e)}")
            return {"error": str(e)}, 400



class MFAResource(Resource):
    @oidc.require_login
    def get(self):
        try:
            user_info = oidc.user_getinfo(["sub"])
            okta_id = user_info.get("sub")
            
            # Get user from Okta
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            user, resp, err = loop.run_until_complete(
                okta_client.get_user(okta_id)
            )
            
            if err:
                app.logger.error(f"MFA get error: {str(err)}")
                return {"error": str(err)}, 400
                
            # Get subscription
            subscription = user.profile.subscription if hasattr(user.profile, 'subscription') else "basic"
            
            # Get available factors based on subscription
            available_factors = get_mfa_factors_by_subscription(subscription)
            
            # Get enrolled factors (simplified)
            enrolled_factors = []
            
            return {
                "available_factors": available_factors,
                "enrolled_factors": enrolled_factors
            }
        except Exception as e:
            app.logger.error(f"MFA get exception: {str(e)}")
            return {"error": str(e)}, 400

    
    @oidc.require_login
    def post(self):
        data = request.get_json()
        user_info = oidc.user_getinfo(["sub"])
        okta_id = user_info.get("sub")
        
        factor_type = data.get("factor_type")
        
        try:
            # Get user from Okta
            user, resp, err = okta_client.get_user(okta_id)
            if err:
                return {"error": str(err)}, 400
                
            # Get subscription
            subscription = user.profile.subscription if hasattr(user.profile, 'subscription') else "basic"
            
            # Verify if the factor is allowed for this subscription
            available_factors = get_mfa_factors_by_subscription(subscription)
            if factor_type not in available_factors:
                return {"error": "Factor not available for your subscription"}, 403
            
            # In a real implementation, you would enroll the factor using Okta API
            # This is a simplified example
            
            return {"message": f"{factor_type} factor enrolled successfully"}
        except Exception as e:
            return {"error": str(e)}, 400

class LoginStatusResource(Resource):
    def get(self):
        try:
            # Check if user is logged in
            is_logged_in = oidc.user_loggedin
            # If logged in, get some basic user info
            user_info = None
            if is_logged_in:
                user_info = oidc.user_getinfo(['sub', 'name', 'email'])
            
            return {
                "loggedIn": is_logged_in,
                "userInfo": user_info
            }
        except Exception as e:
            return {"loggedIn": False, "error": str(e)}


# Add resources to API
api.add_resource(SignupResource, '/api/signup')
api.add_resource(UserProfileResource, '/api/profile')
api.add_resource(MFAResource, '/api/mfa')
api.add_resource(LoginStatusResource, '/api/login-status')

# Login and logout routes
# In app.py, update your login route
@app.route('/login')
def login():
    # Generate a secure state parameter
    state = os.urandom(16).hex()
    session['oauth_state'] = state
    
    # Include state in the authorization request
    return oidc.redirect_to_auth_server(
        redirect_uri=url_for('oidc_callback', _external=True),
        state=state
    )



import logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/oidc/callback')
def oidc_callback():
    try:
        app.logger.debug("Callback received")
        app.logger.debug(f"Request args: {request.args}")
        
        # Process the callback
        info = oidc.callback()
        app.logger.debug(f"Callback info: {info}")
        
        # Set a session variable to indicate successful login
        user_info = oidc.user_getinfo(['sub', 'name', 'email'])
        session['user_info'] = user_info
        app.logger.debug(f"User info: {user_info}")
        
        # Redirect to frontend profile page
        return redirect('http://localhost:8080/profile')
    except Exception as e:
        app.logger.error(f"Callback error: {str(e)}")
        app.logger.error(f"Callback error details: {repr(e)}")
        return jsonify({"error": str(e)}), 500





@app.route('/')
def index():
    # Redirect to the frontend
    return redirect('http://localhost:8080')



@app.route('/logout')
def logout():
    # Clear the Flask session
    session.clear()
    # Redirect to Okta's logout endpoint with a post_logout_redirect_uri
    return oidc.logout(return_to=url_for('index', _external=True))


if __name__ == '__main__':
    app.run(debug=True)
