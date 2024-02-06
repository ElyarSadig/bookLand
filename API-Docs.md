# API Endpoints

## Authentication Endpoints

- **/api/auth/login**: Allows users and publishers to log in to the platform.
- **/api/auth/user/signup**: Enables users to sign up for a new account.
- **/api/auth/publisher/signup**: Allows publishers to sign up for a new account.
- **/api/auth/reset-password**: Handles the password reset process for users and publishers.
- **/api/auth/send-resetpassword-code**: Sends a reset password code to the user's email.
- **/api/auth/send-signup-email**: Sends a signup confirmation email to the user or publisher.
- **/api/auth/verify-email-code**: Verifies the activation code sent to the user's email.

## User Endpoints

- **/api/user/profile**: Retrieves the user's profile information.
- **/api/user/change-password**: Allows users to change their passwords.
- **/api/user/wallet-balance**: Retrieves the user's wallet balance.
- **/api/user/wallet-history**: Retrieves the user's wallet transaction history.
- **/api/user/books**: Retrieves books bookmarked by the user.
- **/api/user/bookmarks**: Allows users to bookmark or unbookmark books.
  
## Publisher Endpoints

- **/api/publisher/profile**: Retrieves the publisher's profile information.
- **/api/publisher/change-password**: Allows publishers to change their passwords.
- **/api/publisher/wallet-balance**: Retrieves the publisher's wallet balance.
- **/api/publisher/wallet-history**: Retrieves the publisher's wallet transaction history.
- **/api/publisher/books**: Retrieves books published by the publisher.

## API Swagger
- **api/schema/**: This endpoint provides the OpenAPI schema for the API.

- **api/schema/swagger-ui/**: This endpoint serves the Swagger UI interface, which is a user-friendly graphical representation of your API's documentation.
