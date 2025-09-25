#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from openai import OpenAI
from typing import List, Dict, Any

class OpenAIModel:
    """OpenAI模型API封装"""
    
    def __init__(self, model_name: str, api_key: str, base_url: str = None):
        self.model_name = model_name
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=60.0)
        else:
            self.client = OpenAI(api_key=api_key, timeout=60.0)
        
    def generate(self, prompt: str, images: List[Dict] = None) -> str:
        """生成响应"""
        try:
            # Build message
            messages = []
            
            # 添加文本提示
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            })
            
            # 添加图像（如果有）
            if images:
                for image in images:
                    messages[0]["content"].append(image)
            
            # 调用API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=2000,
                temperature=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return f"Error: {str(e)}"
    
    def generate_with_retry(self, prompt: str, images: List[Dict] = None, max_retries: int = 3) -> str:
        """带重试的生成响应"""
        for attempt in range(max_retries):
            try:
                return self.generate(prompt, images)
            except Exception as e:
                if attempt == max_retries - 1:
                    return f"Error after {max_retries} attempts: {str(e)}"
                time.sleep(2 ** attempt)  # 指数退避
        
        return "Error: Max retries exceeded"
