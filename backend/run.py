"""Application entry point."""

from werkzeug.serving import WSGIRequestHandler

from app import create_app


class SecureRequestHandler(WSGIRequestHandler):
    """Hide Werkzeug and Python version information."""

    def version_string(self) -> str:
        return "SecureBankingServer"


app = create_app()


if __name__ == "__main__":
    app.run(
        # Binding to all interfaces is required inside the Docker container.
        host="0.0.0.0",  # nosec B104
        port=5000,
        debug=False,
        request_handler=SecureRequestHandler,
    )