document.addEventListener('DOMContentLoaded', function () {

    const calendarEl = document.getElementById('calendar');

    if (!calendarEl) {
        return;
    }

    const userRole =
        calendarEl.dataset.role;

    const eventsUrl =
        calendarEl.dataset.eventsUrl;


    /*
        ============================================================
        TRANSLATIONS
        ============================================================
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
        LANGUAGE HELPERS
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

        const localeMap = {
            en: 'en-GB',
            es: 'es-ES',
            ca: 'ca-ES',
            fr: 'fr-FR'
        };

        return (
            localeMap[getCurrentLanguage()]
            || 'en-GB'
        );
    }


    function getFullCalendarLocale() {

        const localeMap = {
            en: 'en-gb',
            es: 'es',
            ca: 'ca',
            fr: 'fr'
        };

        return (
            localeMap[getCurrentLanguage()]
            || 'en-gb'
        );
    }


    function capitalizeFirstLetter(text) {

        if (!text) {
            return '';
        }

        return (
            text.charAt(0).toUpperCase()
            + text.slice(1)
        );
    }


    /*
        ============================================================
        WEEKDAY LABELS
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

        return dayNames[
            getCurrentLanguage()
        ][date.getDay()];
    }


    /*
        ============================================================
        ORDINALS
        ============================================================
    */

    function getOrdinalSuffix(day) {

        if (
            day > 3
            && day < 21
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
        DAY VIEW HEADER
        ============================================================
    */

    function formatDayGridHeader(date) {

        const language =
            getCurrentLanguage();

        const day =
            date.getDate();


        if (language === 'en') {

            const weekday =
                date.toLocaleDateString(
                    'en-GB',
                    {
                        weekday: 'long'
                    }
                );

            return {
                html:
                    `${weekday} ${day}<sup>${getOrdinalSuffix(day)}</sup>`
            };
        }


        const weekday =
            date.toLocaleDateString(
                getDateLocale(),
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
        EVENT ACTION
        ============================================================

        Single source of truth for:

        - Month List button
        - Modal button

        Rules:

        COMPANY ADMIN
            Always -> Group details

        EVERYONE ELSE
            meeting_link exists
                -> Join class

            otherwise
                -> Group details
        ============================================================
    */

    function getEventAction(event) {

        const labels =
            getLabels();

        const props =
            event.extendedProps || {};

        const meetingLink =
            props.meeting_link || '';

        const groupDetailsUrl =
            props.group_details_url || '';


        /*
            ============================================================
            COMPANY ADMIN
            ============================================================

            Company Admin always gets Group Details,
            even when the class has already passed.
        */

        if (
            userRole ===
            'company_admin'
        ) {

            if (!groupDetailsUrl) {
                return null;
            }

            return {
                label:
                    labels.groupDetails,

                href:
                    groupDetailsUrl,

                target:
                    '_self',

                rel:
                    null
            };
        }


        /*
            ============================================================
            PAST SESSION
            ============================================================

            Teacher / Employee / Individual:

            If the class has already finished,
            do not show any action button.
        */

        if (
            event.end
            &&
            event.end < new Date()
        ) {
            return null;
        }


        /*
            ============================================================
            FUTURE / CURRENT SESSION
            ============================================================

            All non-admin roles:

            meeting link exists
                -> Join class

            otherwise
                -> Group details
        */

        if (meetingLink) {

            return {
                label:
                    labels.joinClass,

                href:
                    meetingLink,

                target:
                    '_blank',

                rel:
                    'noopener noreferrer'
            };
        }


        if (groupDetailsUrl) {

            return {
                label:
                    labels.groupDetails,

                href:
                    groupDetailsUrl,

                target:
                    '_self',

                rel:
                    null
            };
        }


        return null;
    }

    /*
        ============================================================
        CREATE ACTION BUTTON
        ============================================================
    */

    function createEventActionButton(event) {

        const action =
            getEventAction(event);

        if (!action) {
            return null;
        }


        const button =
            document.createElement('a');

        button.href =
            action.href;

        button.target =
            action.target;

        button.textContent =
            action.label;

        button.classList.add(
            'calendar-join-btn'
        );


        if (action.rel) {

            button.rel =
                action.rel;
        }


        button.addEventListener(
            'click',
            function (event) {

                event.stopPropagation();
            }
        );


        return button;
    }


    /*
        ============================================================
        APPLY ACTION TO MODAL BUTTON
        ============================================================
    */

    function applyEventActionToButton(
        button,
        event
    ) {

        const action =
            getEventAction(event);


        /*
            NO ACTION AVAILABLE
        */

        if (!action) {

            button.classList.add(
                'd-none'
            );

            button.removeAttribute(
                'href'
            );

            button.removeAttribute(
                'target'
            );

            button.removeAttribute(
                'rel'
            );

            return;
        }


        /*
            ACTION AVAILABLE
        */

        button.textContent =
            action.label;

        button.href =
            action.href;

        button.target =
            action.target;


        if (action.rel) {

            button.rel =
                action.rel;

        } else {

            button.removeAttribute(
                'rel'
            );
        }


        button.classList.remove(
            'd-none'
        );
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
                left:
                    'prev',

                center:
                    'title',

                right:
                    'next todayOnly,timeGridWeek,dayGridMonth,listMonth'
            };
        }


        return {
            left:
                'prev',

            center:
                'title',

            right:
                'next todayOnly,timeGridWeek,dayGridMonth,listMonth,multiMonthYear'
        };
    }


    /*
        ============================================================
        TOOLBAR BUTTONS
        ============================================================
    */

    function replaceButtonText(
        selector,
        text
    ) {

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


        function getCapitalizedMonth(date) {

            const month =
                date.toLocaleString(
                    locale,
                    {
                        month:
                            'long'
                    }
                );

            return (
                month.charAt(0).toUpperCase()
                + month.slice(1)
            );
        }


        /*
            DAY
        */

        if (
            viewType ===
            'timeGridDay'
        ) {

            const currentDate =
                calendar.getDate();

            const day =
                currentDate.getDate();

            const month =
                getCapitalizedMonth(
                    currentDate
                );


            if (
                language ===
                'en'
            ) {

                titleEl.innerHTML =
                    `${day}<sup>${getOrdinalSuffix(day)}</sup> ${month}`;

            } else {

                titleEl.replaceChildren(
                    document.createTextNode(
                        `${day} ${month}`
                    )
                );
            }


            return;
        }


        /*
            WEEK
        */

        if (
            viewType ===
            'timeGridWeek'
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
                FullCalendar end date is exclusive.
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
                start.getMonth()
                === end.getMonth();

            const sameYear =
                start.getFullYear()
                === end.getFullYear();


            if (
                language ===
                'en'
            ) {

                if (
                    sameMonth
                    && sameYear
                ) {

                    titleEl.innerHTML =
                        `${startDay}<sup>${getOrdinalSuffix(startDay)}</sup> - `
                        + `${endDay}<sup>${getOrdinalSuffix(endDay)}</sup> ${endMonth}`;

                } else {

                    titleEl.innerHTML =
                        `${startDay}<sup>${getOrdinalSuffix(startDay)}</sup> ${startMonth} - `
                        + `${endDay}<sup>${getOrdinalSuffix(endDay)}</sup> ${endMonth}`;
                }


                return;
            }


            let titleText;


            if (
                sameMonth
                && sameYear
            ) {

                titleText =
                    `${startDay} - ${endDay} ${endMonth}`;

            } else {

                titleText =
                    `${startDay} ${startMonth} - ${endDay} ${endMonth}`;
            }


            titleEl.replaceChildren(
                document.createTextNode(
                    titleText
                )
            );


            return;
        }


        /*
            MONTH / MONTH LIST
        */

        if (
            viewType ===
            'dayGridMonth'
            ||
            viewType ===
            'listMonth'
        ) {

            const currentDate =
                calendar.getDate();

            const month =
                getCapitalizedMonth(
                    currentDate
                );

            const year =
                String(
                    currentDate.getFullYear()
                ).slice(-2);


            titleEl.replaceChildren(
                document.createTextNode(
                    `${month} '${year}`
                )
            );


            return;
        }


        /*
            YEAR
        */

        if (
            viewType ===
            'multiMonthYear'
        ) {

            titleEl.replaceChildren(
                document.createTextNode(
                    String(
                        calendar
                            .getDate()
                            .getFullYear()
                    )
                )
            );
        }
    }


    /*
        ============================================================
        SYNC UI
        ============================================================
    */

    function syncCalendarUI(info) {

        window.requestAnimationFrame(
            function () {

                syncToolbarButtons();

                updateCalendarTitle(
                    info
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

        return {

            todayOnly: {

                text:
                    getLabels().today,


                click:
                    function () {

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
                    HEADERS
                    =================================================
                */

                dayHeaderContent:
                    function (arg) {

                        const weekday =
                            getShortWeekday(
                                arg.date
                            );

                        const day =
                            arg.date.getDate();


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
                            WEEK VIEW
                        */

                        if (
                            arg.view.type ===
                            'timeGridWeek'
                        ) {

                            return {
                                html:
                                    `
                                    <span class="calendar-week-day-label">
                                        ${weekday}
                                        <span class="calendar-week-day-number">
                                            ${day}
                                        </span>
                                    </span>
                                    `
                            };
                        }


                        /*
                            MONTH LIST
                        */

                        if (
                            arg.view.type ===
                            'listMonth'
                        ) {

                            const language =
                                getCurrentLanguage();


                            if (
                                language ===
                                'en'
                            ) {

                                const month =
                                    arg.date.toLocaleString(
                                        'en-GB',
                                        {
                                            month:
                                                'short'
                                        }
                                    );


                                return {

                                    html:
                                        `
                                        <span class="calendar-list-date-label">
                                            ${weekday}. ${day}<sup>${getOrdinalSuffix(day)}</sup> ${month}.
                                        </span>
                                        `
                                };
                            }


                            const month =
                                arg.date.toLocaleString(
                                    getDateLocale(),
                                    {
                                        month:
                                            'short'
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


                        return weekday;
                    },


                /*
                    =================================================
                    MONTH DATE CLICK
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
                                Same button logic as modal.
                            */

                            const actionButton =
                                createEventActionButton(
                                    arg.event
                                );


                            if (actionButton) {

                                row.appendChild(
                                    actionButton
                                );
                            }


                            return {
                                domNodes:
                                    [row]
                            };
                        }


                        /*
                            WEEK / DAY
                        */

                        if (
                            arg.view.type ===
                            'timeGridWeek'
                            ||
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

                        const event =
                            info.event;

                        const start =
                            event.start;

                        const end =
                            event.end;

                        const props =
                            event.extendedProps || {};


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
                            !modalTitle
                            ||
                            !modalTime
                            ||
                            !modalCourse
                            ||
                            !modalClassNumber
                            ||
                            !modalJoinBtn
                        ) {
                            return;
                        }


                        /*
                            TITLE
                        */

                        modalTitle.textContent =
                            event.title;


                        /*
                            DATE / TIME
                        */

                        const startText =
                            start

                                ? start.toLocaleString(
                                    getDateLocale(),
                                    {
                                        weekday:
                                            'long',

                                        day:
                                            'numeric',

                                        month:
                                            'long',

                                        hour:
                                            '2-digit',

                                        minute:
                                            '2-digit'
                                    }
                                )

                                : '';


                        const endText =
                            end

                                ? end.toLocaleTimeString(
                                    getDateLocale(),
                                    {
                                        hour:
                                            '2-digit',

                                        minute:
                                            '2-digit'
                                    }
                                )

                                : '';


                        modalTime.textContent =
                            endText

                                ? `${startText} - ${endText}`

                                : startText;


                        /*
                            COURSE
                        */

                        modalCourse.textContent =
                            props.course
                            ||
                            labels.courseUnavailable;


                        /*
                            CLASS NUMBER
                        */

                        modalClassNumber.textContent =
                            props.class_number

                                ? `${labels.lesson} ${props.class_number}`

                                : '';


                        /*
                            ACTION BUTTON

                            Uses exactly the same logic as Month List.
                        */

                        applyEventActionToButton(
                            modalJoinBtn,
                            event
                        );


                        $('#classSessionModal')
                            .modal('show');
                    },


                /*
                    =================================================
                    RESPONSIVE
                    =================================================
                */

                windowResize:
                    function () {

                        const newMobileState =
                            isMobileCalendar();


                        if (
                            newMobileState ===
                            calendarIsMobile
                        ) {
                            return;
                        }


                        calendarIsMobile =
                            newMobileState;


                        calendar.setOption(
                            'headerToolbar',
                            getHeaderToolbar()
                        );


                        window.requestAnimationFrame(
                            function () {

                                syncToolbarButtons();
                            }
                        );
                    }
            }
        );


    /*
        ============================================================
        LANGUAGE CHANGE
        ============================================================
    */

    function applyCalendarLanguage() {

        calendar.setOption(
            'locale',
            getFullCalendarLocale()
        );


        calendar.setOption(
            'buttonText',
            getButtonText()
        );


        calendar.rerenderEvents();


        const currentViewType =
            calendar.view.type;

        const currentDate =
            calendar.getDate();


        calendar.changeView(
            currentViewType,
            currentDate
        );


        window.requestAnimationFrame(
            function () {

                syncToolbarButtons();

                updateCalendarTitle({
                    view:
                        calendar.view,

                    start:
                        calendar.view.activeStart,

                    end:
                        calendar.view.activeEnd
                });
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
        LANGUAGE WATCH
        ============================================================
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
            attributes:
                true,

            attributeFilter:
                ['lang']
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