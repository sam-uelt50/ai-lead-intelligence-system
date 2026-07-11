const BaseScraper = require('./BaseScraper');

class CompanyWebsiteScraper extends BaseScraper {
    async scrapeCompanyWebsite(url) {
        console.log(`Scraping company website: ${url}`);
        
        try {
            const $ = await this.fetchPage(url);
            if (!$) return null;

            const companyData = {
                name: this.extractName($),
                description: this.extractMetaDescription($),
                email: this.extractEmail($),
                phone: this.extractPhone($),
                address: this.extractAddress($),
                socialLinks: this.extractSocialLinks($),
                technologies: this.extractTechnologies($),
                pages: this.scrapeImportantPages($, url)
            };

            return companyData;
        } catch (error) {
            console.error(`Website scraping error: ${error.message}`);
            return null;
        }
    }

    extractName($) {
        // Try multiple selectors for company name
        const selectors = [
            'h1', '.company-name', '.brand', 'title',
            'meta[property="og:site_name"]',
            'meta[name="application-name"]'
        ];

        for (const selector of selectors) {
            const text = $(selector).first().text().trim();
            if (text && text.length < 100) {
                return text.split('|')[0].split('-')[0].trim();
            }
        }
        return null;
    }

    extractMetaDescription($) {
        return $('meta[name="description"]').attr('content') ||
               $('meta[property="og:description"]').attr('content') ||
               $('p').first().text().substring(0, 300);
    }

    extractEmail($) {
        const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
        const pageText = $('body').text();
        const emails = pageText.match(emailRegex);
        return emails ? emails[0] : null;
    }

    extractPhone($) {
        const phoneRegex = /(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}/g;
        const pageText = $('body').text();
        const phones = pageText.match(phoneRegex);
        return phones ? phones[0] : null;
    }

    extractSocialLinks($) {
        const social = {};
        const socialPlatforms = {
            'linkedin.com': 'linkedin',
            'twitter.com': 'twitter',
            'facebook.com': 'facebook',
            'instagram.com': 'instagram',
            'github.com': 'github'
        };

        $('a[href]').each((i, el) => {
            const href = $(el).attr('href');
            for (const [domain, platform] of Object.entries(socialPlatforms)) {
                if (href.includes(domain)) {
                    social[platform] = href;
                    break;
                }
            }
        });

        return social;
    }

    scrapeImportantPages($, baseUrl) {
        const pages = {};
        const pageSelectors = {
            about: ['/about', 'about-us', 'company'],
            contact: ['/contact', 'contact-us', 'get-in-touch'],
            careers: ['/careers', 'jobs', 'work-with-us'],
            team: ['/team', 'people', 'leadership']
        };

        $('a[href]').each((i, el) => {
            const href = $(el).attr('href');
            const text = $(el).text().toLowerCase();
            
            for (const [pageType, keywords] of Object.entries(pageSelectors)) {
                if (keywords.some(keyword => 
                    href.includes(keyword) || text.includes(keyword)
                )) {
                    pages[pageType] = new URL(href, baseUrl).href;
                    break;
                }
            }
        });

        return pages;
    }
}

module.exports = CompanyWebsiteScraper;