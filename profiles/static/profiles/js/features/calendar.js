document.addEventListener('DOMContentLoaded', function () {

    const calendarEl = document.getElementById('calendar');

    if (!calendarEl) {
        return;
    }

    const userRole = calendarEl.dataset.role;
    const eventsUrl = calendarEl.dataset.eventsUrl;


    /*
        ============================================================
        HELPERS
        ============================================================
    */

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

        Calendar HTML should remain protected from Google Translate:

            class="my-calendar notranslate"
            translate="no"

        FullCalendar translations are controlled here.
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

        replaceChildren() prevents duplicated labels such as:

            TodayToday
            HoyToday
            SemanaWeek
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
                        month: 'long'
                    }
                );

            return (
                month.charAt(0).toUpperCase() +
                month.slice(1)
            );
        }


        /*
            ========================================================
            DAY

            EN:
                25th August

            ES:
                25 Agosto
            ========================================================
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


            if (
                language === 'en'
            ) {

                const suffix =
                    getOrdinalSuffix(
                        day
                    );

                titleEl.innerHTML =
                    `${day}<sup>${suffix}</sup> ${month}`;

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
            ========================================================
            WEEK

            EN:
                25th - 31st August

            ES:
                25 - 31 Agosto
            ========================================================
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
                FullCalendar end is exclusive.
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


                if (
                    sameMonth &&
                    sameYear
                ) {

                    titleEl.innerHTML =
                        `${startDay}<sup>${startSuffix}</sup> - ` +
                        `${endDay}<sup>${endSuffix}</sup> ${endMonth}`;

                } else {

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


            if (
                sameMonth &&
                sameYear
            ) {

                titleText =
                    `${startDay} - ${endDay} ${endMonth}`;

            } else {

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
            ========================================================
            MONTH

            Agosto '26
            August '26
            ========================================================
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
            ========================================================
            MONTH LIST

            Agosto '26
            August '26
            ========================================================
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
            ========================================================
            YEAR
            ========================================================
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
    */

    function syncCalendarUI(info) {

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


                        /*
                            Specific meeting URL returned by the
                            Django calendar-events endpoint for
                            this ClassSession.
                        */

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
                            =================================================
                            MONTH LIST
                            =================================================
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

                            if (userRole === 'company_admin') {

                                if (groupDetailsUrl) {

                                    const detailsBtn =
                                        document.createElement(
                                            'a'
                                        );

                                    detailsBtn.href = groupDetailsUrl;

                                    detailsBtn.target = '_self';

                                    detailsBtn.classList.add('calendar-join-btn');

                                    detailsBtn.textContent = labels.groupDetails;

                                    detailsBtn.addEventListener('click',function (event) {event.stopPropagation();});


                                    row.appendChild(detailsBtn);
                                }

                            }

                            /*
                                TEACHER / STUDENT / EMPLOYEE

                                If this ClassSession has a meeting URL,
                                show a Join button in Month List.
                            */

                            else {

                                if (meetingLink) {

                                    const joinBtn =
                                        document.createElement(
                                            'a'
                                        );

                                    joinBtn.href = meetingLink;

                                    joinBtn.target = '_blank';

                                    joinBtn.rel = 'noopener noreferrer';

                                    joinBtn.classList.add('calendar-join-btn');

                                    joinBtn.textContent = labels.joinClass;

                                    joinBtn.addEventListener(
                                        'click',
                                        function (event) {

                                            event.stopPropagation();
                                        }
                                    );

                                    row.appendChild(joinBtn);
                                }
                            }


                            return {
                                domNodes:
                                    [row]
                            };
                        }

                        /*
                            =================================================
                            WEEK / DAY GRID
                            =================================================
                        */

                        if (arg.view.type === 'timeGridWeek' || arg.view.type === 'timeGridDay') {

                            const wrapper = document.createElement('div');

                            wrapper.classList.add('calendar-grid-event-content');

                            const timeEl = document.createElement('div');

                            timeEl.classList.add('calendar-grid-event-time');

                            timeEl.textContent = arg.timeText;

                            const titleEl = document.createElement('div');

                            titleEl.classList.add('calendar-grid-event-title');

                            titleEl.textContent = title;

                            wrapper.appendChild(timeEl);

                            wrapper.appendChild(titleEl);

                            return {
                                domNodes:
                                    [wrapper]
                            };
                        }

                        /*
                            =================================================
                            MONTH GRID
                            =================================================
                        */

                        if (arg.view.type === 'dayGridMonth') {

                            const wrapper = document.createElement('div');

                            wrapper.classList.add('calendar-month-event-content');

                            const textEl = document.createElement('span');

                            textEl.classList.add('calendar-month-event-title');

                            textEl.textContent = `${arg.timeText} ${title}`;

                            wrapper.appendChild(textEl);

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


                        /*
                            Meeting link for the exact ClassSession
                            that the user clicked.
                        */

                        const meetingLink =
                            info.event
                                .extendedProps
                                .meeting_link;

                        console.log(
                            'EVENT PROPS:',
                            info.event.extendedProps
                        );

                        console.log(
                            'MEETING LINK:',
                            meetingLink
                        );

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


                        /*
                            MODAL ELEMENTS
                        */

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


                        /*
                            TITLE
                        */

                        modalTitle.textContent =
                            title;


                        /*
                            DATE + TIME
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


                        /*
                            COURSE
                        */

                        modalCourse.textContent =
                            course ||
                            labels.courseUnavailable;


                        /*
                            CLASS NUMBER
                        */

                        modalClassNumber.textContent =
                            classNumber

                                ? `${labels.lesson} ${classNumber}`

                                : '';


                        /*
                            =================================================
                            COMPANY ADMIN

                            Opens group details.
                            =================================================
                        */

                        if (
                            userRole ===
                            'company_admin'
                        ) {

                            modalJoinBtn.textContent =
                                labels.groupDetails;


                            modalJoinBtn.target =
                                '_self';


                            modalJoinBtn.removeAttribute(
                                'rel'
                            );


                            if (
                                groupDetailsUrl
                            ) {

                                modalJoinBtn.href =
                                    groupDetailsUrl;


                                modalJoinBtn.classList.remove(
                                    'd-none'
                                );

                            } else {

                                modalJoinBtn.removeAttribute(
                                    'href'
                                );


                                modalJoinBtn.classList.add(
                                    'd-none'
                                );
                            }

                        }


                        /*
                            =================================================
                            TEACHER / STUDENT / EMPLOYEE

                            Button href receives the meeting link
                            of the clicked ClassSession.
                            =================================================
                        */

                        else {

                            modalJoinBtn.textContent =
                                labels.joinClass;


                            modalJoinBtn.target =
                                '_blank';


                            modalJoinBtn.rel =
                                'noopener noreferrer';


                            if (meetingLink) {

                                modalJoinBtn.href =
                                    meetingLink;


                                modalJoinBtn.classList.remove(
                                    'd-none'
                                );

                            } else {

                                modalJoinBtn.removeAttribute(
                                    'href'
                                );

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

        calendar.setOption(
            'locale',
            getFullCalendarLocale()
        );


        calendar.setOption(
            'buttonText',
            getButtonText()
        );


        /*
            Re-render event content so translated Join Class /
            Group Details labels are refreshed.
        */

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