from fastapi import HTTPException, Request, status
from fastapi_jwt_auth import AuthJWT
from typing import Optional

from models import User
from schemas import Tokens


class AuthUser:
    """
    Class for authenticating user. Authentication is possible by bearer token, email or password and email.
    Additionally user can be verified by two-factor code from Google Authenticator. Use as dependency injection:
    authorize: AuthUser = Depends()
    """

    def __init__(self, request: Request):
        """
        :param request: Incoming request to current API endpoint
        """
        self.user: Optional[User] = None
        self.request = request

    async def requires_access_token(self, required=True):
        """
        Expects Authorization header with Bearer token
        :raise: token-related HTTPExceptions from AuthJWT
        :raise: HTTPException 401 if no user with corresponding token exists
        :return:
        """
        # print(self.request.headers)
        jwt_authorize = AuthJWT(req=self.request)
        if required:
            jwt_authorize.jwt_required()
        user = await User.get_or_none(
            email=jwt_authorize.get_jwt_subject()
        )
        if user is None and required:
            self._raise_unauthorized()
        self.user = user

    def get_user(self) -> User:
        """
        Returns User which contains non-authorization user data and relations: profile info, payment cards,
        transactions, etc. If called before any authorization was performed throws HTTP exception with code 401
        "Unauthorized" :return:
        """
        if self.user is None:
            self._raise_unauthorized()
        return self.user

    def get_user_or_none(self):
        if self.user is None:
            return None
        return self.user

    def _raise_unauthorized(self, msg="Unauthorized"):
        self.user = None
        self.active_user = None
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)

    def create_tokens(self) -> Tokens:
        """
        Requires self.user being not None
        :raise: HTTPException 401 if no user
        :return:
        """
        if self.user is None:
            self._raise_unauthorized()
        jwt_authorize = AuthJWT(self.request)
        access = jwt_authorize.create_access_token(subject=self.user.email)
        refresh = jwt_authorize.create_refresh_token(subject=self.user.email)
        return Tokens(access_token=access, refresh_token=refresh)
