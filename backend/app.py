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






import ssl
from okta.request_executor import RequestExecutor

# Initialize OpenIDConnect
oidc = OpenIDConnect(app)

 

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Patch the requests session

old_init = requests.Session.__init__

 

def new_init(self, *args, **kwargs):

    old_init(self, *args, **kwargs)

    self.verify = False

 

requests.Session.__init__ = new_init

 

# Initialize Okta Client normally

okta_client = OktaClient({

    'orgUrl': os.getenv("OKTA_ORG_URL"),

    'token': os.getenv("OKTA_API_TOKEN")

})




# Helper functions

# def get_mfa_factors_by_subscription(subscription):

#     factors = {

#         "basic": ["oktaverify"],

#         "premium": ["oktaverify", "google"],

#         "premium+": ["oktaverify", "securityquestion", "google"]

#     }

#     return factors.get(subscription, ["oktaverify"])

 

class SignupResource(Resource):

    def post(self):

        data = request.get_json()

       

        try:

            # Create user in Okta using direct requests

            user_profile = {

                "firstName": data["firstName"],

                "lastName": data["lastName"],

                "email": data["email"],

                "login": data["email"],

                "subscription": data.get("subscription", "basic"),

                # "source": request.headers.get("Origin", "direct"),

                "appAccess": True

            }

           

            user_credentials = {

                "password": {"value": data["password"]}

            }

           

            user = {

                "profile": user_profile,

                "credentials": user_credentials

            }

           

            # Prepare the request

            okta_url = f"{os.getenv('OKTA_ORG_URL')}/api/v1/users"

            headers = {

                "Accept": "application/json",

                "Content-Type": "application/json",

                "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}"

            }

            params = {"activate": "true"}

           

            # Make the request with SSL verification disabled

            response = requests.post(

                okta_url,

                headers=headers,

                params=params,

                json=user,

                verify=False

            )

           

            if response.status_code >= 400:

                return {"error": response.json()}, response.status_code

           

            created_user = response.json()

            return {"message": "User created successfully", "id": created_user["id"]}, 201

           

        except Exception as e:

            return {"error": str(e)}, 400





