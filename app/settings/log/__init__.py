from ._log import LoggerSetup

logger = LoggerSetup(name="Archiver").get_logger()

__all__ = ["logger"]
