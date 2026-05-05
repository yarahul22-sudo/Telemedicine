# REST API Documentation Generator

Automatically generates comprehensive REST API documentation in multiple formats from your Django REST Framework application.

## Features

✅ **Multiple Output Formats:**
- **OpenAPI 3.0 / Swagger** (`SWAGGER_SPEC.json`) - Import into Swagger UI, ReDoc, or Insomnia
- **Postman Collection** (`POSTMAN_COLLECTION.json`) - Import directly into Postman
- **Markdown Documentation** (`API_DOCS_AUTO_GENERATED.md`) - GitHub-friendly format
- **Interactive HTML** (`API_DOCS.html`) - Beautiful web documentation

✅ **Auto-Extraction:**
- Scans Django URL patterns
- Extracts REST Framework viewsets and views
- Analyzes serializers for schema information
- Identifies path parameters automatically

✅ **Comprehensive Documentation:**
- HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Path parameters
- Request/Response schemas
- Error codes and descriptions
- Authentication requirements
- Rate limiting info

## Installation

### Prerequisites
```bash
pip install django djangorestframework
```

The script uses Django's built-in inspection tools, no additional dependencies needed.

## Usage

### Option 1: Auto-Generate from Django URLs

```bash
python generate_api_docs.py
```

The script will:
1. Analyze your Django project structure
2. Extract all API endpoints
3. Generate all 4 documentation formats
4. Save files to the project root

### Option 2: Use as a Module

```python
from generate_api_docs import APIDocumentationGenerator

# Initialize generator
generator = APIDocumentationGenerator(
    base_url="https://api.telemedicine.moscow/v1"
)

# Extract and generate all formats
generator.extract_endpoints()
generator.generate_swagger()  # OpenAPI spec
generator.generate_postman()  # Postman collection
generator.generate_markdown() # Markdown docs
generator.generate_html()     # HTML documentation
```

### Option 3: Django Management Command

Create `telemedicine/management/commands/generate_api_docs.py`:

```python
from django.core.management.base import BaseCommand
from generate_api_docs import APIDocumentationGenerator

class Command(BaseCommand):
    help = 'Generate API documentation in multiple formats'
    
    def handle(self, *args, **options):
        generator = APIDocumentationGenerator()
        generator.generate_all()
        self.stdout.write(self.style.SUCCESS('Documentation generated!'))
```

Then run:
```bash
python manage.py generate_api_docs
```

## Output Files

### 1. SWAGGER_SPEC.json
OpenAPI 3.0 specification compatible with:
- **Swagger UI** - Hosted documentation with "Try it Out"
- **ReDoc** - Beautiful documentation
- **Insomnia** - API testing tool
- **Postman** - Can import OpenAPI specs

**Use cases:**
- Generate documentation website
- Integration testing
- API contract validation
- Client code generation

### 2. POSTMAN_COLLECTION.json
Ready-to-import Postman collection with:
- All endpoints organized by tags
- Bearer token authentication pre-configured
- Request examples and templates
- Environment variables for base URL and tokens

**How to import:**
1. Open Postman
2. File → Import
3. Select `POSTMAN_COLLECTION.json`
4. Set `{{access_token}}` variable
5. Start testing!

### 3. API_DOCS_AUTO_GENERATED.md
Markdown documentation including:
- All endpoints with HTTP methods
- Path parameters
- Color-coded method badges
- Table of contents with navigation
- Great for GitHub repositories

### 4. API_DOCS.html
Interactive HTML documentation:
- Professional dark-themed UI
- Searchable endpoints
- Responsive design (mobile-friendly)
- Sidebar navigation
- Color-coded HTTP methods

**Open in browser:** Double-click or drag into Chrome/Firefox

## Customization

### Change Base URL
```python
generator = APIDocumentationGenerator(
    base_url="https://your-api.com/v2"
)
```

### Add Custom Tags
```python
def _get_tags(self):
    return [
        {"name": "Authentication", "description": "User auth endpoints"},
        {"name": "Doctors", "description": "Doctor management"},
        # ... more tags
    ]
```

