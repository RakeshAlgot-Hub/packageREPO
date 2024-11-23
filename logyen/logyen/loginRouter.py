from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from .config import KeycloakConfig,MongoConfig
from .mongoData import findUser
from .logConfig import setupLogging

class UserLogin(BaseModel):
    email:str
    password:str

router = APIRouter()
@router.post("/login")
async def userLogin(user: UserLogin, response: Response):
    try:   
        logger = setupLogging()        
        email = user.email.lower()
        logger.debug(f"Attempting login for user: {email}")

        if KeycloakConfig.keycloak_openid is None or MongoConfig.collection is None:
            print(MongoConfig.collection)
            logger.error("KeycloakConfig or MongoConfig is not configured.")
            return {"code": 9997, "message": "Please configure MongoConfig and KeycloakConfig first."}

        token_response = KeycloakConfig.keycloak_openid.token(grant_type='password', username=email, password=user.password)
        logger.info(f"Token response received for user: {email}")

        try:
            existingUser = findUser(email)
            if not existingUser:
                logger.warning(f"User {email} not found in MongoDB. Please check configuration.")
                return {"code": 9999, "message": "Please contact customer support."}

        except Exception as e:
            logger.error(f"Error while finding user {email} in MongoDB: {e}")
            return {"code": 9998, "message": "Please try again later."}

        response.set_cookie(key="access_token", value=token_response["access_token"], httponly=True, secure=False)
        existingUser.pop("_id", None)
        user_details = existingUser

        logger.info(f"User {email} successfully logged in.")
        return {"code": 1004, "message": "Login successful.", "result": user_details}

    except Exception as e:
        if "invalid_grant" in str(e):
            logger.error(f"Invalid username or password for {email}.")
            return {"code": 1003, "message": "Invalid username or password"}
        
        logger.error(f"Unexpected error during login for {email}: {e}")
        return {"code": 9998, "message": "Please try again later."}

@router.post("/logout")
async def userLogout(request: Request, response: Response):
    try:
        logger = setupLogging() 
        access_token = request.cookies.get('access_token')
        if access_token:
            user_info = KeycloakConfig.keycloak_openid.userinfo(access_token)
            logger.info(f"Logging out user {user_info['email']}")
            await KeycloakConfig.keycloak_openid.a_logout(user_info["email"])
        else:
            logger.warning("No access token found, deleting cookie.")
            response.delete_cookie(key="access_token")

        logger.info("User successfully logged out.")
        return {"code": 1025, "message": "User successfully logged out."}
    
    except Exception as e:
        logger.error(f"Logout failed: {e}")
        return {"code": 1026, "message": "User logout failed."}