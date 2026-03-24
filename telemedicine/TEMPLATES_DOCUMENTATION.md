# Telemedicine Web Templates Documentation

## Overview
This document outlines all the HTML templates created for the telemedicine web application.

## Templates Structure

```
templates/
├── base.html           # Base template with header, footer, navigation, and styling
├── home.html           # Home/landing page
├── login.html          # User login page
├── register.html       # User registration/signup page
├── dashboard.html      # User dashboard (protected, login required)
├── about.html          # About Us page
├── services.html       # Services and pricing page
├── 404.html            # 404 Not Found error page
└── 500.html            # 500 Server Error page
```

## Template Details

### base.html
**Purpose**: Base layout template that all other pages extend

**Features**:
- Responsive navigation header with logo
- Navigation links (Home, About, Services)
- Authentication-aware navigation (Login/Signup vs Dashboard/Logout)
- Message display system (for success/error messages)
- Styled footer with company info, links, and contact details
- Responsive design with mobile-friendly CSS
- CSS utility classes for styling

**Blocks Used**:
- `title`: Page title
- `extra_css`: Additional CSS for specific pages
- `content`: Main page content

### home.html
**Purpose**: Landing page with hero section and feature showcase

**Features**:
- Hero section with call-to-action buttons
- Statistics section (10,000+ users, 500+ doctors, etc.)
- Feature cards highlighting key benefits (6 features)
- "How It Works" section with 4-step process
- Testimonials from happy patients and doctors
- Final CTA section
- Conditional buttons based on authentication status

**Responsive**: Yes, mobile-optimized

### login.html
**Purpose**: User login form

**Features**:
- Email and password input fields
- "Forgot Password" link
- Sign-in and Cancel buttons
- Link to signup page
- Error display for failed logins
- Form validation messages

**Form Fields**:
- Email address
- Password

### register.html
**Purpose**: User registration/signup form

**Features**:
- First and last name fields
- Email address field
- Role selection (Patient/Doctor) with visual radio buttons
- Password and confirm password fields
- Terms and conditions checkbox
- Sign up and Cancel buttons
- Link to login page
- Form validation and error messages

**Form Fields**:
- First Name
- Last Name
- Email
- Role (Patient/Doctor)
- Password
- Confirm Password
- Terms agreement checkbox

### dashboard.html
**Purpose**: User dashboard after login

**Features**:
- Welcome greeting with user's name
- Quick stats cards:
  - Upcoming appointments
  - Your doctors
  - Medical records
  - Unread messages
- Quick action buttons:
  - Book Appointment
  - Start Consultation
  - View Records
  - Edit Profile
- Upcoming appointments section
- Recent activity table
- User profile information display
- Edit profile button

**Requirements**: User must be logged in (login_required decorator)

### about.html
**Purpose**: Company information and mission

**Features**:
- Attractive hero section
- Mission statement
- Company values (4 value cards)
- Company story/history
- Team member profiles (3 team members shown)
- List of reasons to choose the platform

**Sections**:
- Mission
- Values
- Story
- Team
- Why Choose Us

### services.html
**Purpose**: Service offerings and pricing

**Features**:
- Hero section
- Service categories:
  - Consultation Services (GPs, Specialists, Mental Health)
  - Additional Services (Medical Records, Prescriptions, Lab Integration)
- Pricing plans with 3 tiers:
  - Basic ($25/consultation)
  - Professional ($40/consultation) - Featured as popular
  - Premium ($99/month)
- Each plan includes feature list and CTA button
- Contact CTA section at bottom

**Service Categories**:
- General Practitioners
- Specialists
- Mental Health
- Medical Records
- Prescription Management
- Lab Integration

### 404.html
**Purpose**: Page not found error page

**Features**:
- Large 404 error code
- "Page Not Found" message
- Helpful action buttons (Go Home, Learn More)
- Professional error styling

### 500.html
**Purpose**: Server error page

**Features**:
- Large 500 error code in red
- "Server Error" message
- Explanation text
- Action buttons (Go Home, Contact Support)
- Professional error styling

## URL Routes

The following routes have been configured in `telemedicine/urls.py`:

| Route | View | Template | Authentication |
|-------|------|----------|-----------------|
| `/` | `home` | home.html | Not required |
| `/register/` | `register_view` | register.html | Not required |
| `/login/` | `login_view` | login.html | Not required |
| `/logout/` | `logout_view` | - | Required |
| `/dashboard/` | `dashboard` | dashboard.html | Required |
| `/about/` | `about` | about.html | Not required |
| `/services/` | `services` | services.html | Not required |

## Design Features

### Color Scheme
- Primary: #667eea (Purple/Blue)
- Secondary: #764ba2 (Purple)
- Background: #f8f9fa (Light Gray)
- Text: #333 (Dark Gray)
- White backgrounds for cards

### Typography
- Font Family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- Responsive font sizes
- Clear hierarchy

### Responsive Design
- Mobile-first approach
- Breakpoint: 768px for tablet/mobile adaptations
- Flexible grid layouts using CSS Grid
- Auto-scaling images and content

### Interactive Elements
- Hover effects on buttons and links
- Smooth transitions
- Card elevation on hover
- Form field focus states

## Settings Configuration

### Updated in settings.py:
1. Added 'accounts' to INSTALLED_APPS
2. Updated TEMPLATES['DIRS'] to include: `BASE_DIR / 'templates'`

### Installed Apps Order:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    'appointments',
    'accounts',  # Added
    'rest_framework.authtoken',
]
```

## Views Implementation

All views are implemented in `accounts/views.py`:

### Views Created:
1. **home(request)** - Renders home.html
2. **register_view(request)** - Handles user registration with validation
3. **login_view(request)** - Handles user login
4. **logout_view(request)** - Handles user logout
5. **dashboard(request)** - Renders dashboard.html (login required)
6. **about(request)** - Renders about.html
7. **services(request)** - Renders services.html

### Registration Validation:
- All fields required
- Password confirmation match
- Password minimum 8 characters
- Email uniqueness check
- Terms agreement required
- Valid role selection

### Login Features:
- Email-based authentication
- Error messages for invalid credentials
- User role support (Patient/Doctor)
- Creates patient/doctor profiles on registration

## Usage

### For Development:
1. Ensure Django development server is running
2. Access templates via browser at configured routes
3. Test forms with different input scenarios

### For Production:
1. Set DEBUG = False in settings.py
2. Ensure error templates (404.html, 500.html) are properly configured
3. Collect static files if using custom CSS
4. Configure ALLOWED_HOSTS
5. Use proper database (currently configured for MySQL)

## Future Enhancements

Potential templates/features to add:
- Appointment booking page
- Consultation interface page
- User profile edit page
- Medical records page
- Contact/Support page
- FAQ page
- Privacy policy page
- Terms of service page
- Payment/billing page
- Doctor search page
- Patient reviews page

## Notes

- All templates use Bootstrap-like styling patterns but with custom CSS
- No external CSS frameworks (Bootstrap, Tailwind) required
- All styling is inline in style blocks within each template
- The authentication system uses Django's built-in auth framework
- Messages framework is configured for user feedback
- Templates are responsive and mobile-friendly