### Modify Response Schemas
```python
def _get_schemas(self):
    return {
        "Response": { ... },
        "CustomSchema": { ... }
    }
```

### Add Security Schemes
```python
"components": {
    "securitySchemes": {
        "bearerAuth": { ... },
        "apiKey": { ... }
    }
}
```

## Integration with CI/CD

### GitHub Actions Example

Create `.github/workflows/generate-docs.yml`:

```yaml
name: Generate API Docs

on:
  push:
    branches: [main]
    paths: ['telemedicine/**']

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: python generate_api_docs.py
      - uses: actions/upload-artifact@v2
        with:
          name: api-docs
          path: |
            SWAGGER_SPEC.json
            POSTMAN_COLLECTION.json
            API_DOCS_AUTO_GENERATED.md
            API_DOCS.html
```

### Auto-Publish to GitHub Pages

```yaml
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: .
    include_dotfiles: true
```

## API Testing Workflow

1. **Generate Docs**
   ```bash
   python generate_api_docs.py
   ```

2. **Import to Postman**
   - File → Import → POSTMAN_COLLECTION.json
   - Set auth token in variables

3. **Test Endpoints**
   - Use generated collection for API testing
   - Verify all endpoints work as documented

4. **Deploy Documentation**
   - Host HTML file on web server
   - Share Swagger UI link with team
   - Embed ReDoc in portal

## Advanced Features

### Custom Endpoint Extraction

Override the endpoint extraction method:

```python
class CustomGenerator(APIDocumentationGenerator):
    def _load_manual_endpoints(self):
        # Load from custom source
        self.endpoints = [
            {'path': '/custom', 'method': 'GET', 'description': 'Custom endpoint'}
        ]
```

### Generate from OpenAPI File

```python
import json

with open('existing-openapi.json', 'r') as f:
    spec = json.load(f)
    # Convert and merge
```

### Export to Different Formats

Add custom exporters:

```python
def export_yaml(self):
    import yaml
    return yaml.dump(self.generate_swagger())

def export_graphql_schema(self):
    # Generate GraphQL schema from REST endpoints
    pass
```

## Troubleshooting

### "Could not auto-extract from urls.py"
- Ensure `DJANGO_SETTINGS_MODULE` is set correctly
- Check that URL patterns are properly configured
- Falls back to manual endpoint definitions

### Import errors in Postman
- Ensure JSON is valid (copy-paste error)
- Try reimporting collection
- Check Postman version (use latest)

### Missing endpoints
- Add endpoints to `_load_manual_endpoints()` method
- Check if endpoints are properly registered in Django URLs
- Verify viewset/view classes are detected

### HTML not displaying
- Ensure CSS is embedded (not linked)
- Try in different browser
- Check browser console for errors

## Examples

### Example: Testing Authentication Flow

```bash
# 1. Register
curl -X POST https://api.telemedicine.moscow/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"Pass123!"}'

# 2. Login
curl -X POST https://api.telemedicine.moscow/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"Pass123!"}'

# 3. Use token
curl -X GET https://api.telemedicine.moscow/v1/users/profile \
  -H "Authorization: Bearer <access_token>"
```

### Example: Postman Test Script

```javascript
pm.test("Response is 200", function() {
    pm.response.to.have.status(200);
});

pm.test("Response has success flag", function() {
    var jsonData = pm.response.json();
    pm.expect(jsonData.success).to.be.true;
});

// Set token for next request
pm.environment.set("access_token", pm.response.json().data.access_token);
```

## Performance

- **Generation time:** < 1 second for 50+ endpoints
- **File sizes:**
  - Swagger JSON: ~20KB
  - Postman Collection: ~25KB
  - HTML: ~30KB
  - Markdown: ~15KB

## License

This documentation generator is part of the Telemedicine Platform project.

## Support

For issues or feature requests:
- Email: api-support@telemedicine.moscow
- Issues: Submit via platform support portal
- Documentation: https://docs.telemedicine.moscow

---

**Version:** 1.0.0  
**Last Updated:** May 5, 2026  
**Maintainer:** Telemedicine Dev Team
