document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    if (!calendarEl) {
        return;
    }

    // refers to property data-events-urls of id="calendar"
    const eventsUrl = calendarEl.dataset.eventsUrl;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,listWeek'
        },

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
        }
    });

    calendar.render();

    // Updates every 5 minutes
    setInterval(function () {
        calendar.refetchEvents();
    }, 300000);
});