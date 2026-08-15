## 📑 Table of Contents
- [Color Palette](#color-palette)
- [Site Structure](#site-structure)
  - [Home App](#home-app)
  - [Profiles App](#profiles-app)
    - [User Profile & Role Management](#user-profile--role-management)
    - [Learner / Employee Area](#learner--employee-area)
    - [Teacher Area](#teacher-area)
    - [Company Admin Area](#company-admin-area)
    - [Role-Based Access Control](#role-based-access-control)
  - [Courses App](#courses-app)
    - [Course Types](#course-types)
    - [Course Management](#course-management)
    - [Course Enrolment](#course-enrolment)
    - [Course Timetable](#course-timetable)
    - [Class Session Generation](#class-session-generation)
    - [Class Session Lifecycle](#class-session-lifecycle)
    - [Attendance](#attendance)
    - [Attendance Reporting](#attendance-reporting)
  - [Learning Assessment & Progress](#learning-assessment--progress)
    - [Student Skill Assessment](#student-skill-assessment)
    - [Student Subskill Assessment](#student-subskill-assessment)
    - [Detailed Assessment Snapshots](#detailed-assessment-snapshots)
    - [Term Assessment Snapshots](#term-assessment-snapshots)
  - [Calendar](#calendar)
  - [Django Admin](#django-admin)

- [Database Structure — Models](#database-structure--models)
  - [ERD — Entity Relationship Diagram](#erd--entity-relationship-diagram)
  - [Key Data-Integrity Rules](#key-data-integrity-rules)

- [Application Data Flow](#application-data-flow)

- [Architectural Design Choices](#architectural-design-choices)
  - [Authentication vs. Application Profile](#authentication-vs-application-profile)
  - [Course Configuration vs. Lesson Delivery](#course-configuration-vs-lesson-delivery)
  - [Enrolment vs. User Identity](#enrolment-vs-user-identity)
  - [Current Assessment vs. Assessment History](#current-assessment-vs-assessment-history)
  - [Shared Data, Role-Specific Presentation](#shared-data-role-specific-presentation)

- [Design Choices](#design-choices)
  - [Colour System](#colour-system)
  - [Responsive Design](#responsive-design)
  - [Data Visualisation](#data-visualisation)

---

## 🎨 Colour Palette
<img width="1600" height="1200" alt="EnglishGrows_ColorPalette_final" src="https://github.com/user-attachments/assets/ebd1867a-743e-45e2-a019-0593eff1cd54" />

<img width="221" height="393" alt="image" src="https://github.com/user-attachments/assets/5aace972-d513-401b-b99d-0d1f1e01fe42" />

| Colour | Hex | Role in the Design System |
|---|---|---|
| **Oxford Navy** | `#0B355F` | Primary brand colour — headings, navigation, sidebar and major UI elements |
| **Stormy Teal** | `#006B7D` | Secondary brand colour — H3 headings, icons and secondary emphasis |
| **Strong Cyan** | `#07C0C7` | Functional accent — interactive elements, active states, progress indicators and data visualisation |
| **Turquoise** | `#5FF0DF` | Structural accent — borders, dividers, HRs and subtle button details |
| **Electric Aqua** | `#5FF5FC` | Expressive brand accent — marketing and occasional high-impact UI highlights on dark backgrounds |
| **Icy Aqua** | `#C7FFF9` | Highlight surface — selected states, pills, badges and softly highlighted areas |
| **Azure Mist** | `#EDF9F7` | Subtle surface — section backgrounds, cards and low-emphasis UI areas |
| **Slate Grey** | `#6A7F81` | Secondary text — metadata, supporting information and muted UI content |
| **Cool Steel** | `#96A0A1` | Low-emphasis neutral — disabled, inactive and tertiary UI elements |


# MODELS - DATABASE STRUCTURE
## ASSESSMENT
### SKILLS ASSESSMENT
<img width="485" height="310" alt="image" src="https://github.com/user-attachments/assets/17f89c31-a78e-45be-a2b1-775316973018" />
<img width="308" height="459" alt="image" src="https://github.com/user-attachments/assets/acb9153e-34ca-43e8-babe-ecbe5f3abdfd" />

## SITE STRUCTURE

EnglishGrows has been developed using **Django 6.0.5** with **Python 3.12**.

The application follows Django's Model-Template-View architecture and is currently organised into three principal custom Django apps:

- **Home**
- **Profiles**
- **Courses**

Each app contains the relevant combination of **models**, **views**, **URLs**, **templates**, **forms**, static assets, and supporting logic required for its area of responsibility.

Authentication is handled using Django's authentication system together with **django-allauth**. Application-specific user information and role-based behaviour are managed through the `UserProfile` model.

The platform supports four principal user roles:

- **Teacher**
- **Individual learner**
- **Employee learner**
- **Company administrator**

Access to platform functionality and data is controlled according to the authenticated user's role and, where applicable, their associated company.

---

### HOME App

The `home` app is responsible primarily for the public-facing area of EnglishGrows and serves as the entry point to the platform.

#### Main responsibilities

- Provides the public **landing page**
- Presents EnglishGrows' training services and platform
- Provides navigation into the authenticated learning platform
- Contains public-facing marketing and informational content
- Directs users towards the relevant learning or company-training journey
- Integrates the public website with the authenticated Django platform

The Home app is intentionally kept separate from the teaching-management functionality so that public marketing content and authenticated platform features remain logically independent.

---

### PROFILES App

The `profiles` app contains most of the user-facing platform experience.

It extends Django authentication with application-specific profile information and provides dedicated interfaces according to each user's role.

The app includes functionality for:

- **Learners**
- **Teachers**
- **Company administrators**

The same underlying course, attendance, and assessment data is presented differently depending on the authenticated user's permissions and responsibilities.

---

#### USER PROFILE & ROLE MANAGEMENT

The platform uses Django's authenticated `User` as the primary user identity and associates it with a dedicated `UserProfile`.

The profile stores additional application information such as:

- User role
- Associated company, where applicable
- Native language
- Country
- Current CEFR level
- Profile photograph
- User-specific platform information

This avoids maintaining separate authentication models for teachers, employees, individual learners, and company administrators.

Instead, role-based access is determined through the user's profile.

---

#### LEARNER / EMPLOYEE AREA

Learners have access to a dedicated learning area containing information specific to their own active course enrolments.

Principal functionality includes:

- **Learner dashboard**
- **My Course**
- **My Attendance**
- **My Learning Progress**
- **Skill overview**
- **Detailed skill progress graphs**
- **Teacher assessment feedback**
- **Course selector when enrolled in multiple active courses**
- **Upcoming-class information**
- **Attendance and absence history**
- **Course completion information**

Only enrolments that are currently active and belong to active courses are exposed through the learner-facing course selectors.

Learners therefore interact only with relevant current training data rather than historical, cancelled, or inactive courses.

---

#### TEACHER AREA

Teachers have a dedicated operational dashboard for managing the courses and learners assigned to them.

Principal functionality includes:

- **Teacher dashboard**
- **Assigned courses**
- **Course details**
- **Class/session management**
- **Attendance management**
- **Individual attendance submission**
- **Group attendance submission**
- **Attendance history**
- **Student details**
- **Student skill assessment**
- **Subskill assessment**
- **Assessment notes**
- **Learner progress graphs**
- **Class rescheduling**
- **Calendar**
- **Course and learner progress reporting**

Teacher access is restricted to courses assigned to the authenticated teacher.

The teacher dashboard provides operational summaries for current teaching activity, including active courses, students, upcoming/completed sessions, and attendance information.

---

#### COMPANY ADMIN AREA

Company administrators have a dedicated B2B management area allowing them to monitor the training delivered to employees belonging to their organisation.

Principal functionality includes:

- **Company dashboard**
- **Employee list**
- **Employee profile and learning progress**
- **Company course list**
- **Course details**
- **Course learner list**
- **Company class/session list**
- **Company-wide attendance reporting**
- **Employee attendance records**
- **Employee skill development**
- **Assessment information**
- **Progress graphs**
- **Company calendar**

Company administrators can only access information associated with their own `Company`.

This prevents cross-company data exposure while allowing an authorised company representative to monitor employee participation, attendance, course progression, and learning outcomes.

---

#### ROLE-BASED ACCESS CONTROL

Role-based views validate the authenticated user's `UserProfile` before exposing protected information.

The application therefore applies restrictions such as:

```text
Teacher
    ↓
Only courses assigned to that teacher

Company Administrator
    ↓
Only courses and employees belonging to that company

Learner / Employee
    ↓
Only that learner's own enrolments,
attendance and assessment data


