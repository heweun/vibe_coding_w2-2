import os
import pytest
from pathlib import Path

class TestProjectStructure:
    """프로젝트 구조가 올바르게 생성되는지 테스트"""
    
    def test_backend_directory_exists(self):
        """backend 디렉토리가 존재하는지 확인"""
        assert os.path.exists("backend"), "backend 디렉토리가 존재해야 합니다"
    
    def test_frontend_directory_exists(self):
        """frontend 디렉토리가 존재하는지 확인"""
        assert os.path.exists("frontend"), "frontend 디렉토리가 존재해야 합니다"
    
    def test_requirements_file_exists(self):
        """requirements.txt 파일이 존재하는지 확인"""
        assert os.path.exists("requirements.txt"), "requirements.txt 파일이 존재해야 합니다"
    
    def test_env_template_file_exists(self):
        """env_template.txt 파일이 존재하는지 확인"""
        assert os.path.exists("env_template.txt"), "env_template.txt 파일이 존재해야 합니다"
    
    def test_gitignore_file_exists(self):
        """.gitignore 파일이 존재하는지 확인"""
        assert os.path.exists(".gitignore"), ".gitignore 파일이 존재해야 합니다"
    
    def test_backend_main_file_exists(self):
        """backend/main.py 파일이 존재하는지 확인"""
        assert os.path.exists("backend/main.py"), "backend/main.py 파일이 존재해야 합니다"
    
    def test_frontend_app_file_exists(self):
        """frontend/app.py 파일이 존재하는지 확인"""
        assert os.path.exists("frontend/app.py"), "frontend/app.py 파일이 존재해야 합니다"
    
    def test_backend_init_file_exists(self):
        """backend/__init__.py 파일이 존재하는지 확인"""
        assert os.path.exists("backend/__init__.py"), "backend/__init__.py 파일이 존재해야 합니다" 