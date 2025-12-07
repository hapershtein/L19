"""
Repository cloning and analysis module
"""
import os
import sys
import asyncio
import shutil
from logger_config import LoggerConfig
from .excel_handler import ExcelHandler

logger = LoggerConfig.setup_logger('analyze_repos')


class RepoAnalyzer:
    """Agent to clone and analyze GitHub repositories"""

    def __init__(self, input_file, output_file='Output_23.xlsx', temp_dir='TempFiles', small_file_threshold=150):
        """
        Initialize the Repo Analyzer

        Args:
            input_file: Path to input Excel file with GitHub URLs
            output_file: Path to output Excel file
            temp_dir: Directory to store cloned repositories
            small_file_threshold: Maximum line count for a file to be considered "small" (default: 150)
        """
        self.input_file = input_file
        self.output_file = output_file
        self.temp_dir = temp_dir
        self.small_file_threshold = small_file_threshold
        self.repos_data = []
        self.semaphore = asyncio.Semaphore(5)

    def read_excel_data(self):
        """
        Read data from input Excel file

        Returns:
            List of dictionaries with repo data
        """
        logger.info(f"Starting to read data from {self.input_file}")
        return ExcelHandler.read_input_file(self.input_file)

    async def clone_repo(self, repo_data):
        """
        Clone a single repository asynchronously

        Args:
            repo_data: Dictionary with repository information

        Returns:
            Updated repo_data dictionary
        """
        async with self.semaphore:
            repo_id = repo_data['id']
            github_url = repo_data['github_url']

            if not github_url or github_url.strip() == '':
                print(f"[{repo_id}] Skipping - No GitHub URL")
                repo_data['status'] = 'no_url'
                return repo_data

            os.makedirs(self.temp_dir, exist_ok=True)
            repo_folder = os.path.join(self.temp_dir, repo_id)

            if os.path.exists(repo_folder):
                shutil.rmtree(repo_folder)

            print(f"[{repo_id}] Cloning {github_url}...")

            process = await asyncio.create_subprocess_exec(
                'git', 'clone', '--depth', '1', github_url, repo_folder,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode('utf-8', errors='ignore')
                print(f"[{repo_id}] ✗ Clone failed: {error_msg.strip()}")
                repo_data['status'] = 'clone_failed'
                return repo_data

            logger.info(f"[{repo_id}] Clone successful")
            print(f"[{repo_id}] ✓ Clone successful")
            repo_data['status'] = 'cloned'
            repo_data['repo_folder'] = repo_folder

            return repo_data

    def count_lines_in_file(self, file_path):
        """
        Count lines in a single file

        Args:
            file_path: Path to file

        Returns:
            Number of lines in file
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def analyze_repo(self, repo_data):
        """
        Analyze a cloned repository and count lines

        Args:
            repo_data: Dictionary with repository information

        Returns:
            Updated repo_data dictionary
        """
        if repo_data['status'] != 'cloned':
            return repo_data

        repo_folder = repo_data['repo_folder']
        repo_id = repo_data['id']

        logger.info(f"[{repo_id}] Starting code analysis")
        print(f"[{repo_id}] Analyzing code...")

        total_lines = 0
        small_files_lines = 0

        for root, dirs, files in os.walk(repo_folder):
            if '.git' in dirs:
                dirs.remove('.git')

            for file in files:
                file_path = os.path.join(root, file)
                line_count = self.count_lines_in_file(file_path)

                if line_count > 0:
                    total_lines += line_count

                    if line_count < self.small_file_threshold:
                        small_files_lines += line_count

        if total_lines > 0:
            grade = (small_files_lines / total_lines) * 100
        else:
            grade = 0.0

        repo_data['total_lines'] = total_lines
        repo_data['small_files_lines'] = small_files_lines
        repo_data['grade'] = round(grade, 2)
        repo_data['status'] = 'analyzed'

        print(f"[{repo_id}] ✓ Analysis complete: {total_lines} total lines, "
              f"{small_files_lines} lines in small files (<{self.small_file_threshold} lines), "
              f"Grade: {repo_data['grade']}%")

        return repo_data

    async def clone_all_repos(self, repos_data):
        """
        Clone all repositories in parallel

        Args:
            repos_data: List of repository data dictionaries

        Returns:
            List of updated repository data dictionaries
        """
        print(f"\n{'='*70}")
        print(f"Starting parallel repository cloning")
        print(f"{'='*70}\n")

        tasks = [self.clone_repo(repo) for repo in repos_data]
        results = await asyncio.gather(*tasks)

        return results

    def analyze_all_repos(self, repos_data):
        """
        Analyze all cloned repositories

        Args:
            repos_data: List of repository data dictionaries

        Returns:
            List of updated repository data dictionaries
        """
        print(f"\n{'='*70}")
        print(f"Starting repository analysis")
        print(f"{'='*70}\n")

        for repo_data in repos_data:
            self.analyze_repo(repo_data)

        return repos_data
