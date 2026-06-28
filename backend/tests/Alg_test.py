#!/usr/bin/env python3
"""
FarmTech-ProFertilizer Algorithm Tester - FINAL FIXED VERSION
Complete self-contained testing tool with integrated backend server

FIXES:
- Fixed 'str' object has no attribute 'get' error
- Properly parses all fertilizer data
- Uses ALL system fertilizers
- Includes Mg, Mn, Na containing fertilizers
"""

import os
import sys
import json
import time
import sqlite3
import random
import socket
import subprocess
import signal
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import requests

# ============================================================
# Color Support
# ============================================================
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = ""
    class Style:
        RESET_ALL = BRIGHT = ""


class Colors:
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT


# ============================================================
# Configuration
# ============================================================
BASE_DIR = Path(__file__).parent.parent.parent.absolute()
BACKEND_DIR = BASE_DIR / "backend"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "test_reports"

DEFAULT_BACKEND_PORT = 8000

TEST_USER = {
    "phone_number": "09121234567",
    "password": "Test@123456",
    "first_name": "Test",
    "last_name": "User"
}


# ============================================================
# Server Manager
# ============================================================
class ServerManager:
    """Manages the backend server lifecycle"""
    
    def __init__(self, port: int = DEFAULT_BACKEND_PORT):
        self.port = port
        self.process = None
        self.is_running = False
        
    def is_port_available(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            try:
                s.bind(('127.0.0.1', self.port))
                return True
            except OSError:
                return False
    
    def find_available_port(self) -> int:
        for port in range(self.port, self.port + 20):
            if self.is_port_available():
                return port
        raise RuntimeError("No available port found")
    
    def start(self) -> bool:
        print(f"{Colors.BLUE}🚀 Starting backend server on port {self.port}...{Colors.RESET}")
        
        if not self.is_port_available():
            print(f"{Colors.YELLOW}⚠️ Port {self.port} is occupied.{Colors.RESET}")
            new_port = self.find_available_port()
            if new_port != self.port:
                print(f"{Colors.GREEN}✅ Using port {new_port} instead{Colors.RESET}")
                self.port = new_port
        
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        python_exe = self._get_python_executable()
        log_file = LOGS_DIR / "backend_test.log"
        
        try:
            self.process = subprocess.Popen(
                [
                    python_exe, "-m", "uvicorn",
                    "app.main:app",
                    "--reload",
                    "--host", "0.0.0.0",
                    "--port", str(self.port)
                ],
                cwd=str(BACKEND_DIR),
                stdout=open(log_file, "w", encoding="utf-8"),
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8"
            )
            
            if self._wait_for_server():
                self.is_running = True
                print(f"{Colors.GREEN}✅ Backend server is ready: http://localhost:{self.port}{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}❌ Server failed to start{Colors.RESET}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}❌ Error starting server: {e}{Colors.RESET}")
            return False
    
    def _get_python_executable(self) -> str:
        if sys.platform == 'win32':
            venv_python = BACKEND_DIR / "venv" / "Scripts" / "python.exe"
        else:
            venv_python = BACKEND_DIR / "venv" / "bin" / "python"
        
        if venv_python.exists():
            return str(venv_python)
        return sys.executable
    
    def _wait_for_server(self, timeout: int = 60) -> bool:
        print(f"{Colors.YELLOW}⏳ Waiting for server to start...{Colors.RESET}")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(
                    f"http://localhost:{self.port}/health",
                    timeout=2
                )
                if response.status_code == 200:
                    return True
            except:
                pass
            time.sleep(0.5)
        
        return False
    
    def stop(self):
        if self.process:
            print(f"{Colors.YELLOW}⏹️ Stopping backend server...{Colors.RESET}")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.is_running = False
            print(f"{Colors.GREEN}✅ Server stopped{Colors.RESET}")


# ============================================================
# Database Manager
# ============================================================
class DatabaseManager:
    """Manages database operations"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = None
        
    def connect(self) -> bool:
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Database connection error: {e}{Colors.RESET}")
            return False
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def execute(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        if not self.conn:
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ Query error: {e}{Colors.RESET}")
            return []
    
    def create_test_user(self) -> bool:
        existing = self.execute(
            "SELECT id FROM users WHERE phone_number = ?",
            (TEST_USER["phone_number"],)
        )
        
        if existing:
            print(f"{Colors.GREEN}✅ Test user already exists (ID: {existing[0]['id']}){Colors.RESET}")
            return True
        
        import hashlib
        import secrets
        
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((salt + TEST_USER["password"]).encode('utf-8'))
        password_hash = f"{salt}:{hash_obj.hexdigest()}"
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO users (first_name, last_name, phone_number, password_hash, is_active)
                VALUES (?, ?, ?, ?, ?)
            """, (
                TEST_USER["first_name"],
                TEST_USER["last_name"],
                TEST_USER["phone_number"],
                password_hash,
                1
            ))
            self.conn.commit()
            user_id = cursor.lastrowid
            print(f"{Colors.GREEN}✅ Test user created (ID: {user_id}){Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Error creating test user: {e}{Colors.RESET}")
            return False
    
    def get_all_system_fertilizers(self) -> List[Dict[str, Any]]:
        """Get ALL system fertilizers - FIXED: properly parse elements"""
        query = """
            SELECT id, name, brand, category, form, concentration, 
                   elements, price_per_kg, is_acid, acid_type, ph_level, description
            FROM fertilizers 
            WHERE is_system_default = 1 AND user_id IS NULL
            ORDER BY id
        """
        result = self.execute(query)
        
        # ✅ FIX: Properly parse elements for each fertilizer
        parsed_result = []
        for row in result:
            fert = dict(row)
            # Parse elements if it's a string
            if 'elements' in fert and isinstance(fert['elements'], str):
                try:
                    fert['elements'] = json.loads(fert['elements'])
                except json.JSONDecodeError:
                    fert['elements'] = {}
            elif 'elements' not in fert:
                fert['elements'] = {}
            parsed_result.append(fert)
        
        return parsed_result
    
    def get_system_recipes(self) -> List[Dict[str, Any]]:
        query = """
            SELECT id, name, description, target_values, category, stage
            FROM recipes 
            WHERE is_system = 1
            ORDER BY name
        """
        result = self.execute(query)
        
        # ✅ FIX: Parse target_values for each recipe
        parsed_result = []
        for row in result:
            recipe = dict(row)
            if 'target_values' in recipe and isinstance(recipe['target_values'], str):
                try:
                    recipe['target_values'] = json.loads(recipe['target_values'])
                except json.JSONDecodeError:
                    recipe['target_values'] = {}
            parsed_result.append(recipe)
        
        return parsed_result