class UserProfileResource(Resource):

    @oidc.require_login

    def get(self):

        try:

            user_info = oidc.user_getinfo(["sub", "name", "email"])

            okta_id = user_info.get("sub")

           

            # Get full user profile from Okta using direct requests

            okta_url = f"{os.getenv('OKTA_ORG_URL')}/api/v1/users/{okta_id}"

            headers = {

                "Accept": "application/json",

                "Content-Type": "application/json",

                "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}"

            }

           

            # Make the request with SSL verification disabled

            response = requests.get(

                okta_url,

                headers=headers,

                verify=False

            )

           

            if response.status_code >= 400:

                return {"error": response.json()}, response.status_code

           

            user_data = response.json()

           

            # Get user's subscription and other profile attributes

            profile = user_data.get("profile", {})

            subscription = profile.get("subscription", "basic")

            source = profile.get("source", "direct")

           

            # Get additional profile attributes if they exist

            mobilePhone = profile.get("mobilePhone", "")

            secondEmail = profile.get("secondEmail", "")

            city = profile.get("city", "")

            state = profile.get("state", "")

            countryCode = profile.get("countryCode", "")

           

            # Get available factors based on subscription

            # available_factors = get_mfa_factors_by_subscription(subscription)

           

            # Get enrolled factors

            # enrolled_factors = []

            # In a real implementation, you would get enrolled factors from Okta API

           

            return {

                "profile": {

                    "id": okta_id,

                    "firstName": profile.get("firstName", ""),

                    "lastName": profile.get("lastName", ""),

                    "email": profile.get("email", ""),

                    "subscription": subscription,

                    "source": source,

                    "mobilePhone": mobilePhone,

                    "secondEmail": secondEmail,

                    "city": city,

                    "state": state,

                    "countryCode": countryCode

                },

                # "mfa": {

                #     "available": available_factors,

                #     "enrolled": enrolled_factors

                # }

            }

        except Exception as e:

            app.logger.error(f"Profile error: {str(e)}")

            return {"error": str(e)}, 400

 

    @oidc.require_login

    def put(self):

        try:

            data = request.get_json()

            user_info = oidc.user_getinfo(["sub", "email"])

            okta_id = user_info.get("sub")

           

            # Update user in Okta using direct requests

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

           

            # Prepare the request

            okta_url = f"{os.getenv('OKTA_ORG_URL')}/api/v1/users/{okta_id}"

            headers = {

                "Accept": "application/json",

                "Content-Type": "application/json",

                "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}"

            }

           

            # Make the request with SSL verification disabled

            response = requests.post(

                okta_url,

                headers=headers,

                json=user_data,

                verify=False

            )

           

            if response.status_code >= 400:

                app.logger.error(f"Update error: {response.json()}")

                return {"error": response.json()}, response.status_code

               

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
            
            # List all supported factors
            okta_url_supported = f"{os.getenv('OKTA_ORG_URL')}/api/v1/users/{okta_id}/factors/catalog"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}"
            }
            response_supported = requests.get(okta_url_supported, headers=headers, verify=False)
            
            if response_supported.status_code >= 400:
                return {"error": response_supported.json()}, response_supported.status_code
            
            supported_factors = response_supported.json()
            
            # List all enrolled factors
            okta_url_enrolled = f"{os.getenv('OKTA_ORG_URL')}/api/v1/users/{okta_id}/factors"
            response_enrolled = requests.get(okta_url_enrolled, headers=headers, verify=False)
            
            if response_enrolled.status_code >= 400:
                return {"error": response_enrolled.json()}, response_enrolled.status_code
            
            enrolled_factors = response_enrolled.json()

            for factor in enrolled_factors:
                factor_id = factor.get("factorType")
                factore_name = factor.get("provider") if factor_id == "token:software:totp" else factor_id
                factor["name"] = factore_name
            
            # Prepare response
            response_data = {
                "supported_factors": supported_factors,
                "enrolled_factors": enrolled_factors
            }
            
            # Add enrollment status for each supported factor
            for factor in supported_factors:
                factor_id = factor.get("factorType")
                factore_name = factor.get("provider") if factor_id == "token:software:totp" else factor_id
                factor["name"] = factore_name
                is_enrolled = any([f for f in enrolled_factors if f.get("name") == factore_name])
                factor["enrolled"] = is_enrolled
            
            return response_data
        
        except Exception as e:
            return {"error": str(e)}, 400

    @oidc.require_login
    def post(self):
        try:
            data = request.get_json()
            user_info = oidc.user_getinfo(["sub"])
            okta_id = user_info.get("sub")
            
            # Enroll a new factor
            okta_url_enroll = f"{os.getenv('OKTA_ORG_URL')}/api/v1/users/{okta_id}/factors"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}"
            }
            
            # Prepare factor data based on type
            factor_type = data.get("factor_type")
            if factor_type == "question":
                factor_data = {
                    "factorType": "question",
                    "provider": "OKTA",
                    "profile": {
                        "question": data.get("question"),
                        "answer": data.get("answer")

                    }
                }
            elif factor_type == "OKTA":
                factor_data = {
                    "factorType": "token:software:totp",
                    "provider": "OKTA"
                }
            elif factor_type == "GOOGLE":
                factor_data = {
                    "factorType": "token:software:totp",
                    "provider": "GOOGLE"
                }
            else:
                return {"error": "Unsupported factor type"}, 400
            
            response = requests.post(okta_url_enroll, headers=headers, json=factor_data, verify=False)
            
            if response.status_code >= 400:
                return {"error": response.json()}, response.status_code
            
            # Return the enrollment response including QR code and activation links
            enrollment_data = response.json()
            return enrollment_data, 201
        
        except Exception as e:
            return {"error": str(e)}, 400
        
    @oidc.require_login
    def put(self):
        try:
            data = request.get_json()
            activation_link = data.get("activation_link")
            pass_code = data.get("pass_code")
            
            if not activation_link or not pass_code:
                return {"error": "Activation link and pass code are required"}, 400
                
            # Prepare the activation request
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}"
            }
            
            activation_data = {
                "passCode": pass_code
            }
            
            # Make the activation request
            response = requests.post(
                activation_link,
                headers=headers,
                json=activation_data,
                verify=False
            )
            
            if response.status_code >= 400:
                return {"error": response.json()}, response.status_code
            
            return {"message": "Factor activated successfully"}, 200
            
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
        
@app.route('/api/mfa/questions', methods=['GET'])
@oidc.require_login
def get_security_questions():
    try:
        user_info = oidc.user_getinfo(["sub"])
        okta_id = user_info.get("sub")
        
        # Get security questions from Okta
        okta_url = f"{os.getenv('OKTA_ORG_URL')}/api/v1/users/{okta_id}/factors/questions"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}"
        }
        
        response = requests.get(okta_url, headers=headers, verify=False)
        
        if response.status_code >= 400:
            return jsonify({"error": response.json()}), response.status_code
        
        return jsonify(response.json()), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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

        state=state,

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


    return oidc.logout(return_to=url_for('index', _external=True))

if __name__ == '__main__':
    app.run(debug=True)