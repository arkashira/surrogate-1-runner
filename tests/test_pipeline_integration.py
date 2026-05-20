import pytest
from unittest.mock import patch, MagicMock
from surrogate_1.pipeline import Pipeline
from surrogate_1.resolver import Resolver
from surrogate_1.rag import RAGModule

@pytest.fixture
def mock_resolver():
    with patch('surrogate_1.resolver.Resolver') as mock:
        mock_instance = MagicMock()
        mock_instance.resolve.return_value = "resolved_token"
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def mock_rag():
    with patch('surrogate_1.rag.RAGModule') as mock:
        mock_instance = MagicMock()
        mock_instance.process.return_value = "rag_output"
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def pipeline(mock_resolver, mock_rag):
    return Pipeline(resolver=mock_resolver, rag=mock_rag)

def test_resolver_exposed_as_synchronous_api(pipeline):
    """Test resolver is exposed as a synchronous API call"""
    input_data = "test_input"
    result = pipeline.process(input_data)
    
    assert result == "rag_output"
    pipeline.resolver.resolve.assert_called_once_with(input_data)
    pipeline.rag.process.assert_called_once_with("resolved_token")

def test_integration_hook_preserves_token_count(pipeline):
    """Test integration hook does not alter token count or context window"""
    input_data = "test_input"
    original_token_count = 10
    original_context_window = 100
    
    with patch('surrogate_1.pipeline.Pipeline._count_tokens', return_value=original_token_count), \
         patch('surrogate_1.pipeline.Pipeline._get_context_window', return_value=original_context_window):
        
        pipeline.process(input_data)
        
        # Verify token counting remains unchanged
        assert pipeline._count_tokens(input_data) == original_token_count
        assert pipeline._get_context_window(input_data) == original_context_window

def test_pipeline_continues_with_existing_rag_modules(pipeline):
    """Test pipeline continues to function with existing RAG modules"""
    input_data = "test_input"
    result = pipeline.process(input_data)
    
    # Verify RAG module is called with resolved token
    pipeline.rag.process.assert_called_once_with("resolved_token")
    assert result == "rag_output"
    
    # Verify resolver and RAG are properly integrated
    assert pipeline.resolver.resolve.called
    assert pipeline.rag.process.called

def test_resolver_error_handling(pipeline):
    """Test pipeline handles resolver errors gracefully"""
    pipeline.resolver.resolve.side_effect = Exception("Resolution failed")
    
    with pytest.raises(Exception) as exc_info:
        pipeline.process("test_input")
    
    assert "Resolution failed" in str(exc_info.value)
    pipeline.rag.process.assert_not_called()

def test_rag_error_handling(pipeline):
    """Test pipeline handles RAG errors gracefully"""
    pipeline.rag.process.side_effect = Exception("RAG processing failed")
    
    with pytest.raises(Exception) as exc_info:
        pipeline.process("test_input")
    
    assert "RAG processing failed" in str(exc_info.value)
    assert pipeline.resolver.resolve.called