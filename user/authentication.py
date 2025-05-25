# from rest_framework import authentication, exceptions
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from rest_framework_simplejwt.token_blacklist.models import (BlacklistedToken,
#                                                              OutstandingToken)
# from rest_framework_simplejwt.tokens import AccessToken


# class CustomJWTAuthentication(JWTAuthentication):
#     """
#     Custom JWT authentication that checks if the refresh token has been blacklisted.
#     This prevents users who have logged out from accessing protected endpoints
#     with their access token that hasn't expired yet.
#     """

#     def authenticate(self, request):
#         try:
#             # Perform the standard JWT authentication first
#             result = super().authenticate(request)

#             # If authentication didn't return anything, return None
#             if result is None:
#                 return None

#             user, token = result

#             # Extract the raw token string
#             raw_token = self.get_raw_token(self.get_header(request))
#             if raw_token is None:
#                 return None

#             # Decode the token
#             try:
#                 access_token = AccessToken(raw_token)
#                 token_payload = access_token.payload

#                 # Check if the related refresh token is blacklisted
#                 # Get the jti (JWT ID) from the token payload
#                 token_jti = token_payload.get("jti")

#                 # Check if any blacklisted token exists with this user
#                 # outstanding_tokens = OutstandingToken.objects.filter(
#                 #     user=user, jti=token_jti
#                 # )
#                 blacklisted_tokens = BlacklistedToken.objects.filter(
#                     token__user=user
#                 ).exists()
#                 if blacklisted_tokens:
#                     raise exceptions.AuthenticationFailed(
#                         "User telah logout, harap login kembali."
#                     )

#                 # If token is blacklisted, deny authentication
#                 # for outstanding_token in outstanding_tokens:
#                 #     if BlacklistedToken.objects.filter(
#                 #         token=outstanding_token
#                 #     ).exists():
#                 #         raise exceptions.AuthenticationFailed(
#                 #             "Token is blacklisted due to logout. Please login again."
#                 #         )

#             except (InvalidToken, TokenError):
#                 raise exceptions.AuthenticationFailed("Invalid token")

#             return result

#         except Exception as e:
#             # If any exception occurs during authentication, deny access
#             raise exceptions.AuthenticationFailed(str(e))
