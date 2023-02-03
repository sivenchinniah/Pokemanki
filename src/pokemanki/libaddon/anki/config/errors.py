class ConfigError(Exception):
    """
    Thrown whenever a config-specific exception occurs
    """

    pass


class ConfigNotReadyError(ConfigError):
    pass


class ConfigFutureError(ConfigError):
    pass
