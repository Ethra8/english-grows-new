document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    if (!calendarEl) {
        return;
    }

    // refers to property data-events-urls of id="calendar"
    const eventsUrl = calendarEl.dataset.eventsUrl;

    // Mobile toolbar setup
    function isMobileCalendar() {
        return window.innerWidth <= 768;
    }

    function getHeaderToolbar() {
        if (isMobileCalendar()) {
            return {
                left: 'prev',
                center: 'title',
                right: 'next today dayGridMonth,timeGridWeek,listWeek'
            };
        }

        return {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,listWeek'
        };
    }

    function getFooterToolbar() {
        return false;
    }

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',

        headerToolbar: getHeaderToolbar(),
        footerToolbar: getFooterToolbar(),

        events: eventsUrl,

        firstDay: 1,
        height: 'auto',

        // Only show Monday-Friday
        weekends: false,

        // Only shows working hours 8:00 - 21:00
        slotMinTime: '08:00:00',
        slotMaxTime: '21:00:00',

        eventTimeFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },

        eventClick: function (info) {
            const meetingLink = info.event.extendedProps.meeting_link;

            if (meetingLink) {
                window.open(meetingLink, '_blank');
            }
        },

        windowResize: function () {
            calendar.setOption('headerToolbar', getHeaderToolbar());
            calendar.setOption('footerToolbar', getFooterToolbar());
        }
    });

    calendar.render();

    // Updates every 5 minutes
    setInterval(function () {
        calendar.refetchEvents();
    }, 300000);
});