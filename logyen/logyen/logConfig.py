from ddtrace import tracer
import json, os, logging
from datetime import datetime


class LogConfig:
    ddAgent = os.getenv("DD_AGENT", None)
    ddAgentPort = os.getenv("DD_AGENT_PORT", None)
    loggerName = os.getenv("LOGGER_NAME", None)
    loggingLevel = os.getenv("LOGGING_LEVEL", logging.DEBUG)
    logDir = os.getenv("LOGS_DIR", None)

    logger = None

    @classmethod
    def initialize(cls, datadogHost=None, datadogPort=None, loggerName=None, logsDirectory=None, logLevel=None):
        # Set values from provided arguments or environment variables
        cls.ddAgent = datadogHost or cls.ddAgent
        cls.ddAgentPort = datadogPort or cls.ddAgentPort
        cls.loggerName = loggerName or cls.loggerName
        cls.logDir = logsDirectory or cls.logDir
        cls.loggingLevel = logLevel or cls.loggingLevel

        cls._validate_config()
        cls.setup_Logging()

    @classmethod
    def setup_Logging(cls):
        """Set up logging with Datadog tracer and file handler."""
        cls._validate_config()

        tracer.configure(hostname=cls.ddAgent, port=cls.ddAgentPort)
        cls.logger = logging.getLogger(cls.loggerName)
        cls.logger.setLevel(cls.loggingLevel)

        # Ensure log directory exists
        os.makedirs(cls.logDir, exist_ok=True)
        logFilePath = os.path.join(cls.logDir, datetime.now().strftime("%Y-%m-%d") + '.log')

        # Set up file handler
        file_handler = logging.FileHandler(logFilePath)
        file_handler.setFormatter(cls.JSONFormatter())
        cls.logger.addHandler(file_handler)

    @classmethod
    def _validate_config(cls):
        """Ensure all required configuration values are set."""
        if not all([cls.ddAgent, cls.ddAgentPort, cls.loggerName, cls.loggingLevel, cls.logDir]):
            raise ValueError("All required values (DD_AGENT, DD_AGENT_PORT, LOGGER_NAME, LOGGING_LEVEL, LOGS_DIR) must be provided.")

    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                'timeStamp': self.formatTime(record),
                'level': record.levelname,
                'name': record.name,
                'message': record.getMessage(),
                'lineNumber': record.lineno,
                'filename': record.filename
            }
            return json.dumps(log_entry)


# Simplified Function for Logging Initialization
def setupLogging(datadogHost=None, datadogPort=None, loggerName=None, logsDirectory=None, logLevel=None):

    LogConfig.initialize(
        datadogHost=datadogHost,
        datadogPort=datadogPort,
        loggerName=loggerName,
        logsDirectory=logsDirectory,
        logLevel=logLevel,
    )
    return LogConfig.logger
