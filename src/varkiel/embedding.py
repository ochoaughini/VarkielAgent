from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class SymbolicEmbedder:
    """Dense semantic embedding using transformer models"""
    def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2'):
        # Lazy import heavy transformers
        from transformers import AutoTokenizer, AutoModel
        import torch
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        
    def embed_text(self, text: str) -> np.ndarray:
        """Generate 768-dimensional semantic embeddings"""
        inputs = self.tokenizer(text, return_tensors="pt", 
                              padding=True, truncation=True, 
                              max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Mean pooling with attention masking
        token_embeddings = outputs.last_hidden_state
        input_mask = inputs['attention_mask']
        token_embeddings = token_embeddings * input_mask.unsqueeze(-1).float()
        sum_embeddings = torch.sum(token_embeddings, dim=1)
        sum_mask = torch.clamp(input_mask.sum(dim=1), min=1e-9)
        return (sum_embeddings / sum_mask.unsqueeze(-1)).squeeze().numpy()
