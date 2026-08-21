## 📑 Table of Contents

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
    - [Core Brand / Interface Palette](#core-brand---interface-palette)
    - [CEFR Levels Colours](#cefr-levels-colours)
    - [Language Skills Colours](#language-skills-colours)
    - [Semantic and Status Colours](#semantic-and-status-colours)
  - [Responsive Design](#responsive-design)
  - [Data Visualisation](#data-visualisation)

---


---

# SITE STRUCTURE

EnglishGrows has been developed using **Django 6.0.5** with **Python 3.12**.

The application follows Django's Model-Template-View architecture and is currently organised into three principal custom Django apps:

- **Home**
- **Profiles**
- **Courses**

Each app contains the relevant combination of ***models***, ***views***, ***URLs***, ***templates***, ***forms***, static assets, and supporting logic required for its area of responsibility.

## USER ROLES

**User Authentication is handled using Django's authentication system together with ***django-allauth***. Application-specific user information and role-based behaviour are managed through the `UserProfile` model.**

The platform supports four principal user roles:

- **Teacher**
- **Individual learner**
- **Employee learner**
- **Company administrator**

Access to platform functionality and data is controlled according to the authenticated user's role and, where applicable, their associated company.

---

## HOME App

The `home` app is responsible primarily for the public-facing area of EnglishGrows and serves as the entry point to the platform.

### Main responsibilities

- Provides the public **landing page**
- Presents EnglishGrows' training services and platform
- Provides navigation into the authenticated learning platform
- Contains public-facing informational and marketing content
- Directs users towards the relevant learning or company-training journey
- Integrates the public website with the authenticated Django platform

The Home app is intentionally kept separate from the teaching-management functionality so that public marketing content and authenticated platform features remain logically independent.

---

## PROFILES App

The `profiles` app contains most of the user-facing platform experience.

It extends Django authentication with application-specific profile information and provides dedicated interfaces according to each user's role.

The app includes functionality for:

- **Learners**
- **Teachers**
- **Company administrators**

The same underlying course, attendance, and assessment data is presented differently depending on the authenticated user's permissions and responsibilities.

---

### USER PROFILE & ROLE MANAGEMENT

The platform uses Django's authenticated `User` as the primary user identity and associates it with a dedicated `UserProfile`.

The profile stores additional application information such as:

- User role
- Associated company *(where applicable)*
- Native language
- Country
- Current CEFR level
- Profile photograph
- User-specific platform information

This avoids maintaining separate authentication models for teachers, employees, individual learners, and company administrators.

Instead, role-based access is determined through the user's profile.

---

### LEARNER / EMPLOYEE AREA

Learners have access to a dedicated learning area containing information specific to their own active course enrolments.

Principal functionality includes:

- **Learner dashboard**
- **My Course**
- **My Attendance**
- **My Calendar**
- **My Learning Progress**
- **Skill overview**
- **Detailed skill progress graphs**
- **Teacher assessment feedback**
- **Course selector when enrolled in multiple active courses**
- **Upcoming-class information**
- **Attendance and absence history**
- **Course completion information**
- **Account settings**

Only enrolments that are currently active and belong to active courses are exposed through the learner-facing course selectors.

Learners therefore interact only with relevant current training data rather than historical, cancelled, or inactive courses.

---

### TEACHER AREA

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

### COMPANY ADMIN AREA

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
- **Employee assessment information**
- **Employee progress graphs**
- **Company class calendar**

Company administrators can only access information associated with their own `Company`.

This prevents cross-company data exposure while allowing an authorised company representative to monitor employee participation, attendance, course progression, and learning outcomes.

---

### ROLE-BASED ACCESS CONTROL

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
```
---

## COURSES App

The `courses` app contains the core **course-delivery, scheduling, enrolment, and attendance architecture** of the EnglishGrows platform.

It manages the relationships between:

- **Course types**
- **Courses**
- **Teachers**
- **Learners**
- **Companies**
- **Course enrolments**
- **Recurring timetables**
- **Individual class sessions**
- **Attendance records**
- **Bank holidays**

The app also contains the business logic responsible for automatically generating lessons and attendance records and for maintaining the lifecycle of courses, enrolments, and class sessions.

The principal models managed by this area of the application include:

- `CourseType`
- `Course`
- `CourseTimetableSlot`
- `CourseEnrollment`
- `ClassSession`
- `Attendance`
- `BankHoliday`

---

### Course Types

`CourseType` defines the reusable categories of training that can be offered through the platform.

Rather than storing the same general course information repeatedly for every individual course, a `CourseType` acts as a reusable definition from which specific `Course` instances can be created.

A course type can contain information such as:

- **Name**
- **Description**
- **Default training hours**
- **Availability for individual learners**
- **Availability for company training**

A single `CourseType` can therefore be associated with multiple `Course` instances.

```text
CourseType
    │
    │ 1 : N
    ▼
  Course
```

This separates the **type of training being offered** from the **actual delivery of that training**.

---

### Course Management

The `Course` model represents a concrete training programme delivered to one or more learners.

Each course can be associated with:

- A `CourseType`
- An assigned teacher
- A company, when the course is corporate
- One or more learners through `CourseEnrollment`
- One or more recurring timetable slots
- Multiple generated class sessions

A course stores delivery-specific information including:

- **Course name**
- **Course type**
- **CEFR level**
- **Teacher**
- **Company**, where applicable
- **Total training hours**
- **Class duration**
- **Class-duration source**
- **Start date**
- **End date**
- **Course status**
- **Creation date**

Course statuses currently support:

```text
Confirmed
Active
Paused
Completed
Cancelled
```

Course duration and class-generation logic are linked. The application uses the total number of training hours and lesson duration to determine the number of lessons required.

A course is not considered completed simply because its scheduled end date has passed.

Instead, course completion depends on its actual lessons:

```text
Course
   │
   ▼
ClassSessions
   │
   ▼
All sessions completed?
   │
   ├── No  → Course remains open
   │
   └── Yes → Course becomes completed
```

When all `ClassSession` records belonging to a course have reached `completed` status, the course is automatically moved to `completed`.

Active learner enrolments belonging to that course are then also moved to `completed`.

This ensures that course status reflects **actual teaching delivery rather than dates alone**.

---

### Course Enrolment

Learners are connected to courses through the `CourseEnrollment` model.

This is an association model between `User` and `Course`:

```text
User
  │
  │ 1 : N
  ▼
CourseEnrollment
  ▲
  │ N : 1
  │
Course
```

Using a dedicated enrolment model rather than a simple many-to-many relationship allows EnglishGrows to store information that belongs specifically to the learner's participation in a particular course.

Each enrolment can contain:

- **Student**
- **Course**
- **Enrolment date**
- **Enrolment status**
- **Target CEFR level**
- **Learning objective**

Enrolment statuses include:

```text
Active
Paused
Completed
Cancelled
```

The database prevents the same learner from being enrolled more than once in the same course.

When a learner becomes actively enrolled in a course that already contains generated lessons, the application automatically creates any missing `Attendance` records for applicable unfinished sessions.

Completed lessons are deliberately excluded.

This prevents a learner who joins a course after it has started from receiving artificial attendance records for lessons that took place before their enrolment.

---

### Course Timetable

Recurring weekly scheduling is managed through `CourseTimetableSlot`.

A timetable slot defines the normal weekly teaching pattern of a course.

For example:

|Monday|09:00 – 10:30|
|Wednesday|09:00 – 10:30|


Each timetable slot stores:

- **Course**
- **Day of the week**
- **Start time**
- **End time**

The timetable represents a **scheduling rule**, not an individual lesson.

This distinction is important:

```text
CourseTimetableSlot
        │
        │ defines recurring schedule
        ▼
   ClassSession
        │
        │ represents
        ▼
   Actual lesson

The database prevents duplicate timetable slots with the same:
```
```
course
+ day_of_week
+ start_time
+ end_time
```
Validation also ensures that the end time occurs after the start time.

The timetable architecture allows the system to generate individual class sessions automatically while keeping those generated lessons independent enough to be completed or rescheduled later.

---

### Class Session Generation

`ClassSession` represents an **actual lesson instance** belonging to a course.

Once the required course configuration exists, EnglishGrows can automatically generate the lessons required to deliver the complete course.

The generation process uses:

- **Course start date**
- **Total course hours**
- **Class duration**
- **Recurring timetable slots**
- **Active learner enrolments**

Conceptually:

```text
Course configuration
        │
        ├── Start date
        ├── Total hours
        ├── Class duration
        └── Timetable
                │
                ▼
        Generate sessions
                │
                ▼
        ClassSession 1
        ClassSession 2
        ClassSession 3
              ...
                │
                ▼
        Final ClassSession
```

The generation process is designed to be **idempotent** and guarded against accidental duplication.

If the required class sessions already exist, saving the course does not generate a second copy of its schedule.

Each generated session receives a sequential `class_number`.

For example:

```text
Course
├── Lesson 1
├── Lesson 2
├── Lesson 3
├── Lesson 4
└── Lesson 5
```

The combination of:

```text
course + class_number
```

is unique.

Attendance records are also automatically generated for active learners when the class-session structure is created.

---

### Class Session Lifecycle

A `ClassSession` has its own lifecycle independently of the parent course.

The normal lesson flow is:

```text
scheduled
    │
    ▼
completed
```
---

### Rescheduling a Class Lesson

When a lesson needs to be rescheduled, either the **learner/employee or the teacher** can mark the session as requiring rescheduling:

```text
                         ┌─────────────────────┐
                         │      scheduled      │
                         └──────────┬──────────┘
                                    │
                     Reschedule requested by
                         either party
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                Learner / Employee          Teacher
                         │                     │
                         └──────────┬──────────┘
                                    ▼
                         pending_reschedule
                                    │
                          New date/time agreed
                                    │
                                    ▼
                       Teacher reschedules class
                                    │
                                    ▼
                              rescheduled
                                    │
                           Lesson takes place
                                    │
                                    ▼
                               completed
```

The `pending_reschedule` status therefore represents a **rescheduling request or an unresolved scheduling change**, rather than a cancelled lesson.

Both parties involved in the training can initiate this workflow:

- **Learners / employees** can flag a scheduled class when they need it to be rescheduled.
- **Teachers** can also mark a scheduled class as requiring rescheduling.
- Once a new date and time have been agreed, the **teacher updates the session schedule** and the class moves to `rescheduled`.
- After the rescheduled lesson has taken place and attendance has been recorded, the session can be moved to `completed`.

A fundamental design decision is that a rescheduled lesson remains the **same `ClassSession` database record** throughout this process.

For example:

```text
Lesson 8
12 Oct · 10:00
scheduled
       │
       │ Reschedule requested
       ▼
Lesson 8
pending_reschedule
       │
       │ New date/time agreed
       ▼
Lesson 8
15 Oct · 16:00
rescheduled
       │
       │ Lesson delivered
       ▼
Lesson 8
completed
```

The application does **not** delete the original lesson and create a replacement.

Instead, the existing `ClassSession` is updated with the newly agreed date and time while retaining its original identity.

This preserves:

- **Lesson identity**
- **Class number**
- **Course relationship**
- **Learner attendance relationships**
- **Course progression**
- **Historical consistency**
- **References from other areas of the application**

This architecture also ensures that rescheduling a lesson does not accidentally increase the number of classes belonging to the course.

The distinction between the statuses is therefore:

| Status | Meaning |
|---|---|
| `scheduled` | The lesson is scheduled normally |
| `pending_reschedule` | A learner/employee or teacher has indicated that the lesson needs to be rescheduled and a new date/time is still to be agreed |
| `rescheduled` | The teacher has updated the existing session with the newly agreed date/time |
| `completed` | The lesson has taken place and has been completed |

This workflow allows rescheduling to be initiated by either side while keeping responsibility for modifying the official course schedule with the teacher.
---

### Attendance

The `Attendance` model records the attendance status of an individual learner for an individual `ClassSession`.

The relationship can be represented as:

```text
ClassSession
     │
     │ 1 : N
     ▼
 Attendance
     ▲
     │ N : 1
     │
    User
```

Each attendance record can store:

- **Class session**
- **Student**
- **Attendance status**
- **Minutes late**
- **Teacher notes**
- **Recorded timestamp**

**Attendance statuses include:**

```text
Scheduled
Attended
Missed
Excused
Cancelled
Pending reschedule
```

**The database enforces a unique learner/session relationship:**

```text
class_session + student = unique
```

A learner therefore cannot accidentally have two contradictory attendance records for the same lesson.

For example, this is prevented:

```text
Lesson 4
├── Student A → Attended
└── Student A → Missed   ✗
```

Instead, the existing attendance record changes status.

Attendance records initially act as scheduled placeholders and are subsequently updated when the teacher records the actual attendance outcome.

---

### Attendance Reporting

Attendance data provides a shared source of information for the three principal authenticated areas of the platform.

#### Learners

Learners can review their own:

- **Attendance history**
- **Attendance rate**
- **Attended classes**
- **Missed classes**
- **Excused absences**
- **Individual lesson records**

#### Teachers

Teachers can:

- **Submit attendance**
- **Review previously submitted attendance**
- **Manage attendance for group courses**
- **Identify classes requiring attendance submission**
- **Review attendance by learner**
- **Review attendance by course**

#### Company Administrators

Company administrators can review:

- **Employee attendance**
- **Attendance by course**
- **Attendance rates**
- **Missed lessons**
- **Excused absences**
- **Attendance submission status**
- **Company-wide training participation**

**Attendance percentages** are calculated from ***recorded attendance outcomes***.

Future `scheduled` records are not treated as attended or missed lessons and are therefore excluded from the denominator used to calculate the learner's actual attendance rate.

**This prevents future lessons from artificially reducing attendance statistics.**

---

## Learning Assessment & Progress

The assessment architecture tracks both a learner's **current language-skill performance** and the **historical development of those skills over time**.

Assessment is course-specific.

A learner can therefore have different skill assessments in different courses rather than having one global assessment attached permanently to their user account.

The assessment architecture consists of four principal models:

```text
StudentSkillAssessment
        │
        ├── StudentSubSkillAssessment
        │
        ├── StudentSkillAssessmentSnapshot
        │
        └── StudentSkillTermSnapshot
```

### Language Skills Assessed:

Each skill is represented by a distinctive colour, to make it easier to visually track on the progress bars and skill cards

| Skill | Colour | Hex |
| :--- | :---: | :---: |
| 🎙️ **Speaking** | 🟨 Sunflower Gold | `#F5BE58` |
| 🎧 **Listening** | 🟪 Indigo Velvet | `#4E2496` |
| 📖 **Reading** | 🟧 Chocolate | `#E1752D` |
| ✍️ **Writing** | 🟦 Pacific Blue | `#0EA5B7` |

---

### Student Skill Assessment

`StudentSkillAssessment` represents the learner's **current assessment state for one main language skill within one course**.

Each assessment belongs to:

```text
Student
   +
Course
   +
Skill
```

For example:

```text
Student: Jane Doe
Course: Business English B2
Skill: Speaking
```

The database maintains only one current assessment for each:

```text
student + course + skill
```

combination.

The model also stores teacher notes associated with the skill.

Rather than storing a manually entered overall percentage, the current skill score is calculated dynamically from the learner's assessed subskills.

Conceptually:

```text
StudentSkillAssessment
        │
        ├── Subskill rating
        ├── Subskill rating
        ├── Subskill rating
        └── Subskill rating
                │
                ▼
          Average score
             0 – 10
```

Only subskills that have actually been rated participate in this calculation.

***Unrated subskills are excluded rather than being interpreted as zero performance.***

---

### Student Subskill Assessment

`StudentSubSkillAssessment` provides the detailed assessment information from which the overall skill assessment is calculated.

**Each principal language skill is divided into several pedagogically relevant subskills, *aligned with CEFR descriptors and informed by Cambridge English assessment criteria***.

The current subskill structure is:

```text
Speaking
├── Fluency
├── Grammar & vocabulary (Accuracy & range)
├── Pronunciation
└── Interaction

Reading
├── Scanning (Specific information)
├── Skimming (General Idea)
└── In detail (Deep Understanding)

Listening
├── For Gist (General Idea)
├── For Specific Information
└── In detail (Deep Understanding)

Writing
├── Structure & Organization
├── Cohesion & Coherence
├── Grammar & vocabulary (Accuracy & range)
└── Register (Style accuracy)
```

Each `StudentSubSkillAssessment` belongs to one `StudentSkillAssessment`.

The relationship can be represented as:

```text
StudentSkillAssessment
        │
        │ 1 : N
        ▼
StudentSubSkillAssessment
```

The combination:

```text
skill_assessment + subskill
```

is unique.

This prevents the same subskill from being duplicated within a learner's assessment for a particular skill.

Subskills use descriptive performance categories rather than user-facing percentages.

The current assessment categories are:

| Assessment Category | Internal Score |
|---|---:|
| **Priority areas** | `4.0 / 10` |
| **Developing areas** | `5.0 / 10` |
| **Required standard achieved** | `6.0 / 10` |
| **Confident areas** | `7.5 / 10` |
| **Key strengths** | `10.0 / 10` |

The internal numerical representation is used to:

- Calculate the learner's current overall skill score
- Build skill-progress graphs
- Compare skill development over time
- Generate historical assessment snapshots
- Support term-based progress reporting

Only subskills that have actually been assessed are included when calculating the parent skill's average score.

For example:

```text
Speaking

Fluency                                  7.5
Grammar & vocabulary (Accuracy & range)  6.0
Pronunciation                             —
Interaction                              5.0
                                         ───
Average score                            6.2 / 10
```

The unrated `Pronunciation` subskill is excluded from the calculation rather than being treated as a zero score.

This allows the assessment score to represent only the areas that have genuinely been assessed.

---

#### Detailed Assessment Snapshots

`StudentSkillAssessmentSnapshot` records the **fine-grained historical evolution** of a learner's skill assessment.

A snapshot is created when a genuine subskill rating is added or changed.

The process can be represented as:

```text
Teacher assesses subskill
          │
          ▼
Subskill rating changes
          │
          ▼
Overall skill score recalculated
          │
          ▼
StudentSkillAssessmentSnapshot
          │
          ▼
Score + exact timestamp stored
```

This produces a chronological history of meaningful assessment changes.

For example:

```text
Speaking

10 Sep  → 5.8
24 Sep  → 6.1
08 Oct  → 6.5
22 Oct  → 6.8
12 Nov  → 7.2
```

Snapshots are not created merely because an assessment object is saved.

A new historical entry requires a genuine rating change.

Likewise, unrated placeholder subskills do not generate artificial historical data.

This prevents unnecessary duplicate records and produces a cleaner representation of actual learner development.

---

#### Term Assessment Snapshots

`StudentSkillTermSnapshot` provides a second and deliberately separate form of assessment history.

While `StudentSkillAssessmentSnapshot` captures detailed changes, a term snapshot represents a **formal progress checkpoint**.

Examples may include:

```text
Term 1
Term 2
Mid-course Review
End-of-course Review
```

Each term snapshot stores:

- **Skill assessment**
- **Term label**
- **Skill score**
- **Recorded date**

The combination:

```text
skill_assessment + term_label
```

is unique.

The two historical models therefore serve different purposes:

| Model | Purpose | Frequency |
|---|---|---|
| `StudentSkillAssessmentSnapshot` | Detailed progression history | Whenever a genuine assessment change occurs |
| `StudentSkillTermSnapshot` | Formal progress checkpoint | At defined assessment periods |

Conceptually:

```text
                  StudentSkillAssessment
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
 Assessment Snapshot          Term Snapshot
              │                     │
              ▼                     ▼
 Detailed progression       Formal checkpoints
```

This separation allows EnglishGrows to provide both **fine-grained progress graphs** and **structured term-to-term reporting** without conflating the two types of historical data.

---

### Calendar

EnglishGrows includes a role-aware calendar built from the platform's existing `ClassSession` records.

A separate calendar-event model is not required.

Instead:

```text
Course
   │
   ▼
ClassSession
   │
   ▼
Calendar presentation
```

This ensures that the calendar reflects the same lesson information used throughout the rest of the application.

If a class is rescheduled, the corresponding calendar entry therefore reflects the updated `ClassSession` rather than requiring a second calendar record to be manually synchronised.

The calendar is available in the relevant interfaces for:

- **Teachers**
- **Learners**
- **Company administrators**

Depending on device size, the interface supports views such as:

- **Day**
- **Week**
- **Month**
- **List**
- **Multi-month / year**

Calendar events provide contextual information and links appropriate to the authenticated user's role.

For example:

```text
Teacher
    ↓
Course / class management

Learner
    ↓
Own lesson information

Company Administrator
    ↓
Company course information
```

The calendar therefore acts as a visual representation of the underlying lesson-delivery architecture rather than as an independent scheduling system.

---

### Django Admin

The built-in Django Admin interface provides authorised administrative access to the application's core database records.

It is used as an operational and development-management interface rather than as the primary user-facing interface.

Administrators can manage data including:

- **Users and profiles**
- **Companies**
- **Course types**
- **Courses**
- **Course enrolments**
- **Timetable slots**
- **Class sessions**
- **Attendance**
- **Bank holidays**
- **Skill assessments**
- **Subskill assessments**
- **Assessment snapshots**

Where appropriate, related objects are presented through Django Admin inlines.

For example, course administration can expose related:

```text
Course
├── Enrolments
├── Timetable Slots
└── Class Sessions
```

Generated class sessions are primarily intended to be **managed and updated rather than manually recreated**, helping protect the integrity of the automatically generated course structure.

The Django Admin therefore complements the role-specific application interfaces while providing authorised access to lower-level database administration.

---

## DATABASE STRUCTURE — MODELS

EnglishGrows uses a **relational database architecture** managed through Django's ORM.

**PostgreSQL** is used for the production database, while **SQLite** is used for local development.

The database architecture is divided into four principal domains:

```text
IDENTITY & ORGANISATION
├── Django User
├── UserProfile
└── Company

COURSE MANAGEMENT
├── CourseType
├── Course
├── CourseTimetableSlot
├── CourseEnrollment
└── BankHoliday

LESSON DELIVERY & ATTENDANCE
├── ClassSession
└── Attendance

LEARNING & ASSESSMENT
├── StudentSkillAssessment
├── StudentSubSkillAssessment
├── StudentSkillAssessmentSnapshot
└── StudentSkillTermSnapshot
```

This separation prevents unrelated responsibilities from being concentrated in a single model and allows the different areas of the application to evolve independently.

The architecture distinguishes between:

- **Authentication data**
- **Organisation data**
- **Course configuration**
- **Learner enrolment**
- **Recurring scheduling rules**
- **Actual lesson instances**
- **Attendance outcomes**
- **Current learner assessment**
- **Detailed assessment history**
- **Formal term-based assessment history**

---

### ERD — Entity Relationship Diagram

The following Entity Relationship Diagram represents the principal database relationships within EnglishGrows:

```mermaid
erDiagram

    USER {
        bigint id PK
        varchar username
        varchar first_name
        varchar last_name
        varchar email
        boolean is_active
    }

    USER_PROFILE {
        bigint id PK
        bigint user_id FK
        bigint company_id FK
        varchar role
        varchar native_language
        varchar country
        varchar current_level
        varchar profile_photo
    }

    COMPANY {
        bigint id PK
        varchar name
        varchar tax_id
        varchar billing_email
        text billing_address
        varchar phone_number
        varchar country
    }

    COURSE_TYPE {
        bigint id PK
        varchar name
        text description
        decimal default_hours
        boolean is_for_companies
        boolean is_for_individual
    }

    COURSE {
        bigint id PK
        bigint course_type_id FK
        bigint teacher_id FK
        bigint company_id FK
        varchar name
        varchar course_level
        decimal total_hours
        decimal class_duration
        varchar class_duration_source
        date start_date
        date end_date
        varchar status
        datetime created_at
    }

    COURSE_TIMETABLE_SLOT {
        bigint id PK
        bigint course_id FK
        smallint day_of_week
        time start_time
        time end_time
    }

    COURSE_ENROLLMENT {
        bigint id PK
        bigint course_id FK
        bigint student_id FK
        datetime enrolled_at
        varchar status
        varchar target_level
        text learning_objective
    }

    CLASS_SESSION {
        bigint id PK
        bigint course_id FK
        varchar title
        integer class_number
        datetime start_time
        datetime end_time
        varchar meeting_link
        varchar topic
        varchar status
        datetime created_at
    }

    ATTENDANCE {
        bigint id PK
        bigint class_session_id FK
        bigint student_id FK
        varchar status
        integer minutes_late
        text notes
        datetime recorded_at
    }

    STUDENT_SKILL_ASSESSMENT {
        bigint id PK
        bigint student_id FK
        bigint course_id FK
        varchar skill
        text teacher_notes
        datetime updated_at
    }

    STUDENT_SUBSKILL_ASSESSMENT {
        bigint id PK
        bigint skill_assessment_id FK
        varchar subskill
        varchar rating
        datetime updated_at
    }

    STUDENT_SKILL_ASSESSMENT_SNAPSHOT {
        bigint id PK
        bigint skill_assessment_id FK
        decimal score
        datetime recorded_at
    }

    STUDENT_SKILL_TERM_SNAPSHOT {
        bigint id PK
        bigint skill_assessment_id FK
        varchar term_label
        decimal score
        date recorded_at
    }

    USER ||--|| USER_PROFILE : "has profile"

    COMPANY o|--o{ USER_PROFILE : "contains members"

    COURSE_TYPE ||--o{ COURSE : "categorises"

    USER o|--o{ COURSE : "teaches"
    COMPANY o|--o{ COURSE : "owns"

    COURSE ||--o{ COURSE_TIMETABLE_SLOT : "defines timetable"

    USER ||--o{ COURSE_ENROLLMENT : "enrols"
    COURSE ||--o{ COURSE_ENROLLMENT : "has learners"

    COURSE ||--o{ CLASS_SESSION : "contains"

    CLASS_SESSION ||--o{ ATTENDANCE : "records"
    USER ||--o{ ATTENDANCE : "has attendance"

    USER ||--o{ STUDENT_SKILL_ASSESSMENT : "is assessed"
    COURSE ||--o{ STUDENT_SKILL_ASSESSMENT : "assessment context"

    STUDENT_SKILL_ASSESSMENT ||--o{ STUDENT_SUBSKILL_ASSESSMENT : "contains"

    STUDENT_SKILL_ASSESSMENT ||--o{ STUDENT_SKILL_ASSESSMENT_SNAPSHOT : "tracks changes"

    STUDENT_SKILL_ASSESSMENT ||--o{ STUDENT_SKILL_TERM_SNAPSHOT : "tracks terms"
```

The ERD highlights several important architectural decisions.

`CourseEnrollment` acts as an association entity between users and courses rather than using a simple direct many-to-many relationship.

Likewise, `Attendance` acts as the relationship between a learner and a specific lesson.

Assessment history is deliberately separated from current assessment state through the two snapshot models:

- `StudentSkillAssessmentSnapshot` — detailed change-by-change history
- `StudentSkillTermSnapshot` — formal periodic assessment history

---

### Key Data-Integrity Rules

EnglishGrows implements database constraints and application-level business rules to protect the consistency of teaching and learner data.

#### User & Organisation

- Each authenticated user has one `UserProfile`.
- A profile may optionally be associated with a `Company`.
- A company may contain multiple employees and company administrators.
- Corporate courses can be associated with a company.
- Individual courses do not require a company relationship.

#### Course & Enrolment

- A teacher may teach multiple courses.
- A learner may participate in multiple courses.
- The learner-course relationship is represented through `CourseEnrollment`.
- A learner cannot have duplicate enrolments for the same course.
- Enrolment status is maintained independently from course status.
- Completing a course automatically completes its active enrolments.

#### Timetable & Sessions

- A course may contain multiple timetable slots.
- Duplicate timetable slots for the same course, day, start time, and end time are prevented.
- Timetable end time must occur after start time.
- `CourseTimetableSlot` represents a recurring scheduling rule.
- `ClassSession` represents an actual lesson.
- Each class number is unique within its course.
- Class-session generation is protected against accidental duplication.
- A rescheduled lesson remains the same `ClassSession`.
- A course only becomes completed when all of its sessions are completed.

#### Attendance

- Each attendance record belongs to one learner and one class session.
- A learner can have only one attendance record per class session.
- Attendance records are automatically created for active learners when applicable.
- Learners joining an existing course receive attendance records only for unfinished sessions.
- Future `scheduled` attendance does not affect recorded attendance-rate calculations.

#### Assessment

- Skill assessments are course-specific.
- One current `StudentSkillAssessment` exists for each student/course/skill combination.
- Each subskill appears only once within its parent skill assessment.
- Unrated subskills are excluded from the calculated skill average.
- Assessment uses descriptive pedagogical categories with internal **0–10 scores**, rather than user-facing percentages.
- Genuine subskill rating changes create `StudentSkillAssessmentSnapshot` records.
- Saving an unchanged rating does not create an artificial snapshot.
- `StudentSkillAssessmentSnapshot` stores detailed chronological assessment history.
- `StudentSkillTermSnapshot` stores formal periodic assessment checkpoints.
- A term label can occur only once for each skill assessment.

Together, these constraints help ensure that the database remains a consistent **single source of truth** for course delivery, attendance, learner assessment, and historical progress.

---

## Application Data Flow

The application follows a **role-aware data flow** in which authenticated users interact with the same underlying business data through interfaces adapted to their permissions and responsibilities.

At a high level, application data moves through the following structure:

```text
User Authentication
        │
        ▼
UserProfile
        │
        ├── Teacher
        ├── Individual Student
        ├── Employee
        └── Company Administrator
        │
        ▼
Role-specific Dashboard / Navigation
        │
        ▼
Courses
        │
        ├── Course Configuration
        │       ├── Course Type
        │       ├── Level
        │       ├── Timetable
        │       ├── Teacher
        │       ├── Company
        │       └── Class Duration
        │
        ├── Enrolments
        │       └── Students / Employees
        │
        └── Class Sessions
                │
                ├── Attendance
                ├── Rescheduling
                ├── Lesson Information
                └── Course Progress
                        │
                        ├── Skill Assessment
                        ├── Subskill Assessment
                        ├── Teacher Notes
                        └── Assessment Snapshots
```

The Django views act as the intermediary between the database and the user interface. Each view retrieves only the information relevant to the authenticated user's role and, where appropriate, further restricts access by teacher, company, course or student.

For example:

- A **teacher** may access only courses assigned to them and the students enrolled in those courses.
- A **company administrator** may access employees and courses belonging to their own company.
- A **student or employee** may access only their own enrolments, attendance records, assessments and course information.

This approach allows the platform to maintain a **single source of truth at database level** while presenting different views of that information depending on the user's role.

Course activity also drives several dependent data flows automatically. When class sessions are generated, attendance records are created for enrolled students. When new students join a course already in progress, attendance records are generated only for the relevant future sessions.

Attendance, session completion and assessment data then contribute to the progress information displayed throughout the platform.

---

## Architectural Design Choices

The architecture of **English Grows** has been designed around the separation of identity, learning configuration, lesson delivery and assessment history.

Several areas that could initially appear suitable for a single model have deliberately been separated in order to reduce duplication, improve maintainability and preserve historical data.

### Authentication vs. Application Profile

Django's built-in `User` model is responsible for authentication-related information such as:

- username;
- email;
- password;
- login state;
- authentication permissions.

Application-specific information is stored separately in `UserProfile`.

The profile contains information such as:

- application role;
- company;
- current English level;
- native language;
- country;
- profile photograph;
- active status.

This avoids modifying Django's authentication model unnecessarily and keeps authentication concerns separate from business-specific user information.

The relationship is therefore:

```text
User
 │
 └── UserProfile
        ├── Role
        ├── Company
        ├── Current level
        ├── Native language
        ├── Country
        └── Profile information
```

This structure also allows the same authentication system to support several user roles while providing each role with different application functionality.

---

### Course Configuration vs. Lesson Delivery

A `Course` represents the overall teaching programme rather than an individual lesson.

It stores long-term configuration such as:

- course name;
- course type;
- level;
- teacher;
- company;
- total contracted hours;
- class duration;
- number of classes;
- start and end dates;
- meeting link;
- course status.

Recurring timetable information is stored independently through `CourseTimetableSlot`.

```text
Course
 │
 ├── CourseTimetableSlot
 │      ├── Day of week
 │      ├── Start time
 │      └── End time
 │
 └── ClassSession
        ├── Date and time
        ├── Class number
        ├── Topic
        ├── Status
        └── Meeting link
```

`ClassSession`, by contrast, represents one concrete occurrence of a lesson.

This separation is important because individual classes may later:

- be completed;
- be rescheduled;
- become pending reschedule;
- receive a different date or time;
- contain specific lesson information;
- generate attendance records.

Changing one class therefore does not require changing the general course configuration.

---

### Enrolment vs. User Identity

A student's identity and their participation in a course are intentionally stored separately.

`User` and `UserProfile` describe **who the person is**, while `CourseEnrollment` describes **their relationship with a particular course**.

An enrolment can therefore contain course-specific information such as:

- enrolment status;
- enrolment date;
- target level;
- learning objective;
- attendance statistics;
- course participation.

The relationship can be represented as:

```text
Student
   │
   ├── CourseEnrollment ─── Course A
   │
   ├── CourseEnrollment ─── Course B
   │
   └── CourseEnrollment ─── Course C
```

This is particularly important because the same student may participate in more than one course over time.

Completed or previous enrolments can remain in the database without altering the student's account or creating duplicate user records.

The same architecture also supports employees who may undertake multiple company-sponsored courses during their time with an organisation.

---

### Current Assessment vs. Assessment History

The assessment system deliberately separates a student's **current assessment state** from their **historical progress data**.

`StudentSkillAssessment` represents the current teacher assessment for one principal skill:

- Speaking;
- Listening;
- Reading;
- Writing.

Each skill contains several pedagogically relevant subskills stored through `StudentSubSkillAssessment`.

```text
StudentSkillAssessment
        │
        ├── Skill
        ├── Current aggregated score
        ├── Teacher notes
        │
        └── StudentSubSkillAssessment
                ├── Subskill
                └── Rating
```

Subskills are evaluated using qualitative assessment categories such as:

- **Strong**
- **Confident**
- **Required Standard**
- **Developing**
- **Needs Work**

The overall skill score is derived from the student's subskill assessments and presented on a `/10` scale.

Historical progress is stored independently through assessment snapshots.

```text
Current Assessment
        │
        ├── Snapshot — Term / Assessment Point 1
        ├── Snapshot — Term / Assessment Point 2
        └── Snapshot — Term / Assessment Point 3
```

A snapshot records a skill score at a particular stage of the course without replacing earlier results.

This distinction is essential because updating the student's current assessment should not destroy the data required to visualise their development over time.

The resulting historical records are used by the progress charts shown to teachers, students and company administrators.

---

### Shared Data, Role-Specific Presentation

The platform does not create separate course, attendance or assessment data for each type of user.

Instead, the same underlying records are reused across role-specific views.

For example:

```text
                    Attendance
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       Teacher       Student      Company Admin
        View           View            View
```

The difference lies in:

- what information each user is authorised to access;
- what actions they may perform;
- how the information is presented.

A teacher may record or modify an assessment, while a student can only view their own assessment.

Similarly, a company administrator can review employee progress but does not receive the same teaching controls as the teacher.

This architecture reduces duplicated business logic and ensures that different areas of the platform remain synchronised because they are reading from the same underlying records.

---

# Design Choices

The user interface has been designed for a **boutique corporate training environment**, rather than as a generic educational platform.

The visual system therefore prioritises:

- clarity;
- restrained use of colour;
- professional hierarchy;
- easily scannable business information;
- consistent interaction patterns;
- responsive behaviour across devices.

Role-specific dashboards and navigation expose the information most relevant to each user while secondary information remains available through dedicated pages.

---

## Colour System

The **English Grows** interface uses a carefully defined colour system centred around navy, teal, cyan, aqua and turquoise tones, supported by cool neutrals and a small set of purpose-specific semantic colours.

The system has been designed to reinforce the platform's **boutique corporate identity** while maintaining clear visual hierarchy, consistency and readability across dashboards, navigation, cards, forms, assessment interfaces and data visualisations.

Colour is used deliberately to communicate:

- brand identity;
- visual hierarchy;
- interaction and emphasis;
- interface depth and surface differentiation;
- application and operational status;
- assessment categories;
- data visualisation.

Colour is therefore treated as a **functional component of the design system**, rather than as decoration alone.

---

### Colour Architecture

The overall colour architecture is organised into **three functional layers**:

1. **Brand / Interface Colours** — establish the visual identity and general UI hierarchy of the application.
2. **Assessment / Data Colours** — provide persistent visual identification of the four principal language skills.
3. **Semantic / Status Colours** — communicate operational meaning such as active, confirmed, paused, completed, attended, excused or missed.

These layers are **functionally distinct rather than mutually exclusive palettes**. Selected brand colours are intentionally reused for semantic states where their visual character supports the intended meaning. This avoids unnecessary expansion of the overall palette while maintaining consistent semantic associations.

```text
COLOUR SYSTEM
│
├── BRAND / INTERFACE COLOURS
│   │
│   ├── DARK / CORPORATE
│   │   ├── #0B355F  Oxford Blue
│   │   └── #006B7D  Stormy Teal
│   │
│   ├── BRAND / INTERACTIVE ACCENTS
│   │   ├── #07C0C7  Strong Cyan
│   │   ├── #5FF0DF  Turquoise
│   │   └── #5FF5FC  Electric Aqua
│   │
│   ├── LIGHT SURFACES / ACCENTS
│   │   ├── #C7FFF9  Icy Aqua
│   │   ├── #EDF9F7  Azure Mist
│   │   └── #F5F5F5  White Smoke
│   │
│   └── COOL NEUTRALS
│       ├── #4F6870  Blue Slate
│       └── #7A949B  Cool Steel
│
├── ASSESSMENT / DATA COLOURS
│   │
│   ├── #F5BE58  Speaking — Sunflower Gold
│   ├── #4E2496  Listening — Indigo Velvet
│   ├── #E1752D  Reading — Chocolate
│   └── #0EA5B7  Writing — Pacific Blue
│
└── SEMANTIC / STATUS COLOURS
    │
    ├── LEARNER STATUS
    │   ├── #38DF9C  Active
    │   └── #7A949B  Inactive
    │
    ├── COURSE STATUS
    │   ├── #006B7D  Confirmed
    │   ├── #5FF0DF  Active
    │   ├── #FFB000  Paused
    │   ├── #EF4444  Cancelled
    │   └── #4F6870  Completed
    │
    └── ATTENDANCE STATUS
        ├── #38DF9C  Attended
        ├── #07C0C7  Excused
        └── #FF5A5A  Missed
```

The three layers are **conceptually independent but intentionally interconnected**:

- the **brand/interface palette** establishes the identity and visual hierarchy of English Grows;
- the **assessment/data palette** provides persistent visual identification of pedagogical information;
- the **semantic/status palette** communicates application state, reusing selected brand colours where appropriate and introducing dedicated semantic colours only where necessary.

Colour is always accompanied by text, labels, icons or other interface context rather than being used as the sole means of communicating meaning.

---

### Core Brand - Interface Palette

The core **English Grows** interface palette consists of ten colours:

<img width="1600" height="1200" alt="Color Palette_EnglishGrows" src="https://github.com/user-attachments/assets/a92e4372-16ec-4776-96e2-314406eaeed6" />

| Colour | Preview | Hex | Primary UI Role |
| :--- | :---: | :---: | :--- |
| **Oxford Blue** | ![#0B355F](https://img.shields.io/badge/Oxford_Blue-0B355F?style=flat&labelColor=0B355F&color=0B355F) | `#0B355F` | Primary brand colour, navigation, headings and high-emphasis elements |
| **Stormy Teal** | ![#006B7D](https://img.shields.io/badge/Stormy_Teal-006B7D?style=flat&labelColor=006B7D&color=006B7D) | `#006B7D` | Strong secondary brand colour, darker accents and interactive emphasis |
| **Strong Cyan** | ![#07C0C7](https://img.shields.io/badge/Strong_Cyan-07C0C7?style=flat&labelColor=07C0C7&color=07C0C7) | `#07C0C7` | Primary interactive colour and distinctive brand accent |
| **Electric Aqua** | ![#5FF5FC](https://img.shields.io/badge/Electric_Aqua-5FF5FC?style=flat&labelColor=5FF5FC&color=5FF5FC) | `#5FF5FC` | Bright accent and high-visibility interface details |
| **Turquoise** | ![#5FF0DF](https://img.shields.io/badge/Turquoise-5FF0DF?style=flat&labelColor=5FF0DF&color=5FF0DF) | `#5FF0DF` | Secondary accent, indicators and selected interface elements |
| **Icy Aqua** | ![#C7FFF9](https://img.shields.io/badge/Icy_Aqua-C7FFF9?style=flat&labelColor=C7FFF9&color=C7FFF9) | `#C7FFF9` | Soft highlighted backgrounds and subtle accent surfaces |
| **Azure Mist** | ![#EDF9F7](https://img.shields.io/badge/Azure_Mist-EDF9F7?style=flat&labelColor=EDF9F7&color=EDF9F7) | `#EDF9F7` | Light backgrounds, surfaces and subtle visual separation |
| **White Smoke** | ![#F5F5F5](https://img.shields.io/badge/White_Smoke-F5F5F5?style=flat&labelColor=F5F5F5&color=F5F5F5) | `#F5F5F5` | Neutral data surfaces and card backgrounds; occasionally used as light text on dark surfaces |
| **Blue Slate** | ![#4F6870](https://img.shields.io/badge/Blue_Slate-4F6870?style=flat&labelColor=4F6870&color=4F6870) | `#4F6870` | Dark neutral, secondary text and subdued interface elements |
| **Cool Steel** | ![#7A949B](https://img.shields.io/badge/Cool_Steel-7A949B?style=flat&labelColor=7A949B&color=7A949B) | `#7A949B` | Secondary neutral, supporting text, borders and low-emphasis elements |

#### Brand Palette Rationale

The core palette is organised into four complementary functional families:

```text
DARK / CORPORATE
#0B355F  Oxford Blue
    │
    └── #006B7D  Stormy Teal

BRAND / INTERACTIVE ACCENTS
#07C0C7  Strong Cyan
    │
    ├── #5FF0DF  Turquoise
    └── #5FF5FC  Electric Aqua

LIGHT SURFACES / ACCENTS
#C7FFF9  Icy Aqua
    │
    └── #EDF9F7  Azure Mist
            │
            └── #F5F5F5  White Smoke

COOL NEUTRALS
#4F6870  Blue Slate
    │
    └── #7A949B  Cool Steel
```

- **Oxford Blue** provides the strongest corporate anchor and is used where visual authority and high contrast are required.
- **Stormy Teal** bridges the darker corporate foundation with the brighter cyan, aqua and turquoise identity of the application.
- **Strong Cyan**, **Turquoise** and **Electric Aqua** provide the most recognisable English Grows accent colours and are used selectively for interaction, emphasis and active interface elements.
- **Icy Aqua** and **Azure Mist** provide subtle tinted surfaces and visual separation without relying exclusively on pure white.
- **White Smoke** provides a clean neutral surface for cards and data-heavy areas while remaining softer than pure white.
- **Blue Slate** and **Cool Steel** provide a controlled neutral hierarchy for secondary information, borders and lower-emphasis elements.

This hierarchy allows brighter colours to remain distinctive because they are used selectively against a restrained corporate and neutral foundation.

---

### CEFR Level Colours

The application uses a dedicated colour system to provide immediate visual identification of a learner's **CEFR proficiency level**.

The official [**Common European Framework of Reference for Languages (CEFR)**](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions), developed by the **Council of Europe**, defines six principal proficiency levels from **A1 to C2** through language proficiency descriptors. It does **not prescribe a mandatory or universal colour scheme** for those levels.

Colour coding is nevertheless commonly used in language-learning materials and multi-level course series to help learners and teachers distinguish proficiency levels visually. Major educational publishers such as **Pearson** organise extensive course ranges around clearly differentiated CEFR levels, although the colours assigned to individual levels vary between publishers and product families.

English Grows follows this broader visual convention while defining its **own consistent CEFR colour mapping** as part of the application's design system.

| CEFR Level | Preview | Colour | Hex |
| :---: | :---: | :--- | :---: |
| **A1** | ![#6EFF7F](https://img.shields.io/badge/A1-6EFF7F?style=flat&labelColor=6EFF7F&color=6EFF7F) | Mint Glow | `#6EFF7F` |
| **A2** | ![#FF954F](https://img.shields.io/badge/A2-FF954F?style=flat&labelColor=FF954F&color=FF954F) | Tangerine Dream | `#FF954F` |
| **B1** | ![#436EFD](https://img.shields.io/badge/B1-436EFD?style=flat&labelColor=436EFD&color=436EFD) | Electric Sapphire | `#436EFD` |
| **B2** | ![#7B27A5](https://img.shields.io/badge/B2-7B27A5?style=flat&labelColor=7B27A5&color=7B27A5) | Indigo Bloom | `#7B27A5` |
| **C1** | ![#DBDF2B](https://img.shields.io/badge/C1-DBDF2B?style=flat&labelColor=DBDF2B&color=DBDF2B) | Lemon Lime | `#DBDF2B` |
| **C2** | ![#902331](https://img.shields.io/badge/C2-902331?style=flat&labelColor=902331&color=902331) | Burgundy | `#902331` |

#### CEFR Colour Rationale

The CEFR palette is intentionally **more varied than the core English Grows brand palette**.

Unlike brand colours, which establish interface identity and hierarchy, CEFR colours need to make adjacent proficiency levels immediately distinguishable when they appear in course lists, learner profiles, filters, badges and other data-dense interfaces.

The six colours therefore function primarily as **categorical identifiers**:

```text
CEFR LEVEL COLOURS
│
├── BASIC USER
│   ├── A1  #6EFF7F  Mint Glow
│   └── A2  #FF954F  Tangerine Dream
│
├── INDEPENDENT USER
│   ├── B1  #436EFD  Electric Sapphire
│   └── B2  #7B27A5  Indigo Bloom
│
└── PROFICIENT USER
    ├── C1  #DBDF2B  Lemon Lime
    └── C2  #902331  Burgundy
```

This grouping reflects the three broad CEFR proficiency bands:

- **A1–A2 — Basic User**
- **B1–B2 — Independent User**
- **C1–C2 — Proficient User**

The individual colours are deliberately distinct in hue so that the level can be recognised quickly without requiring progressively darker or lighter versions of a single colour.

The CEFR colours are therefore used as **persistent level identifiers**, rather than as indicators of success, warning or status. For example, **C2 Burgundy does not represent an error state**, just as **A1 Mint Glow does not represent a success state**; each colour identifies a proficiency category within the learning system.

As with the rest of the English Grows colour system, colour reinforces rather than replaces textual information. CEFR colours are always accompanied by their corresponding **A1, A2, B1, B2, C1 or C2 label**, ensuring that proficiency level remains explicit regardless of colour perception.

The resulting hierarchy keeps four different uses of colour clearly separated:

```text
BRAND / INTERFACE       → Product identity and UI hierarchy
ASSESSMENT / DATA       → Speaking, Listening, Reading and Writing
CEFR LEVELS             → Language proficiency classification
SEMANTIC / STATUS       → Operational meaning and application state
```
---

### Language Skills Colours

The language assessment system uses a dedicated colour set for the four principal language skills.

These colours are intentionally separate from the core brand palette because they carry a **persistent pedagogical meaning**, rather than a general interface function.

<img width="1600" height="1200" alt="Skills_color_palette" src="https://github.com/user-attachments/assets/c7694cb2-94e2-4a78-a2e2-2a9ddd330612" />

| Skill | Preview | Colour | Hex |
| :--- | :---: | :--- | :---: |
| 🎙️ **Speaking** | ![#F5BE58](https://img.shields.io/badge/Sunflower_Gold-F5BE58?style=flat&labelColor=F5BE58&color=F5BE58) | Sunflower Gold | `#F5BE58` |
| 🎧 **Listening** | ![#4E2496](https://img.shields.io/badge/Indigo_Velvet-4E2496?style=flat&labelColor=4E2496&color=4E2496) | Indigo Velvet | `#4E2496` |
| 📖 **Reading** | ![#E1752D](https://img.shields.io/badge/Chocolate-E1752D?style=flat&labelColor=E1752D&color=E1752D) | Chocolate | `#E1752D` |
| ✍️ **Writing** | ![#0EA5B7](https://img.shields.io/badge/Pacific_Blue-0EA5B7?style=flat&labelColor=0EA5B7&color=0EA5B7) | Pacific Blue | `#0EA5B7` |

These colours remain consistent across:

- skill assessment cards;
- subskill assessment interfaces;
- skill progress graphs;
- chart datasets;
- legends;
- skill-specific visual indicators.

Maintaining a permanent colour assignment for each skill improves visual recognition across different areas of the application and prevents assessment data from becoming visually dependent on the surrounding interface.

For example, **Sunflower Gold** consistently represents Speaking, while **Indigo Velvet** consistently represents Listening, regardless of whether the user is viewing an assessment card, progress graph or historical assessment data.

This creates a clear distinction between **interface colour** and **assessment colour**: the core palette establishes the product identity, while the skill palette identifies pedagogical information.

---

### Semantic / Status Colours

Semantic colours communicate the **state or operational meaning of application data**, rather than the identity of an interface component.

The semantic system follows a consistent rationale:

| Colour Family | Semantic Meaning |
| :--- | :--- |
| **Green** | Positive, valid or successfully fulfilled state |
| **Cyan / Teal / Turquoise** | Operational or informational state without warning or negative meaning |
| **Amber** | Interruption or state requiring attention |
| **Red** | Negative outcome or termination |
| **Blue-grey neutrals** | Inactive, completed, historical or de-emphasised state |

Some semantic colours intentionally reuse colours from the core brand palette. This reduces unnecessary palette expansion while allowing colours to perform clearly defined roles within specific application contexts.

#### Learner Status

Learner status distinguishes between profiles currently participating in the platform and those that are inactive.

| Status | Preview | Hex | Rationale |
| :--- | :---: | :---: | :--- |
| **Active** | ![#38DF9C](https://img.shields.io/badge/Active-38DF9C?style=flat&labelColor=38DF9C&color=38DF9C) | `#38DF9C` | Green communicates a positive, currently active learner state |
| **Inactive** | ![#7A949B](https://img.shields.io/badge/Inactive-7A949B?style=flat&labelColor=7A949B&color=7A949B) | `#7A949B` | Cool Steel provides a de-emphasised neutral state |

#### Course Status

Course status colours communicate both the normal lifecycle of a course and exceptional states requiring attention.

| Status | Preview | Hex | Rationale |
| :--- | :---: | :---: | :--- |
| **Confirmed** | ![#006B7D](https://img.shields.io/badge/Confirmed-006B7D?style=flat&labelColor=006B7D&color=006B7D) | `#006B7D` | Stormy Teal represents an established course that has been confirmed but is not yet active |
| **Active** | ![#5FF0DF](https://img.shields.io/badge/Active-5FF0DF?style=flat&labelColor=5FF0DF&color=5FF0DF) | `#5FF0DF` | Brighter Turquoise gives currently running courses greater visual immediacy |
| **Paused** | ![#FFB000](https://img.shields.io/badge/Paused-FFB000?style=flat&labelColor=FFB000&color=FFB000) | `#FFB000` | Amber communicates temporary interruption and a state requiring attention |
| **Cancelled** | ![#EF4444](https://img.shields.io/badge/Cancelled-EF4444?style=flat&labelColor=EF4444&color=EF4444) | `#EF4444` | Red communicates termination and a negative operational state |
| **Completed** | ![#4F6870](https://img.shields.io/badge/Completed-4F6870?style=flat&labelColor=4F6870&color=4F6870) | `#4F6870` | Blue Slate communicates a closed, historical state without implying an error |

The normal course lifecycle follows a deliberate visual progression:

```text
CONFIRMED              ACTIVE                 COMPLETED
#006B7D                #5FF0DF               #4F6870
Stormy Teal      →     Turquoise       →     Blue Slate
Established            Current                Historical
```

**Paused** and **Cancelled** sit outside this normal progression because they represent exceptional course states:

```text
PAUSED                 CANCELLED
#FFB000                #EF4444
Amber                  Red
Attention              Negative / Terminated
```

#### Attendance Status

Attendance colours distinguish between a positive attendance outcome, an accepted absence and a negative absence.

| Status | Preview | Hex | Rationale |
| :--- | :---: | :---: | :--- |
| **Attended** | ![#38DF9C](https://img.shields.io/badge/Attended-38DF9C?style=flat&labelColor=38DF9C&color=38DF9C) | `#38DF9C` | Green communicates a positive attendance outcome |
| **Excused** | ![#07C0C7](https://img.shields.io/badge/Excused-07C0C7?style=flat&labelColor=07C0C7&color=07C0C7) | `#07C0C7` | Strong Cyan communicates a neutral, acknowledged exception without implying a warning |
| **Missed** | ![#FF5A5A](https://img.shields.io/badge/Missed-FF5A5A?style=flat&labelColor=FF5A5A&color=FF5A5A) | `#FF5A5A` | Red communicates a negative attendance outcome |

The attendance palette follows a simple semantic model:

```text
ATTENDED               EXCUSED                MISSED
#38DF9C                #07C0C7               #FF5A5A
Positive         →     Informational    →     Negative
```

This distinction is particularly important for **Excused**. An excused absence represents an accepted exception rather than a warning or failure, so **Strong Cyan** is used instead of amber or red.

---

### Colour Usage Principles

Across the application, colour follows several consistent principles:

- **Colour reinforces meaning rather than replacing it.** Statuses and assessment information are always accompanied by text, labels, icons or other contextual information.
- **Brand colours are used selectively.** Brighter cyan, aqua and turquoise tones are reserved for emphasis so that they retain their visual impact.
- **Assessment colours remain persistent.** Each language skill retains the same colour wherever it appears.
- **Semantic colours reflect meaning.** Green communicates positive states, amber communicates attention, red communicates negative states and cool colours communicate neutral or operational information.
- **Neutral colours control hierarchy.** Blue Slate and Cool Steel allow secondary and historical information to remain visible without competing with active content.
- **Palette expansion is avoided where possible.** Existing brand colours are reused for semantic purposes when their established visual character appropriately supports the intended meaning.

Together, these principles create a colour system that is **consistent, scalable and semantically meaningful**, while preserving the restrained boutique/corporate visual identity of English Grows.

## Responsive Design

The platform follows a responsive interface strategy intended to support **desktop, tablet and mobile use**.

Desktop layouts make greater use of:

- multi-column grids;
- persistent side navigation;
- wider data tables;
- horizontally distributed dashboard metrics.

At smaller viewport sizes, layouts progressively collapse into simpler structures.

Key responsive behaviours include:

- grid layouts reducing to a single column;
- navigation converting to a mobile sidebar controlled through a burger button;
- a backdrop appearing behind the open mobile navigation;
- horizontally scrollable wrappers for information-heavy tables;
- adaptive page padding;
- flexible typography;
- cards expanding to the available width;
- charts constrained to their parent container.

The main content area uses flexible sizing together with `min-width: 0` where necessary so that charts, tables and long content cannot force the page outside its intended layout.

Responsive behaviour is therefore considered part of the component architecture rather than being added as a separate mobile-only interface.

---

## Data Visualisation

Data visualisation is used selectively where graphical representation communicates progress more effectively than isolated numerical values.

The principal visualisations currently include:

- course completion indicators;
- attendance percentages;
- skill assessment scores;
- historical skill progress graphs.

The surrounding interface follows the core **English Grows brand palette**:

```text
Oxford Blue      → #0B355F
Stormy Teal      → #006B7D
Strong Cyan      → #07C0C7
Electric Aqua    → #5FF5FC
Icy Aqua         → #C7FFF9
Turquoise        → #5FF0DF
Azure Mist       → #EDF9F7
Blue Slate       → #4F6870
Cool Steel       → #7A949B
```

Skill-specific data visualisation uses the dedicated assessment palette:

```text
Speaking        → #F5BE58
Listening       → #4E2496
Reading         → #E1752D
Writing         → #0EA5B7
```

This separation ensures that brand colours retain their interface function while skill colours communicate a specific pedagogical meaning.

Progress charts use historical assessment snapshots rather than current assessment values. This ensures that each data point represents the student's assessment at a particular stage of the course instead of repeatedly displaying the latest score.

Each language skill retains the same colour throughout the system, meaning that skill progress graphs remain visually consistent with assessment cards and other skill-related components.

Charts use restrained styling and smoothed data lines to communicate progression without overwhelming the surrounding interface.

Percentage-based indicators are used where the underlying data represents an actual proportion, such as:

- attendance;
- course completion.

Assessment ability, however, is displayed using a `/10` score rather than a percentage because the value represents a pedagogical evaluation rather than completion of a quantity.

This distinction prevents visually similar metrics from implying the same meaning.

The overall visualisation strategy therefore follows three principles:

1. **Brand colours provide interface structure and identity.**
2. **Assessment colours identify pedagogical data consistently.**
3. **Semantic colours communicate application state and operational meaning.**

This approach allows data visualisation to remain consistent with the wider English Grows design system while ensuring that colour always carries a clear and predictable purpose.


