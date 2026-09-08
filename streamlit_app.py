import streamlit as st

st.set_page_config(
    page_title="Suno Interface Clone",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS and HTML structure matching the exact Suno mobile advanced interface
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: #121212;
        color: white;
    }
</style>

<div class="pb-28 font-sans">
    <!-- Top Navigation -->
    <header class="flex items-center justify-between px-4 py-3 border-b border-neutral-800 bg-[#121212] sticky top-0 z-50">
        <div class="flex items-center space-x-3">
            <span class="text-xl font-bold tracking-wider">SUNO</span>
        </div>
        <div class="flex items-center space-x-3">
            <div class="flex items-center bg-neutral-800 px-2.5 py-1 rounded-full text-xs">
                <span class="mr-1">🎵</span> 50
            </div>
            <button class="text-neutral-400 hover:text-white">🔍</button>
            <button class="text-neutral-400 hover:text-white">🔔</button>
            <button class="text-neutral-400 hover:text-white">⋯</button>
        </div>
    </header>

    <!-- Main Creation Form Container -->
    <main class="max-w-md mx-auto p-4 space-y-4">
        <!-- Mode & Version Selector Bar -->
        <div class="flex items-center justify-between bg-neutral-900 p-1.5 rounded-full border border-neutral-800 text-sm">
            <button class="flex-1 py-1.5 font-medium rounded-full text-neutral-400 text-center">Simple</button>
            <button class="flex-1 py-1.5 font-medium rounded-full bg-neutral-700 text-white shadow text-center">Avanzado</button>
            <div class="px-3 text-neutral-300 flex items-center space-x-1 cursor-pointer">
                <span>v5.5</span>
                <span>▼</span>
            </div>
        </div>

        <!-- Estilos Section -->
        <div class="bg-[#18181b] rounded-xl p-4 border border-neutral-800 space-y-3">
            <div class="flex items-center justify-between text-sm text-neutral-400">
                <span>Estilos</span>
                <span>\\ || /</span>
            </div>
            <div class="w-full bg-neutral-900 border border-neutral-700 rounded-lg p-3 text-sm text-neutral-200 min-h-[60px]">
                Resistente, tambores ligeros, rap afro, dizi, hueco
            </div>
            <div class="flex flex-wrap gap-2 pt-1">
                <span class="bg-blue-600 text-white px-3 py-1 rounded-full text-xs flex items-center space-x-1"><span>✨</span></span>
                <span class="bg-neutral-800 text-neutral-300 px-3 py-1 rounded-full text-xs border border-neutral-700">resiliente</span>
                <span class="bg-neutral-800 text-neutral-300 px-3 py-1 rounded-full text-xs border border-neutral-700">tambores d...</span>
            </div>
        </div>

        <!-- Lírica Section -->
        <div class="bg-[#18181b] rounded-xl p-4 border border-neutral-800 space-y-3">
            <div class="flex items-center justify-between text-sm text-neutral-400">
                <span>Lírica</span>
                <div class="flex space-x-3 text-neutral-400">
                    <button>↺</button>
                    <button>✏️</button>
                    <button>\\ || /</button>
                </div>
            </div>
            <div class="w-full bg-neutral-900 border border-neutral-700 rounded-lg p-3 text-sm text-neutral-500 min-h-[80px]">
                Empieza a escribir la letra, o deja esto en blanco para la parte instrumental.
            </div>
        </div>

        <!-- Más opciones (Advanced Accordion) -->
        <div class="bg-[#18181b] rounded-xl p-4 border border-neutral-800 space-y-4">
            <div class="flex items-center justify-between text-sm text-neutral-400 cursor-pointer">
                <span>Más opciones</span>
                <span>▼</span>
            </div>
            
            <div class="space-y-4 pt-2 border-t border-neutral-800 text-sm">
                <!-- Excluir estilos -->
                <div class="bg-neutral-900 border border-neutral-800 rounded-lg p-3 flex items-center justify-between text-neutral-400">
                    <span>❌ Excluir estilos</span>
                </div>

                <!-- Género vocal -->
                <div class="bg-neutral-900 border border-neutral-800 rounded-lg p-3 flex items-center justify-between">
                    <span class="text-neutral-400">Género vocal ℹ️</span>
                    <div class="space-x-4 text-xs text-neutral-500">
                        <span>Masculino</span>
                        <span>Femenino</span>
                    </div>
                </div>

                <!-- Duración -->
                <div class="bg-neutral-900 border border-neutral-800 rounded-lg p-3 flex items-center justify-between">
                    <span class="text-neutral-400">Duración ℹ️</span>
                    <div class="flex bg-neutral-800 p-1 rounded-lg text-xs">
                        <span class="px-2 py-1 text-neutral-400">Costumbre</span>
                        <span class="px-2 py-1 bg-neutral-700 text-white rounded">Auto</span>
                    </div>
                </div>

                <!-- Sliders -->
                <div class="space-y-3 pt-2">
                    <div class="flex justify-between items-center text-neutral-300">
                        <span>Rareza ℹ️</span>
                        <span class="text-neutral-400">50 %</span>
                    </div>
                    <div class="w-full bg-neutral-800 h-1 rounded-full relative">
                        <div class="bg-pink-500 h-2.5 w-2.5 rounded-full absolute -top-1 left-1/2"></div>
                    </div>

                    <div class="flex justify-between items-center text-neutral-300 pt-2">
                        <span>Influencia del estilo 🔄</span>
                        <span class="text-neutral-400">50 %</span>
                    </div>
                    <div class="w-full bg-neutral-800 h-1 rounded-full relative">
                        <div class="bg-pink-500 h-2.5 w-2.5 rounded-full absolute -top-1 left-3/4"></div>
                    </div>

                    <div class="space-y-1 pt-2">
                        <div class="flex justify-between items-center text-neutral-300">
                            <span>Influencia del audio ℹ️</span>
                            <span class="text-neutral-400">25 %</span>
                        </div>
                        <div class="w-full bg-neutral-800 h-1 rounded-full relative">
                            <div class="bg-pink-500 h-2.5 w-2.5 rounded-full absolute -top-1 left-1/4"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Create Button -->
        <button class="w-full py-3.5 rounded-full bg-gradient-to-r from-pink-500 via-orange-500 to-yellow-500 text-white font-bold text-base shadow-lg transition">
            🎵 Crear
        </button>
    </main>

    <!-- Sticky Bottom Player -->
    <div class="fixed bottom-0 left-0 right-0 bg-[#18181b] border-t border-neutral-800 px-4 py-3 flex items-center justify-between z-50 shadow-2xl max-w-md mx-auto">
        <div class="flex items-center space-x-3 overflow-hidden">
            <div class="w-10 h-10 rounded-lg bg-neutral-700 flex-shrink-0 overflow-hidden">
                <img src="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=100&h=100&fit=crop" alt="Cover" class="w-full h-full object-cover">
            </div>
            <div class="truncate">
                <p class="text-sm font-medium text-white truncate">Colombia se levanta</p>
                <p class="text-xs text-neutral-400 truncate">Flujo de Darcko</p>
            </div>
        </div>
        <div class="flex items-center space-x-4 text-neutral-300">
            <button class="hover:text-white">⏮</button>
            <button class="w-8 h-8 rounded-full bg-white text-black flex items-center justify-center font-bold">▶</button>
            <button class="hover:text-white">⏭</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
