# Este arquivo instrui o Jupyter a lançar o Streamlit automaticamente na inicialização
c.ServerProxy.servers = {
    'streamlit': {
        'command': [
            'streamlit', 'run', 'app.py',
            '--server.port', '{port}',
            '--server.address', '0.0.0.0',
            '--browser.gatherUsageStats', 'false',
            '--server.headless', 'true',
            '--server.enableCORS', 'false'
        ],
        'timeout': 60,
        'launcher_entry': {
            'title': 'Streamlit App',
        }
    }
}