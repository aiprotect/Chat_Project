
        // Dark mode toggle
        const themeToggle = document.getElementById('theme-toggle');
        const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
        const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
            themeToggleLightIcon.classList.remove('hidden');
        } else {
            document.documentElement.classList.remove('dark');
            themeToggleDarkIcon.classList.remove('hidden');
        }

        themeToggle.addEventListener('click', function() {
            themeToggleDarkIcon.classList.toggle('hidden');
            themeToggleLightIcon.classList.toggle('hidden');

            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        });

        // Mobile menu toggle
        const mobileMenuButton = document.querySelector('[aria-controls="mobile-menu"]');
        const mobileMenu = document.getElementById('mobile-menu');

        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');

            const expanded = mobileMenuButton.getAttribute('aria-expanded') === 'true' || false;
            mobileMenuButton.setAttribute('aria-expanded', !expanded);

            const icon = mobileMenuButton.querySelector('svg:not(.hidden)');
            const otherIcon = mobileMenuButton.querySelector('svg.hidden');

            icon.classList.add('hidden');
            otherIcon.classList.remove('hidden');
        });




        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            const messagesContainer = document.querySelector('.bg-gray-50.dark\\:bg-gray-700');

            // Create message element based on message type
            const messageElement = createMessageElement(data);

            // Append to messages container
            messagesContainer.appendChild(messageElement);

            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        };

        function createMessageElement(data) {
            const isCurrentUser = data.sender === 'current_user'; // You would replace this with actual user check

            if (data.type === 'text') {
                return createTextMessage(data, isCurrentUser);
            } else if (data.type === 'image') {
                return createImageMessage(data, isCurrentUser);
            } else if (data.type === 'file') {
                return createFileMessage(data, isCurrentUser);
            } else if (data.type === 'voice') {
                return createVoiceMessage(data, isCurrentUser);
            }

            // Default to text message if type is unknown
            return createTextMessage(data, isCurrentUser);
        }

        function createTextMessage(data, isCurrentUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `flex items-start ${isCurrentUser ? 'justify-end' : ''}`;

            if (!isCurrentUser) {
                messageDiv.innerHTML = `
                    <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full" src="${data.avatar}" alt="">
                    </div>
                    <div class="ml-3">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">${data.sender}</div>
                        <div class="mt-1 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 p-3 rounded-lg shadow-sm max-w-xs lg:max-w-md">
                            ${data.message}
                        </div>
                        <div class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                            ${data.timestamp}
                        </div>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="mr-3 text-right">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">You</div>
                        <div class="mt-1 text-sm text-white bg-primary-600 p-3 rounded-lg shadow-sm max-w-xs lg:max-w-md">
                            ${data.message}
                        </div>
                        <div class="mt-1 text-xs text-gray-500 dark:text-gray-400 flex items-center justify-end">
                            <span>${data.timestamp}</span>
                            <svg class="ml-1 h-4 w-4 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                            </svg>
                        </div>
                    </div>
                    <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full" src="${data.avatar}" alt="">
                    </div>
                `;
            }

            return messageDiv;
        }

        function createImageMessage(data, isCurrentUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `flex items-start ${isCurrentUser ? 'justify-end' : ''}`;

            if (!isCurrentUser) {
                messageDiv.innerHTML = `
                    <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full" src="${data.avatar}" alt="">
                    </div>
                    <div class="ml-3">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">${data.sender}</div>
                        <div class="mt-1 bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden max-w-xs lg:max-w-md">
                            <img class="w-full" src="${data.url}" alt="${data.caption || 'Image'}">
                            ${data.caption ? `<div class="p-3 text-sm text-gray-700 dark:text-gray-300">${data.caption}</div>` : ''}
                        </div>
                        <div class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                            ${data.timestamp}
                        </div>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="mr-3 text-right">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">You</div>
                        <div class="mt-1 bg-primary-100 dark:bg-primary-900 rounded-lg shadow-sm overflow-hidden max-w-xs lg:max-w-md">
                            <img class="w-full" src="${data.url}" alt="${data.caption || 'Image'}">
                            ${data.caption ? `<div class="p-3 text-sm text-primary-800 dark:text-primary-200">${data.caption}</div>` : ''}
                        </div>
                        <div class="mt-1 text-xs text-gray-500 dark:text-gray-400 flex items-center justify-end">
                            <span>${data.timestamp}</span>
                            <svg class="ml-1 h-4 w-4 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                            </svg>
                        </div>
                    </div>
                    <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full" src="${data.avatar}" alt="">
                    </div>
                `;
            }

            return messageDiv;
        }

        function createFileMessage(data, isCurrentUser) {
            const fileIcon = getFileIcon(data.fileType);

            const messageDiv = document.createElement('div');
            messageDiv.className = `flex items-start ${isCurrentUser ? 'justify-end' : ''}`;

            if (!isCurrentUser) {
                messageDiv.innerHTML = `
                    <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full" src="${data.avatar}" alt="">
                    </div>
                    <div class="ml-3">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">${data.sender}</div>
                        <div class="mt-1 bg-white dark:bg-gray-800 rounded-lg shadow-sm p-3 max-w-xs lg:max-w-md">
                            <div class="flex items-center">
                                <div class="flex-shrink-0 h-10 w-10 ${fileIcon.bgColor} rounded-md flex items-center justify-center">
                                    ${fileIcon.svg}
                                </div>
                                <div class="ml-4">
                                    <p class="text-sm font-medium text-gray-900 dark:text-white">${data.filename}</p>
                                    <p class="text-sm text-gray-500 dark:text-gray-400">${formatFileSize(data.fileSize)}</p>
                                </div>
                            </div>
                        </div>
                        <div class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                            ${data.timestamp}
                        </div>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="mr-3 text-right">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">You</div>
                        <div class="mt-1 bg-primary-100 dark:bg-primary-900 rounded-lg shadow-sm p-3 max-w-xs lg:max-w-md">
                            <div class="flex items-center">
                                <div class="flex-shrink-0 h-10 w-10 ${fileIcon.bgColor} rounded-md flex items-center justify-center">
                                    ${fileIcon.svg}
                                </div>
                                <div class="ml-4">
                                    <p class="text-sm font-medium text-gray-900 dark:text-white">${data.filename}</p>
                                    <p class="text-sm text-gray-500 dark:text-gray-400">${formatFileSize(data.fileSize)}</p>
                                </div>
                            </div>
                        </div>
                        <div class="mt-1 text-xs text-gray-500 dark:text-gray-400 flex items-center justify-end">
                            <span>${data.timestamp}</span>
                            <svg class="ml-1 h-4 w-4 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                            </svg>
                        </div>
                    </div>
                    <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full" src="${data.avatar}" alt="">
                    </div>
                `;
            }

            return messageDiv;
        }

        function createVoiceMessage(data, isCurrentUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `flex items-start ${isCurrentUser ? 'justify-end' : ''}`;

            if (!isCurrentUser) {
                messageDiv.innerHTML = `
                    <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full" src="${data.avatar}" alt="">
                    </div>
                    <div class="ml-3">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">${data.sender}</div>
                        <div class="mt-1 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 p-3 rounded-lg shadow-sm max-w-xs lg:max-w-md flex items-center">
                            <button class="flex items-center justify-center bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-300 rounded-full h-10 w-10">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </button>
                            <div class="waveform ml-3">
                                ${Array.from({length: 8}).map(() => '<div class="waveform-bar"></div>').join('')}
                            </div>
                            <div class="ml-3 text-xs text-gray-500 dark:text-gray-400">${data.duration}</div>
                        </div>
                        <div class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                            ${data.timestamp}
                        </div>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="mr-3 text-right">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">You</div>
                        <div class="mt-1 text-sm text-white bg-primary-600 p-3 rounded-lg shadow-sm max-w-xs lg:max-w-md flex items-center">
                            <button class="flex items-center justify-center bg-primary-700 text-white rounded-full h-10 w-10">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </button>
                            <div class="waveform ml-3">
                                ${Array.from({length: 8}).map(() => '<div class="waveform-bar"></div>').join('')}
                            </div>
                            <div class="ml-3 text-xs text-primary-200">${data.duration}</div>
                        </div>
                        <div class="mt-1 text-xs text-gray-500 dark:text-gray-400 flex items-center justify-end">
                            <span>${data.timestamp}</span>
                            <svg class="ml-1 h-4 w-4 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                            </svg>
                        </div>
                    </div>
                    <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full" src="${data.avatar}" alt="">
                    </div>
                `;
            }

            return messageDiv;
        }

        function getFileIcon(fileType) {
            const icons = {
                'pdf': {
                    bgColor: 'bg-red-100 dark:bg-red-900',
                    svg: '<svg class="h-6 w-6 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>'
                },
                'doc': {
                    bgColor: 'bg-blue-100 dark:bg-blue-900',
                    svg: '<svg class="h-6 w-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>'
                },
                'xls': {
                    bgColor: 'bg-green-100 dark:bg-green-900',
                    svg: '<svg class="h-6 w-6 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>'
                },
                'ppt': {
                    bgColor: 'bg-orange-100 dark:bg-orange-900',
                    svg: '<svg class="h-6 w-6 text-orange-600 dark:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" /></svg>'
                },
                'img': {
                    bgColor: 'bg-purple-100 dark:bg-purple-900',
                    svg: '<svg class="h-6 w-6 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>'
                },
                'zip': {
                    bgColor: 'bg-yellow-100 dark:bg-yellow-900',
                    svg: '<svg class="h-6 w-6 text-yellow-600 dark:text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" /></svg>'
                },
                'default': {
                    bgColor: 'bg-gray-100 dark:bg-gray-900',
                    svg: '<svg class="h-6 w-6 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>'
                }
            };

            if (fileType.match(/pdf/i)) return icons.pdf;
            if (fileType.match(/(doc|docx)/i)) return icons.doc;
            if (fileType.match(/(xls|xlsx)/i)) return icons.xls;
            if (fileType.match(/(ppt|pptx)/i)) return icons.ppt;
            if (fileType.match(/(jpg|jpeg|png|gif|bmp)/i)) return icons.img;
            if (fileType.match(/(zip|rar|tar|gz)/i)) return icons.zip;

            return icons.default;
        }

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // Message input handling
        const messageInput = document.querySelector('input[placeholder="Type a message"]');
        const sendButton = document.querySelector('button[aria-label="Send message"]');

        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        sendButton.addEventListener('click', sendMessage);

        function sendMessage() {
            const message = messageInput.value.trim();
            if (message) {
                chatSocket.send(JSON.stringify({
                    type: 'text',
                    message: message,
                    sender: 'current_user', // This would be the actual user ID
                    timestamp: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
                    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
                }));
                messageInput.value = '';
            }
        }

        // Simulate typing indicator
        setInterval(() => {
            const typingIndicator = document.querySelector('.typing-indicator');
            if (typingIndicator) {
                typingIndicator.style.display = Math.random() > 0.7 ? 'inline-block' : 'none';
            }
        }, 3000);
