from flask import Flask, Response


def register_security_headers(app: Flask) -> None:
    """Add security-related HTTP headers to every response."""

    @app.after_request
    def add_security_headers(response: Response) -> Response:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            "style-src 'self'  https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "font-src 'self' data: https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'"
        )

        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["Referrer-Policy"] = (
            "strict-origin-when-cross-origin"
        )

        response.headers["Permissions-Policy"] = (
            "camera=(), "
            "microphone=(), "
            "geolocation=(), "
            "payment=(), "
            "usb=()"
        )

        response.headers["Cross-Origin-Opener-Policy"] = (
            "same-origin"
        )

        response.headers["Cross-Origin-Resource-Policy"] = (
            "same-origin"
        )

        response.headers["Cross-Origin-Embedder-Policy"] = (
            "credentialless"
        )

        return response