# ============================================================
# Test Data Classes
# ============================================================
@dataclass
class TestCase:
    id: str
    name: str
    description: str
    target_values: Dict[str, float]
    selected_fertilizers: List[str]
    water_values: Dict[str, float]
    expected_behavior: str
    validation_criteria: Dict[str, Any]

@dataclass
class TestResult:
    test_id: str
    test_name: str
    passed: bool
    execution_time_ms: float
    weights: Dict[str, float]
    concentrations: Dict[str, float]
    residual_error: float
    cost_total: float
    ion_balance: Dict[str, Any]
    target_achievement: Dict[str, float]
    warnings: List[str]
    suggestions: List[str]
    is_converged: bool
    summary: str
    errors: List[str] = field(default_factory=list)

@dataclass
class TestSuite:
    suite_id: str
    timestamp: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    results: List[TestResult] = field(default_factory=list)


# ============================================================
# API Client
# ============================================================
class APIClient:
    """API client for testing"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
    
    def login(self) -> bool:
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={
                    "phone_number": TEST_USER["phone_number"],
                    "password": TEST_USER["password"]
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access_token')
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}'
                })
                return True
            return False
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ Login failed: {e}{Colors.RESET}")
            return False
    
    def optimize(self, target_values: Dict[str, float], 
                 fertilizers: List[Dict[str, Any]],
                 water_values: Dict[str, float] = None,
                 options: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.token:
            return {"error": "Not authenticated"}
        
        try:
            ferts_for_opt = []
            for f in fertilizers:
                elements = f.get('elements', {})
                if isinstance(elements, str):
                    try:
                        elements = json.loads(elements)
                    except:
                        elements = {}
                
                ferts_for_opt.append({
                    "id": str(f.get('id')),
                    "name": f.get('name', 'Unknown'),
                    "elements": elements,
                    "price_per_kg": f.get('price_per_kg', 0),
                    "purity": f.get('concentration', 100),
                    "is_acid": f.get('is_acid', False),
                    "is_system_default": f.get('is_system_default', False)
                })
            
            data = {
                "target_values": target_values,
                "water_values": water_values or {},
                "fertilizers": ferts_for_opt,
                "options": options or {
                    "method": "nnls",
                    "use_precipitation_check": True,
                    "use_ion_balance_check": True,
                    "reservoir_mode": "auto",
                    "max_iterations": 1000,
                    "tolerance": 1e-6,
                    "cost_weight": 0.01
                },
                "tank_volume": 1000,
                "stock_volume": 100,
                "injection_ratio": 100
            }
            
            response = self.session.post(
                f"{self.base_url}/calculations/optimize",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                try:
                    error_data = response.json()
                    return {"error": error_data.get('detail', f'Status {response.status_code}')}
                except:
                    return {"error": f"Status {response.status_code}"}
                    
        except Exception as e:
            return {"error": str(e)}


# ============================================================
# Test Engine - FINAL FIXED VERSION
# ============================================================
class TestEngine:
    """Main test engine - FINAL FIXED VERSION"""
    
    def __init__(self, db_manager: DatabaseManager, api_client: APIClient):
        self.db = db_manager
        self.api = api_client
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []
        
        # Store all fertilizers for reference
        self.all_fertilizers: List[Dict] = []
        self.fertilizer_map: Dict[str, Dict] = {}
        
    def build_fertilizer_map(self, fertilizers: List[Dict]):
        """Build a map of fertilizer IDs to fertilizer data"""
        self.all_fertilizers = fertilizers
        self.fertilizer_map = {}
        for fert in fertilizers:
            if fert is None:
                continue
            fert_id = str(fert.get('id', ''))
            if fert_id:
                self.fertilizer_map[fert_id] = fert
    
    def get_fertilizer_elements(self, fert: Dict) -> Dict[str, float]:
        """Safely get elements from a fertilizer"""
        if fert is None:
            return {}
        elements = fert.get('elements', {})
        if isinstance(elements, str):
            try:
                return json.loads(elements)
            except:
                return {}
        if isinstance(elements, dict):
            return elements
        return {}
    
    def generate_test_cases(self):
        """Generate all test cases - USING ALL FERTILIZERS"""
        print(f"\n{Colors.BLUE}📋 Generating test cases...{Colors.RESET}")
        
        self.test_cases = []
        
        # Get ALL system data
        recipes = self.db.get_system_recipes()
        all_fertilizers = self.db.get_all_system_fertilizers()
        
        # Build fertilizer map
        self.build_fertilizer_map(all_fertilizers)
        
        print(f"   Found {len(recipes)} system recipes")
        print(f"   Found {len(all_fertilizers)} system fertilizers (ALL will be used)")
        
        # Generate from recipes - using ALL fertilizers
        for recipe in recipes:
            if recipe is None:
                continue
            test_case = self._create_test_case_from_recipe(recipe, all_fertilizers)
            if test_case:
                self.test_cases.append(test_case)
        
        # Add edge cases
        self._add_edge_cases(all_fertilizers)
        
        # Add variation cases
        self._add_variation_cases(all_fertilizers)
        
        print(f"   Generated {len(self.test_cases)} test cases")
    
    def _create_test_case_from_recipe(self, recipe: Dict, 
                                       all_fertilizers: List[Dict]) -> Optional[TestCase]:
        """Create a test case from a recipe - USING ALL FERTILIZERS"""
        if recipe is None:
            return None
            
        target_values = recipe.get('target_values', {})
        if isinstance(target_values, str):
            try:
                target_values = json.loads(target_values)
            except:
                return None
        
        if not target_values or not isinstance(target_values, dict):
            return None
        
        # Filter out zero values
        target_values = {k: v for k, v in target_values.items() if isinstance(v, (int, float)) and v > 0}
        
        if len(target_values) < 2:
            return None
        
        # ✅ FIX: Select fertilizers for EACH target element
        selected = self._select_fertilizers_for_targets(target_values, all_fertilizers)
        
        # ✅ FIX: If we don't have enough, add more fertilizers
        if len(selected) < 3:
            # Add top fertilizers by element coverage
            for fert in all_fertilizers:
                if fert is None:
                    continue
                if len(selected) >= 10:
                    break
                fert_id = str(fert.get('id', ''))
                if fert_id and fert_id not in selected:
                    selected.append(fert_id)
        
        # ✅ FIX: Ensure Mg fertilizers are included if Mg is a target
        if 'Mg' in target_values and target_values['Mg'] > 0:
            mg_fertilizers = []
            for fert in all_fertilizers:
                if fert is None:
                    continue
                elements = self.get_fertilizer_elements(fert)
                if elements.get('Mg', 0) > 0:
                    fert_id = str(fert.get('id', ''))
                    if fert_id:
                        mg_fertilizers.append(fert_id)
            for mg_id in mg_fertilizers:
                if mg_id and mg_id not in selected:
                    selected.append(mg_id)
                    break
        
        # ✅ FIX: Ensure Mn fertilizers are included if Mn is a target
        if 'Mn' in target_values and target_values['Mn'] > 0:
            mn_fertilizers = []
            for fert in all_fertilizers:
                if fert is None:
                    continue
                elements = self.get_fertilizer_elements(fert)
                if elements.get('Mn', 0) > 0:
                    fert_id = str(fert.get('id', ''))
                    if fert_id:
                        mn_fertilizers.append(fert_id)
            for mn_id in mn_fertilizers:
                if mn_id and mn_id not in selected:
                    selected.append(mn_id)
                    break
        
        print(f"   📋 Recipe '{recipe.get('name', 'Unknown')[:30]}...' using {len(selected)} fertilizers")
        
        return TestCase(
            id=f"RECIPE_{recipe.get('id', 'unknown')}",
            name=recipe.get('name', 'Unnamed'),
            description=recipe.get('description', 'System recipe test'),
            target_values=target_values,
            selected_fertilizers=selected,
            water_values={},
            expected_behavior='success',
            validation_criteria={
                'max_residual_error': 30.0,
                'min_achievement': 20.0,
                'allow_warnings': True
            }
        )
    
    def _select_fertilizers_for_targets(self, targets: Dict[str, float], 
                                        all_fertilizers: List[Dict]) -> List[str]:
        """
        Select fertilizers that can provide the targets - FIXED VERSION
        Uses ALL fertilizers and ensures each element is covered
        """
        selected = []
        target_elements = list(targets.keys())
        
        # ✅ STEP 1: For each target element, find the BEST fertilizer
        for element in target_elements:
            best_fert = None
            best_pct = 0
            
            for fert in all_fertilizers:
                if fert is None:
                    continue
                elements = self.get_fertilizer_elements(fert)
                pct = elements.get(element, 0)
                if pct > best_pct:
                    best_pct = pct
                    best_fert = str(fert.get('id', ''))
            
            if best_fert and best_fert not in selected:
                selected.append(best_fert)
        
        # ✅ STEP 2: Add fertilizers that cover multiple elements
        fert_scores = []
        for fert in all_fertilizers:
            if fert is None:
                continue
            fert_id = str(fert.get('id', ''))
            if not fert_id or fert_id in selected:
                continue
            
            elements = self.get_fertilizer_elements(fert)
            score = sum(1 for e in target_elements if e in elements and elements.get(e, 0) > 0)
            if score > 0:
                fert_scores.append((fert_id, score))
        
        fert_scores.sort(key=lambda x: x[1], reverse=True)
        
        for fert_id, score in fert_scores:
            if len(selected) >= 15:
                break
            if fert_id not in selected:
                selected.append(fert_id)
        
        # ✅ STEP 3: Ensure minimum 3 fertilizers
        if len(selected) < 3:
            for fert in all_fertilizers:
                if fert is None:
                    continue
                if len(selected) >= 5:
                    break
                fert_id = str(fert.get('id', ''))
                if fert_id and fert_id not in selected:
                    selected.append(fert_id)
        
        # ✅ STEP 4: Log selected fertilizers
        selected_names = []
        for fert in all_fertilizers:
            if fert is None:
                continue
            fert_id = str(fert.get('id', ''))
            if fert_id in selected:
                name = fert.get('name', 'Unknown')
                # Show if it has Mg or Mn
                elements = self.get_fertilizer_elements(fert)
                has_mg = elements.get('Mg', 0) > 0
                has_mn = elements.get('Mn', 0) > 0
                marker = ""
                if has_mg:
                    marker = " [Mg]"
                if has_mn:
                    marker = " [Mn]"
                selected_names.append(f"{name}{marker}")
        
        if selected_names:
            print(f"      Selected {len(selected_names)} fertilizers:")
            for name in selected_names[:6]:
                print(f"        - {name}")
            if len(selected_names) > 6:
                print(f"        ... and {len(selected_names) - 6} more")
        
        return selected
    
    def _add_edge_cases(self, all_fertilizers: List[Dict]):
        """Add edge case test cases"""
        
        # Get first available elements
        first_elements = []
        for fert in all_fertilizers[:10]:
            if fert is None:
                continue
            elements = self.get_fertilizer_elements(fert)
            for el, val in elements.items():
                if val > 0 and el not in first_elements:
                    first_elements.append(el)
                    if len(first_elements) >= 3:
                        break
            if len(first_elements) >= 3:
                break
        
        if not first_elements:
            return
        
        # Single target
        self.test_cases.append(
            TestCase(
                id="EDGE_001",
                name="Single Target Element",
                description="Test with only one target element",
                target_values={first_elements[0]: 200},
                selected_fertilizers=self._select_fertilizers_for_targets(
                    {first_elements[0]: 200}, all_fertilizers
                ),
                water_values={},
                expected_behavior='warning',
                validation_criteria={
                    'max_residual_error': 30.0,
                    'min_achievement': 20.0,
                    'allow_warnings': True
                }
            )
        )
        
        # High values
        high_targets = {}
        for el in first_elements[:3]:
            high_targets[el] = 500
        self.test_cases.append(
            TestCase(
                id="EDGE_002",
                name="High Target Values",
                description="Test with very high target values",
                target_values=high_targets,
                selected_fertilizers=self._select_fertilizers_for_targets(high_targets, all_fertilizers),
                water_values={},
                expected_behavior='warning',
                validation_criteria={
                    'max_residual_error': 30.0,
                    'min_achievement': 20.0,
                    'allow_warnings': True
                }
            )
        )
        
        # All elements - using first 10 elements that have coverage
        all_targets = {}
        for fert in all_fertilizers[:10]:
            if fert is None:
                continue
            elements = self.get_fertilizer_elements(fert)
            for el, val in elements.items():
                if val > 0 and el not in all_targets:
                    all_targets[el] = 100 + random.randint(0, 50)
                    if len(all_targets) >= 10:
                        break
            if len(all_targets) >= 10:
                break
        
        if len(all_targets) >= 5:
            self.test_cases.append(
                TestCase(
                    id="EDGE_004",
                    name="Multiple Elements",
                    description="Test with multiple target elements",
                    target_values=all_targets,
                    selected_fertilizers=self._select_fertilizers_for_targets(all_targets, all_fertilizers),
                    water_values={},
                    expected_behavior='success',
                    validation_criteria={
                        'max_residual_error': 30.0,
                        'min_achievement': 20.0,
                        'allow_warnings': True
                    }
                )
            )
    
    def _add_variation_cases(self, all_fertilizers: List[Dict]):
        """Add variation test cases"""
        
        # Get base targets
        base_targets = {}
        for fert in all_fertilizers[:5]:
            if fert is None:
                continue
            elements = self.get_fertilizer_elements(fert)
            for el, val in elements.items():
                if val > 0 and el not in base_targets:
                    base_targets[el] = 100
                    if len(base_targets) >= 5:
                        break
            if len(base_targets) >= 5:
                break
        
        if len(base_targets) < 3:
            return
        
        # Different water qualities
        variations = [
            {"name": "Good Water", "N-NO3": 10, "K": 20, "Ca": 50, "Fe": 0.5},
            {"name": "Salty Water", "Na": 50, "Cl": 80, "Ca": 150, "Mg": 60},
            {"name": "Poor Water", "N-NO3": 30, "P": 20, "S": 40, "Fe": 3}
        ]
        
        for i, water in enumerate(variations):
            filtered_targets = {k: v for k, v in base_targets.items() if k not in water or k == 'name'}
            if len(filtered_targets) < 2:
                continue
                
            self.test_cases.append(
                TestCase(
                    id=f"VAR_{i+1:03d}",
                    name=f"Water Variation: {water.get('name')}",
                    description=f"Test with {water.get('name')}",
                    target_values=filtered_targets,
                    selected_fertilizers=self._select_fertilizers_for_targets(filtered_targets, all_fertilizers),
                    water_values={k: v for k, v in water.items() if k != 'name' and k in filtered_targets},
                    expected_behavior='success',
                    validation_criteria={
                        'max_residual_error': 30.0,
                        'min_achievement': 20.0,
                        'allow_warnings': True
                    }
                )
            )
    
    def run_tests(self) -> TestSuite:
        """Execute all test cases"""
        print(f"\n{Colors.BLUE}🧪 Running tests...{Colors.RESET}")
        
        self.results = []
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n  {Colors.CYAN}[{i}/{len(self.test_cases)}] {test_case.name}{Colors.RESET}")
            result = self._run_single_test(test_case)
            self.results.append(result)
            
            if result.passed:
                print(f"    {Colors.GREEN}✅ PASSED{Colors.RESET}")
            else:
                print(f"    {Colors.RED}❌ FAILED{Colors.RESET}")
                if result.errors:
                    for err in result.errors[:3]:
                        print(f"    {Colors.YELLOW}   - {err}{Colors.RESET}")
        
        suite = TestSuite(
            suite_id=f"SUITE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            total_tests=len(self.results),
            passed_tests=sum(1 for r in self.results if r.passed),
            failed_tests=sum(1 for r in self.results if not r.passed),
            skipped_tests=0,
            results=self.results
        )
        
        return suite
    
    def _run_single_test(self, test_case: TestCase) -> TestResult:
        """Execute a single test case"""
        start_time = time.time()
        errors = []
        
        try:
            # Get fertilizer details for ALL selected fertilizers
            fertilizers = []
            for fert_id in test_case.selected_fertilizers:
                if fert_id in self.fertilizer_map:
                    fert = self.fertilizer_map[fert_id].copy()
                    # Parse elements if needed
                    if isinstance(fert.get('elements'), str):
                        try:
                            fert['elements'] = json.loads(fert['elements'])
                        except:
                            fert['elements'] = {}
                    fertilizers.append(fert)
                else:
                    errors.append(f"Fertilizer {fert_id} not found")
            
            if not fertilizers:
                return TestResult(
                    test_id=test_case.id,
                    test_name=test_case.name,
                    passed=False,
                    execution_time_ms=(time.time() - start_time) * 1000,
                    weights={},
                    concentrations={},
                    residual_error=0,
                    cost_total=0,
                    ion_balance={},
                    target_achievement={},
                    warnings=[],
                    suggestions=[],
                    is_converged=False,
                    summary="No fertilizers available",
                    errors=["No valid fertilizers found"]
                )
            
            # Call optimization
            result = self.api.optimize(
                test_case.target_values,
                fertilizers,
                test_case.water_values
            )
            
            if 'error' in result:
                errors.append(f"API error: {result['error']}")
                return TestResult(
                    test_id=test_case.id,
                    test_name=test_case.name,
                    passed=False,
                    execution_time_ms=(time.time() - start_time) * 1000,
                    weights={},
                    concentrations={},
                    residual_error=0,
                    cost_total=0,
                    ion_balance={},
                    target_achievement={},
                    warnings=[],
                    suggestions=[],
                    is_converged=False,
                    summary=f"API Error: {result['error']}",
                    errors=errors
                )
            
            # Validate
            passed = self._validate_result(result, test_case, errors)
            
            return TestResult(
                test_id=test_case.id,
                test_name=test_case.name,
                passed=passed,
                execution_time_ms=(time.time() - start_time) * 1000,
                weights=result.get('weights', {}),
                concentrations=result.get('concentrations', {}),
                residual_error=result.get('residual_error', 0),
                cost_total=result.get('cost_total', 0),
                ion_balance=result.get('ion_balance', {}),
                target_achievement=result.get('target_achievement', {}),
                warnings=result.get('warnings', []),
                suggestions=result.get('suggestions', []),
                is_converged=result.get('is_converged', False),
                summary=result.get('summary', ''),
                errors=errors
            )
            
        except Exception as e:
            errors.append(f"Unexpected error: {str(e)}")
            return TestResult(
                test_id=test_case.id,
                test_name=test_case.name,
                passed=False,
                execution_time_ms=(time.time() - start_time) * 1000,
                weights={},
                concentrations={},
                residual_error=0,
                cost_total=0,
                ion_balance={},
                target_achievement={},
                warnings=[],
                suggestions=[],
                is_converged=False,
                summary=f"Test error: {str(e)}",
                errors=errors
            )
    
    def _validate_result(self, result: Dict, test_case: TestCase, errors: List[str]) -> bool:
        """Validate optimization result"""
        criteria = test_case.validation_criteria
        
        # Check convergence
        if not result.get('is_converged', False):
            errors.append("Algorithm did not converge")
        
        # Check residual error
        max_error = criteria.get('max_residual_error', 30.0)
        residual = result.get('residual_error', float('inf'))
        if residual > max_error:
            errors.append(f"Residual error: {residual:.4f} > {max_error}")
        
        # Check target achievement
        min_achievement = criteria.get('min_achievement', 20.0)
        achievement = result.get('target_achievement', {})
        
        # Only check elements that have targets
        for element, target in test_case.target_values.items():
            if target > 0:
                actual = achievement.get(element, 0)
                if actual < min_achievement:
                    errors.append(f"Low achievement for {element}: {actual:.1f}% < {min_achievement}%")
        
        # Check ion balance (warning only, not failure)
        ion_balance = result.get('ion_balance', {})
        if not ion_balance.get('is_balanced', False):
            cation = ion_balance.get('cation', 0)
            anion = ion_balance.get('anion', 0)
            diff = abs(cation - anion)
            if diff > 2.0:
                errors.append(f"Ion balance: difference {diff:.2f} meq/L")
        
        # Pass if not too many errors
        return len(errors) < 3


# ============================================================
# Report Generator
# ============================================================
class ReportGenerator:
    """Generates test reports"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, suite: TestSuite) -> Dict[str, Path]:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f"test_report_{timestamp}"
        
        reports = {}
        
        json_path = self.output_dir / f"{base_name}.json"
        self._generate_json(suite, json_path)
        reports['json'] = json_path
        
        csv_path = self.output_dir / f"{base_name}.csv"
        self._generate_csv(suite, csv_path)
        reports['csv'] = csv_path
        
        txt_path = self.output_dir / f"{base_name}.txt"
        self._generate_text(suite, txt_path)
        reports['txt'] = txt_path
        
        md_path = self.output_dir / f"{base_name}.md"
        self._generate_markdown(suite, md_path)
        reports['md'] = md_path
        
        return reports
    
    def _generate_json(self, suite: TestSuite, path: Path):
        data = {
            'suite_id': suite.suite_id,
            'timestamp': suite.timestamp,
            'total_tests': suite.total_tests,
            'passed_tests': suite.passed_tests,
            'failed_tests': suite.failed_tests,
            'skipped_tests': suite.skipped_tests,
            'results': []
        }
        
        for r in suite.results:
            data['results'].append({
                'test_id': r.test_id,
                'test_name': r.test_name,
                'passed': r.passed,
                'execution_time_ms': r.execution_time_ms,
                'weights': r.weights,
                'concentrations': r.concentrations,
                'residual_error': r.residual_error,
                'cost_total': r.cost_total,
                'ion_balance': r.ion_balance,
                'target_achievement': r.target_achievement,
                'warnings': r.warnings,
                'suggestions': r.suggestions,
                'is_converged': r.is_converged,
                'errors': r.errors
            })
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_csv(self, suite: TestSuite, path: Path):
        import csv
        
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Test ID', 'Test Name', 'Passed', 'Execution Time (ms)',
                'Residual Error', 'Cost Total', 'Converged',
                'Warnings Count', 'Errors Count'
            ])
            
            for r in suite.results:
                writer.writerow([
                    r.test_id,
                    r.test_name,
                    'PASS' if r.passed else 'FAIL',
                    f"{r.execution_time_ms:.2f}",
                    f"{r.residual_error:.6f}",
                    f"{r.cost_total:.2f}",
                    'YES' if r.is_converged else 'NO',
                    len(r.warnings),
                    len(r.errors)
                ])
    
    def _generate_text(self, suite: TestSuite, path: Path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("FARMTECH - TEST REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Suite ID: {suite.suite_id}\n")
            f.write(f"Timestamp: {suite.timestamp}\n")
            f.write(f"Total Tests: {suite.total_tests}\n")
            f.write(f"Passed: {suite.passed_tests}\n")
            f.write(f"Failed: {suite.failed_tests}\n")
            f.write(f"Skipped: {suite.skipped_tests}\n")
            
            if suite.total_tests > 0:
                rate = (suite.passed_tests / suite.total_tests) * 100
                f.write(f"Success Rate: {rate:.1f}%\n")
            
            f.write("\n" + "-" * 80 + "\n")
            f.write("DETAILED RESULTS\n")
            f.write("-" * 80 + "\n\n")
            
            for i, r in enumerate(suite.results, 1):
                f.write(f"{i}. {r.test_id}: {r.test_name}\n")
                f.write(f"   Status: {'✅ PASSED' if r.passed else '❌ FAILED'}\n")
                f.write(f"   Execution Time: {r.execution_time_ms:.2f}ms\n")
                f.write(f"   Converged: {'Yes' if r.is_converged else 'No'}\n")
                f.write(f"   Residual Error: {r.residual_error:.4f}\n")
                f.write(f"   Cost Total: {r.cost_total:,.0f} تومان\n")
                
                if r.weights:
                    f.write(f"   Weights: {r.weights}\n")
                
                if r.errors:
                    f.write(f"   Errors:\n")
                    for err in r.errors:
                        f.write(f"     - {err}\n")
                
                if r.warnings:
                    f.write(f"   Warnings:\n")
                    for warn in r.warnings:
                        f.write(f"     - {warn}\n")
                
                f.write("\n")
            
            f.write("=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
    
    def _generate_markdown(self, suite: TestSuite, path: Path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# FarmTech Test Report\n\n")
            f.write(f"**Suite ID:** `{suite.suite_id}`\n\n")
            f.write(f"**Timestamp:** {suite.timestamp}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Tests | {suite.total_tests} |\n")
            f.write(f"| Passed | {suite.passed_tests} |\n")
            f.write(f"| Failed | {suite.failed_tests} |\n")
            f.write(f"| Skipped | {suite.skipped_tests} |\n")
            if suite.total_tests > 0:
                rate = (suite.passed_tests / suite.total_tests) * 100
                f.write(f"| Success Rate | {rate:.1f}% |\n")
            
            f.write("\n## Test Results\n\n")
            f.write("| # | Test ID | Name | Status | Time (ms) | Converged | Errors |\n")
            f.write("|---|---------|------|--------|-----------|-----------|--------|\n")
            
            for i, r in enumerate(suite.results, 1):
                status = "✅ PASS" if r.passed else "❌ FAIL"
                f.write(f"| {i} | {r.test_id} | {r.test_name} | {status} | {r.execution_time_ms:.1f} | {'Yes' if r.is_converged else 'No'} | {len(r.errors)} |\n")
            
            failed = [r for r in suite.results if not r.passed]
            if failed:
                f.write("\n## Failed Tests\n\n")
                for r in failed:
                    f.write(f"### {r.test_id}: {r.test_name}\n\n")
                    if r.errors:
                        f.write("**Errors:**\n")
                        for err in r.errors:
                            f.write(f"- {err}\n")
                        f.write("\n")
            
            f.write("\n---\n\n")
            f.write(f"*Report generated by FarmTech Test Engine*\n")


# ============================================================
# Test Runner
# ============================================================
class TestRunner:
    """Main test runner"""
    
    def __init__(self):
        self.db_manager = None
        self.api_client = None
        self.server_manager = ServerManager()
        self.engine = None
        self.reporter = ReportGenerator(REPORTS_DIR)
        self.quick_mode = False
    
    def run_full_test(self) -> bool:
        print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}  🧪 FarmTech Algorithm Tester - FINAL VERSION{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}")
        
        if not self._start_server():
            return False
        
        try:
            if not self._setup_database():
                return False
            
            if not self._login():
                return False
            
            self._run_tests()
            self._generate_reports()
            return True
            
        finally:
            self._cleanup()
    
    def _start_server(self) -> bool:
        print(f"\n{Colors.BLUE}📡 Starting backend server...{Colors.RESET}")
        self._kill_process_on_port(DEFAULT_BACKEND_PORT)
        time.sleep(1)
        return self.server_manager.start()
    
    def _kill_process_on_port(self, port: int):
        try:
            if sys.platform == 'win32':
                result = subprocess.run(
                    f'netstat -ano | findstr :{port}',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if f':{port}' in line and 'LISTENING' in line:
                            parts = line.split()
                            if parts:
                                pid = parts[-1]
                                subprocess.run(f'taskkill /PID {pid} /F', shell=True, capture_output=True)
            else:
                result = subprocess.run(
                    f'lsof -ti :{port}',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0 and result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        try:
                            os.kill(int(pid), signal.SIGKILL)
                        except:
                            pass
        except:
            pass
    
    def _setup_database(self) -> bool:
        print(f"\n{Colors.BLUE}🗄️ Setting up database...{Colors.RESET}")
        
        db_path = BACKEND_DIR / "farmtech.db"
        self.db_manager = DatabaseManager(db_path)
        
        if not self.db_manager.connect():
            print(f"{Colors.RED}❌ Failed to connect to database{Colors.RESET}")
            return False
        
        if not self.db_manager.create_test_user():
            print(f"{Colors.RED}❌ Failed to create test user{Colors.RESET}")
            return False
        
        return True
    
    def _login(self) -> bool:
        print(f"\n{Colors.BLUE}🔐 Logging in to API...{Colors.RESET}")
        
        self.api_client = APIClient(f"http://localhost:{self.server_manager.port}/api/v1")
        
        if not self.api_client.login():
            print(f"{Colors.RED}❌ Failed to login{Colors.RESET}")
            return False
        
        print(f"{Colors.GREEN}✅ Login successful{Colors.RESET}")
        return True
    
    def _run_tests(self):
        print(f"\n{Colors.BLUE}🧪 Running tests...{Colors.RESET}")
        
        self.engine = TestEngine(self.db_manager, self.api_client)
        self.engine.generate_test_cases()
        
        if self.quick_mode:
            self.engine.test_cases = self.engine.test_cases[:15]
            print(f"{Colors.YELLOW}⚠️ Quick mode: limited to 15 test cases{Colors.RESET}")
        
        self.suite = self.engine.run_tests()
    
    def _generate_reports(self):
        print(f"\n{Colors.BLUE}📄 Generating reports...{Colors.RESET}")
        
        reports = self.reporter.generate(self.suite)
        
        print(f"\n{Colors.GREEN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}📊 Test Summary{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*70}{Colors.RESET}")
        print(f"  Total Tests:   {self.suite.total_tests}")
        print(f"  {Colors.GREEN}✅ Passed:      {self.suite.passed_tests}{Colors.RESET}")
        print(f"  {Colors.RED}❌ Failed:      {self.suite.failed_tests}{Colors.RESET}")
        if self.suite.total_tests > 0:
            rate = (self.suite.passed_tests / self.suite.total_tests) * 100
            print(f"  Success Rate:  {rate:.1f}%")
        
        print(f"\n{Colors.CYAN}📄 Reports generated:{Colors.RESET}")
        for fmt, path in reports.items():
            print(f"  {fmt.upper()}: {path}")
    
    def _cleanup(self):
        self.server_manager.stop()
        if self.db_manager:
            self.db_manager.close()


# ============================================================
# CLI Menu
# ============================================================
class CLIMenu:
    """Interactive CLI menu"""
    
    def __init__(self):
        self.runner = TestRunner()
    
    def show_header(self):
        os.system('cls' if sys.platform == 'win32' else 'clear')
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║  {Colors.BOLD}{Colors.MAGENTA}🌱 FarmTech - Algorithm Tester{Colors.RESET}{Colors.CYAN}                              ║
║  FINAL FIXED VERSION - Uses ALL system fertilizers               ║
║  Includes Mg, Mn, Na containing fertilizers                       ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
        """)
    
    def show_menu(self):
        print(f"{Colors.YELLOW}  Main Menu:{Colors.RESET}")
        print()
        print(f"  {Colors.BOLD}{Colors.GREEN}1{Colors.RESET}  🚀 Run Full Test Suite")
        print(f"  {Colors.BOLD}{Colors.GREEN}2{Colors.RESET}  ⚡ Run Quick Test (limited cases)")
        print(f"  {Colors.BOLD}{Colors.GREEN}3{Colors.RESET}  📋 View Test Reports")
        print(f"  {Colors.BOLD}{Colors.GREEN}4{Colors.RESET}  🗄️  Check Database Status")
        print(f"  {Colors.BOLD}{Colors.GREEN}5{Colors.RESET}  🔧 Install Dependencies")
        print(f"  {Colors.BOLD}{Colors.RED}0{Colors.RESET}  🚪 Exit")
        print()
    
    def run_full_test(self):
        self.runner.quick_mode = False
        self.runner.run_full_test()
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
    
    def run_quick_test(self):
        self.runner.quick_mode = True
        self.runner.run_full_test()
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
    
    def view_reports(self):
        print(f"\n{Colors.BLUE}📋 Available Test Reports:{Colors.RESET}")
        
        reports = list(REPORTS_DIR.glob("*.json"))
        reports = sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not reports:
            print(f"{Colors.YELLOW}  No reports found{Colors.RESET}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            return
        
        print()
        for i, report in enumerate(reports, 1):
            size = report.stat().st_size / 1024
            mtime = datetime.fromtimestamp(report.stat().st_mtime)
            print(f"  {i}. {report.name} ({size:.1f} KB) - {mtime.strftime('%Y-%m-%d %H:%M')}")
        
        print()
        choice = input(f"{Colors.CYAN}Enter number to view (or 0 to cancel): {Colors.RESET}").strip()
        
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(reports):
                report_path = reports[idx - 1]
                try:
                    with open(report_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        print(f"\n{Colors.GREEN}Report: {report_path.name}{Colors.RESET}")
                        print(f"  Total Tests: {data.get('total_tests', 0)}")
                        print(f"  Passed: {data.get('passed_tests', 0)}")
                        print(f"  Failed: {data.get('failed_tests', 0)}")
                        
                        results = data.get('results', [])
                        if results:
                            print(f"\n  First 5 results:")
                            for r in results[:5]:
                                status = "✅ PASS" if r.get('passed') else "❌ FAIL"
                                print(f"    {status} - {r.get('test_name')} ({r.get('execution_time_ms', 0):.1f}ms)")
                except Exception as e:
                    print(f"{Colors.RED}Error reading report: {e}{Colors.RESET}")
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
    
    def check_database(self):
        print(f"\n{Colors.BLUE}🗄️ Database Status:{Colors.RESET}")
        
        db_path = BACKEND_DIR / "farmtech.db"
        
        if not db_path.exists():
            print(f"{Colors.RED}  ❌ Database not found: {db_path}{Colors.RESET}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            return
        
        size = db_path.stat().st_size / 1024
        print(f"  📁 Location: {db_path}")
        print(f"  📦 Size: {size:.1f} KB")
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"  📊 Tables: {len(tables)}")
            
            # Check fertilizers with Mg and Mn
            cursor.execute("SELECT COUNT(*) FROM fertilizers WHERE is_system_default = 1 AND user_id IS NULL")
            total = cursor.fetchone()[0]
            print(f"    - System fertilizers: {total}")
            
            cursor.execute("SELECT COUNT(*) FROM fertilizers WHERE is_system_default = 1 AND user_id IS NULL AND elements LIKE '%Mg%'")
            mg_count = cursor.fetchone()[0]
            print(f"    - Fertilizers with Mg: {mg_count}")
            
            cursor.execute("SELECT COUNT(*) FROM fertilizers WHERE is_system_default = 1 AND user_id IS NULL AND elements LIKE '%Mn%'")
            mn_count = cursor.fetchone()[0]
            print(f"    - Fertilizers with Mn: {mn_count}")
            
            # Show Mg fertilizers
            cursor.execute("SELECT id, name FROM fertilizers WHERE is_system_default = 1 AND user_id IS NULL AND elements LIKE '%Mg%'")
            mg_ferts = cursor.fetchall()
            if mg_ferts:
                print(f"    - Mg fertilizers:")
                for f in mg_ferts:
                    print(f"      * {f[1]} (id: {f[0]})")
            
            conn.close()
        except Exception as e:
            print(f"{Colors.RED}  ❌ Error reading database: {e}{Colors.RESET}")
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
    
    def install_dependencies(self):
        print(f"\n{Colors.BLUE}📦 Installing Dependencies...{Colors.RESET}")
        
        print(f"\n{Colors.YELLOW}Installing backend dependencies...{Colors.RESET}")
        python_exe = sys.executable
        
        if sys.platform == 'win32':
            venv_python = BACKEND_DIR / "venv" / "Scripts" / "python.exe"
        else:
            venv_python = BACKEND_DIR / "venv" / "bin" / "python"
        
        if venv_python.exists():
            python_exe = str(venv_python)
        else:
            print(f"{Colors.YELLOW}Creating virtual environment...{Colors.RESET}")
            subprocess.run([sys.executable, "-m", "venv", str(BACKEND_DIR / "venv")], check=True)
            if sys.platform == 'win32':
                python_exe = str(BACKEND_DIR / "venv" / "Scripts" / "python.exe")
            else:
                python_exe = str(BACKEND_DIR / "venv" / "bin" / "python")
        
        req_file = BACKEND_DIR / "requirements.txt"
        if req_file.exists():
            subprocess.run([python_exe, "-m", "pip", "install", "-r", str(req_file), "--upgrade"], check=True)
            print(f"{Colors.GREEN}✅ Backend dependencies installed{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ requirements.txt not found{Colors.RESET}")
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
    
    def run(self):
        while True:
            self.show_header()
            self.show_menu()
            
            choice = input(f"{Colors.CYAN}Your choice: {Colors.RESET}").strip()
            
            if choice == '1':
                self.run_full_test()
            elif choice == '2':
                self.run_quick_test()
            elif choice == '3':
                self.view_reports()
            elif choice == '4':
                self.check_database()
            elif choice == '5':
                self.install_dependencies()
            elif choice == '0':
                print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.RESET}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}❌ Invalid choice{Colors.RESET}")
                time.sleep(1)


# ============================================================
# Main Entry Point
# ============================================================
def main():
    try:
        menu = CLIMenu()
        menu.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⏹️ Interrupted{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()