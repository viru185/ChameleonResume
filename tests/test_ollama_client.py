import unittest
from unittest.mock import patch, MagicMock
from src.utils.ollama_client import generate_resume_with_ollama, ResponseError, RequestError

class TestGenerateResumeWithOllama(unittest.TestCase):

    @patch('utils.ollama_client.chat')
    @patch('utils.ollama_client.logger')
    def test_generate_resume_success(self, mock_logger, mock_chat):
        # Mocking the response from the chat function
        mock_response = MagicMock()
        mock_response.message = {'content': '<html>Generated Resume</html>'}
        mock_chat.return_value = mock_response

        candidate_data = {
            "personal_information": {"name": "John", "surname": "Doe"},
            "skills": ["Python", "Django"]
        }
        job_description = "Looking for a Python developer."

        result = generate_resume_with_ollama(candidate_data, job_description)

        self.assertEqual(result, '<html>Generated Resume</html>')
        mock_logger.info.assert_called_with('Received response from Ollama client successfully.')

    @patch('utils.ollama_client.chat')
    @patch('utils.ollama_client.logger')
    def test_generate_resume_response_error(self, mock_logger, mock_chat):
        # Simulate a ResponseError
        mock_chat.side_effect = ResponseError("Response error occurred")

        candidate_data = {
            "personal_information": {"name": "John", "surname": "Doe"},
            "skills": ["Python", "Django"]
        }
        job_description = "Looking for a Python developer."

        result = generate_resume_with_ollama(candidate_data, job_description)

        self.assertIsNone(result)
        mock_logger.error.assert_called_with('Error generating resume with Ollama: Response error occurred')

    @patch('utils.ollama_client.chat')
    @patch('utils.ollama_client.logger')
    def test_generate_resume_request_error(self, mock_logger, mock_chat):
        # Simulate a RequestError
        mock_chat.side_effect = RequestError("Request error occurred")

        candidate_data = {
            "personal_information": {"name": "John", "surname": "Doe"},
            "skills": ["Python", "Django"]
        }
        job_description = "Looking for a Python developer."

        result = generate_resume_with_ollama(candidate_data, job_description)

        self.assertIsNone(result)
        mock_logger.error.assert_called_with('Error generating resume with Ollama: Request error occurred')

    @patch('utils.ollama_client.chat')
    @patch('utils.ollama_client.logger')
    def test_generate_resume_unexpected_error(self, mock_logger, mock_chat):
        # Simulate an unexpected exception
        mock_chat.side_effect = Exception("Unexpected error occurred")

        candidate_data = {
            "personal_information": {"name": "John", "surname": "Doe"},
            "skills": ["Python", "Django"]
        }
        job_description = "Looking for a Python developer."

        result = generate_resume_with_ollama(candidate_data, job_description)

        self.assertIsNone(result)
        mock_logger.error.assert_called_with('Error generating resume with Ollama: Unexpected error occurred')


if __name__ == '__main__':
    unittest.main()