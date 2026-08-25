document.addEventListener('DOMContentLoaded', function () {

    const calendarEl = document.getElementById('calendar');

    if (!calendarEl) {
        return;
    }

    const userRole = calendarEl.dataset.role;
    const eventsUrl = calendarEl.dataset.eventsUrl;

    function capitalizeFirstLetter(text) {

        if (!text) {
            return '';
        }

        return (
            text.charAt(0).toUpperCase() +
            text.slice(1)
        );
    }
    /*
        ============================================================
        CONTROLLED CALENDAR TRANSLATIONS
        ============================================================

        IMPORTANT:

        The calendar HTML should remain:

            class="my-calendar notranslate"
            translate="no"

        Google / Chrome translates the rest of the page.

        FullCalendar translations are controlled entirely here.
    */

    const calendarTranslations = {

        en: {
            today: 'Today',
            week: 'Week',
            month: 'Month',
            monthList: 'Month List',
            year: 'Year',

            joinClass: 'Join class',
            groupDetails: 'Group details',
            lesson: 'Lesson',

            courseUnavailable:
                'Course information unavailable'
        },

        es: {
            today: 'Hoy',
            week: 'Semana',
            month: 'Mes',
            monthList: 'Lista Mensual',
            year: 'Año',

            joinClass: 'Conectarse',
            groupDetails: 'Detalles',
            lesson: 'Clase',

            courseUnavailable:
                'Información del curso no disponible'
        },

        ca: {
            today: 'Avui',
            week: 'Setmana',
            month: 'Mes',
            monthList: 'Llista mensual',
            year: 'Any',

            joinClass: 'Conectar-se',
            groupDetails: 'Detalls',
            lesson: 'Classe',

            courseUnavailable:
                'Informació del curs no disponible'
        },

        fr: {
            today: "Aujourd'hui",
            week: 'Semaine',
            month: 'Mois',
            monthList: 'Liste du mois',
            year: 'Année',

            joinClass: 'Se connecter',
            groupDetails: 'Détails du groupe',
            lesson: 'Cours',

            courseUnavailable:
                'Informations du cours indisponibles'
        }
    };


    /*
        ============================================================
        LANGUAGE
        ============================================================
    */

    function getCurrentLanguage() {

        const locale =
            document.documentElement.lang || 'en';

        const language =
            locale
                .split('-')[0]
                .toLowerCase();

        return calendarTranslations[language]
            ? language
            : 'en';
    }


    function getLabels() {

        return calendarTranslations[
            getCurrentLanguage()
        ];
    }


    function getDateLocale() {

        const language =
            getCurrentLanguage();

        const localeMap = {
            en: 'en-GB',
            es: 'es-ES',
            ca: 'ca-ES',
            fr: 'fr-FR'
        };

        return localeMap[language] || 'en-GB';
    }


    function getFullCalendarLocale() {

        const language =
            getCurrentLanguage();

        const localeMap = {
            en: 'en-gb',
            es: 'es',
            ca: 'ca',
            fr: 'fr'
        };

        return localeMap[language] || 'en-gb';
    }


    /*
        ============================================================
        WEEKDAY ABBREVIATIONS
        ============================================================
    */

    const dayNames = {

        en: [
            'Sun',
            'Mon',
            'Tue',
            'Wed',
            'Thu',
            'Fri',
            'Sat'
        ],

        es: [
            'DO',
            'LU',
            'MA',
            'MI',
            'JU',
            'VI',
            'SA'
        ],

        ca: [
            'Diu',
            'Dil',
            'Dim',
            'Dic',
            'Dij',
            'Div',
            'Dis'
        ],

        fr: [
            'Di',
            'Lu',
            'Ma',
            'Me',
            'Je',
            'Ve',
            'Sa'
        ]
    };


    function getShortWeekday(date) {

        const language =
            getCurrentLanguage();

        return dayNames[language][
            date.getDay()
        ];
    }


    /*
        ============================================================
        RESPONSIVE TOOLBAR
        ============================================================
    */

    function isMobileCalendar() {

        return window.innerWidth <= 768;
    }


    let calendarIsMobile =
        isMobileCalendar();


    function getHeaderToolbar() {

        if (isMobileCalendar()) {

            return {
                left: 'prev',
                center: 'title',
                right:
                    'next todayOnly,timeGridWeek,dayGridMonth,listMonth'
            };
        }

        return {
            left: 'prev',
            center: 'title',
            right:
                'next todayOnly,timeGridWeek,dayGridMonth,listMonth,multiMonthYear'
        };
    }


    /*
        ============================================================
        ORDINAL SUFFIX
        ============================================================
    */

    function getOrdinalSuffix(day) {

        if (
            day > 3 &&
            day < 21
        ) {
            return 'th';
        }


        switch (day % 10) {

            case 1:
                return 'st';

            case 2:
                return 'nd';

            case 3:
                return 'rd';

            default:
                return 'th';
        }
    }


    /*
        ============================================================
        DAY TITLE
        ============================================================
    */

    function buildDayTitle(date) {

        const language =
            getCurrentLanguage();

        const day =
            date.getDate();

        const year =
            String(
                date.getFullYear()
            ).slice(-2);


        /*
            ENGLISH

            25th Aug. '26
        */

        if (language === 'en') {

            const suffix =
                getOrdinalSuffix(day);

            const month =
                date.toLocaleString(
                    'en-GB',
                    {
                        month: 'short'
                    }
                );


            const fragment =
                document.createDocumentFragment();


            fragment.appendChild(
                document.createTextNode(
                    String(day)
                )
            );


            const sup =
                document.createElement('sup');

            sup.textContent =
                suffix;

            fragment.appendChild(
                sup
            );


            fragment.appendChild(
                document.createTextNode(
                    ` ${month}. '${year}`
                )
            );


            return fragment;
        }


        /*
            SPANISH / CATALAN / FRENCH
        */

        const month =
            date.toLocaleString(
                getDateLocale(),
                {
                    month: 'short'
                }
            );


        return document.createTextNode(
            `${day} ${month} '${year}`
        );
    }


    /*
        ============================================================
        DAY GRID HEADER
        ============================================================
    */

    function formatDayGridHeader(date) {

        const language =
            getCurrentLanguage();

        const day =
            date.getDate();


        /*
            ENGLISH

            Wednesday 8th
        */

        if (language === 'en') {

            const weekday =
                date.toLocaleDateString(
                    'en-GB',
                    {
                        weekday: 'long'
                    }
                );

            const suffix =
                getOrdinalSuffix(day);

            return {
                html:
                    `${weekday} ${day}<sup>${suffix}</sup>`
            };
        }


        /*
            SPANISH

            Miércoles 8
        */

        if (language === 'es') {

            const weekday =
                date.toLocaleDateString(
                    'es-ES',
                    {
                        weekday: 'long'
                    }
                );

            return (
                `${capitalizeFirstLetter(weekday)} ${day}`
            );
        }


        /*
            CATALAN

            Dimecres 8
        */

        if (language === 'ca') {

            const weekday =
                date.toLocaleDateString(
                    'ca-ES',
                    {
                        weekday: 'long'
                    }
                );

            return (
                `${capitalizeFirstLetter(weekday)} ${day}`
            );
        }


        /*
            FRENCH

            Mercredi 8
        */

        const weekday =
            date.toLocaleDateString(
                'fr-FR',
                {
                    weekday: 'long'
                }
            );

        return (
            `${capitalizeFirstLetter(weekday)} ${day}`
        );
    }

    /*
        ============================================================
        TOOLBAR BUTTON CONTENT
        ============================================================

        replaceChildren() is intentional.

        It removes anything previously inserted by FullCalendar
        or a browser translator before adding the correct label.

        This prevents:

            TodayToday
            HoyToday
            SemanaWeek
            etc.
    */

    function replaceButtonText(selector, text) {

        const button =
            calendarEl.querySelector(
                selector
            );

        if (!button) {
            return;
        }


        button.replaceChildren(
            document.createTextNode(
                text
            )
        );
    }


    function syncToolbarButtons() {

        const labels =
            getLabels();


        replaceButtonText(
            '.fc-todayOnly-button',
            labels.today
        );


        replaceButtonText(
            '.fc-timeGridWeek-button',
            labels.week
        );


        replaceButtonText(
            '.fc-dayGridMonth-button',
            labels.month
        );


        replaceButtonText(
            '.fc-listMonth-button',
            labels.monthList
        );


        replaceButtonText(
            '.fc-multiMonthYear-button',
            labels.year
        );
    }


    /*
        ============================================================
        TOOLBAR TITLE
        ============================================================

        The title is ALWAYS replaced completely.

        This prevents a Day title remaining attached when changing
        to Week, Month, Month List or Year.
    */

    function updateCalendarTitle(info) {

        const titleEl =
            calendarEl.querySelector(
                '.fc-toolbar-title'
            );

        if (!titleEl) {
            return;
        }

        const language =
            getCurrentLanguage();

        const locale =
            getDateLocale();

        const viewType =
            info.view.type;


        /*
            Helper:
            Capitalize month names.

            agosto -> Agosto
            august -> August
            août   -> Août
        */

        function getCapitalizedMonth(date) {

            const month =
                date.toLocaleString(
                    locale,
                    {
                        month: 'long'
                    }
                );

            return (
                month.charAt(0).toUpperCase() +
                month.slice(1)
            );
        }


        /*
            ============================================================
            DAY

            English:
                25th August

            Spanish:
                25 Agosto

            Catalan:
                25 Agost

            French:
                25 Août
            ============================================================
        */

        if (
            viewType === 'timeGridDay'
        ) {

            const day =
                info.start.getDate();

            const month =
                getCapitalizedMonth(
                    info.start
                );


            /*
                ENGLISH:
                25th August
            */

            if (
                language === 'en'
            ) {

                const suffix =
                    getOrdinalSuffix(
                        day
                    );

                titleEl.innerHTML =
                    `${day}<sup>${suffix}</sup> ${month}`;

            }


            /*
                OTHER LANGUAGES:
                25 Agosto
            */

            else {

                titleEl.replaceChildren(
                    document.createTextNode(
                        `${day} ${month}`
                    )
                );
            }


            return;
        }


        /*
            ============================================================
            WEEK

            English:
                25th - 31st August

            Spanish:
                25 - 31 Agosto

            If week crosses months:

            English:
                31st August - 6th September

            Spanish:
                31 Agosto - 6 Septiembre
            ============================================================
        */

        if (
            viewType === 'timeGridWeek'
        ) {

            const start =
                new Date(
                    info.start
                );

            const end =
                new Date(
                    info.end
                );


            /*
                FullCalendar's end is exclusive.
            */

            end.setDate(
                end.getDate() - 1
            );


            const startDay =
                start.getDate();

            const endDay =
                end.getDate();


            const startMonth =
                getCapitalizedMonth(
                    start
                );

            const endMonth =
                getCapitalizedMonth(
                    end
                );


            const sameMonth =
                start.getMonth() ===
                end.getMonth();

            const sameYear =
                start.getFullYear() ===
                end.getFullYear();


            /*
                ENGLISH
            */

            if (
                language === 'en'
            ) {

                const startSuffix =
                    getOrdinalSuffix(
                        startDay
                    );

                const endSuffix =
                    getOrdinalSuffix(
                        endDay
                    );


                /*
                    Same month:
                    25th - 31st August
                */

                if (
                    sameMonth &&
                    sameYear
                ) {

                    titleEl.innerHTML =
                        `${startDay}<sup>${startSuffix}</sup> - ` +
                        `${endDay}<sup>${endSuffix}</sup> ${endMonth}`;

                }


                /*
                    Crosses months:
                    31st August - 6th September
                */

                else {

                    titleEl.innerHTML =
                        `${startDay}<sup>${startSuffix}</sup> ${startMonth} - ` +
                        `${endDay}<sup>${endSuffix}</sup> ${endMonth}`;
                }


                return;
            }


            /*
                SPANISH / CATALAN / FRENCH
            */

            let titleText;


            /*
                Same month:
                25 - 31 Agosto
            */

            if (
                sameMonth &&
                sameYear
            ) {

                titleText =
                    `${startDay} - ${endDay} ${endMonth}`;

            }


            /*
                Crosses months:
                31 Agosto - 6 Septiembre
            */

            else {

                titleText =
                    `${startDay} ${startMonth} - ` +
                    `${endDay} ${endMonth}`;
            }


            titleEl.replaceChildren(
                document.createTextNode(
                    titleText
                )
            );


            return;
        }


        /*
            ============================================================
            MONTH

            Agosto '26
            August '26
            ============================================================
        */

        if (
            viewType === 'dayGridMonth'
        ) {

            const month =
                getCapitalizedMonth(
                    info.start
                );

            const year =
                String(
                    info.start.getFullYear()
                ).slice(-2);


            titleEl.replaceChildren(
                document.createTextNode(
                    `${month} '${year}`
                )
            );


            return;
        }


        /*
            ============================================================
            MONTH LIST

            Agosto 26
            August 26
            ============================================================
        */

        if (
            viewType === 'listMonth'
        ) {

            const month =
                getCapitalizedMonth(
                    info.start
                );

            const year =
                String(
                    info.start.getFullYear()
                ).slice(-2);


            titleEl.replaceChildren(
                document.createTextNode(
                    `${month} '${year}`
                )
            );


            return;
        }


        /*
            ============================================================
            YEAR

            2026
            ============================================================
        */

        if (
            viewType === 'multiMonthYear'
        ) {

            titleEl.replaceChildren(
                document.createTextNode(
                    String(
                        info.start.getFullYear()
                    )
                )
            );
        }
    }
    /*
        ============================================================
        SYNC CALENDAR UI
        ============================================================

        Called after every FullCalendar view/date change.
    */

    function syncCalendarUI(info) {

        /*
            Two animation frames ensure FullCalendar has finished
            rebuilding the toolbar before we replace its contents.
        */

        window.requestAnimationFrame(
            function () {

                window.requestAnimationFrame(
                    function () {

                        syncToolbarButtons();

                        updateCalendarTitle(
                            info
                        );
                    }
                );
            }
        );
    }


    /*
        ============================================================
        FULLCALENDAR
        ============================================================
    */

    let calendar;


    function getCustomButtons() {

        const labels =
            getLabels();


        return {

            todayOnly: {

                text:
                    labels.today,


                click:
                    function () {

                        /*
                            Go directly to TODAY in day view.
                        */

                        calendar.changeView(
                            'timeGridDay',
                            new Date()
                        );


                        calendar.refetchEvents();
                    }
            }
        };
    }


    function getButtonText() {

        const labels =
            getLabels();


        return {

            timeGridWeek:
                labels.week,

            dayGridMonth:
                labels.month,

            listMonth:
                labels.monthList,

            multiMonthYear:
                labels.year
        };
    }


    /*
        ============================================================
        CREATE CALENDAR
        ============================================================
    */

    calendar =
        new FullCalendar.Calendar(
            calendarEl,
            {

                initialView:
                    'timeGridWeek',


                locale:
                    getFullCalendarLocale(),


                customButtons:
                    getCustomButtons(),


                buttonText:
                    getButtonText(),


                headerToolbar:
                    getHeaderToolbar(),


                footerToolbar:
                    false,


                events:
                    eventsUrl,


                firstDay:
                    1,


                height:
                    'auto',


                weekends:
                    false,


                slotMinTime:
                    '08:00:00',


                slotMaxTime:
                    '21:00:00',


                eventTimeFormat: {

                    hour:
                        '2-digit',

                    minute:
                        '2-digit',

                    hour12:
                        false
                },


                /*
                    =================================================
                    VIEW / DATE CHANGE
                    =================================================
                */

                datesSet:
                    function (info) {

                        syncCalendarUI(
                            info
                        );
                    },


                /*
                    =================================================
                    WEEKDAY HEADERS
                    =================================================
                */

                dayHeaderContent:
                    function (arg) {

                        const weekday =
                            getShortWeekday(
                                arg.date
                            );


                        /*
                            DAY VIEW
                        */

                        if (
                            arg.view.type ===
                            'timeGridDay'
                        ) {

                            return (
                                formatDayGridHeader(
                                    arg.date
                                )
                            );
                        }


                        /*
                            MONTH LIST
                        */

                        if (
                            arg.view.type ===
                            'listMonth'
                        ) {

                            const day =
                                arg.date.getDate();


                            const language =
                                getCurrentLanguage();


                            /*
                                ENGLISH

                                Wed. 3rd Oct.
                            */

                            if (
                                language === 'en'
                            ) {

                                const suffix =
                                    getOrdinalSuffix(
                                        day
                                    );


                                const month =
                                    arg.date.toLocaleString(
                                        'en-GB',
                                        {
                                            month: 'short'
                                        }
                                    );


                                return {

                                    html:
                                        `
                                        <span class="calendar-list-date-label">
                                            ${weekday}. ${day}<sup>${suffix}</sup> ${month}.
                                        </span>
                                        `
                                };
                            }


                            /*
                                SPANISH / CATALAN / FRENCH
                            */

                            const month =
                                arg.date.toLocaleString(
                                    getDateLocale(),
                                    {
                                        month: 'short'
                                    }
                                );


                            return {

                                html:
                                    `
                                    <span class="calendar-list-date-label">
                                        ${weekday}. ${day} ${month}
                                    </span>
                                    `
                            };
                        }


                        /*
                            WEEK / MONTH / YEAR
                        */

                        return weekday;
                    },


                /*
                    =================================================
                    MONTH GRID DATE CLICK
                    =================================================
                */

                dateClick:
                    function (info) {

                        const clickableViews = [
                            'dayGridMonth',
                            'multiMonthYear'
                        ];


                        if (
                            clickableViews.includes(
                                info.view.type
                            )
                        ) {

                            calendar.changeView(
                                'timeGridDay',
                                info.dateStr
                            );
                        }
                    },


                /*
                    =================================================
                    EVENT CONTENT
                    =================================================
                */

                eventContent:
                    function (arg) {

                        const labels =
                            getLabels();


                        const meetingLink =
                            arg.event
                                .extendedProps
                                .meeting_link;


                        const groupDetailsUrl =
                            arg.event
                                .extendedProps
                                .group_details_url;


                        const title =
                            arg.event.title;


                        /*
                            MONTH LIST
                        */

                        if (
                            arg.view.type ===
                            'listMonth'
                        ) {

                            const row =
                                document.createElement(
                                    'div'
                                );


                            row.classList.add(
                                'calendar-list-event-row'
                            );


                            const titleEl =
                                document.createElement(
                                    'span'
                                );


                            titleEl.classList.add(
                                'calendar-list-event-title'
                            );


                            titleEl.textContent =
                                title;


                            row.appendChild(
                                titleEl
                            );


                            /*
                                COMPANY ADMIN
                            */

                            if (
                                userRole ===
                                'company_admin'
                            ) {

                                if (
                                    groupDetailsUrl
                                ) {

                                    const detailsBtn =
                                        document.createElement(
                                            'a'
                                        );


                                    detailsBtn.href =
                                        groupDetailsUrl;


                                    detailsBtn.target =
                                        '_self';


                                    detailsBtn.classList.add(
                                        'calendar-join-btn'
                                    );


                                    detailsBtn.textContent =
                                        labels.groupDetails;


                                    detailsBtn.addEventListener(
                                        'click',
                                        function (event) {

                                            event.stopPropagation();
                                        }
                                    );


                                    row.appendChild(
                                        detailsBtn
                                    );
                                }

                            }


                            /*
                                TEACHER / STUDENT / EMPLOYEE
                            */

                            else {

                                if (
                                    meetingLink
                                ) {

                                    const joinBtn =
                                        document.createElement(
                                            'a'
                                        );


                                    joinBtn.href =
                                        meetingLink;


                                    joinBtn.target =
                                        '_blank';


                                    joinBtn.rel =
                                        'noopener noreferrer';


                                    joinBtn.classList.add(
                                        'calendar-join-btn'
                                    );


                                    joinBtn.textContent =
                                        labels.joinClass;


                                    joinBtn.addEventListener(
                                        'click',
                                        function (event) {

                                            event.stopPropagation();
                                        }
                                    );


                                    row.appendChild(
                                        joinBtn
                                    );
                                }
                            }


                            return {

                                domNodes:
                                    [row]
                            };
                        }


                        /*
                            WEEK / DAY GRID
                        */

                        if (
                            arg.view.type ===
                                'timeGridWeek' ||

                            arg.view.type ===
                                'timeGridDay'
                        ) {

                            const wrapper =
                                document.createElement(
                                    'div'
                                );


                            wrapper.classList.add(
                                'calendar-grid-event-content'
                            );


                            const timeEl =
                                document.createElement(
                                    'div'
                                );


                            timeEl.classList.add(
                                'calendar-grid-event-time'
                            );


                            timeEl.textContent =
                                arg.timeText;


                            const titleEl =
                                document.createElement(
                                    'div'
                                );


                            titleEl.classList.add(
                                'calendar-grid-event-title'
                            );


                            titleEl.textContent =
                                title;


                            wrapper.appendChild(
                                timeEl
                            );


                            wrapper.appendChild(
                                titleEl
                            );


                            return {

                                domNodes:
                                    [wrapper]
                            };
                        }


                        /*
                            MONTH GRID
                        */

                        if (
                            arg.view.type ===
                            'dayGridMonth'
                        ) {

                            const wrapper =
                                document.createElement(
                                    'div'
                                );


                            wrapper.classList.add(
                                'calendar-month-event-content'
                            );


                            const textEl =
                                document.createElement(
                                    'span'
                                );


                            textEl.classList.add(
                                'calendar-month-event-title'
                            );


                            textEl.textContent =
                                `${arg.timeText} ${title}`;


                            wrapper.appendChild(
                                textEl
                            );


                            return {

                                domNodes:
                                    [wrapper]
                            };
                        }


                        /*
                            FALLBACK
                        */

                        const fallback =
                            document.createElement(
                                'span'
                            );


                        fallback.textContent =
                            title;


                        return {

                            domNodes:
                                [fallback]
                        };
                    },


                /*
                    =================================================
                    EVENT CLICK / MODAL
                    =================================================
                */

                eventClick:
                    function (info) {

                        info.jsEvent.preventDefault();


                        const labels =
                            getLabels();


                        const title =
                            info.event.title;


                        const start =
                            info.event.start;


                        const end =
                            info.event.end;


                        const meetingLink =
                            info.event
                                .extendedProps
                                .meeting_link;


                        const groupDetailsUrl =
                            info.event
                                .extendedProps
                                .group_details_url;


                        const course =
                            info.event
                                .extendedProps
                                .course;


                        const classNumber =
                            info.event
                                .extendedProps
                                .class_number;


                        const modalTitle =
                            document.getElementById(
                                'classSessionModalTitle'
                            );


                        const modalTime =
                            document.getElementById(
                                'classSessionModalTime'
                            );


                        const modalCourse =
                            document.getElementById(
                                'classSessionModalCourse'
                            );


                        const modalClassNumber =
                            document.getElementById(
                                'classSessionModalClassNumber'
                            );


                        const modalJoinBtn =
                            document.getElementById(
                                'classSessionModalJoinBtn'
                            );


                        if (
                            !modalTitle ||
                            !modalTime ||
                            !modalCourse ||
                            !modalClassNumber ||
                            !modalJoinBtn
                        ) {
                            return;
                        }


                        modalTitle.textContent =
                            title;


                        /*
                            Localized date + time.
                        */

                        const startText =
                            start

                                ? start.toLocaleString(
                                    getDateLocale(),
                                    {
                                        weekday: 'long',
                                        day: 'numeric',
                                        month: 'long',
                                        hour: '2-digit',
                                        minute: '2-digit'
                                    }
                                )

                                : '';


                        const endText =
                            end

                                ? end.toLocaleTimeString(
                                    getDateLocale(),
                                    {
                                        hour: '2-digit',
                                        minute: '2-digit'
                                    }
                                )

                                : '';


                        modalTime.textContent =
                            endText

                                ? `${startText} - ${endText}`

                                : startText;


                        modalCourse.textContent =
                            course ||
                            labels.courseUnavailable;


                        modalClassNumber.textContent =
                            classNumber

                                ? `${labels.lesson} ${classNumber}`

                                : '';


                        /*
                            COMPANY ADMIN
                        */

                        if (
                            userRole ===
                            'company_admin'
                        ) {

                            modalJoinBtn.textContent =
                                labels.groupDetails;


                            modalJoinBtn.target =
                                '_self';


                            modalJoinBtn.rel =
                                '';


                            if (
                                groupDetailsUrl
                            ) {

                                modalJoinBtn.href =
                                    groupDetailsUrl;


                                modalJoinBtn.classList.remove(
                                    'd-none'
                                );

                            } else {

                                modalJoinBtn.href =
                                    '#';


                                modalJoinBtn.classList.add(
                                    'd-none'
                                );
                            }

                        }


                        /*
                            TEACHER / STUDENT / EMPLOYEE
                        */

                        else {

                            modalJoinBtn.textContent =
                                labels.joinClass;


                            modalJoinBtn.target =
                                '_blank';


                            modalJoinBtn.rel =
                                'noopener noreferrer';


                            if (
                                meetingLink
                            ) {

                                modalJoinBtn.href =
                                    meetingLink;


                                modalJoinBtn.classList.remove(
                                    'd-none'
                                );

                            } else {

                                modalJoinBtn.href =
                                    '#';


                                modalJoinBtn.classList.add(
                                    'd-none'
                                );
                            }
                        }


                        $('#classSessionModal')
                            .modal('show');
                    },


                /*
                    =================================================
                    RESPONSIVE TOOLBAR
                    =================================================
                */

                windowResize:
                    function () {

                        const newMobileState =
                            isMobileCalendar();


                        if (
                            newMobileState !==
                            calendarIsMobile
                        ) {

                            calendarIsMobile =
                                newMobileState;


                            calendar.setOption(
                                'headerToolbar',
                                getHeaderToolbar()
                            );


                            /*
                                Toolbar has been rebuilt.
                                Reapply exactly one label per button.
                            */

                            window.requestAnimationFrame(
                                function () {

                                    syncToolbarButtons();
                                }
                            );
                        }
                    }
            }
        );


    /*
        ============================================================
        LANGUAGE CHANGE
        ============================================================
    */

    function applyCalendarLanguage() {

        /*
            FullCalendar locale.
        */

        calendar.setOption(
            'locale',
            getFullCalendarLocale()
        );


        /*
            Standard view buttons.
        */

        calendar.setOption(
            'buttonText',
            getButtonText()
        );


        /*
            Redraw event buttons such as Join class.
        */

        calendar.rerenderEvents();


        /*
            Redraw the CURRENT view.

            This makes dayHeaderContent execute again in the
            newly selected language.
        */

        const currentViewType =
            calendar.view.type;


        const currentDate =
            calendar.getDate();


        calendar.changeView(
            currentViewType,
            currentDate
        );


        /*
            Reassert the toolbar labels after FullCalendar finishes
            rebuilding it.

            replaceChildren() guarantees no duplicated words.
        */

        window.requestAnimationFrame(
            function () {

                window.requestAnimationFrame(
                    function () {

                        syncToolbarButtons();
                    }
                );
            }
        );
    }


    /*
        ============================================================
        RENDER
        ============================================================
    */

    calendar.render();


    /*
        ============================================================
        GOOGLE / CHROME LANGUAGE WATCH
        ============================================================

        Detects:

            <html lang="en">

        changing to:

            <html lang="es">
            <html lang="ca">
            <html lang="fr">
    */

    let lastLanguage =
        getCurrentLanguage();


    const languageObserver =
        new MutationObserver(
            function () {

                const newLanguage =
                    getCurrentLanguage();


                if (
                    newLanguage ===
                    lastLanguage
                ) {
                    return;
                }


                lastLanguage =
                    newLanguage;


                window.setTimeout(
                    function () {

                        applyCalendarLanguage();

                    },
                    50
                );
            }
        );


    languageObserver.observe(
        document.documentElement,
        {
            attributes: true,
            attributeFilter: ['lang']
        }
    );


    /*
        ============================================================
        EVENT REFRESH
        ============================================================
    */

    setInterval(
        function () {

            calendar.refetchEvents();

        },
        300000
    );

});