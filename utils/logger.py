"""
Logging configuration for Jungle Game.
Provides centralized logging setup for debugging and troubleshooting.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class GameLogger:
    """
    Centralized logging configuration for the Jungle Game.
    
    Provides methods to configure logging with different levels and outputs,
    including console and file logging with rotation support.
    """
    
    # Default log format
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DETAILED_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    
    # Log directory
    LOG_DIR = Path('logs')
    
    _initialized = False
    _log_file: Optional[Path] = None
    
    @classmethod
    def initialize(
        cls,
        level: int = logging.INFO,
        log_to_file: bool = True,
        log_to_console: bool = True,
        detailed: bool = False
    ) -> None:
        """
        Initialize the logging system.
        
        Args:
            level: Logging level (e.g., logging.DEBUG, logging.INFO)
            log_to_file: Whether to log to a file
            log_to_console: Whether to log to console
            detailed: Whether to use detailed format with file/line info
        """
        if cls._initialized:
            return
        
        # Create logs directory if it doesn't exist
        if log_to_file:
            cls.LOG_DIR.mkdir(exist_ok=True)
            
            # Create log file with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            cls._log_file = cls.LOG_DIR / f'jungle_game_{timestamp}.log'
        
        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Remove existing handlers
        root_logger.handlers.clear()
        
        # Choose format
        log_format = cls.DETAILED_FORMAT if detailed else cls.DEFAULT_FORMAT
        formatter = logging.Formatter(log_format)
        
        # Add console handler
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # Add file handler
        if log_to_file and cls._log_file:
            file_handler = logging.FileHandler(cls._log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        cls._initialized = True
        
        # Log initialization
        logger = logging.getLogger(__name__)
        logger.info("Logging system initialized")
        if cls._log_file:
            logger.info(f"Log file: {cls._log_file}")
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get a logger instance for a specific module.
        
        Args:
            name: Name of the module (typically __name__)
        
        Returns:
            Logger instance
        """
        if not cls._initialized:
            cls.initialize()
        
        return logging.getLogger(name)
    
    @classmethod
    def set_level(cls, level: int) -> None:
        """
        Change the logging level for all handlers.
        
        Args:
            level: New logging level
        """
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        for handler in root_logger.handlers:
            handler.setLevel(level)
    
    @classmethod
    def get_log_file(cls) -> Optional[Path]:
        """
        Get the current log file path.
        
        Returns:
            Path to log file, or None if file logging is disabled
        """
        return cls._log_file
    
    @classmethod
    def cleanup_old_logs(cls, keep_days: int = 7) -> int:
        """
        Clean up log files older than specified days.
        
        Args:
            keep_days: Number of days to keep logs
        
        Returns:
            Number of files deleted
        """
        if not cls.LOG_DIR.exists():
            return 0
        
        deleted_count = 0
        cutoff_time = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        
        for log_file in cls.LOG_DIR.glob('jungle_game_*.log'):
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    deleted_count += 1
                except Exception as e:
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to delete old log file {log_file}: {e}")
        
        return deleted_count


# Convenience function for getting loggers
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    This is a convenience function that wraps GameLogger.get_logger().
    
    Args:
        name: Name of the module (typically __name__)
    
    Returns:
        Logger instance
    """
    return GameLogger.get_logger(name)
