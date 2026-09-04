# Design Choices

---

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

---

The **English Grows** interface uses a carefully defined colour system centred around navy, tropical teal, cyan, turquoise and aquamarine tones, supported by cool neutrals and a small set of purpose-specific semantic colours.

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

---

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
│   │   └── #0B355F  Oxford Blue
│   │
│   ├── BRAND / INTERACTIVE ACCENTS
│   │   ├── #16AFB5  Tropical Teal
│   │   ├── #07C0C7  Strong Cyan
│   │   └── #5FF0DF  Turquoise
│   │
│   ├── LIGHT / CONTEXTUAL SURFACES
│   │   ├── #B5F9DE  Aquamarine
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
    │   ├── #16AFB5  Confirmed
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

---

The core **English Grows** interface palette consists of ten colours:

<img width="1600" height="1200" alt="Color Palette_EnglishGrows" src="https://github.com/user-attachments/assets/a92e4372-16ec-4776-96e2-314406eaeed6" />

| Colour | Preview | Hex | Primary UI Role |
| :--- | :---: | :---: | :--- |
| **Oxford Blue** | ![#0B355F](https://img.shields.io/badge/Oxford_Blue-0B355F?style=flat&labelColor=0B355F&color=0B355F) | `#0B355F` | Primary brand colour, navigation, headings and high-emphasis elements |
| **Tropical Teal** | ![#16AFB5](https://img.shields.io/badge/Tropical_Teal-16AFB5?style=flat&labelColor=16AFB5&color=16AFB5) | `#16AFB5` | Principal mid-tone (`rgb(22, 175, 181)`), data / completion fills and restrained interactive emphasis on light surfaces |
| **Strong Cyan** | ![#07C0C7](https://img.shields.io/badge/Strong_Cyan-07C0C7?style=flat&labelColor=07C0C7&color=07C0C7) | `#07C0C7` | Primary interactive colour and distinctive brand accent |
| **Turquoise** | ![#5FF0DF](https://img.shields.io/badge/Turquoise-5FF0DF?style=flat&labelColor=5FF0DF&color=5FF0DF) | `#5FF0DF` | Secondary accent, indicators and selected interface elements |
| **Aquamarine** | ![#B5F9DE](https://img.shields.io/badge/Aquamarine-B5F9DE?style=flat&labelColor=B5F9DE&color=B5F9DE) | `#B5F9DE` | Restricted contextual / identity surface for course headers and static featured information; typically used as a very soft tint rather than as a general accent |
| **Icy Aqua** | ![#C7FFF9](https://img.shields.io/badge/Icy_Aqua-C7FFF9?style=flat&labelColor=C7FFF9&color=C7FFF9) | `#C7FFF9` | Soft highlighted backgrounds and subtle accent surfaces |
| **Azure Mist** | ![#EDF9F7](https://img.shields.io/badge/Azure_Mist-EDF9F7?style=flat&labelColor=EDF9F7&color=EDF9F7) | `#EDF9F7` | Light backgrounds, surfaces and subtle visual separation |
| **White Smoke** | ![#F5F5F5](https://img.shields.io/badge/White_Smoke-F5F5F5?style=flat&labelColor=F5F5F5&color=F5F5F5) | `#F5F5F5` | Neutral data surfaces and card backgrounds; occasionally used as light text on dark surfaces |
| **Blue Slate** | ![#4F6870](https://img.shields.io/badge/Blue_Slate-4F6870?style=flat&labelColor=4F6870&color=4F6870) | `#4F6870` | Dark neutral, secondary text and subdued interface elements |
| **Cool Steel** | ![#7A949B](https://img.shields.io/badge/Cool_Steel-7A949B?style=flat&labelColor=7A949B&color=7A949B) | `#7A949B` | Secondary neutral, supporting text, borders and low-emphasis elements |

---

#### Brand Palette Rationale

---

The core palette is organised into four complementary functional families:

```text
DARK / CORPORATE
#0B355F  Oxford Blue

BRAND / INTERACTIVE ACCENTS
#16AFB5  Tropical Teal
    │
    ├── #07C0C7  Strong Cyan
    └── #5FF0DF  Turquoise

LIGHT / CONTEXTUAL SURFACES
#B5F9DE  Aquamarine
    │
    ├── #C7FFF9  Icy Aqua
    ├── #EDF9F7  Azure Mist
    └── #F5F5F5  White Smoke

COOL NEUTRALS
#4F6870  Blue Slate
    │
    └── #7A949B  Cool Steel
```

- **Oxford Blue** provides the strongest corporate anchor and is used where visual authority and high contrast are required.
- **Tropical Teal** (`#16AFB5`, `rgb(22, 175, 181)`) provides the principal mid-tone between Oxford Blue and the lighter aqua / turquoise family. It is strong enough for data fills, completion indicators and selected emphasis against light surfaces while remaining more restrained than the brightest accents.
- **Strong Cyan** and **Turquoise** provide brighter English Grows accents and are used selectively for interaction, emphasis and active interface elements.
- **Aquamarine** (`#B5F9DE`) is intentionally restricted to **soft contextual / identity surfaces**, particularly course-identity or page-header areas and static featured-information emphasis. It is typically used as a very light tint such as `rgba(181, 249, 222, 0.15)`, rather than for buttons, KPI cards, borders, icons, progress rings, hover states or other general interactive UI.
- **Icy Aqua** and **Azure Mist** provide subtle tinted surfaces and visual separation without relying exclusively on pure white.
- **White Smoke** provides a clean neutral surface for cards and data-heavy areas while remaining softer than pure white.
- **Blue Slate** and **Cool Steel** provide a controlled neutral hierarchy for secondary information, borders and lower-emphasis elements.

This hierarchy allows brighter colours to remain distinctive because they are used selectively against a restrained corporate and neutral foundation.

---

### CEFR Level Colours

---

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

---

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

---

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
| **Confirmed** | ![#16AFB5](https://img.shields.io/badge/Confirmed-16AFB5?style=flat&labelColor=16AFB5&color=16AFB5) | `#16AFB5` | Tropical Teal represents an established course that has been confirmed but is not yet active |
| **Active** | ![#5FF0DF](https://img.shields.io/badge/Active-5FF0DF?style=flat&labelColor=5FF0DF&color=5FF0DF) | `#5FF0DF` | Brighter Turquoise gives currently running courses greater visual immediacy |
| **Paused** | ![#FFB000](https://img.shields.io/badge/Paused-FFB000?style=flat&labelColor=FFB000&color=FFB000) | `#FFB000` | Amber communicates temporary interruption and a state requiring attention |
| **Cancelled** | ![#EF4444](https://img.shields.io/badge/Cancelled-EF4444?style=flat&labelColor=EF4444&color=EF4444) | `#EF4444` | Red communicates termination and a negative operational state |
| **Completed** | ![#4F6870](https://img.shields.io/badge/Completed-4F6870?style=flat&labelColor=4F6870&color=4F6870) | `#4F6870` | Blue Slate communicates a closed, historical state without implying an error |

The normal course lifecycle follows a deliberate visual progression:

```text
CONFIRMED              ACTIVE                 COMPLETED
#16AFB5                #5FF0DF               #4F6870
Tropical Teal      →     Turquoise       →     Blue Slate
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

---

Across the application, colour follows several consistent principles:

- **Colour reinforces meaning rather than replacing it.** Statuses and assessment information are always accompanied by text, labels, icons or other contextual information.
- **Brand colours are used selectively.** Tropical Teal, Strong Cyan and Turquoise are reserved for purposeful emphasis so that they retain their visual impact.
- **Aquamarine remains contextual rather than interactive.** It is reserved for soft course-identity / page-header surfaces and static featured-information emphasis, not for buttons, KPI cards, borders, icons, progress rings or hover states.
- **Assessment colours remain persistent.** Each language skill retains the same colour wherever it appears.
- **Semantic colours reflect meaning.** Green communicates positive states, amber communicates attention, red communicates negative states and cool colours communicate neutral or operational information.
- **Neutral colours control hierarchy.** Blue Slate and Cool Steel allow secondary and historical information to remain visible without competing with active content.
- **Palette expansion is avoided where possible.** Existing brand colours are reused for semantic purposes when their established visual character appropriately supports the intended meaning.

Together, these principles create a colour system that is **consistent, scalable and semantically meaningful**, while preserving the restrained boutique/corporate visual identity of English Grows.

---

## Responsive Design

---

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

---

Data visualisation is used selectively throughout **English Grows** where graphical representation improves the interpretation of progress, performance or application data more effectively than isolated numerical values.

The principal visualisations currently include:

- course completion indicators;
- attendance rates and attendance summaries;
- skill assessment scores;
- historical skill progress graphs;
- CEFR proficiency level indicators;
- status and lifecycle indicators.

Visualisations follow the wider English Grows design system and maintain a clear distinction between **interface identity, pedagogical data, proficiency classification and operational status**.

### Visualisation Colour Architecture

Colour used within data visualisation follows the same four functional layers established by the wider colour system:

```text
DATA VISUALISATION
│
├── BRAND / INTERFACE COLOURS
│   └── Structure, hierarchy and supporting visual elements
│
├── ASSESSMENT / DATA COLOURS
│   └── Persistent identification of language skills
│
├── CEFR LEVEL COLOURS
│   └── Persistent identification of proficiency levels
│
└── SEMANTIC / STATUS COLOURS
    └── Operational states, outcomes and exceptions
```

This separation ensures that colour has a **predictable purpose** rather than being applied decoratively or assigned independently to individual components.

---

### Brand Colours in Visualisation

The surrounding interface and supporting elements of data visualisations follow the core **English Grows brand palette**:

```text
Oxford Blue      → #0B355F
Tropical Teal    → #16AFB5
Strong Cyan      → #07C0C7
Turquoise        → #5FF0DF
Aquamarine       → #B5F9DE  (contextual surfaces only)
Icy Aqua         → #C7FFF9
Azure Mist       → #EDF9F7
White Smoke      → #F5F5F5
Blue Slate       → #4F6870
Cool Steel       → #7A949B
```

These colours provide visual structure through elements such as:

- chart containers and card surfaces;
- headings and labels;
- progress indicators;
- supporting lines and borders;
- active interface elements;
- secondary and de-emphasised information.

Brighter accent colours are used selectively so that they retain visual prominence, while the lighter and neutral tones provide sufficient space for data to remain the primary focus. **Aquamarine is the exception to general chart-accent use:** it remains a contextual surface colour and is not used as a data series, progress-ring fill or interactive chart state.

---

### Skill Assessment Visualisation

Skill-specific data visualisation uses the dedicated **Assessment / Data palette**:

```text
Speaking         → #F5BE58  Sunflower Gold
Listening        → #4E2496  Indigo Velvet
Reading          → #E1752D  Chocolate
Writing          → #0EA5B7  Pacific Blue
```

Each language skill retains the same colour throughout the application.

This creates a persistent visual relationship between:

- skill assessment cards;
- subskill information;
- chart datasets;
- chart legends;
- historical progress graphs;
- other skill-specific indicators.

The user can therefore associate a colour with a particular skill regardless of the page or visualisation in which that skill appears.

These colours function as **categorical identifiers**. They do not indicate whether performance is positive or negative; they identify the pedagogical category represented by the data.

---

### Historical Skill Progress

Historical skill progress graphs use `StudentSkillTermSnapshot` records to represent assessment results at different stages of a learner's course.

Each snapshot stores a skill score at a particular assessment point, allowing progression to be visualised over time without replacing previous results.

Conceptually:

```text
ASSESSMENT HISTORY

Assessment 1        Assessment 2        Assessment 3
     │                   │                   │
     ●───────────────────●───────────────────●
     │                   │                   │
   Score               Score               Score
```

Each skill retains its dedicated assessment colour throughout the graph, allowing several skill datasets to be displayed together while remaining visually distinguishable.

Charts use restrained styling and smoothed data lines to communicate progression without overwhelming the surrounding interface.

Historical visualisation is deliberately separated from the learner's current assessment state: the current assessment describes **where the learner is now**, while snapshots provide the historical data required to show **how that assessment has developed over time**.

---

### CEFR Level Visualisation

CEFR colours provide persistent visual identification of language proficiency levels:

```text
A1  → #6EFF7F  Mint Glow
A2  → #FF954F  Tangerine Dream
B1  → #436EFD  Electric Sapphire
B2  → #7B27A5  Indigo Bloom
C1  → #DBDF2B  Lemon Lime
C2  → #902331  Burgundy
```

These colours function as **categorical identifiers**, rather than as indicators of performance, success or application status.

For example, the green used for **A1** does not imply a successful state, and the Burgundy used for **C2** does not represent an error or warning. Each colour simply provides a persistent visual identity for its corresponding proficiency level.

CEFR colours are always accompanied by their textual level labels to ensure that proficiency information never depends on colour alone.

---

### Semantic and Status Visualisation

Semantic colours are used when the visualisation represents an **application state, outcome or exception**, rather than a pedagogical category.

Examples include:

```text
LEARNER
Active           → #38DF9C
Inactive         → #7A949B

COURSE
Confirmed        → #16AFB5
Active           → #5FF0DF
Paused           → #FFB000
Cancelled        → #EF4444
Completed        → #4F6870

ATTENDANCE
Attended         → #38DF9C
Excused          → #07C0C7
Missed           → #FF5A5A
```

The semantic system follows a consistent visual rationale:

- **green** communicates a positive or successfully fulfilled state;
- **cyan, teal and turquoise** communicate informational or operational states;
- **amber** communicates interruption or attention;
- **red** communicates negative outcomes or termination;
- **blue-grey neutrals** communicate inactive, completed, historical or de-emphasised states.

This prevents semantic colours from being confused with categorical colours used for skills or CEFR proficiency levels.

---

### Proportional Indicators

Percentage-based visualisations are used only where the underlying value represents a genuine proportion.

Examples include:

- attendance rates;
- course completion;
- completed versus remaining classes.

Course completion can therefore be represented through progress bars or completion rings because the value describes progress towards a finite total.

Attendance percentages similarly represent a proportion derived from completed attendance records.

Assessment ability, however, is displayed using a **`/10` score rather than a percentage** because the value represents a pedagogical evaluation rather than completion of a quantity.

This distinction prevents visually similar metrics from implying the same meaning.

```text
COURSE COMPLETION     → Percentage / proportion
ATTENDANCE RATE       → Percentage / proportion
SKILL ASSESSMENT      → Score /10
CEFR LEVEL            → Categorical classification
STATUS                → Semantic state
```

---

### Visualisation Principles

The overall data visualisation strategy follows several consistent principles:

1. **Brand colours provide interface structure and identity.**
2. **Assessment colours identify language skills consistently.**
3. **CEFR colours identify proficiency categories consistently.**
4. **Semantic colours communicate application state and operational meaning.**
5. **Percentages are reserved for genuinely proportional data.**
6. **Assessment scores use a `/10` scale to distinguish evaluation from completion.**
7. **Historical data is preserved and visualised separately from current assessment state.**
8. **Colour reinforces information but never acts as its sole means of communication.**

This approach allows data visualisation to remain consistent with the wider **English Grows design system** while ensuring that each visual element communicates a clear and predictable meaning.