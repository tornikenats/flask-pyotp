import pyotp
from flask import request, Response


class PyOTP():
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app, config_prefix='PYOTP'):
        def key(suffix):
            return '%s_%s' % (config_prefix, suffix)

        secret_key = app.config[key('SECRET_KEY')]
        if not secret_key:
            raise Exception(f"{key('SECRET_KEY')} must best set")

        self.otp_type = app.config.get(key('OTP_TYPE'), 'TOTP')

        if self.otp_type == 'TOTP':
            self.totp = pyotp.TOTP(secret_key)
        elif self.otp_type == 'HOTP':
            self.hotp = pyotp.HOTP(secret_key)

    def now(self):
        check_type('HOTP')
        return self.totp.now()

    def at(self, counter):
        check_type('TOTP')
        return self.hotp.at(counter)

    def verify(self, token, counter=None):
        if self.otp_type == 'HOTP':
            if not counter:
                raise Exception('Must supply counter to verify HOTP token')
            return self.hotp.verify(token, counter)
        elif self.otp_type == 'TOTP':
            return self.totp.verify(token)

    def check_type(self, wrong_type):
        if self.otp_type == wrong_type:
            raise Exception(f'Not initialized for {wrong_type}')
