import config
import sentry_sdk
from redbloom import routes
from taozi import create_app
from sentry_sdk.integrations.flask import FlaskIntegration

app = create_app(config, name='redbloom', blueprints=[routes])

if not app.debug:
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=[FlaskIntegration()]
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
