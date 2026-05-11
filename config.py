import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

REPO_PATH = "./data/spring-rest-sakila"

ALLOWED_EXTENSIONS = [".java"]
IGNORE_DIRS = ["target", ".git", "test", "node_modules"]