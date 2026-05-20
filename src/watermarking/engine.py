
    def _select_watermark_token(self, input_ids: torch.Tensor) -> int:
        """Select a token ID to use for watermarking."""
        special_ids = set(self.tokenizer.all_special_ids)
        vocab_size = self.tokenizer.vocab_size
        
        # Pick from middle of vocab to avoid special tokens
        watermark_id = (vocab_size // 2) % vocab_size
        while watermark_id in special_ids:
            watermark_id = (watermark_id + 1) % vocab_size
            
        return watermark_id
    
    def verify_watermark(
        self, 
        text: str, 
        return_scores: bool = False
    ) -> Dict[str, Any]:
        """
        Verify if text contains the watermark.
        
        Args:
            text: Text to verify
            return_scores: Whether to return detailed scores
            
        Returns:
            Dictionary with verification results
        """
        if self.model_wrapper is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Tokenize
        inputs = self.tokenizer(text, return_tensors="pt", padding=True)
        input_ids = inputs["input_ids"].to(self.device)
        
        # Check for watermark tokens
        watermark_token_id = self._select_watermark_token(input_ids)
        
        # Count watermark token occurrences
        matches = (input_ids == watermark_token_id).sum().item()
        total_tokens = input_ids.numel()
        
        # Calculate detection score
        expected_ratio = 0.05  # Expected ~5% watermarked tokens
        actual_ratio = matches / max(total_tokens, 1)
        
        # Score based on ratio vs expected
        score = min(actual_ratio / expected_ratio, 1.0) if expected_ratio > 0 else 0.0
        is_watermarked = score >= self.config.verification_threshold
        
        result = {
            "is_watermarked": is_watermarked,
            "confidence": score,
            "watermark_token_count": matches,
            "total_tokens": total_tokens,
            "watermark_ratio": actual_ratio
        }
        
        if return_scores:
            result["detailed_scores"] = {
                "expected_ratio": expected_ratio,
                "actual_ratio": actual_ratio,
                "threshold": self.config.verification_threshold
            }
            
        return result