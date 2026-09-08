<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Suno Interface Clone</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#121212] text-white font-sans pb-24">
    <!-- Top Navigation -->
    <header class="flex items-center justify-between px-4 py-3 border-b border-neutral-800 bg-[#121212] sticky top-0 z-50">
        <div class="flex items-center space-x-3">
            <span class="text-xl font-bold tracking-wider">SUNO</span>
        </div>
        <div class="flex items-center space-x-4">
            <div class="flex items-center bg-neutral-800 px-2.5 py-1 rounded-full text-xs">
                <span class="mr-1">♫</span> 50
            </div>
            <button class="text-neutral-400 hover:text-white" aria-label="Buscar"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg></button>
            <button class="text-neutral-400 hover:text-white" aria-label="Notificaciones"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg></button>
        </div>
    </header>

    <!-- Main Creation Form -->
    <main class="max-w-md mx-auto p-4 space-y-4">
        <!-- Mode Selector -->
        <div class="flex items-center justify-between bg-neutral-900 p-1.5 rounded-full border border-neutral-800">
            <button class="flex-1 py-1.5 text-sm font-medium rounded-full text-neutral-400">Simple</button>
            <button class="flex-1 py-1.5 text-sm font-medium rounded-full bg-neutral-700 text-white shadow">Avanzado</button>
            <div class="px-3 text-sm text-neutral-300 flex items-center space-x-1">
                <span>v5.5</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </div>
        </div>

        <!-- Estilos Section -->
        <div class="bg-[#18181b] rounded-xl p-4 border border-neutral-800 space-y-3">
            <div class="flex items-center justify-between text-sm text-neutral-400">
                <span>Estilos</span>
                <span>\ || /</span>
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
                <div class="flex space-x-3">
                    <button class="hover:text-white">↺</button>
                    <button class="hover:text-white">✏️</button>
                    <button class="hover:text-white">\ || /</button>
                </div>
            </div>
            <div class="w-full bg-neutral-900 border border-neutral-700 rounded-lg p-3 text-sm text-neutral-500 min-h-[80px]">
                Empieza a escribir la letra, o deja esto en blanco para la parte instrumental.
            </div>
        </div>

        <!-- Más opciones (Sliders) -->
        <div class="bg-[#18181b] rounded-xl p-4 border border-neutral-800 space-y-4">
            <div class="flex items-center justify-between text-sm text-neutral-400 cursor-pointer">
                <span>Más opciones</span>
                <span>▼</span>
            </div>
            
            <div class="space-y-3 pt-2 border-t border-neutral-800 text-sm">
                <div class="flex justify-between items-center text-neutral-300">
                    <span>Rareza</span>
                    <span class="text-neutral-400">50 %</span>
                </div>
                <div class="w-full bg-neutral-800 h-1 rounded-full relative">
                    <div class="bg-pink-500 h-2 w-2 rounded-full absolute -top-0.5 left-1/2"></div>
                </div>

                <div class="flex justify-between items-center text-neutral-300 pt-2">
                    <span>Influencia del estilo</span>
                    <span class="text-neutral-400">50 %</span>
                </div>
                <div class="w-full bg-neutral-800 h-1 rounded-full relative">
                    <div class="bg-pink-500 h-2 w-2 rounded-full absolute -top-0.5 left-3/4"></div>
                </div>

                <div class="flex justify-between items-center text-neutral-300 pt-2">
                    <span>Influencia del audio</span>
                    <span class="text-neutral-400">25 %</span>
                </div>
                <div class="w-full bg-neutral-800 h-1 rounded-full relative">
                    <div class="bg-pink-500 h-2 w-2 rounded-full absolute -top-0.5 left-1/4"></div>
                </div>
            </div>
        </div>

        <!-- Crear Button -->
        <button class="w-full py-3.5 rounded-full bg-gradient-to-r from-pink-500 via-orange-500 to-yellow-500 text-white font-bold text-base shadow-lg hover:opacity-95 transition">
            Crear
        </button>
    </main>

    <!-- Sticky Bottom Player -->
    <div class="fixed bottom-0 left-0 right-0 bg-[#18181b] border-t border-neutral-800 px-4 py-3 flex items-center justify-between z-50 shadow-2xl">
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
            <button class="hover:text-white" aria-label="Anterior">⏮</button>
            <button class="w-8 h-8 rounded-full bg-white text-black flex items-center justify-center font-bold" aria-label="Reproducir">▶</button>
            <button class="hover:text-white" aria-label="Siguiente">⏭</button>
        </div>
    </div>
</body>
</html>
