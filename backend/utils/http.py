"""HTTP utilities for API communication and request handling."""

import logging
from typing import Optional, Dict, Any
import json

logger = logging.getLogger(__name__)


class HTTPHelper:
    """Helper class for HTTP operations and request/response handling."""

    @staticmethod
    def serialize_response(data: Any) -> Dict[str, Any]:
        """
        Serialize response data to JSON-compatible format.
        
        Args:
            data: Data to serialize (may contain datetime objects, etc)
            
        Returns:
            JSON-serializable dictionary
        """
        try:
            # Try to JSON encode first to catch non-serializable objects
            json.dumps(data)
            return {"status": "success", "data": data}
        except (TypeError, ValueError) as e:
            logger.error(f"Failed to serialize response: {e}")
            return {"status": "error", "message": f"Serialization failed: {str(e)}"}

    @staticmethod
    def error_response(message: str, status_code: int = 400) -> Dict[str, Any]:
        """
        Create standardized error response.
        
        Args:
            message: Error message
            status_code: HTTP status code
            
        Returns:
            Error response dictionary
        """
        return {
            "status": "error",
            "status_code": status_code,
            "message": message,
        }

    @staticmethod
    def success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
        """
        Create standardized success response.
        
        Args:
            data: Response data
            message: Success message
            
        Returns:
            Success response dictionary
        """
        return {
            "status": "success",
            "message": message,
            "data": data,
        }
