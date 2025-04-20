class AIError(Exception):
    def __init__(self, message, error_type=None):
        """
        Custom exception for AI-related errors.

        :param message: Error message describing the issue.
        :param error_type: Optional type of the error (e.g., 'PromptError').
        """
        super().__init__(message)
        self.message = message
        self.error_type = error_type

    def __str__(self):
        if self.error_type:
            return f"[{self.error_type}] {self.message}"
        return self.message