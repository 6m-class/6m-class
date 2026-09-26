/* ===== Настройки сайта: тема + шрифт через localStorage ===== */

(function() {
    // CSS для всех 5 тем
    const themeCSS = `
[data-theme="red"]{--primary:#ff0033;--primary-rgb:255,0,51;--glow:rgba(255,0,51,0.15);--glow-strong:rgba(255,0,51,0.8);--border:rgba(255,0,51,0.3);--shadow:rgba(255,0,51,0.2)}
[data-theme="yellow"]{--primary:#ffcc00;--primary-rgb:255,204,0;--glow:rgba(255,204,0,0.15);--glow-strong:rgba(255,204,0,0.8);--border:rgba(255,204,0,0.3);--shadow:rgba(255,204,0,0.2)}
[data-theme="green"]{--primary:#00ff66;--primary-rgb:0,255,102;--glow:rgba(0,255,102,0.15);--glow-strong:rgba(0,255,102,0.8);--border:rgba(0,255,102,0.3);--shadow:rgba(0,255,102,0.2)}
[data-theme="blue"]{--primary:#00aaff;--primary-rgb:0,170,255;--glow:rgba(0,170,255,0.15);--glow-strong:rgba(0,170,255,0.8);--border:rgba(0,170,255,0.3);--shadow:rgba(0,170,255,0.2)}
[data-theme="purple"]{--primary:#aa00ff;--primary-rgb:170,0,255;--glow:rgba(170,0,255,0.15);--glow-strong:rgba(170,0,255,0.8);--border:rgba(170,0,255,0.3);--shadow:rgba(170,0,255,0.2)}
`;

    // CSS для шрифтов
    const fontCSS = `
/* Шрифт: Обычный */
[data-font="normal"] body, [data-font="normal"] * { font-family: 'Montserrat', sans-serif !important; }
/* Шрифт: Жирный */
[data-font="bold"] body, [data-font="bold"] * { font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; }
/* Шрифт: Miama Nueva Medium */
@font-face{font-family:'Miama Nueva';src:url('https://fontlibrary.org/assets/fonts/miama-nueva/miamanueva_regular-webfont.woff2') format('woff2'),url('https://fontlibrary.org/assets/fonts/miama-nueva/miamanueva_regular-webfont.woff') format('woff'),url('https://fontlibrary.org/assets/fonts/miama-nueva/miamanueva_regular-webfont.ttf') format('truetype');font-weight:normal;font-style:normal;font-display:swap}
[data-font="fancy"] body, [data-font="fancy"] h1, [data-font="fancy"] h2, [data-font="fancy"] .section-title, [data-font="fancy"] .news-title, [data-font="fancy"] .activity-title, [data-font="fancy"] .card-title, [data-font="fancy"] .gate-title, [data-font="fancy"] .logo, [data-font="fancy"] .typewriter-line { font-family: 'Miama Nueva', cursive !important; font-weight: normal !important; }
`;

    const style = document.createElement('style');
    style.textContent = themeCSS + fontCSS;
    document.head.appendChild(style);

    // Применяем сохранённые настройки
    const savedTheme = localStorage.getItem('site-theme') || 'red';
    const savedFont = localStorage.getItem('site-font') || 'normal';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-font', savedFont);
})();

// Глобальная функция смены темы
function setSiteTheme(theme) {
    localStorage.setItem('site-theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
}

// Глобальная функция смены шрифта
function setSiteFont(font) {
    localStorage.setItem('site-font', font);
    document.documentElement.setAttribute('data-font', font);
}
