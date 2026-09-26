/* ===== ОБЩИЙ ЗАГРУЗЧИК НАСТРОЕК ===== */
/* Подключается на каждой странице через <script src="settings.js"></script> */
(function() {
    /* @font-face для Ankona Kursive */
    var styleEl = document.createElement('style');
    styleEl.textContent = `
@font-face{font-family:'Ankona Kursive';src:url('fonts/AnkonaKursive.woff2') format('woff2'),url('fonts/AnkonaKursive.ttf') format('truetype');font-weight:normal;font-style:normal;font-display:swap}
[data-font="bold"] body{font-weight:700}
[data-font="beautiful"] body{font-family:'Ankona Kursive',cursive!important}
[data-font="beautiful"] h1,[data-font="beautiful"] h2,[data-font="beautiful"] h3,
[data-font="beautiful"] .news-title,[data-font="beautiful"] .section-title,
[data-font="beautiful"] .card-title,[data-font="beautiful"] .activity-title,
[data-font="beautiful"] .day-tab,[data-font="beautiful"] .logo,
[data-font="beautiful"] .gate-title,[data-font="beautiful"] .teacher-name,
[data-font="beautiful"] .student-name{font-family:'Ankona Kursive',cursive!important}
`;
    document.head.appendChild(styleEl);

    /* Применяем сохранённые настройки */
    var color = localStorage.getItem('site-color') || 'red';
    var font = localStorage.getItem('site-font') || 'normal';
    document.documentElement.setAttribute('data-theme', color);
    document.documentElement.setAttribute('data-font', font);
})();
