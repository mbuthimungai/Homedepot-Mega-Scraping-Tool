const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

const COOKIES_FILE_PATH = './cookies.json';
const URL = 'https://www.homedepot.com/p/Milwaukee-M18-FUEL-18-Volt-Lithium-Ion-Brushless-Cordless-Gen-II-18-Gauge-Brad-Nailer-Tool-Only-2746-20/309752194';

const navigateToPage = async (page) => {
    try {
        console.log('Navigating to the webpage...');
        await page.goto(URL, { waitUntil: 'load', timeout: 60000 }); // Set timeout to 60 seconds
        console.log('Page loaded successfully.');
    } catch (error) {
        console.error('Navigation failed:', error);
        throw error;
    }
};

(async () => {
    try {
        // Launch browser with the executable path from the mounted host directory
        const browser = await puppeteer.launch({
            headless: true, // Run in headless mode
            executablePath: '/usr/bin/google-chrome-stable', // Path inside the container
            args: [
                '--no-sandbox', // Disable sandboxing
                '--disable-setuid-sandbox', // Disable setuid sandbox (Linux only)
                '--disable-dev-shm-usage' // Disable shared memory usage
            ]
        });

        const page = await browser.newPage();        
        // Attempt to navigate to the webpage
        try {
            await navigateToPage(page);
        } catch (error) {
            console.log('Retrying navigation...');
            await page.reload({ waitUntil: 'load', timeout: 60000 }); // Retry navigation with a fresh load
        }

        

        // Save cookies
        console.log('Saving cookies...');
        const cookies = await page.cookies();
        fs.writeFileSync(COOKIES_FILE_PATH, JSON.stringify(cookies, null, 2));

        // Close browser
        await browser.close();
        console.log('Browser closed.');
    } catch (error) {
        console.error('Error during script execution:', error);
    }
})();