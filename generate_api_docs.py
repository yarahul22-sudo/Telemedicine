#!/usr/bin/env python
"""
REST API Documentation Generator
Automatically generates API documentation from Django REST Framework
Supports: OpenAPI/Swagger, Postman Collection, Markdown
"""

import os
import json
import re
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Optional Django setup - will work without it
try:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
except Exception as e:
    # Django not available or not configured, will use manual endpoints
    pass

# Optional Django imports - imported conditionally where needed
# from django.urls import get_resolvers, URLPattern, URLResolver
# from rest_framework.viewsets import ViewSet, ModelViewSet
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework import serializers


class APIDocumentationGenerator:
    """Generate REST API documentation from Django REST Framework"""

    def __init__(self, base_url: str = "https://api.telemedicine.moscow/v1"):
        self.base_url = base_url
        self.endpoints = []
        self.schemas = {}
        self.tags = {}

    def generate_all(self):
        """Generate all documentation formats"""
        print("[*] Extracting API endpoints...")
        self.extract_endpoints()

        print("[*] Generating OpenAPI/Swagger specification...")
        swagger_spec = self.generate_swagger()
        self.save_json("SWAGGER_SPEC.json", swagger_spec)

        print("[*] Generating Postman collection...")
        postman_collection = self.generate_postman()
        self.save_json("POSTMAN_COLLECTION.json", postman_collection)

        print("[*] Generating Markdown documentation...")
        markdown_doc = self.generate_markdown()
        self.save_markdown("API_DOCS_AUTO_GENERATED.md", markdown_doc)

        print("[*] Generating HTML documentation...")
        html_doc = self.generate_html()
        self.save_html("API_DOCS.html", html_doc)

        print("\n✅ Documentation generated successfully!")
        print(f"   - SWAGGER_SPEC.json (OpenAPI 3.0)")
        print(f"   - POSTMAN_COLLECTION.json")
        print(f"   - API_DOCS_AUTO_GENERATED.md")
        print(f"   - API_DOCS.html")

    def extract_endpoints(self):
        """Extract all API endpoints from Django URL patterns"""
        try:
            try:
                from django.urls import get_resolvers, URLPattern, URLResolver
                from telemedicine.urls import urlpatterns
                self._process_url_patterns(urlpatterns, "")
            except ImportError:
                raise Exception("Django not available")
        except Exception as e:
            print(f"[!] Could not auto-extract from urls.py: {e}")
            print("[*] Using manual endpoint definitions...")
            self._load_manual_endpoints()

    def _process_url_patterns(self, patterns, prefix=""):
        """Recursively process URL patterns"""
        try:
            from django.urls import URLPattern, URLResolver
        except ImportError:
            return
            
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                # Nested URL patterns
                new_prefix = prefix + str(pattern.pattern).rstrip("$")
                self._process_url_patterns(pattern.url_patterns, new_prefix)
            elif isinstance(pattern, URLPattern):
                path = prefix + str(pattern.pattern).rstrip("$")
                callback = pattern.callback

                # Extract method information
                if hasattr(callback, 'cls'):  # ViewSet
                    self._extract_viewset_endpoints(callback.cls, path)
                elif hasattr(callback, 'actions'):  # APIView
                    self._extract_apiview_endpoints(callback, path)

    def _extract_viewset_endpoints(self, viewset_class, path):
        """Extract endpoints from a ViewSet"""
        methods_map = {
            'list': ('GET', 'List items'),
            'create': ('POST', 'Create item'),
            'retrieve': ('GET', 'Retrieve item'),
            'update': ('PUT', 'Update item'),
            'partial_update': ('PATCH', 'Partial update item'),
            'destroy': ('DELETE', 'Delete item'),
        }

        for method_name, (http_method, description) in methods_map.items():
            if hasattr(viewset_class, method_name):
                endpoint = {
                    'path': path,
                    'method': http_method,
                    'name': f"{viewset_class.__name__}.{method_name}",
                    'description': description,
                    'class': viewset_class.__name__,
                    'operation_id': f"{viewset_class.__name__}_{method_name}",
                    'tags': [self._get_tag(viewset_class.__name__)],
                }
                self.endpoints.append(endpoint)

    def _extract_apiview_endpoints(self, view_callback, path):
        """Extract endpoints from APIView"""
        if hasattr(view_callback, 'actions'):
            for method, action in view_callback.actions.items():
                endpoint = {
                    'path': path,
                    'method': method.upper(),
                    'name': f"{view_callback.__name__}.{action}",
                    'description': getattr(view_callback, '__doc__', ''),
                    'class': view_callback.__name__,
                    'operation_id': f"{view_callback.__name__}_{action}",
                    'tags': [self._get_tag(view_callback.__name__)],
                }
                self.endpoints.append(endpoint)

    def _load_manual_endpoints(self):
        """Load manually defined endpoints (fallback)"""
        endpoints_raw = [
            # Auth Endpoints
            {'path': '/auth/register', 'method': 'POST', 'description': 'Register new user', 'tags': ['Authentication']},
            {'path': '/auth/login', 'method': 'POST', 'description': 'Login user', 'tags': ['Authentication']},
            {'path': '/auth/logout', 'method': 'POST', 'description': 'Logout user', 'tags': ['Authentication']},
            {'path': '/auth/refresh-token', 'method': 'POST', 'description': 'Refresh access token', 'tags': ['Authentication']},
            {'path': '/auth/verify-email', 'method': 'POST', 'description': 'Verify email', 'tags': ['Authentication']},
            {'path': '/auth/password-reset', 'method': 'POST', 'description': 'Request password reset', 'tags': ['Authentication']},
            {'path': '/auth/password-reset-confirm', 'method': 'POST', 'description': 'Confirm password reset', 'tags': ['Authentication']},
            {'path': '/auth/2fa/enable', 'method': 'POST', 'description': 'Enable 2FA', 'tags': ['Authentication']},
            
            # Users
            {'path': '/users/profile', 'method': 'GET', 'description': 'Get user profile', 'tags': ['Users']},
            {'path': '/users/profile', 'method': 'PUT', 'description': 'Update user profile', 'tags': ['Users']},
            {'path': '/users/password', 'method': 'PUT', 'description': 'Change password', 'tags': ['Users']},
            {'path': '/users/preferences', 'method': 'GET', 'description': 'Get preferences', 'tags': ['Users']},
            {'path': '/users/preferences', 'method': 'PUT', 'description': 'Update preferences', 'tags': ['Users']},
            
            # Doctors
            {'path': '/doctors', 'method': 'GET', 'description': 'List doctors', 'tags': ['Doctors']},
            {'path': '/doctors/{doctor_id}', 'method': 'GET', 'description': 'Get doctor details', 'tags': ['Doctors']},
            {'path': '/doctors/{doctor_id}/availability', 'method': 'GET', 'description': 'Get availability', 'tags': ['Doctors']},
            {'path': '/doctors/{doctor_id}/reviews', 'method': 'GET', 'description': 'Get reviews', 'tags': ['Doctors']},
            {'path': '/doctors/register', 'method': 'POST', 'description': 'Register as doctor', 'tags': ['Doctors']},
            {'path': '/doctors/profile', 'method': 'PUT', 'description': 'Update doctor profile', 'tags': ['Doctors']},
            
            # Patients
            {'path': '/patients/profile', 'method': 'GET', 'description': 'Get patient profile', 'tags': ['Patients']},
            {'path': '/patients/profile', 'method': 'PUT', 'description': 'Update patient profile', 'tags': ['Patients']},
            {'path': '/patients/medical-records', 'method': 'GET', 'description': 'Get medical records', 'tags': ['Patients']},
            
            # Appointments
            {'path': '/appointments/book', 'method': 'POST', 'description': 'Book appointment', 'tags': ['Appointments']},
            {'path': '/appointments', 'method': 'GET', 'description': 'List appointments', 'tags': ['Appointments']},
            {'path': '/appointments/{appointment_id}', 'method': 'GET', 'description': 'Get appointment', 'tags': ['Appointments']},
            {'path': '/appointments/{appointment_id}/reschedule', 'method': 'PUT', 'description': 'Reschedule appointment', 'tags': ['Appointments']},
            {'path': '/appointments/{appointment_id}', 'method': 'DELETE', 'description': 'Cancel appointment', 'tags': ['Appointments']},
            {'path': '/appointments/{appointment_id}/complete', 'method': 'POST', 'description': 'Complete appointment', 'tags': ['Appointments']},
            
            # Video Calls
            {'path': '/video-calls/initialize', 'method': 'POST', 'description': 'Initialize video call', 'tags': ['Video Calls']},
            {'path': '/video-calls/{call_session_id}/stats', 'method': 'GET', 'description': 'Get call stats', 'tags': ['Video Calls']},
            {'path': '/video-calls/{call_session_id}/end', 'method': 'POST', 'description': 'End call', 'tags': ['Video Calls']},
            {'path': '/video-calls/{call_session_id}/record', 'method': 'POST', 'description': 'Record call', 'tags': ['Video Calls']},
            
            # Prescriptions
            {'path': '/prescriptions/create', 'method': 'POST', 'description': 'Create prescription', 'tags': ['Prescriptions']},
            {'path': '/prescriptions', 'method': 'GET', 'description': 'List prescriptions', 'tags': ['Prescriptions']},
            {'path': '/prescriptions/{prescription_id}', 'method': 'GET', 'description': 'Get prescription', 'tags': ['Prescriptions']},
            {'path': '/prescriptions/{prescription_id}/download', 'method': 'POST', 'description': 'Download prescription', 'tags': ['Prescriptions']},
            
            # Medical Records
            {'path': '/medical-records/upload', 'method': 'POST', 'description': 'Upload medical record', 'tags': ['Medical Records']},
            {'path': '/medical-records', 'method': 'GET', 'description': 'List medical records', 'tags': ['Medical Records']},
            {'path': '/medical-records/{record_id}', 'method': 'DELETE', 'description': 'Delete record', 'tags': ['Medical Records']},
            
            # Payments
            {'path': '/payments/process', 'method': 'POST', 'description': 'Process payment', 'tags': ['Payments']},
            {'path': '/payments/history', 'method': 'GET', 'description': 'Payment history', 'tags': ['Payments']},
            {'path': '/payments/refund', 'method': 'POST', 'description': 'Request refund', 'tags': ['Payments']},
            {'path': '/payments/invoices/{invoice_id}', 'method': 'GET', 'description': 'Get invoice', 'tags': ['Payments']},
            
            # Admin
            {'path': '/admin/dashboard', 'method': 'GET', 'description': 'Admin dashboard', 'tags': ['Admin']},
            {'path': '/admin/doctors/pending', 'method': 'GET', 'description': 'Pending approvals', 'tags': ['Admin']},
            {'path': '/admin/doctors/{application_id}/approve', 'method': 'POST', 'description': 'Approve doctor', 'tags': ['Admin']},
            {'path': '/admin/doctors/{application_id}/reject', 'method': 'POST', 'description': 'Reject doctor', 'tags': ['Admin']},
            {'path': '/admin/payments/report', 'method': 'GET', 'description': 'Payment report', 'tags': ['Admin']},
        ]
        
        # Add operation_id to each endpoint
        self.endpoints = []
        for idx, endpoint in enumerate(endpoints_raw):
            endpoint_with_id = endpoint.copy()
            # Generate operation_id from path and method
            path_parts = endpoint['path'].replace('/{', '_').replace('}', '').replace('/', '_').strip('_')
            endpoint_with_id['operation_id'] = f"{path_parts}_{endpoint['method'].lower()}_{idx}"
            self.endpoints.append(endpoint_with_id)

    def _get_tag(self, class_name: str) -> str:
        """Extract tag from class name"""
        # Convert CamelCase to Title Case
        name = re.sub(r'([A-Z])', r' \1', class_name).strip()
        return name.replace(' View', '').replace(' ViewSet', '')

    def generate_swagger(self) -> Dict[str, Any]:
        """Generate OpenAPI 3.0 / Swagger specification"""
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Telemedicine Platform API",
                "description": "Complete REST API for telemedicine platform",
                "version": "1.0.0",
                "contact": {
                    "name": "API Support",
                    "email": "api-support@telemedicine.moscow"
                },
                "license": {
                    "name": "Proprietary"
                }
            },
            "servers": [
                {
                    "url": self.base_url,
                    "description": "Production API Server"
                }
            ],
            "tags": self._get_tags(),
            "paths": self._generate_swagger_paths(),
            "components": {
                "schemas": self._get_schemas(),
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            },
            "security": [
                {"bearerAuth": []}
            ]
        }
        return spec

    def _get_tags(self) -> List[Dict[str, str]]:
        """Extract unique tags from endpoints"""
        tags_set = set()
        for endpoint in self.endpoints:
            for tag in endpoint.get('tags', []):
                tags_set.add(tag)
        
        return [{"name": tag, "description": f"{tag} operations"} for tag in sorted(tags_set)]

    def _generate_swagger_paths(self) -> Dict[str, Any]:
        """Generate Swagger paths object"""
        paths = {}
        
        for endpoint in self.endpoints:
            path = endpoint['path']
            method = endpoint['method'].lower()
            
            if path not in paths:
                paths[path] = {}
            
            paths[path][method] = {
                "summary": endpoint.get('description', ''),
                "operationId": endpoint.get('operation_id', path + method),
                "tags": endpoint.get('tags', ['General']),
                "parameters": self._get_swagger_parameters(path),
                "requestBody": self._get_swagger_request_body(method),
                "responses": self._get_swagger_responses(),
                "security": [{"bearerAuth": []}]
            }
        
        return paths

    def _get_swagger_parameters(self, path: str) -> List[Dict[str, Any]]:
        """Extract path parameters"""
        params = []
        param_pattern = r'\{(\w+)\}'
        matches = re.findall(param_pattern, path)
        
        for match in matches:
            params.append({
                "name": match,
                "in": "path",
                "required": True,
                "schema": {"type": "string"}
            })
        
        return params

    def _get_swagger_request_body(self, method: str) -> Optional[Dict[str, Any]]:
        """Get request body schema"""
        if method not in ['post', 'put', 'patch']:
            return None
        
        return {
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Request"}
                }
            }
        }

    def _get_swagger_responses(self) -> Dict[str, Any]:
        """Get standard response schemas"""
        return {
            "200": {
                "description": "Successful operation",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Response"}
                    }
                }
            },
            "201": {
                "description": "Resource created",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Response"}
                    }
                }
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Error"}
                    }
                }
            },
            "401": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Error"}
                    }
                }
            },
            "404": {
                "description": "Not found",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Error"}
                    }
                }
            }
        }

    def _get_schemas(self) -> Dict[str, Any]:
        """Get schema definitions"""
        return {
            "Response": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "message": {"type": "string"},
                    "data": {"type": "object"}
                }
            },
            "Error": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "error": {"type": "string"},
                    "message": {"type": "string"}
                }
            },
            "Request": {
                "type": "object",
                "properties": {}
            }
        }

    def generate_postman(self) -> Dict[str, Any]:
        """Generate Postman collection"""
        collection = {
            "info": {
                "name": "Telemedicine Platform API",
                "description": "Complete API collection for telemedicine platform",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
                "version": "1.0.0"
            },
            "servers": [
                {
                    "url": self.base_url,
                    "variables": {
                        "base_url": {"default": "api.telemedicine.moscow"}
                    }
                }
            ],
            "item": self._generate_postman_items(),
            "auth": {
                "type": "bearer",
                "bearer": [
                    {"key": "token", "value": "{{access_token}}", "type": "string"}
                ]
            },
            "variable": [
                {
                    "key": "access_token",
                    "value": "your_access_token_here",
                    "type": "string"
                },
                {
                    "key": "base_url",
                    "value": self.base_url,
                    "type": "string"
                }
            ]
        }
        return collection

    def _generate_postman_items(self) -> List[Dict[str, Any]]:
        """Generate Postman request items organized by tag"""
        items_by_tag = {}
        
        for endpoint in self.endpoints:
            tag = endpoint.get('tags', ['General'])[0]
            if tag not in items_by_tag:
                items_by_tag[tag] = []
            
            items_by_tag[tag].append({
                "name": endpoint.get('description', endpoint['path']),
                "request": {
                    "method": endpoint['method'],
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        },
                        {
                            "key": "Authorization",
                            "value": "Bearer {{access_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{{{{base_url}}}}{endpoint['path']}",
                        "protocol": "https",
                        "host": ["{{base_url}}"],
                        "path": endpoint['path'].split('/')
                    },
                    "body": {
                        "mode": "raw",
                        "raw": "{}"
                    }
                }
            })
        
        # Convert to folder structure
        items = []
        for tag, endpoints in sorted(items_by_tag.items()):
            items.append({
                "name": tag,
                "item": endpoints
            })
        
        return items

    def generate_markdown(self) -> str:
        """Generate Markdown documentation"""
        md = "# Telemedicine API - Auto-Generated Documentation\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += f"**Base URL:** `{self.base_url}`\n\n"
        md += f"**Total Endpoints:** {len(self.endpoints)}\n\n"
        
        md += "## Table of Contents\n\n"
        tags = set()
        for endpoint in self.endpoints:
            for tag in endpoint.get('tags', []):
                tags.add(tag)
        
        for tag in sorted(tags):
            md += f"- [{tag}](#{tag.lower().replace(' ', '-')})\n"
        
        md += "\n---\n\n"
        
        # Group by tag
        endpoints_by_tag = {}
        for endpoint in self.endpoints:
            tag = endpoint.get('tags', ['General'])[0]
            if tag not in endpoints_by_tag:
                endpoints_by_tag[tag] = []
            endpoints_by_tag[tag].append(endpoint)
        
        for tag in sorted(endpoints_by_tag.keys()):
            md += f"## {tag}\n\n"
            
            for endpoint in endpoints_by_tag[tag]:
                method = endpoint['method']
                path = endpoint['path']
                desc = endpoint.get('description', '')
                
                method_color = {
                    'GET': '🟦',
                    'POST': '🟩',
                    'PUT': '🟨',
                    'PATCH': '🟧',
                    'DELETE': '🟥'
                }
                
                md += f"### {method_color.get(method, '')} `{method}` {path}\n\n"
                if desc:
                    md += f"**Description:** {desc}\n\n"
                
                md += f"**URL:** `{self.base_url}{path}`\n\n"
                md += f"**Authentication:** Bearer Token (Required)\n\n"
                
                # Extract parameters
                params = re.findall(r'\{(\w+)\}', path)
                if params:
                    md += "**Path Parameters:**\n\n"
                    for param in params:
                        md += f"- `{param}` (string, required)\n"
                    md += "\n"
                
                md += "\n"
        
        return md

    def generate_html(self) -> str:
        """Generate interactive HTML documentation"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telemedicine API Documentation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .content {
            display: grid;
            grid-template-columns: 250px 1fr;
            min-height: 600px;
        }
        
        .sidebar {
            background: #f8f9fa;
            border-right: 1px solid #e0e0e0;
            padding: 20px;
            overflow-y: auto;
        }
        
        .sidebar h3 {
            font-size: 14px;
            text-transform: uppercase;
            color: #666;
            margin-bottom: 15px;
            margin-top: 20px;
            font-weight: 600;
        }
        
        .sidebar a {
            display: block;
            padding: 8px 12px;
            margin-bottom: 5px;
            color: #333;
            text-decoration: none;
            border-radius: 4px;
            transition: all 0.3s;
            font-size: 14px;
        }
        
        .sidebar a:hover {
            background: #e0e0e0;
            padding-left: 16px;
        }
        
        .main {
            padding: 40px;
            overflow-y: auto;
        }
        
        .endpoint {
            margin-bottom: 40px;
            padding: 20px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }
        
        .endpoint h3 {
            font-size: 18px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .method {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
            color: white;
        }
        
        .method.GET { background: #61affe; }
        .method.POST { background: #49cc90; }
        .method.PUT { background: #fca130; }
        .method.PATCH { background: #50e3c2; }
        .method.DELETE { background: #f93e3e; }
        
        .path {
            background: white;
            padding: 10px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            margin-bottom: 10px;
            color: #666;
            font-size: 13px;
        }
        
        .description {
            color: #666;
            margin-bottom: 10px;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #e0e0e0;
            color: #666;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
            .sidebar {
                border-right: none;
                border-bottom: 1px solid #e0e0e0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 Telemedicine API</h1>
            <p>Complete REST API Documentation</p>
        </div>
        
        <div class="content">
            <div class="sidebar">
                <h3>Endpoints</h3>
"""
        
        # Group by tags
        tags_set = set()
        for endpoint in self.endpoints:
            for tag in endpoint.get('tags', []):
                tags_set.add(tag)
        
        for tag in sorted(tags_set):
            html += f"<h3 style='margin-top: 30px;'>{tag}</h3>\n"
            for endpoint in self.endpoints:
                if tag in endpoint.get('tags', []):
                    html += f"<a href='#{endpoint['operation_id']}'>{endpoint['method']} {endpoint['path']}</a>\n"
        
        html += """
            </div>
            
            <div class="main">
"""
        
        # Endpoints
        for endpoint in self.endpoints:
            html += f"""
            <div class="endpoint" id="{endpoint['operation_id']}">
                <h3>
                    <span class="method {endpoint['method']}">{endpoint['method']}</span>
                    {endpoint['path']}
                </h3>
                <p class="description">{endpoint.get('description', '')}</p>
                <p class="path">{self.base_url}{endpoint['path']}</p>
            </div>
"""
        
        html += """
            </div>
        </div>
        
        <div class="footer">
            <p>Generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            <p>Telemedicine Platform API v1.0</p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def save_json(self, filename: str, data: Dict):
        """Save JSON file"""
        filepath = Path(__file__).parent / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"   ✓ Saved: {filename}")

    def save_markdown(self, filename: str, content: str):
        """Save Markdown file"""
        filepath = Path(__file__).parent / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✓ Saved: {filename}")

    def save_html(self, filename: str, content: str):
        """Save HTML file"""
        filepath = Path(__file__).parent / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✓ Saved: {filename}")


def main():
    """Main entry point"""
    print("=" * 60)
    print("REST API Documentation Generator")
    print("=" * 60)
    print()
    
    generator = APIDocumentationGenerator(
        base_url="https://api.telemedicine.moscow/v1"
    )
    
    # Try to extract from Django, fall back to manual if needed
    try:
        generator.extract_endpoints()
    except Exception as e:
        print(f"[!] Auto-extraction failed: {e}")
        generator._load_manual_endpoints()
    
    generator.generate_all()
    
    print()
    print("=" * 60)
    print("✅ Documentation generation complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Import SWAGGER_SPEC.json into Swagger UI")
    print("2. Import POSTMAN_COLLECTION.json into Postman")
    print("3. Open API_DOCS.html in your browser")
    print("4. Review API_DOCS_AUTO_GENERATED.md for markdown docs")


if __name__ == '__main__':
    main()
