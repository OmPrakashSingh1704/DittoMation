// DittoMation Demo Vue Application
const { createApp, ref, reactive, onMounted, computed, watch } = Vue;

createApp({
    setup() {
        // Terminal animation state
        const terminalAnimated = ref(false);

        // Fallback chain animation
        const fallbackStep = ref(0);

        // Confidence scores for smart locator visualization
        const confidenceScores = ref({
            resourceId: 0,
            textMatch: 0,
            visualAI: 0
        });

        // Workflow animation step
        const workflowStep = ref(0);

        // NL Command playground
        const nlCommand = ref('');
        const parsedCommand = ref(null);
        const isExecuting = ref(false);

        // Example commands
        const exampleCommands = [
            'open Chrome and search for weather',
            'tap the login button',
            'scroll down and find settings',
            'type hello world in the search box'
        ];

        // Quick commands for simulator
        const quickCommands = [
            'open Settings',
            'open Chrome',
            'open Messages',
            'enable WiFi',
            'enable Dark mode',
            'search for weather'
        ];

        // Code tabs
        const codeTabs = [
            { id: 'cli', label: 'CLI' },
            { id: 'python', label: 'Python' },
            { id: 'json', label: 'Workflow JSON' }
        ];
        const activeCodeTab = ref('cli');
        const codeCopied = ref(false);

        // Comparison data
        const comparisonData = [
            { feature: 'Natural Language Commands', ditto: true, traditional: false },
            { feature: 'Smart Element Locator', ditto: true, traditional: false },
            { feature: 'Multiple Fallback Strategies', ditto: true, traditional: false },
            { feature: 'AI-Powered Matching', ditto: true, traditional: false },
            { feature: 'Record & Replay', ditto: true, traditional: true },
            { feature: 'Variables Support', ditto: true, traditional: 'Limited' },
            { feature: 'Cross-Device Compatibility', ditto: 'High', traditional: 'Low' },
            { feature: 'Maintenance Required', ditto: 'Low', traditional: 'High' }
        ];

        // ========================================
        // Phone Simulator State
        // ========================================

        const phoneScreen = ref('home');
        const phoneTime = ref('12:00');
        const showRealEmulator = ref(false);
        const emulatorTab = ref('browser');
        const adbCopied = ref(false);

        // Feedback form state
        const feedbackSubmitted = ref(false);
        const feedback = ref({
            type: 'general',
            rating: 0,
            name: '',
            email: '',
            message: '',
            interests: []
        });

        const feedbackTypes = [
            { value: 'general', label: 'General', icon: '💬' },
            { value: 'feature', label: 'Feature', icon: '💡' },
            { value: 'bug', label: 'Bug', icon: '🐛' },
            { value: 'praise', label: 'Praise', icon: '🌟' }
        ];

        const interestFeatures = [
            'Natural Language Commands',
            'Smart Locator',
            'Record & Replay',
            'Variables & Control Flow',
            'Cloud Integration',
            'Python API'
        ];

        const recentFeedback = ref([]);
        const tappedApp = ref(null);
        const tapPosition = ref(null);
        const actionIndicator = ref(null);
        const highlightedSetting = ref(null);
        const chromeUrl = ref('');
        const chromeContent = ref('');
        const executionLog = ref([]);

        // Phone apps
        const phoneApps = ref([
            { name: 'Chrome', icon: '🌐', bg: 'bg-blue-500' },
            { name: 'Settings', icon: '⚙️', bg: 'bg-gray-500' },
            { name: 'Messages', icon: '💬', bg: 'bg-green-500' },
            { name: 'Camera', icon: '📷', bg: 'bg-gray-700' },
            { name: 'Photos', icon: '🖼️', bg: 'bg-pink-500' },
            { name: 'Maps', icon: '🗺️', bg: 'bg-green-600' },
            { name: 'Calendar', icon: '📅', bg: 'bg-blue-600' },
            { name: 'Clock', icon: '⏰', bg: 'bg-indigo-500' }
        ]);

        // Settings items
        const settingsItems = ref([
            { name: 'WiFi', icon: '📶', bg: 'bg-blue-100', toggle: true, enabled: false },
            { name: 'Bluetooth', icon: '🔵', bg: 'bg-blue-100', toggle: true, enabled: false },
            { name: 'Dark mode', icon: '🌙', bg: 'bg-purple-100', toggle: true, enabled: false },
            { name: 'Airplane mode', icon: '✈️', bg: 'bg-orange-100', toggle: true, enabled: false },
            { name: 'Sound', icon: '🔊', bg: 'bg-gray-100', toggle: false },
            { name: 'Display', icon: '☀️', bg: 'bg-yellow-100', toggle: false },
            { name: 'Battery', icon: '🔋', bg: 'bg-green-100', toggle: false },
            { name: 'Storage', icon: '💾', bg: 'bg-gray-100', toggle: false },
            { name: 'Security', icon: '🔒', bg: 'bg-red-100', toggle: false },
            { name: 'About', icon: 'ℹ️', bg: 'bg-blue-100', toggle: false }
        ]);

        // Messages
        const messages = ref([
            { id: 1, sender: 'Alice', text: 'Hey! Are you free today?', time: '10:30 AM' },
            { id: 2, sender: 'Bob', text: 'Check out this new app!', time: '9:15 AM' },
            { id: 3, sender: 'Carol', text: 'Meeting at 3pm confirmed', time: 'Yesterday' }
        ]);

        // Update phone time
        const updatePhoneTime = () => {
            const now = new Date();
            phoneTime.value = now.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            });
        };

        // Open app on phone
        const openApp = (appName) => {
            tappedApp.value = appName;
            addLog(`Tapping "${appName}" app icon`);

            setTimeout(() => {
                tappedApp.value = null;
                const screenMap = {
                    'Settings': 'settings',
                    'Chrome': 'chrome',
                    'Messages': 'messages'
                };
                if (screenMap[appName]) {
                    phoneScreen.value = screenMap[appName];
                    addLog(`Opened ${appName}`, 'success');
                } else {
                    showActionIndicator(`${appName} opened`);
                    addLog(`${appName} app launched`, 'success');
                }
            }, 300);
        };

        // Toggle setting
        const toggleSetting = (setting) => {
            setting.enabled = !setting.enabled;
            addLog(`${setting.name} ${setting.enabled ? 'enabled' : 'disabled'}`, 'success');
        };

        // Show tap ripple effect
        const showTapRipple = (x, y) => {
            tapPosition.value = { x, y };
            setTimeout(() => {
                tapPosition.value = null;
            }, 600);
        };

        // Show action indicator
        const showActionIndicator = (text) => {
            actionIndicator.value = text;
            setTimeout(() => {
                actionIndicator.value = null;
            }, 2000);
        };

        // Add to execution log
        const addLog = (message, type = 'info') => {
            const now = new Date();
            const time = now.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            });
            executionLog.value.push({ time, message, type });
            // Keep only last 20 logs
            if (executionLog.value.length > 20) {
                executionLog.value.shift();
            }
        };

        // ========================================
        // Command Execution
        // ========================================

        const executeCommand = async () => {
            if (!nlCommand.value.trim() || isExecuting.value) return;

            isExecuting.value = true;
            executionLog.value = [];
            const command = nlCommand.value.toLowerCase();

            addLog(`Parsing: "${nlCommand.value}"`);
            parseCommand();

            await sleep(500);

            // Execute based on parsed command
            if (command.includes('open settings') || command.includes('go to settings')) {
                await executeOpenSettings();
            } else if (command.includes('open chrome') || command.includes('open browser')) {
                await executeOpenChrome();
            } else if (command.includes('open messages') || command.includes('open sms')) {
                await executeOpenMessages();
            } else if (command.includes('enable wifi') || command.includes('turn on wifi')) {
                await executeToggleSetting('WiFi', true);
            } else if (command.includes('disable wifi') || command.includes('turn off wifi')) {
                await executeToggleSetting('WiFi', false);
            } else if (command.includes('enable dark mode') || command.includes('turn on dark')) {
                await executeToggleSetting('Dark mode', true);
            } else if (command.includes('disable dark mode') || command.includes('turn off dark')) {
                await executeToggleSetting('Dark mode', false);
            } else if (command.includes('enable bluetooth')) {
                await executeToggleSetting('Bluetooth', true);
            } else if (command.includes('search for') || command.includes('search ')) {
                const searchMatch = command.match(/search\s+(?:for\s+)?(.+)/i);
                if (searchMatch) {
                    await executeSearch(searchMatch[1].trim());
                }
            } else if (command.includes('go home') || command.includes('go to home')) {
                phoneScreen.value = 'home';
                addLog('Returned to home screen', 'success');
            } else if (command.includes('scroll')) {
                showActionIndicator('Scrolling...');
                addLog('Performing scroll action', 'success');
            } else if (command.includes('tap') || command.includes('click')) {
                const tapMatch = command.match(/(?:tap|click)\s+(?:on\s+)?(?:the\s+)?(.+)/i);
                if (tapMatch) {
                    await executeTap(tapMatch[1].trim());
                }
            } else {
                addLog('Command parsed - ready to execute on real device', 'success');
                showActionIndicator('Command ready');
            }

            isExecuting.value = false;
        };

        const executeOpenSettings = async () => {
            addLog('Locating Settings app using Smart Locator');
            await sleep(300);
            addLog('Found: resource_id="com.android.settings"', 'success');
            phoneScreen.value = 'home';
            await sleep(200);
            openApp('Settings');
        };

        const executeOpenChrome = async () => {
            addLog('Locating Chrome app using Smart Locator');
            await sleep(300);
            addLog('Found: text="Chrome"', 'success');
            phoneScreen.value = 'home';
            await sleep(200);
            openApp('Chrome');
        };

        const executeOpenMessages = async () => {
            addLog('Locating Messages app using Smart Locator');
            await sleep(300);
            addLog('Found: content_desc="Messages"', 'success');
            phoneScreen.value = 'home';
            await sleep(200);
            openApp('Messages');
        };

        const executeToggleSetting = async (settingName, enable) => {
            // First open settings if not there
            if (phoneScreen.value !== 'settings') {
                await executeOpenSettings();
                await sleep(500);
            }

            addLog(`Locating "${settingName}" toggle`);
            await sleep(300);

            const setting = settingsItems.value.find(s => s.name === settingName);
            if (setting) {
                highlightedSetting.value = settingName;
                addLog(`Found: text="${settingName}"`, 'success');
                await sleep(500);

                if (setting.toggle) {
                    setting.enabled = enable;
                    addLog(`${settingName} ${enable ? 'enabled' : 'disabled'}`, 'success');
                }

                setTimeout(() => {
                    highlightedSetting.value = null;
                }, 1500);
            }
        };

        const executeSearch = async (query) => {
            // Open Chrome first
            if (phoneScreen.value !== 'chrome') {
                await executeOpenChrome();
                await sleep(500);
            }

            addLog(`Entering search query: "${query}"`);
            await sleep(300);

            chromeUrl.value = `google.com/search?q=${encodeURIComponent(query)}`;
            chromeContent.value = `
                <div class="space-y-4">
                    <p class="text-lg font-medium">Search results for "${query}"</p>
                    <div class="p-3 bg-gray-50 rounded-lg">
                        <p class="text-blue-600 font-medium">${query} - Wikipedia</p>
                        <p class="text-green-700 text-xs">en.wikipedia.org</p>
                        <p class="text-gray-600 text-sm mt-1">Information about ${query}...</p>
                    </div>
                    <div class="p-3 bg-gray-50 rounded-lg">
                        <p class="text-blue-600 font-medium">${query} | Latest News</p>
                        <p class="text-green-700 text-xs">news.example.com</p>
                        <p class="text-gray-600 text-sm mt-1">Latest updates on ${query}...</p>
                    </div>
                </div>
            `;

            addLog(`Search completed for "${query}"`, 'success');
        };

        const executeTap = async (target) => {
            addLog(`Locating element: "${target}"`);
            await sleep(400);

            // Try to find matching app or setting
            const app = phoneApps.value.find(a =>
                a.name.toLowerCase().includes(target.toLowerCase())
            );

            if (app) {
                addLog(`Found app: ${app.name}`, 'success');
                openApp(app.name);
                return;
            }

            const setting = settingsItems.value.find(s =>
                s.name.toLowerCase().includes(target.toLowerCase())
            );

            if (setting && phoneScreen.value === 'settings') {
                highlightedSetting.value = setting.name;
                addLog(`Found setting: ${setting.name}`, 'success');
                if (setting.toggle) {
                    setting.enabled = !setting.enabled;
                }
                setTimeout(() => {
                    highlightedSetting.value = null;
                }, 1500);
                return;
            }

            addLog(`Element "${target}" located via Visual AI`, 'success');
            showActionIndicator(`Tapped: ${target}`);
        };

        // Helper sleep function
        const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

        // ========================================
        // Code Snippets
        // ========================================

        const codeSnippets = {
            cli: `# Run a natural language command
ditto run "open settings and enable wifi"

# Record a workflow
ditto record --output my_workflow.json

# Replay a recorded workflow
ditto replay my_workflow.json

# Run with variables
ditto run workflow.json --var username=test@email.com`,

            python: `from dittomatic import DittoMation

# Initialize
ditto = DittoMation()

# Run natural language command
ditto.run("open Chrome and search for weather")

# Use smart locator
element = ditto.find_element(
    text="Login",
    fallback_strategies=["resource_id", "content_desc", "ocr"]
)
element.tap()

# Record and replay
ditto.start_recording()
# ... perform actions ...
workflow = ditto.stop_recording()
workflow.save("login_flow.json")

# Replay with variables
ditto.replay("login_flow.json", variables={
    "username": "test@example.com",
    "password": "secure123"
})`,

            json: `{
  "name": "Login Workflow",
  "variables": {
    "username": "",
    "password": ""
  },
  "steps": [
    {
      "action": "tap",
      "locator": {
        "text": "Login",
        "resource_id": "btn_login",
        "confidence_threshold": 0.8
      }
    },
    {
      "action": "input_text",
      "locator": {"resource_id": "input_username"},
      "value": "\${username}"
    },
    {
      "action": "input_text",
      "locator": {"resource_id": "input_password"},
      "value": "\${password}"
    },
    {
      "action": "tap",
      "locator": {"text": "Submit"}
    }
  ]
}`
        };

        // Parse natural language command (simulated)
        const parseCommand = () => {
            if (!nlCommand.value.trim()) {
                parsedCommand.value = null;
                return;
            }

            const command = nlCommand.value.toLowerCase();
            const result = {
                intent: '',
                target: '',
                action: '',
                value: '',
                steps: []
            };

            // Simple parsing logic for demo
            if (command.includes('open')) {
                result.intent = 'launch_app';
                const appMatch = command.match(/open\s+(\w+)/i);
                if (appMatch) {
                    result.target = appMatch[1].charAt(0).toUpperCase() + appMatch[1].slice(1);
                }
                result.steps.push(`Launch "${result.target}" application`);
            }

            if (command.includes('tap') || command.includes('click')) {
                result.intent = result.intent ? result.intent + ' + tap' : 'tap';
                const tapMatch = command.match(/(?:tap|click)\s+(?:the\s+)?(.+?)(?:\s+and|\s+then|$)/i);
                if (tapMatch) {
                    result.action = 'tap';
                    result.target = result.target || tapMatch[1].trim();
                    result.steps.push(`Tap element: "${tapMatch[1].trim()}"`);
                }
            }

            if (command.includes('enable') || command.includes('turn on')) {
                result.intent = result.intent ? result.intent + ' + toggle' : 'toggle_setting';
                const enableMatch = command.match(/(?:enable|turn on)\s+(.+?)(?:\s+and|$)/i);
                if (enableMatch) {
                    result.action = 'enable';
                    result.value = enableMatch[1].trim();
                    result.steps.push(`Enable: "${result.value}"`);
                }
            }

            if (command.includes('disable') || command.includes('turn off')) {
                result.intent = result.intent ? result.intent + ' + toggle' : 'toggle_setting';
                const disableMatch = command.match(/(?:disable|turn off)\s+(.+?)(?:\s+and|$)/i);
                if (disableMatch) {
                    result.action = 'disable';
                    result.value = disableMatch[1].trim();
                    result.steps.push(`Disable: "${result.value}"`);
                }
            }

            if (command.includes('search') || command.includes('type') || command.includes('enter')) {
                result.intent = result.intent ? result.intent + ' + input' : 'input_text';
                const searchMatch = command.match(/(?:search|type|enter)\s+(?:for\s+)?(.+?)(?:\s+in|$)/i);
                if (searchMatch) {
                    result.value = searchMatch[1].trim();
                    result.steps.push(`Input text: "${result.value}"`);
                }
            }

            if (command.includes('scroll')) {
                result.intent = result.intent ? result.intent + ' + scroll' : 'scroll';
                result.action = command.includes('up') ? 'scroll_up' : 'scroll_down';
                result.steps.push(`Scroll ${command.includes('up') ? 'up' : 'down'}`);
            }

            if (command.includes('find') || command.includes('locate')) {
                const findMatch = command.match(/(?:find|locate)\s+(.+?)(?:\s+and|$)/i);
                if (findMatch) {
                    result.steps.push(`Locate element: "${findMatch[1].trim()}"`);
                }
            }

            if (result.steps.length === 0) {
                result.intent = 'custom';
                result.steps.push('Parse and execute custom command');
            }

            parsedCommand.value = result;
        };

        // Run demo (same as parse for now)
        const runDemo = () => {
            parseCommand();
        };

        // Computed GitHub issue URL
        const githubIssueUrl = computed(() => {
            const type = feedback.value.type;
            const labels = {
                'general': 'feedback',
                'feature': 'enhancement',
                'bug': 'bug',
                'praise': 'feedback'
            };
            const title = encodeURIComponent(`[${type.toUpperCase()}] Feedback from Demo`);
            const body = encodeURIComponent(
                `## Feedback Type\n${type}\n\n` +
                `## Rating\n${'⭐'.repeat(feedback.value.rating || 0)} (${feedback.value.rating || 0}/5)\n\n` +
                `## Message\n${feedback.value.message || '(Please describe your feedback)'}\n\n` +
                `## Interested Features\n${feedback.value.interests.length > 0 ? feedback.value.interests.map(f => `- ${f}`).join('\n') : 'None selected'}\n\n` +
                `---\n*Submitted via Interactive Demo*`
            );
            return `https://github.com/OmPrakashSingh1704/DittoMation/issues/new?title=${title}&body=${body}&labels=${labels[type] || 'feedback'}`;
        });

        // Submit feedback
        const feedbackLoading = ref(false);
        const feedbackError = ref('');

        const submitFeedback = async () => {
            if (!feedback.value.message.trim()) return;

            feedbackLoading.value = true;
            feedbackError.value = '';

            try {
                // Submit to Formspree
                const response = await fetch('https://formspree.io/f/mwvozkrj', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        type: feedback.value.type,
                        rating: feedback.value.rating,
                        name: feedback.value.name || 'Anonymous',
                        email: feedback.value.email || 'Not provided',
                        message: feedback.value.message,
                        interests: feedback.value.interests.join(', ') || 'None selected',
                        _subject: `[DittoMation Demo] ${feedback.value.type.toUpperCase()} Feedback`
                    })
                });

                if (response.ok) {
                    // Add to recent feedback (local display)
                    recentFeedback.value.unshift({
                        ...feedback.value,
                        timestamp: new Date().toISOString()
                    });

                    // Keep only last 5
                    if (recentFeedback.value.length > 5) {
                        recentFeedback.value.pop();
                    }

                    // Save to localStorage
                    try {
                        localStorage.setItem('dittoFeedback', JSON.stringify(recentFeedback.value));
                    } catch (e) {
                        console.log('Could not save to localStorage');
                    }

                    feedbackSubmitted.value = true;
                } else {
                    throw new Error('Submission failed');
                }
            } catch (error) {
                feedbackError.value = 'Failed to submit. Please try again or use the GitHub issue option.';
                console.error('Feedback submission error:', error);
            } finally {
                feedbackLoading.value = false;
            }
        };

        // Reset feedback form
        const resetFeedbackForm = () => {
            feedback.value = {
                type: 'general',
                rating: 0,
                name: '',
                email: '',
                message: '',
                interests: []
            };
        };

        // Load saved feedback from localStorage
        const loadSavedFeedback = () => {
            try {
                const saved = localStorage.getItem('dittoFeedback');
                if (saved) {
                    recentFeedback.value = JSON.parse(saved);
                }
            } catch (e) {
                console.log('Could not load from localStorage');
            }
        };

        // Copy ADB commands to clipboard
        const copyAdbCommands = async () => {
            const commands = `# Check connected devices
adb devices

# Install DittoMation
pip install dittomatic

# Run your first command
ditto run "open settings"

# Or use Python
python -c "from dittomatic import DittoMation; DittoMation().run('open settings')"`;
            try {
                await navigator.clipboard.writeText(commands);
                adbCopied.value = true;
                setTimeout(() => {
                    adbCopied.value = false;
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        };

        // Copy code to clipboard
        const copyCode = async (tabId) => {
            try {
                await navigator.clipboard.writeText(codeSnippets[tabId]);
                codeCopied.value = true;
                setTimeout(() => {
                    codeCopied.value = false;
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        };

        // Animation sequences
        const startAnimations = () => {
            // Terminal animation
            setTimeout(() => {
                terminalAnimated.value = true;
            }, 1000);

            // Fallback chain animation
            const animateFallback = () => {
                let step = 0;
                const interval = setInterval(() => {
                    step++;
                    fallbackStep.value = step;
                    if (step >= 3) {
                        clearInterval(interval);
                        // Reset and repeat
                        setTimeout(() => {
                            fallbackStep.value = 0;
                            setTimeout(animateFallback, 1000);
                        }, 3000);
                    }
                }, 800);
            };
            setTimeout(animateFallback, 2000);

            // Confidence scores animation
            setTimeout(() => {
                confidenceScores.value = {
                    resourceId: 95,
                    textMatch: 88,
                    visualAI: 76
                };
            }, 1500);

            // Workflow animation
            const animateWorkflow = () => {
                let step = 0;
                const interval = setInterval(() => {
                    step++;
                    workflowStep.value = step;
                    if (step >= 3) {
                        clearInterval(interval);
                        // Reset and repeat
                        setTimeout(() => {
                            workflowStep.value = 0;
                            setTimeout(animateWorkflow, 1000);
                        }, 3000);
                    }
                }, 1000);
            };
            setTimeout(animateWorkflow, 2500);
        };

        // Watch for modal open/close to lock body scroll
        watch(showRealEmulator, (isOpen) => {
            if (isOpen) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });

        // Initialize on mount
        onMounted(() => {
            // Initialize AOS
            AOS.init({
                duration: 800,
                easing: 'ease-out-cubic',
                once: true,
                offset: 50
            });

            // Initialize Highlight.js
            document.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });

            // Start animations
            startAnimations();

            // Update phone time
            updatePhoneTime();
            setInterval(updatePhoneTime, 60000);

            // Load saved feedback
            loadSavedFeedback();

            // Smooth scroll for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        });

        return {
            // Original exports
            terminalAnimated,
            fallbackStep,
            confidenceScores,
            workflowStep,
            nlCommand,
            parsedCommand,
            exampleCommands,
            codeTabs,
            activeCodeTab,
            codeCopied,
            comparisonData,
            parseCommand,
            runDemo,
            copyCode,

            // Phone simulator exports
            phoneScreen,
            phoneTime,
            showRealEmulator,
            emulatorTab,
            adbCopied,
            copyAdbCommands,

            // Feedback exports
            feedbackSubmitted,
            feedbackLoading,
            feedbackError,
            feedback,
            feedbackTypes,
            interestFeatures,
            recentFeedback,
            githubIssueUrl,
            submitFeedback,
            resetFeedbackForm,

            phoneApps,
            tappedApp,
            tapPosition,
            actionIndicator,
            settingsItems,
            highlightedSetting,
            chromeUrl,
            chromeContent,
            messages,
            openApp,
            toggleSetting,
            quickCommands,
            isExecuting,
            executionLog,
            executeCommand
        };
    }
}).mount('#app');
