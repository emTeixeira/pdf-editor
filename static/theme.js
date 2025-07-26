document.addEventListener('DOMContentLoaded', () => {
    const themeButton = document.getElementById('theme-button');
    const themeIcon = document.getElementById('theme-icon');
    const body = document.body;

    const sunIcon = '/static/images/sun.webp';
    const moonIcon = '/static/images/moon.webp';

    function setTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            body.classList.remove('light-mode');
            // No modo escuro, mostrar ícone do sol para alternar para claro
            themeIcon.src = sunIcon;
            themeIcon.alt = "Mudar para tema claro";
        } else {
            body.classList.add('light-mode');
            body.classList.remove('dark-mode');
            // No modo claro, mostrar ícone da lua para alternar para escuro
            themeIcon.src = moonIcon;
            themeIcon.alt = "Mudar para tema escuro";
        }
        localStorage.setItem('theme', theme);
    }

    themeButton.addEventListener('click', () => {
        const isDark = body.classList.contains('dark-mode');
        setTheme(isDark ? 'light' : 'dark');
    });

    // Aplica o tema salvo ao carregar a página
    const saved = localStorage.getItem('theme') || 'light';
    setTheme(saved);
});
