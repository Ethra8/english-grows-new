
document.addEventListener('DOMContentLoaded', function () {
    
    const calendarEl = document.getElementById('calendar');
    const userRole = calendarEl.dataset.role;

    if (!calendarEl) {
        return;
    }

    const eventsUrl = calendarEl.dataset.eventsUrl;

    function isMobileCalendar() {
        return window.innerWidth <= 768;
    }

    function getHeaderToolbar() {
        if (isMobileCalendar()) {
            return {
                left: 'prev',
                center: 'title',
                right: 'next todayOnly,timeGridWeek,dayGridMonth,listMonth'
            };
        }

        return {
            left: 'prev',
            center: 'title',
            right: 'next todayOnly,timeGridWeek,dayGridMonth,listMonth,multiMonthYear'
        };
    }

    function getOrdinalSuffix(day) {
        if (day > 3 && day < 21) {
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

    function formatBigDayTitle(date) {
        const day = date.getDate();
        const suffix = getOrdinalSuffix(day);
        const month = date.toLocaleString('en-GB', {
            month: 'short'
        });
        const year = String(date.getFullYear()).slice(-2);

        return `${day}<sup>${suffix}</sup> ${month}. '${year}`;
    }

    function formatDayGridHeader(date) {
        const weekday = date.toLocaleString('en-GB', {
            weekday: 'short'
        });

        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = String(date.getFullYear()).slice(-2);

        return `${weekday}. ${day}/${month}/${year}`;
    }

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        locale: 'en-gb',

        customButtons: {
            todayOnly: {
                text: 'Today',
                click: function () {
                    calendar.changeView('timeGridDay', new Date());
                    calendar.refetchEvents();
                }
            }
        },

        buttonText: {
            timeGridWeek: 'Week',
            dayGridMonth: 'Month',
            listMonth: 'Month List',
            multiMonthYear: 'Year'
        },

        headerToolbar: getHeaderToolbar(),
        footerToolbar: false,

        events: eventsUrl,

        firstDay: 1,
        height: 'auto',

        weekends: false,

        slotMinTime: '08:00:00',
        slotMaxTime: '21:00:00',

        eventTimeFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },

        /*
            Date title format:
            - Day view: custom format, e.g. 3rd Aug. '26
            - Other views: FullCalendar default title
        */
        datesSet: function (info) {
            const titleEl = calendarEl.querySelector('.fc-toolbar-title');

            if (!titleEl) {
                return;
            }

            if (info.view.type === 'timeGridDay') {
                titleEl.innerHTML = formatBigDayTitle(info.start);
            } else {
                titleEl.textContent = info.view.title;
            }
        },
        /*
            Grid column header:
            - Only day view uses: Wed. 19/08/26
            - Week/month views keep FullCalendar default headers
        */
        dayHeaderContent: function (arg) {
            if (arg.view.type === 'timeGridDay') {
                return formatDayGridHeader(arg.date);
            }

            return arg.text;
        },

        /*
            Month grid:
            Clicking an empty day cell opens that day view.
            Clicking an event still opens the event modal.
        */
        dateClick: function (info) {
            const clickableViews = [
                'dayGridMonth',
                'multiMonthYear'
            ];

            if (clickableViews.includes(info.view.type)) {
                calendar.changeView('timeGridDay', info.dateStr);
            }
        },
        /*
            Custom event rendering:
            - Month List gets custom layout with Join Class button.
            - Week / Day / Month grids show event text without overflowing.
        */
        eventContent: function (arg) {
            const meetingLink = arg.event.extendedProps.meeting_link;
            const groupDetailsUrl = arg.event.extendedProps.group_details_url;
            const title = arg.event.title;

            /*
                MONTH LIST VIEW
                Custom row with Join class button.
            */
            if (arg.view.type === 'listMonth') {
                const row = document.createElement('div');
                row.classList.add('calendar-list-event-row');

                const titleEl = document.createElement('span');
                titleEl.classList.add('calendar-list-event-title');
                titleEl.textContent = title;

                row.appendChild(titleEl);

                if (userRole === 'company_admin') {
                    if (groupDetailsUrl) {
                        const detailsBtn = document.createElement('a');

                        detailsBtn.href = groupDetailsUrl;
                        detailsBtn.target = '_self';
                        detailsBtn.classList.add('calendar-join-btn');
                        detailsBtn.textContent = 'Group details';

                        detailsBtn.addEventListener('click', function (event) {
                            event.stopPropagation();
                        });

                        row.appendChild(detailsBtn);
                    }
                } else {
                    if (meetingLink) {
                        const joinBtn = document.createElement('a');

                        joinBtn.href = meetingLink;
                        joinBtn.target = '_blank';
                        joinBtn.rel = 'noopener noreferrer';
                        joinBtn.classList.add('calendar-join-btn');
                        joinBtn.textContent = 'Join class';

                        joinBtn.addEventListener('click', function (event) {
                            event.stopPropagation();
                        });

                        row.appendChild(joinBtn);
                    }
                }

                return {
                    domNodes: [row]
                };
            }

            /*
                WEEK / DAY GRID VIEW
                Show time + title inside coloured event block.
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
                    domNodes: [wrapper]
                };
            }

            /*
                MONTH GRID VIEW
                Show compact text, clipped by CSS if too long.
            */
            if (arg.view.type === 'dayGridMonth') {
                const wrapper = document.createElement('div');
                wrapper.classList.add('calendar-month-event-content');

                const textEl = document.createElement('span');
                textEl.classList.add('calendar-month-event-title');
                textEl.textContent = `${arg.timeText} ${title}`;

                wrapper.appendChild(textEl);

                return {
                    domNodes: [wrapper]
                };
            }

            const fallback = document.createElement('span');
            fallback.textContent = title;

            return {
                domNodes: [fallback]
            };
        },

        eventClick: function (info) {
            info.jsEvent.preventDefault();

            const title = info.event.title;
            const start = info.event.start;
            const end = info.event.end;

            const meetingLink = info.event.extendedProps.meeting_link;
            const groupDetailsUrl = info.event.extendedProps.group_details_url;

            const course = info.event.extendedProps.course;
            const classNumber = info.event.extendedProps.class_number;

            const modalTitle = document.getElementById('classSessionModalTitle');
            const modalTime = document.getElementById('classSessionModalTime');
            const modalCourse = document.getElementById('classSessionModalCourse');
            const modalClassNumber = document.getElementById('classSessionModalClassNumber');
            const modalJoinBtn = document.getElementById('classSessionModalJoinBtn');

            if (
                !modalTitle ||
                !modalTime ||
                !modalCourse ||
                !modalClassNumber ||
                !modalJoinBtn
            ) {
                return;
            }

            modalTitle.textContent = title;

            const startText = start ? start.toLocaleString('en-GB', {
                weekday: 'long',
                day: 'numeric',
                month: 'long',
                hour: '2-digit',
                minute: '2-digit'
            }) : '';

            const endText = end ? end.toLocaleTimeString('en-GB', {
                hour: '2-digit',
                minute: '2-digit'
            }) : '';

            modalTime.textContent = endText
                ? `${startText} - ${endText}`
                : startText;

            modalCourse.textContent =
                course || 'Course information unavailable';

            modalClassNumber.textContent =
                classNumber ? `Lesson ${classNumber}` : '';

            if (userRole === 'company_admin') {
                modalJoinBtn.textContent = 'Group details';
                modalJoinBtn.target = '_self';
                modalJoinBtn.rel = '';

                if (groupDetailsUrl) {
                    modalJoinBtn.href = groupDetailsUrl;
                    modalJoinBtn.classList.remove('d-none');
                } else {
                    modalJoinBtn.href = '#';
                    modalJoinBtn.classList.add('d-none');
                }
            } else {
                modalJoinBtn.textContent = 'Join class';
                modalJoinBtn.target = '_blank';
                modalJoinBtn.rel = 'noopener noreferrer';

                if (meetingLink) {
                    modalJoinBtn.href = meetingLink;
                    modalJoinBtn.classList.remove('d-none');
                } else {
                    modalJoinBtn.href = '#';
                    modalJoinBtn.classList.add('d-none');
                }
            }

            $('#classSessionModal').modal('show');
        },

        windowResize: function () {
            calendar.setOption('headerToolbar', getHeaderToolbar());
        }
    });

    calendar.render();

    setInterval(function () {
        calendar.refetchEvents();
    }, 300000);
});